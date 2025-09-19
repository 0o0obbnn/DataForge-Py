"""
DataForge核心生成器接口和基类
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, Optional, TypeVar

T = TypeVar("T")


class GeneratorType(Enum):
    """生成器类型枚举"""

    BASIC_INFO = "basic_info"
    IDENTIFIER = "identifier"
    CONTACT = "contact"
    NETWORK = "network"
    TEXT = "text"
    STRUCTURED = "structured"
    NUMERIC = "numeric"
    DATETIME = "datetime"
    SECURITY = "security"
    MEDIA = "media"
    ENUM = "enum"
    SPECIAL = "special"
    USERNAME = "username"
    PASSWORD = "password"
    EMAIL_VERIFICATION = "email_verification"
    SMS_VERIFICATION = "sms_verification"
    FINANCE = "finance"


@dataclass
class GeneratorConfig:
    """生成器配置类"""

    generator_type: str  # 生成器名称，用于在工厂中查找生成器类
    parameters: dict[str, Any] = None
    count: int = 1
    validate: bool = True
    unique: bool = False
    related_fields: Optional[dict[str, str]] = None

    def __post_init__(self):
        """初始化后处理"""
        if self.parameters is None:
            self.parameters = {}


@dataclass
class GenerationContext:
    """生成上下文类，用于在生成过程中传递相关数据"""

    related_data: Optional[dict[str, Any]] = None
    generation_id: Optional[str] = None
    batch_id: Optional[str] = None
    user_id: Optional[str] = None
    session_data: Optional[dict[str, Any]] = None

    def __post_init__(self):
        """初始化后处理"""
        if self.related_data is None:
            self.related_data = {}
        if self.session_data is None:
            self.session_data = {}


class DataGenerator(ABC, Generic[T]):
    """数据生成器抽象基类"""

    def __init__(self, config: GeneratorConfig):
        """
        初始化数据生成器

        Args:
            config: 生成器配置
        """
        self.config = config
        self.parameters = config.parameters or {}
        self._setup()

    @abstractmethod
    def _setup(self) -> None:
        """设置生成器参数，子类必须实现"""
        pass

    @abstractmethod
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> T:
        """生成原始数据，子类必须实现"""
        pass

    def generate(self, context: Optional[GenerationContext] = None) -> T:
        """
        生成数据

        Args:
            context: 生成上下文

        Returns:
            生成的数据
        """
        return self._generate_raw(context)

    def generate_batch(self, count: int, context: Optional[GenerationContext] = None) -> list[T]:
        """
        批量生成数据

        Args:
            count: 生成数量
            context: 生成上下文

        Returns:
            生成的数据列表
        """
        return [self.generate(context) for _ in range(count)]

    def validate(self, data: T) -> bool:
        """
        验证数据有效性，默认实现返回True

        Args:
            data: 要验证的数据

        Returns:
            验证结果
        """
        return True

    @property
    @abstractmethod
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        pass

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


class ValidatedDataGenerator(DataGenerator[T], ABC):
    """带验证功能的数据生成器基类"""

    def generate(self, context: Optional[GenerationContext] = None) -> T:
        """
        生成并验证数据

        Args:
            context: 生成上下文

        Returns:
            生成的数据

        Raises:
            ValueError: 如果生成的数据无效
        """
        data = self._generate_raw(context)
        if self.config.validate and not self.validate(data):
            raise ValueError(f"Generated data failed validation: {data}")
        return data