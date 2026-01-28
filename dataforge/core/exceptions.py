"""
DataForge统一异常处理模块
"""

from typing import Any


class DataForgeException(Exception):
    """DataForge基础异常类"""

    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}

    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class GeneratorConfigError(DataForgeException):
    """生成器配置错误"""

    def __init__(
        self,
        message: str,
        generator_type: str | None = None,
        invalid_params: list[str] | None = None,
    ):
        super().__init__(message, "GENERATOR_CONFIG_ERROR")
        self.generator_type = generator_type
        self.invalid_params = invalid_params or []


class ValidationError(DataForgeException):
    """数据校验错误"""

    def __init__(
        self,
        message: str,
        data: Any | None = None,
        validation_rule: str | None = None,
    ):
        super().__init__(message, "VALIDATION_ERROR")
        self.data = data
        self.validation_rule = validation_rule


class GeneratorNotFoundError(DataForgeException):
    """生成器未找到错误"""

    def __init__(self, generator_name: str):
        message = f"Generator '{generator_name}' not found in registry"
        super().__init__(message, "GENERATOR_NOT_FOUND")
        self.generator_name = generator_name


class DataGenerationError(DataForgeException):
    """数据生成错误"""

    def __init__(
        self,
        message: str,
        generator_type: str | None = None,
        context: dict[str, Any] | None = None,
    ):
        super().__init__(message, "DATA_GENERATION_ERROR")
        self.generator_type = generator_type
        self.context = context or {}


class RelationError(DataForgeException):
    """数据关联错误"""

    def __init__(
        self,
        message: str,
        field_name: str | None = None,
        related_field: str | None = None,
    ):
        super().__init__(message, "RELATION_ERROR")
        self.field_name = field_name
        self.related_field = related_field


class OutputFormatError(DataForgeException):
    """输出格式错误"""

    def __init__(self, message: str, format_type: str | None = None):
        super().__init__(message, "OUTPUT_FORMAT_ERROR")
        self.format_type = format_type


class APIError(DataForgeException):
    """API相关错误"""

    def __init__(
        self, message: str, status_code: int = 400, endpoint: str | None = None
    ):
        super().__init__(message, "API_ERROR")
        self.status_code = status_code
        self.endpoint = endpoint


class ConfigurationError(DataForgeException):
    """配置错误"""

    def __init__(
        self,
        message: str,
        config_key: str | None = None,
        config_file: str | None = None,
    ):
        super().__init__(message, "CONFIGURATION_ERROR")
        self.config_key = config_key
        self.config_file = config_file


class ResourceError(DataForgeException):
    """资源相关错误（内存、文件等）"""

    def __init__(self, message: str, resource_type: str | None = None):
        super().__init__(message, "RESOURCE_ERROR")
        self.resource_type = resource_type
