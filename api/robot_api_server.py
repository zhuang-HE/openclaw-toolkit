#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器人数据库 API 服务
提供 REST API 接口，支持 AI 智能体和外部应用调用

启动方式：
    python robot_api_server.py

访问：
    http://localhost:8000
    http://localhost:8000/docs (API 文档)
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
    DATABASE_FILE = "机器人数据库_核心版.csv"
    API_KEYS_FILE = "api_keys.json"
    
    # API 配置
    API_PORT = 8000
    API_HOST = "0.0.0.0"
    
    # 安全配置
    API_KEYS = {
        # 默认 API Key（生产环境请修改！）
        "sk_robot_demo_key_123456": {
            "name": "Demo Key",
            "permission": "read",
            "created_at": "2026-03-25"
        },
        # 添加更多 API Key
        # "sk_robot_prod_key_789": {
        #     "name": "Production Key",
        #     "permission": "read",
        #     "created_at": "2026-03-25"
        # }
    }
    
    # 限流配置
    RATE_LIMIT_PER_MINUTE = 60  # 每分钟最多 60 次请求
    
    # CORS 配置
    ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8080",
        # 添加其他允许的域名
    ]

# ==================== 日志配置 ====================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("robot_api")

# ==================== 数据模型 ====================

class RobotResponse(BaseModel):
    """机器人响应模型"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    message: Optional[str] = None

class RobotSearchRequest(BaseModel):
    """搜索请求"""
    query: Optional[str] = None
    category: Optional[str] = None
    company: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    page: int = 1
    page_size: int = 20

# ==================== 数据库管理 ====================

class RobotDatabase:
    """机器人数据库管理器"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.cache = None
        self.cache_time = None
        self.cache_ttl = 60  # 缓存 60 秒
    
    def _load_data(self) -> pd.DataFrame:
        """加载数据（带缓存）"""
        now = datetime.now()
        
        # 检查缓存
        if self.cache is not None and self.cache_time is not None:
            if (now - self.cache_time).total_seconds() < self.cache_ttl:
                return self.cache
        
        # 加载 CSV
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"数据库文件不存在：{self.db_path}")
        
        df = pd.read_csv(self.db_path)
        
        # 填充缓存
        self.cache = df
        self.cache_time = now
        
        logger.info(f"加载数据库：{len(df)} 条记录")
        return df
    
    def invalidate_cache(self):
        """使缓存失效"""
        self.cache = None
        self.cache_time = None
    
    def get_all_robots(self, page: int = 1, page_size: int = 20) -> Dict:
        """获取所有机器人（分页）"""
        df = self._load_data()
        
        # 分页
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
    
    def search(self, query: str = None, category: str = None, 
               company: str = None, price_min: float = None, 
               price_max: float = None, page: int = 1, 
               page_size: int = 20) -> Dict:
        """搜索机器人"""
        df = self._load_data()
        
        # 应用筛选条件
        mask = pd.Series([True] * len(df))
        
        if query:
            # 模糊搜索（名称、型号、描述）
            query_lower = query.lower()
            mask &= (
                df['公司全称'].str.lower().str.contains(query_lower, na=False) |
                df['公司简称'].str.lower().str.contains(query_lower, na=False) |
                df['型号'].str.lower().str.contains(query_lower, na=False) |
                df['主要用途'].str.lower().str.contains(query_lower, na=False)
            )
        
        if category:
            mask &= df['类型'].str.contains(category, na=False)
        
        if company:
            mask &= (
                df['公司全称'].str.contains(company, na=False) |
                df['公司简称'].str.contains(company, na=False)
            )
        
        if price_min is not None:
            mask &= df['价格 (元)'] >= price_min
        
        if price_max is not None:
            mask &= df['价格 (元)'] <= price_max
        
        # 应用筛选
        filtered = df[mask]
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        
        paginated = filtered.iloc[start:end]
        
        return {
            "data": paginated.to_dict('records'),
            "total": len(filtered),
            "page": page,
            "page_size": page_size,
            "total_pages": (len(filtered) + page_size - 1) // page_size
        }
    
    def get_by_id(self, robot_id: str) -> Optional[Dict]:
        """根据 ID 获取机器人详情"""
        df = self._load_data()
        
        # 尝试匹配型号或公司 + 型号
        mask = df['型号'].str.contains(robot_id, na=False, case=False)
        
        if not mask.any():
            # 尝试匹配公司简称
            mask = df['公司简称'].str.contains(robot_id, na=False, case=False)
        
        if not mask.any():
            return None
        
        result = df[mask].iloc[0]
        return result.to_dict()
    
    def get_companies(self) -> List[Dict]:
        """获取公司列表"""
        df = self._load_data()
        
        # 按公司分组统计
        companies = df.groupby('公司全称').agg({
            '型号': 'count',
            '价格 (元)': ['min', 'max'],
            '类型': lambda x: x.unique().tolist()
        }).reset_index()
        
        companies.columns = ['公司全称', '产品数量', '最低价格', '最高价格', '产品类型']
        
        return companies.to_dict('records')
    
    def get_stats(self) -> Dict:
        """获取统计数据"""
        df = self._load_data()
        
        # 按类型统计
        type_stats = df.groupby('类型').size().to_dict()
        
        # 价格统计
        price_stats = {
            "min": float(df['价格 (元)'].min()),
            "max": float(df['价格 (元)'].max()),
            "avg": float(df['价格 (元)'].mean()),
            "median": float(df['价格 (元)'].median())
        }
        
        # 事故统计
        total_accidents = int(df['事故总数'].sum()) if '事故总数' in df.columns else 0
        total_casualties = int(df['伤亡人数'].sum()) if '伤亡人数' in df.columns else 0
        
        return {
            "total_robots": len(df),
            "total_companies": df['公司全称'].nunique(),
            "type_distribution": type_stats,
            "price_stats": price_stats,
            "accident_stats": {
                "total_accidents": total_accidents,
                "total_casualties": total_casualties
            },
            "last_updated": self.cache_time.isoformat() if self.cache_time else None
        }
    
    def get_accident_stats(self, company: str = None, year: int = None) -> Dict:
        """获取事故统计"""
        df = self._load_data()
        
        # 筛选
        mask = df['事故总数'] > 0 if '事故总数' in df.columns else pd.Series([False] * len(df))
        
        if company:
            mask &= df['公司全称'].str.contains(company, na=False)
        
        if year:
            # 假设有发布时间字段
            if '发布时间' in df.columns:
                mask &= df['发布时间'].str.contains(str(year), na=False)
        
        accidents = df[mask]
        
        if len(accidents) == 0:
            return {
                "total": 0,
                "data": [],
                "summary": {}
            }
        
        # 统计
        total_accidents = int(accidents['事故总数'].sum())
        total_casualties = int(accidents['伤亡人数'].sum()) if '伤亡人数' in accidents.columns else 0
        total_loss = float(accidents['机损金额 (元)'].sum()) if '机损金额 (元)' in accidents.columns else 0
        
        return {
            "total": total_accidents,
            "casualties": total_casualties,
            "total_loss": total_loss,
            "data": accidents[['公司全称', '型号', '事故总数', '伤亡人数']].to_dict('records'),
            "summary": {
                "by_company": accidents.groupby('公司全称')['事故总数'].sum().to_dict(),
                "by_type": accidents.groupby('类型')['事故总数'].sum().to_dict() if '类型' in accidents.columns else {}
            }
        }

# ==================== FastAPI 应用 ====================

app = FastAPI(
    title="机器人数据库 API",
    description="提供机器人产品数据的查询和搜索接口",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key 安全
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# 数据库实例
db_path = os.path.join(Config.WORKSPACE, Config.DATABASE_FILE)
database = RobotDatabase(db_path)

# 请求计数（限流用）
request_counts = {}

# ==================== 依赖项 ====================

async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """验证 API Key"""
    if not api_key:
        raise HTTPException(status_code=401, detail="缺少 API Key")
    
    if api_key not in Config.API_KEYS:
        raise HTTPException(status_code=401, detail="无效的 API Key")
    
    key_info = Config.API_KEYS[api_key]
    logger.info(f"API 请求 - Key: {key_info['name']}")
    
    return api_key

async def rate_limit(request: Request, api_key: str = Depends(verify_api_key)) -> str:
    """限流检查"""
    client_ip = request.client.host
    now = datetime.now().replace(second=0, microsecond=0)  # 按分钟限流
    
    key = f"{client_ip}:{now.isoformat()}"
    
    # 初始化计数
    if key not in request_counts:
        request_counts[key] = 0
    
    request_counts[key] += 1
    
    if request_counts[key] > Config.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=429,
            detail=f"请求频率超限（{Config.RATE_LIMIT_PER_MINUTE}次/分钟）"
        )
    
    return api_key

# ==================== API 端点 ====================

@app.get("/", response_model=RobotResponse)
async def root():
    """API 根路径"""
    return RobotResponse(
        success=True,
        message="机器人数据库 API 服务运行中",
        data={
            "docs": "/docs",
            "endpoints": {
                "robots": "/api/robots",
                "search": "/api/robots/search",
                "companies": "/api/companies",
                "stats": "/api/stats",
                "accidents": "/api/accidents/stats"
            }
        }
    )

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "loaded" if database.cache is not None else "not_loaded"
    }

@app.get("/api/robots", response_model=RobotResponse)
async def get_robots(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    api_key: str = Depends(rate_limit)
):
    """获取机器人列表（分页）"""
    try:
        result = database.get_all_robots(page, page_size)
        return RobotResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"获取机器人列表失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/robots/search", response_model=RobotResponse)
async def search_robots(
    q: Optional[str] = Query(None, description="搜索关键词"),
    category: Optional[str] = Query(None, description="类型/分类"),
    company: Optional[str] = Query(None, description="公司名称"),
    price_min: Optional[float] = Query(None, ge=0, description="最低价格"),
    price_max: Optional[float] = Query(None, ge=0, description="最高价格"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    api_key: str = Depends(rate_limit)
):
    """搜索机器人"""
    try:
        result = database.search(
            query=q,
            category=category,
            company=company,
            price_min=price_min,
            price_max=price_max,
            page=page,
            page_size=page_size
        )
        return RobotResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"搜索失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/robots/{robot_id}", response_model=RobotResponse)
async def get_robot(
    robot_id: str,
    api_key: str = Depends(rate_limit)
):
    """获取机器人详情"""
    try:
        result = database.get_by_id(robot_id)
        if not result:
            raise HTTPException(status_code=404, detail="机器人不存在")
        return RobotResponse(success=True, data=result)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取机器人详情失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/companies", response_model=RobotResponse)
async def get_companies(api_key: str = Depends(rate_limit)):
    """获取公司列表"""
    try:
        result = database.get_companies()
        return RobotResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"获取公司列表失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats", response_model=RobotResponse)
async def get_stats(api_key: str = Depends(rate_limit)):
    """获取统计数据"""
    try:
        result = database.get_stats()
        return RobotResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"获取统计数据失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/accidents/stats", response_model=RobotResponse)
async def get_accident_stats(
    company: Optional[str] = Query(None, description="公司名称"),
    year: Optional[int] = Query(None, ge=2000, le=2100, description="年份"),
    api_key: str = Depends(rate_limit)
):
    """获取事故统计"""
    try:
        result = database.get_accident_stats(company=company, year=year)
        return RobotResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"获取事故统计失败：{e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== 错误处理 ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"未处理异常：{exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "服务器内部错误"
        }
    )

# ==================== 主程序 ====================

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("机器人数据库 API 服务启动")
    logger.info(f"数据库路径：{db_path}")
    logger.info(f"API 端口：{Config.API_PORT}")
    logger.info(f"文档地址：http://localhost:{Config.API_PORT}/docs")
    logger.info("=" * 60)
    
    # 测试数据库加载
    try:
        stats = database.get_stats()
        logger.info(f"数据库加载成功：{stats['total_robots']} 条记录")
    except Exception as e:
        logger.error(f"数据库加载失败：{e}")
        raise
    
    # 启动服务
    uvicorn.run(
        app,
        host=Config.API_HOST,
        port=Config.API_PORT,
        log_level="info"
    )
