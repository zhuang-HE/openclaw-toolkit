#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
临床试验数据库 API 服务
提供 REST API 接口，支持 AI 智能体和外部应用调用

启动方式：
    python clinical_trial_api_server.py

访问：
    http://localhost:8082
    http://localhost:8082/docs (API 文档)
"""

import os
import csv
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, Request, Depends, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
from pydantic import BaseModel, Field
import uvicorn

# ==================== 配置 ====================

class Config:
    """系统配置"""
    # 路径配置
    WORKSPACE = "/home/admin/.openclaw/workspace"
    ACCIDENT_DB_FILE = "clinical_trial_data/临床试验事故案例库.csv"
    RATE_DB_FILE = "clinical_trial_data/保险费率历史趋势.csv"
    API_KEYS_FILE = "api_keys.json"
    
    # API 配置
    API_PORT = 8082
    API_HOST = "0.0.0.0"
    
    # 安全配置
    API_KEYS = {
        "sk_clinical_demo_key_123456": {
            "name": "Demo Key",
            "permission": "read",
            "created_at": "2026-03-25"
        },
        "sk_clinical_ai_agent_001": {
            "name": "AI Agent Key",
            "permission": "read",
            "created_at": "2026-03-25"
        }
    }
    
    # 限流配置
    RATE_LIMIT_PER_MINUTE = 60
    
    # CORS 配置
    ALLOWED_ORIGINS = ["*"]

# ==================== 日志配置 ====================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("clinical_api")

# ==================== 数据模型 ====================

class ClinicalResponse(BaseModel):
    """临床试验响应模型"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None

# ==================== 数据库管理 ====================

class ClinicalDatabase:
    """临床试验数据库管理器"""
    
    def __init__(self, accident_db_path: str, rate_db_path: str = None):
        self.accident_db_path = accident_db_path
        self.rate_db_path = rate_db_path
        self.accident_cache = None
        self.rate_cache = None
        self.cache_time = None
        self.cache_ttl = 60
    
    def _load_accident_data(self) -> pd.DataFrame:
        """加载事故数据"""
        now = datetime.now()
        
        if self.accident_cache is not None and self.cache_time is not None:
            if (now - self.cache_time).total_seconds() < self.cache_ttl:
                return self.accident_cache
        
        if not os.path.exists(self.accident_db_path):
            raise FileNotFoundError(f"事故数据库文件不存在：{self.accident_db_path}")
        
        df = pd.read_csv(self.accident_db_path)
        
        self.accident_cache = df
        self.cache_time = now
        
        logger.info(f"加载事故数据库：{len(df)} 条记录")
        return df
    
    def _load_rate_data(self) -> pd.DataFrame:
        """加载费率数据"""
        if not self.rate_db_path or not os.path.exists(self.rate_db_path):
            return pd.DataFrame()
        
        df = pd.read_csv(self.rate_db_path)
        logger.info(f"加载费率数据库：{len(df)} 条记录")
        return df
    
    def get_all_accidents(self, page: int = 1, page_size: int = 20) -> Dict:
        """获取所有事故案例（分页）"""
        df = self._load_accident_data()
        
        # 按时间倒序
        df = df.sort_values('日期', ascending=False)
        
        # 处理 NaN 值，避免 JSON 序列化问题
        df = df.where(pd.notnull(df), None)
        
        start = (page - 1) * page_size
        end = start + page_size
        
        paginated = df.iloc[start:end]
        
        # 转换为原生 Python 类型
        records = []
        for _, row in paginated.iterrows():
            record = {}
            for col in paginated.columns:
                val = row[col]
                if pd.isna(val):
                    record[col] = None
                elif isinstance(val, (int, float)):
                    # 处理大数
                    if isinstance(val, float) and val.is_integer():
                        record[col] = int(val)
                    else:
                        record[col] = val
                else:
                    record[col] = str(val) if val is not None else None
            records.append(record)
        
        return {
            "data": records,
            "total": len(df),
            "page": page,
            "page_size": page_size,
            "total_pages": (len(df) + page_size - 1) // page_size
        }
    
    def search_accidents(self, query: str = None, trial_type: str = None,
                         phase: str = None, start_date: str = None,
                         end_date: str = None, page: int = 1,
                         page_size: int = 20) -> Dict:
        """搜索事故案例"""
        df = self._load_accident_data()
        
        mask = pd.Series([True] * len(df))
        
        if query:
            query_lower = query.lower()
            mask &= (
                df.get('药物类型', pd.Series()).str.lower().str.contains(query_lower, na=False) |
                df.get('器械类型', pd.Series()).str.lower().str.contains(query_lower, na=False) |
                df.get('事件', pd.Series()).str.lower().str.contains(query_lower, na=False) |
                df.get('结果', pd.Series()).str.lower().str.contains(query_lower, na=False)
            )
        
        if trial_type:
            mask &= df.get('类型', pd.Series()).str.contains(trial_type, na=False)
        
        if phase:
            mask &= df.get('分期', pd.Series()).str.contains(phase, na=False)
        
        if start_date:
            mask &= df['日期'] >= start_date
        
        if end_date:
            mask &= df['日期'] <= end_date
        
        filtered = df[mask]
        filtered = filtered.sort_values('日期', ascending=False)
        
        start = (page - 1) * page_size
        end = start + page_size
        
        paginated = filtered.iloc[start:end]
        
        # 处理 NaN 值，避免 JSON 序列化问题
        paginated = paginated.where(pd.notnull(paginated), None)
        
        # 转换为原生 Python 类型
        records = []
        for _, row in paginated.iterrows():
            record = {}
            for col in paginated.columns:
                val = row[col]
                if pd.isna(val) or val is None:
                    record[col] = None
                elif isinstance(val, (int, float)):
                    if isinstance(val, float) and val.is_integer():
                        record[col] = int(val)
                    else:
                        record[col] = val
                else:
                    record[col] = str(val) if val is not None else None
            records.append(record)
        
        return {
            "data": records,
            "total": len(filtered),
            "page": page,
            "page_size": page_size,
            "total_pages": (len(filtered) + page_size - 1) // page_size if len(filtered) > 0 else 0
        }
    
    def get_stats(self) -> Dict:
        """获取统计数据"""
        df = self._load_accident_data()
        
        # 按类型统计
        type_dist = df['类型'].value_counts().to_dict() if '类型' in df.columns else {}
        
        # 按分期统计
        phase_dist = df['分期'].value_counts().to_dict() if '分期' in df.columns else {}
        
        # 赔偿统计
        compensation_col = '赔偿' if '赔偿' in df.columns else None
        total_compensation = 0.0
        if compensation_col:
            try:
                # 处理 NaN 值并转换
                compensation_series = df[compensation_col].fillna('0').str.replace('万元', '', regex=False).str.replace('元', '', regex=False)
                compensation_series = pd.to_numeric(compensation_series, errors='coerce').fillna(0)
                total_compensation = float(compensation_series.sum())
            except Exception as e:
                logger.warning(f"赔偿金额统计失败：{e}")
                total_compensation = 0.0
        
        return {
            "total_accidents": len(df),
            "type_distribution": type_dist,
            "phase_distribution": phase_dist,
            "total_compensation": total_compensation,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_rates(self) -> Dict:
        """获取保险费率数据"""
        df = self._load_rate_data()
        
        if df.empty:
            return {"rates": [], "total": 0}
        
        return {
            "rates": df.to_dict('records'),
            "total": len(df),
            "companies": df['保险公司'].unique().tolist() if '保险公司' in df.columns else []
        }
    
    def get_phase_stats(self) -> Dict:
        """按分期统计"""
        df = self._load_accident_data()
        
        if '分期' not in df.columns:
            return {}
        
        phase_counts = df['分期'].value_counts().to_dict()
        total = len(df)
        
        return {
            phase: {
                "count": count,
                "percentage": round(count / total * 100, 2) if total > 0 else 0
            }
            for phase, count in phase_counts.items()
        }

# ==================== FastAPI 应用 ====================

app = FastAPI(
    title="临床试验数据库 API",
    description="提供临床试验事故案例、保险费率等信息的 REST API 接口",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key 安全
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if not api_key:
        raise HTTPException(status_code=401, detail="缺少 API Key")
    if api_key not in Config.API_KEYS:
        raise HTTPException(status_code=401, detail="无效的 API Key")
    return api_key

# 数据库实例
db_manager = None

@app.on_event("startup")
async def startup_event():
    global db_manager
    accident_path = os.path.join(Config.WORKSPACE, Config.ACCIDENT_DB_FILE)
    rate_path = os.path.join(Config.WORKSPACE, Config.RATE_DB_FILE)
    db_manager = ClinicalDatabase(accident_path, rate_path)
    logger.info(f"临床试验数据库 API 启动，端口：{Config.API_PORT}")

# ==================== API 端点 ====================

@app.get("/")
async def root():
    """API 根路径"""
    return {
        "success": True,
        "data": {
            "docs": "/docs",
            "endpoints": {
                "accidents": "/api/accidents",
                "search": "/api/accidents/search",
                "stats": "/api/stats",
                "rates": "/api/rates",
                "phase_stats": "/api/phase/stats"
            }
        },
        "message": "临床试验数据库 API 服务运行中"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "loaded" if db_manager else "not_loaded"
    }

@app.get("/api/stats", response_model=ClinicalResponse)
async def get_stats(api_key: str = Depends(get_api_key)):
    """获取统计数据"""
    try:
        stats = db_manager.get_stats()
        return ClinicalResponse(success=True, data=stats)
    except Exception as e:
        logger.error(f"获取统计数据失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/accidents", response_model=ClinicalResponse)
async def get_accidents(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    api_key: str = Depends(get_api_key)
):
    """获取所有事故案例"""
    try:
        result = db_manager.get_all_accidents(page=page, page_size=page_size)
        return ClinicalResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"获取事故案例失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/accidents/search", response_model=ClinicalResponse)
async def search_accidents(
    q: Optional[str] = Query(None, description="搜索关键词"),
    trial_type: Optional[str] = Query(None, description="试验类型"),
    phase: Optional[str] = Query(None, description="分期"),
    start_date: Optional[str] = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="结束日期 (YYYY-MM-DD)"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    api_key: str = Depends(get_api_key)
):
    """搜索事故案例"""
    try:
        result = db_manager.search_accidents(
            query=q,
            trial_type=trial_type,
            phase=phase,
            start_date=start_date,
            end_date=end_date,
            page=page,
            page_size=page_size
        )
        return ClinicalResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"搜索失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rates", response_model=ClinicalResponse)
async def get_rates(api_key: str = Depends(get_api_key)):
    """获取保险费率数据"""
    try:
        rates = db_manager.get_rates()
        return ClinicalResponse(success=True, data=rates)
    except Exception as e:
        logger.error(f"获取费率数据失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/phase/stats", response_model=ClinicalResponse)
async def get_phase_stats(api_key: str = Depends(get_api_key)):
    """获取分期统计"""
    try:
        stats = db_manager.get_phase_stats()
        return ClinicalResponse(success=True, data=stats)
    except Exception as e:
        logger.error(f"获取分期统计失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== 异常处理 ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail, "data": None}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"未处理异常：{exc}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(exc), "data": None}
    )

# ==================== 启动入口 ====================

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=Config.API_HOST,
        port=Config.API_PORT,
        log_level="info"
    )
