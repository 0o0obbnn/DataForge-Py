"""
异常处理器模块

定义FastAPI的异常处理函数
"""

import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from ..core.exceptions import DataForgeException, GeneratorNotFoundError

logger = logging.getLogger(__name__)


def register_exception_handlers(app):
    """
    注册所有异常处理器

    Args:
        app: FastAPI应用实例
    """

    @app.exception_handler(DataForgeException)
    async def dataforge_exception_handler(request: Request, exc: DataForgeException):
        """
        处理DataForge自定义异常

        将自定义异常转换为标准化的JSON错误响应
        """
        status_code = 400
        if isinstance(exc, GeneratorNotFoundError):
            status_code = 404
        return JSONResponse(
            status_code=status_code,
            content={
                "error": {
                    "type": exc.error_code or "DATA_FORGE_ERROR",
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """
        处理通用异常

        捕获所有未处理的异常，返回500错误
        """
        logger.error(
            f"Unhandled exception for request {request.url}: {exc}", exc_info=True
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "type": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected internal server error occurred.",
                }
            },
        )
