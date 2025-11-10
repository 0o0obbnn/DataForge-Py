"""
应用全局配置模块

提供安全的配置管理，包括环境变量验证和开发/生产模式区分
"""

import logging
import os
import secrets
from typing import List
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AppSettings(BaseModel):
    """应用全局配置"""

    # API设置
    api_version: str = "1.0.0"
    api_title: str = "DataForge API"
    api_description: str = "高效、灵活的测试数据生成API服务"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    # 环境设置
    development_mode: bool = os.getenv("DEVELOPMENT", "false").lower() == "true"

    # CORS设置
    allowed_origins: List[str] = []

    # Redis设置
    redis_host: str = os.getenv("REDIS_HOST", "localhost")
    redis_port: int = int(os.getenv("REDIS_PORT", "6379"))

    # JWT认证设置
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 30

    def __init__(self, **data):
        super().__init__(**data)
        self._initialize_security_settings()

    def _initialize_security_settings(self):
        """初始化安全配置

        根据环境模式（开发/生产）验证并设置安全相关配置
        """
        # JWT密钥配置
        self.jwt_secret_key = self.validate_jwt_secret()

        # CORS配置
        self.allowed_origins = self._get_cors_origins()

    def validate_jwt_secret(self):
        """验证JWT密钥配置"""
        jwt_key = os.getenv("JWT_SECRET_KEY")

        if jwt_key:
            return jwt_key
        elif self.development_mode:
            # 开发模式：使用固定的开发密钥（带明显警告）
            logger.warning("⚠️  Using insecure development JWT key!")
            logger.warning("⚠️  Set JWT_SECRET_KEY environment variable for production!")
            return "DEV-ONLY-INSECURE-KEY-DO-NOT-USE-IN-PRODUCTION"
        else:
            # 生产模式：必须设置环境变量
            raise ValueError(
                "JWT_SECRET_KEY environment variable must be set in production! "
                "Generate a secure key with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )

    def _get_cors_origins(self):
        """获取CORS配置"""
        cors_origins = os.getenv("ALLOWED_ORIGINS")

        if cors_origins:
            # 移除空白字符并过滤空字符串
            return [
                origin.strip() for origin in cors_origins.split(",") if origin.strip()
            ]
        elif self.development_mode:
            # 开发模式：允许localhost
            return [
                "http://localhost:3000",
                "http://localhost:8080",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:8080",
            ]
        else:
            # 生产模式：必须明确设置
            raise ValueError(
                "ALLOWED_ORIGINS environment variable must be set in production! "
                "Example: ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com"
            )

    @property
    def cors_origins(self):
        """获取CORS来源列表"""
        return self.allowed_origins


# 全局配置实例（延迟初始化）
_settings: AppSettings | None = None


def get_settings() -> AppSettings:
    """返回全局配置实例（延迟初始化）

    Returns:
        AppSettings: 应用配置对象
    """
    global _settings
    if _settings is None:
        _settings = AppSettings()
    return _settings


# 为了向后兼容，提供settings属性
settings = get_settings()
