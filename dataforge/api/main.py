"""
FastAPI主应用模块

DataForge API的主入口，负责应用初始化和路由注册
"""

import logging

import uvicorn
from fastapi import FastAPI

# 导入生成器模块以触发注册
from ..config.settings import get_settings
from ..core.factory import default_registry
from ..core.startup_checks import perform_startup_checks

# 导入API模块
from .exception_handlers import register_exception_handlers
from .middleware import register_middleware
from .routes import register_routes

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

logger.info(f"Registered generators: {len(default_registry.list_generators())}")

# 执行启动检查
try:
    perform_startup_checks()
except RuntimeError as e:
    logger.error(f"Startup failed: {e}")
    raise

# --- App and Settings Initialization ---
settings = get_settings()
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url=(
        settings.docs_url if settings.development_mode else None
    ),  # 生产环境禁用docs
    redoc_url=settings.redoc_url if settings.development_mode else None,
)

# 记录配置信息
env = "Development" if settings.development_mode else "Production"
logger.info(f"Environment: {env}")
logger.info(f"CORS Origins: {settings.allowed_origins}")
docs_status = "Enabled" if settings.development_mode else "Disabled"
logger.info(f"API Docs: {docs_status}")
logger.info(f"Available generators: {len(default_registry.list_generators())}")

# --- Register Components ---
register_exception_handlers(app)
register_middleware(app)
register_routes(app)


def create_app() -> FastAPI:
    """
    创建并返回FastAPI应用实例

    Returns:
        FastAPI应用实例
    """
    return app


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False) -> None:
    """
    运行FastAPI服务器

    Args:
        host: 监听地址
        port: 监听端口
        reload: 是否启用自动重载
    """
    uvicorn.run(
        "dataforge.api.main:app", host=host, port=port, reload=reload, access_log=True
    )


if __name__ == "__main__":
    run_server(reload=True)
