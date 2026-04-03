#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
无人机数据库 API 服务
提供 REST API 接口，支持 AI 智能体和外部应用调用

启动方式：
    python drone_api_server.py

访问：
    http://localhost:8081
    http://localhost:8081/docs (API 文档)
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
    DATABASE_FILE = "无人机 BI 数据库_核心版.csv"
    API_KEYS_FILE = "api_keys.json"
    
    # API 配置
    API_PORT = 8081
    API_HOST = "0.0.0.0"
    
    # 安全配置
    API_KEYS = {
        "sk_drone_demo_key_123456": {
            "name": "Demo Key",
            "permission": "read",
            "created_at": "2026-03-25"
        },
        "sk_drone_ai_agent_001": {
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
logger = logging.getLogger("drone_api")

# ==================== 数据模型 ====================

class DroneResponse(BaseModel):
    """无人机响应模型"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None

# ==================== 数据库管理 ====================

class DroneDatabase:
    """无人机数据库管理器"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.cache = None
        self.cache_time = None
        self.cache_ttl = 60  # 缓存 60 秒
    
    def _load_data(self) -> pd.DataFrame:
        """加载数据（带缓存）"""
        now = datetime.now()
        
        if self.cache is not None and self.cache_time is not None:
            if (now - self.cache_time).total_seconds() < self.cache_ttl:
                return self.cache
        
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"数据库文件不存在：{self.db_path}")
        
        df = pd.read_csv(self.db_path)
        
        self.cache = df
        self.cache_time = now
        
        logger.info(f"加载无人机数据库：{len(df)} 条记录")
        return df
    
    def invalidate_cache(self):
        """使缓存失效"""
        self.cache = None
        self.cache_time = None
    
    def get_all_drones(self, page: int = 1, page_size: int = 20) -> Dict:
        """获取所有无人机（分页）"""
        df = self._load_data()
        
        start = (page - 1) * page_size
        end = start + page_size
        
        paginated = df.iloc[start:end]
        
        return {
            "data": paginated.to_dict('records'),
            "total": len(df),
            "page": page,
            "page_size": page_size,
            "total_pages": (len(df) + page_size - 1) // page_size
        }
    
    def search(self, query: str = None, brand: str = None, 
               usage_type: str = None, price_min: float = None, 
               price_max: float = None, page: int = 1, 
               page_size: int = 20) -> Dict:
        """搜索无人机"""
        df = self._load_data()
        
        mask = pd.Series([True] * len(df))
        
        if query:
            query_lower = query.lower()
            mask &= (
                df['品牌'].str.lower().str.contains(query_lower, na=False) |
                df['型号'].str.lower().str.contains(query_lower, na=False) |
                df['主要用途'].str.lower().str.contains(query_lower, na=False)
            )
        
        if brand:
            mask &= df['品牌'].str.contains(brand, na=False)
        
        if usage_type:
            mask &= df['主要用途'].str.contains(usage_type, na=False)
        
        if price_min is not None:
            mask &= df['价格 (元)'] >= price_min
        
        if price_max is not None:
            mask &= df['价格 (元)'] <= price_max
        
        filtered = df[mask]
        
        start = (page - 1) * page_size
        end = start + page_size
        
        paginated = filtered.iloc[start:end]
        
        return {
            "data": paginated.to_dict('records'),
            "total": len(filtered),
            "page": page,
            "page_size": page_size,
            "total_pages": (len(filtered) + page_size - 1) // page_size if len(filtered) > 0 else 0
        }
    
    def get_stats(self) -> Dict:
        """获取统计数据"""
        df = self._load_data()
        
        return {
            "total_drones": len(df),
            "brand_distribution": df['品牌'].value_counts().to_dict(),
            "usage_distribution": df['主要用途'].value_counts().to_dict(),
            "price_stats": {
                "min": float(df['价格 (元)'].min()),
                "max": float(df['价格 (元)'].max()),
                "avg": float(df['价格 (元)'].mean()),
                "median": float(df['价格 (元)'].median())
            },
            "accident_stats": {
                "total_accidents": int(df['事故总数 (2021 起)'].sum()),
                "total_casualties": int(df['人员伤亡数'].sum()),
                "total_injury_amount": float(df.get('人伤金额 (元)', pd.Series([0])).sum()),
                "total_drone_damage": float(df['机损金额 (元)'].sum()),
                "total_property_damage": float(df['物损金额 (元)'].sum())
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def get_brands(self) -> List[str]:
        """获取所有品牌"""
        df = self._load_data()
        return df['品牌'].unique().tolist()
    
    def get_accidents_stats(self) -> Dict:
        """获取事故统计"""
        df = self._load_data()
        
        return {
            "total_accidents": int(df['事故总数 (2021 起)'].sum()),
            "total_casualties": int(df['人员伤亡数'].sum()),
            "by_brand": df.groupby('品牌')['事故总数 (2021 起)'].sum().to_dict(),
            "by_usage": df.groupby('主要用途')['事故总数 (2021 起)'].sum().to_dict()
        }

# ==================== FastAPI 应用 ====================

app = FastAPI(
    title="无人机数据库 API",
    description="提供无人机产品数据、事故统计等信息的 REST API 接口",
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
    db_path = os.path.join(Config.WORKSPACE, Config.DATABASE_FILE)
    db_manager = DroneDatabase(db_path)
    logger.info(f"无人机数据库 API 启动，端口：{Config.API_PORT}")

# ==================== API 端点 ====================

@app.get("/")
async def root():
    """API 根路径"""
    return {
        "success": True,
        "data": {
            "docs": "/docs",
            "endpoints": {
                "drones": "/api/drones",
                "search": "/api/drones/search",
                "brands": "/api/brands",
                "stats": "/api/stats",
                "accidents": "/api/accidents/stats"
            }
        },
        "message": "无人机数据库 API 服务运行中"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "loaded" if db_manager else "not_loaded"
    }

@app.get("/api/stats", response_model=DroneResponse)
async def get_stats(api_key: str = Depends(get_api_key)):
    """获取统计数据"""
    try:
        stats = db_manager.get_stats()
        return DroneResponse(success=True, data=stats)
    except Exception as e:
        logger.error(f"获取统计数据失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/drones", response_model=DroneResponse)
async def get_drones(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    api_key: str = Depends(get_api_key)
):
    """获取所有无人机列表"""
    try:
        result = db_manager.get_all_drones(page=page, page_size=page_size)
        return DroneResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"获取无人机列表失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/drones/search", response_model=DroneResponse)
async def search_drones(
    q: Optional[str] = Query(None, description="搜索关键词"),
    brand: Optional[str] = Query(None, description="品牌"),
    usage: Optional[str] = Query(None, description="用途"),
    price_min: Optional[float] = Query(None, description="最低价格"),
    price_max: Optional[float] = Query(None, description="最高价格"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    api_key: str = Depends(get_api_key)
):
    """搜索无人机"""
    try:
        result = db_manager.search(
            query=q,
            brand=brand,
            usage_type=usage,
            price_min=price_min,
            price_max=price_max,
            page=page,
            page_size=page_size
        )
        return DroneResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"搜索失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/brands", response_model=DroneResponse)
async def get_brands(api_key: str = Depends(get_api_key)):
    """获取所有品牌"""
    try:
        brands = db_manager.get_brands()
        return DroneResponse(success=True, data={"brands": brands})
    except Exception as e:
        logger.error(f"获取品牌列表失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/accidents/stats", response_model=DroneResponse)
async def get_accidents_stats(api_key: str = Depends(get_api_key)):
    """获取事故统计"""
    try:
        stats = db_manager.get_accidents_stats()
        return DroneResponse(success=True, data=stats)
    except Exception as e:
        logger.error(f"获取事故统计失败：{e}")
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
