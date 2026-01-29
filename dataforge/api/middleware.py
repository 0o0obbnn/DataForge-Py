"""
中间件配置模块

配置CORS等中间件
"""

from fastapi.middleware.cors import CORSMiddleware

from ..config.settings import get_settings

settings = get_settings()


def register_middleware(app):
    """
    注册所有中间件

    Args:
        app: FastAPI应用实例
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "Authorization"],
    )
