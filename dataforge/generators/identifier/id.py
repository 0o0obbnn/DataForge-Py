"""
标识类生成器
"""

import random  # TODO: Convert to secrets
import secrets
import time
import uuid
from datetime import datetime
from typing import Any, Optional

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
)
from ...core.protocols import Validator
from ...core.types import GeneratorType

# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


class UUIDValidator(Validator):
    """Validator for UUIDs."""

    def __init__(self, format_style: str):
        self.format_style = format_style

    def validate(self, data: str) -> bool:
        """校验UUID"""
        if not isinstance(data, str):
            return False

        try:
            # 尝试解析UUID
            if self.format_style.upper() == "NO_HYPHENS":
                if len(data) != 32:
                    return False
                # 添加连字符后验证
                formatted = (
                    f"{data[:8]}-{data[8:12]}-{data[12:16]}-{data[16:20]}-{data[20:]}"
                )
                uuid.UUID(formatted)
            else:
                uuid.UUID(data)
            return True
        except ValueError:
            return False

    @property
    def error_message(self) -> str:
        return "Invalid UUID format"


class UUIDGenerator(DataGenerator[str]):
    """UUID生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.version = self.parameters.get("version", 4)  # UUID版本 1,3,4,5
        self.format_style = self.parameters.get(
            "format", "STANDARD"
        )  # STANDARD, NO_HYPHENS, UPPERCASE
        self.namespace = self.parameters.get("namespace", None)  # 用于v3和v5
        self.name = self.parameters.get("name", None)  # 用于v3和v5
        self.validator = UUIDValidator(self.format_style)

    def _setup(self) -> None:
        self.version = self.parameters.get("version", 4)  # UUID版本 1,3,4,5
        self.format_style = self.parameters.get(
            "format", "STANDARD"
        )  # STANDARD, NO_HYPHENS, UPPERCASE
        self.namespace = self.parameters.get("namespace", None)  # 用于v3和v5
        self.name = self.parameters.get("name", None)  # 用于v3和v5

    def generate(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始UUID"""
        if self.version == 1:
            # 基于MAC地址和时间的UUID
            generated_uuid = uuid.uuid1()
        elif self.version == 3:
            # 基于MD5散列的UUID
            namespace = self._get_namespace()
            name = self.name or str(secrets.randbelow(1000000) / 1000000)
            generated_uuid = uuid.uuid3(namespace, name)
        elif self.version == 5:
            # 基于SHA-1散列的UUID
            namespace = self._get_namespace()
            name = self.name or str(secrets.randbelow(1000000) / 1000000)
            generated_uuid = uuid.uuid5(namespace, name)
        else:  # version 4 (默认)
            # 随机UUID
            generated_uuid = uuid.uuid4()

        # 格式化输出
        return self._format_uuid(str(generated_uuid))

    def _get_namespace(self) -> uuid.UUID:
        """获取命名空间"""
        if self.namespace:
            if isinstance(self.namespace, str):
                return uuid.UUID(self.namespace)
            return self.namespace
        return uuid.NAMESPACE_DNS  # 默认命名空间

    def _format_uuid(self, uuid_str: str) -> str:
        """格式化UUID"""
        if self.format_style.upper() == "NO_HYPHENS":
            return uuid_str.replace("-", "")
        elif self.format_style.upper() == "UPPERCASE":
            return uuid_str.upper()
        else:  # STANDARD
            return uuid_str.lower()

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["format", "name", "namespace", "version"]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


class ULIDValidator(Validator):
    """Validator for ULIDs."""

    BASE32_CHARS = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

    def validate(self, data: str) -> bool:
        """校验ULID"""
        if not isinstance(data, str):
            return False

        # 检查长度
        if len(data) != 26:
            return False

        # 检查字符集
        valid_chars = set(self.BASE32_CHARS + self.BASE32_CHARS.lower())
        if not all(c in valid_chars for c in data):
            return False

        return True

    @property
    def error_message(self) -> str:
        return "Invalid ULID format"


class ULIDGenerator(DataGenerator[str]):
    """ULID生成器 (Universally Unique Lexicographically Sortable Identifier)"""

    # Crockford's Base32编码字符集
    BASE32_CHARS = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.lowercase = self.parameters.get("lowercase", False)
        self.timestamp = self.parameters.get("timestamp", None)  # 固定时间戳
        self.validator = ULIDValidator()

    def _setup(self) -> None:
        self.lowercase = self.parameters.get("lowercase", False)
        self.timestamp = self.parameters.get("timestamp", None)  # 固定时间戳

    def generate(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始ULID"""
        # 获取时间戳部分(48位)
        if self.timestamp:
            timestamp_ms = int(self.timestamp)
        else:
            timestamp_ms = int(time.time() * 1000)

        # 时间戳编码为10个字符
        timestamp_part = self._encode_timestamp(timestamp_ms)

        # 随机部分(80位) - 16个字符
        random_part = self._generate_random_part()

        ulid = timestamp_part + random_part

        return ulid.lower() if self.lowercase else ulid

    def _encode_timestamp(self, timestamp_ms: int) -> str:
        """编码时间戳为10个字符"""
        result = ""
        for _ in range(10):
            result = self.BASE32_CHARS[timestamp_ms % 32] + result
            timestamp_ms //= 32
        return result

    def _generate_random_part(self) -> str:
        """生成16个字符的随机部分"""
        return "".join(random.choices(self.BASE32_CHARS, k=16))

    def extract_timestamp(self, ulid: str) -> Optional[datetime]:
        """从ULID中提取时间戳"""
        if not self.validator.validate(ulid):
            return None

        try:
            timestamp_part = ulid[:10].upper()
            timestamp_ms = 0

            for char in timestamp_part:
                timestamp_ms = timestamp_ms * 32 + self.BASE32_CHARS.index(char)

            return datetime.fromtimestamp(timestamp_ms / 1000)
        except (ValueError, OSError):
            return None

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["lowercase", "timestamp"]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


class BusinessNumberValidator(Validator):
    """Validator for business numbers."""

    def __init__(
        self,
        length: int,
        prefix: str,
        business_type: str,
        type_prefixes: dict,
        checksum: bool,
    ):
        self.length = length
        self.prefix = prefix
        self.business_type = business_type
        self.type_prefixes = type_prefixes
        self.checksum = checksum

    def validate(self, data: str) -> bool:
        """校验业务单据号"""
        if not isinstance(data, str):
            return False

        # 基本长度检查
        if len(data) > self.length:
            return False

        # 检查前缀
        expected_prefix = self.prefix or self.type_prefixes.get(
            self.business_type.upper(), "BIZ"
        )
        if not data.startswith(expected_prefix):
            return False

        # 如果有校验位，验证校验位
        if self.checksum:
            check_part = data[-1]
            main_part = data[:-1]
            expected_check = self._calculate_checksum(main_part)
            if check_part != str(expected_check):
                return False

        return True

    def _calculate_checksum(self, number: str) -> int:
        """计算校验位（使用模10算法）"""
        # 移除非数字字符
        digits = "".join(c for c in number if c.isdigit())

        total = 0
        for i, digit in enumerate(reversed(digits)):
            n = int(digit)
            if i % 2 == 1:  # 奇数位置
                n *= 2
                if n > 9:
                    n = n // 10 + n % 10
            total += n

        return (10 - (total % 10)) % 10

    @property
    def error_message(self) -> str:
        return "Invalid business number format"


class BusinessNumberGenerator(DataGenerator[str]):
    """业务单据号生成器"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.prefix = self.parameters.get("prefix", "BIZ")  # 前缀
        self.length = self.parameters.get("length", 12)  # 总长度
        self.number_length = self.parameters.get("number_length", None)  # 数字部分长度
        self.date_format = self.parameters.get(
            "date_format", None
        )  # 日期格式 YYYYMMDD, YYMMDD
        self.separator = self.parameters.get("separator", "")  # 分隔符
        self.sequence_start = self.parameters.get("sequence_start", 1)  # 序列号起始
        self.checksum = self.parameters.get("checksum", False)  # 是否包含校验位
        self.business_type = self.parameters.get("type", "ORDER")  # 业务类型

        # 业务类型默认前缀
        self.type_prefixes = {
            "ORDER": "ORD",  # 订单号
            "INVOICE": "INV",  # 发票号
            "PAYMENT": "PAY",  # 支付单号
            "REFUND": "REF",  # 退款单号
            "RECEIPT": "RCP",  # 收据号
            "CONTRACT": "CON",  # 合同号
            "TICKET": "TKT",  # 票据号
            "SHIPMENT": "SHP",  # 运单号
            "VOUCHER": "VCH",  # 凭证号
        }
        self.validator = BusinessNumberValidator(
            self.length,
            self.prefix,
            self.business_type,
            self.type_prefixes,
            self.checksum,
        )

    def _setup(self) -> None:
        self.prefix = self.parameters.get("prefix", "BIZ")  # 前缀
        self.length = self.parameters.get("length", 12)  # 总长度
        self.number_length = self.parameters.get("number_length", None)  # 数字部分长度
        self.date_format = self.parameters.get(
            "date_format", None
        )  # 日期格式 YYYYMMDD, YYMMDD
        self.separator = self.parameters.get("separator", "")  # 分隔符
        self.sequence_start = self.parameters.get("sequence_start", 1)  # 序列号起始
        self.checksum = self.parameters.get("checksum", False)  # 是否包含校验位
        self.business_type = self.parameters.get("type", "ORDER")  # 业务类型

    def generate(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始业务单据号"""
        parts = []

        # 1. 前缀部分
        prefix = self.prefix or self.type_prefixes.get(
            self.business_type.upper(), "BIZ"
        )
        parts.append(prefix)

        # 2. 日期部分
        if self.date_format:
            date_part = self._generate_date_part()
            parts.append(date_part)

        # 3. 数字序列部分
        number_part = self._generate_number_part()
        parts.append(number_part)

        # 4. 校验位
        if self.checksum:
            temp_number = self.separator.join(parts)
            check_digit = self._calculate_checksum(temp_number)
            parts.append(str(check_digit))

        # 组合结果
        result = self.separator.join(parts)

        # 确保总长度符合要求
        if len(result) > self.length:
            # 截断数字部分
            excess = len(result) - self.length
            if len(number_part) > excess:
                number_part = number_part[:-excess]
                parts[-2 if self.checksum else -1] = number_part
                result = self.separator.join(parts)

        return result

    def _generate_date_part(self) -> str:
        """生成日期部分（安全处理可选格式）"""
        now = datetime.now()
        df = self.date_format
        if not isinstance(df, str) or not df:
            # 当未设置日期格式时返回空串，调用方需在使用前判断
            return ""
        df_upper = df.upper()
        if df_upper == "YYYYMMDD":
            return now.strftime("%Y%m%d")
        elif df_upper == "YYMMDD":
            return now.strftime("%y%m%d")
        elif df_upper == "MMDD":
            return now.strftime("%m%d")
        else:
            # 明确以字符串作为格式参数，避免 None 传入
            return now.strftime(df)

    def _generate_number_part(self) -> str:
        """生成数字部分"""
        if self.number_length:
            length = self.number_length
        else:
            # 计算剩余长度
            other_parts_length = len(self.prefix or "BIZ")
            if self.date_format:
                other_parts_length += len(self._generate_date_part())
            if self.checksum:
                other_parts_length += 1
            if self.separator:
                separator_count = (2 if self.date_format else 1) + (
                    1 if self.checksum else 0
                )
                other_parts_length += len(self.separator) * separator_count

            length = max(1, self.length - other_parts_length)

        # 生成序列号
        max_value = 10**length - 1
        sequence = (
            secrets.randbelow(max_value - self.sequence_start + 1) + self.sequence_start
        )

        return str(sequence).zfill(length)

    def _calculate_checksum(self, number: str) -> int:
        """计算校验位（使用模10算法）"""
        # 移除非数字字符
        digits = "".join(c for c in number if c.isdigit())

        total = 0
        for i, digit in enumerate(reversed(digits)):
            n = int(digit)
            if i % 2 == 1:  # 奇数位置
                n *= 2
                if n > 9:
                    n = n // 10 + n % 10
            total += n

        return (10 - (total % 10)) % 10

    def parse_number(self, number: str) -> dict[str, Any]:
        """解析业务单据号"""
        result = {
            "original": number,
            "prefix": "",
            "date": "",
            "sequence": "",
            "checksum": "",
            "valid": self.validator.validate(number),
        }

        if not result["valid"]:
            return result

        parts = number.split(self.separator) if self.separator else [number]

        # 解析前缀
        expected_prefix = self.prefix or self.type_prefixes.get(
            self.business_type.upper(), "BIZ"
        )
        if parts[0].startswith(expected_prefix):
            result["prefix"] = expected_prefix
            remaining = parts[0][len(expected_prefix) :]
            if remaining:
                parts[0] = remaining
            else:
                parts = parts[1:]

        # 解析日期（如果有）
        if self.date_format and parts:
            date_length = len(self._generate_date_part())
            if len(parts[0]) >= date_length:
                result["date"] = parts[0][:date_length]
                parts[0] = parts[0][date_length:]
                if not parts[0]:
                    parts = parts[1:]

        # 解析序列号和校验位
        if parts:
            sequence_part = "".join(parts)
            if self.checksum and sequence_part:
                result["checksum"] = sequence_part[-1]
                result["sequence"] = sequence_part[:-1]
            else:
                result["sequence"] = sequence_part

        return result

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return [
            "checksum",
            "date_format",
            "length",
            "number_length",
            "prefix",
            "separator",
            "sequence_start",
            "type",
        ]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return True


@register_generator("generic_uuid", aliases=["uuid", "UUID"])
class GenericUUIDGenerator(UUIDGenerator):
    """通用UUID生成器注册版本"""

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个UUID"""
        return self.generate(context)

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return isinstance(data, str) and bool(data.strip())

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


@register_generator("generic_ulid", aliases=["ulid", "ULID"])
class GenericULIDGenerator(ULIDGenerator):
    """通用ULID生成器注册版本"""

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个ULID"""
        return self.generate(context)

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        if hasattr(self, "validator") and hasattr(self.validator, "validate"):
            return self.validator.validate(data)
        return isinstance(data, str) and bool(data.strip())

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


@register_generator(
    "generic_business_number", aliases=["business_number", "business_id"]
)
class GenericBusinessNumberGenerator(BusinessNumberGenerator):
    """通用业务单据号生成器注册版本"""

    pass


# 通用ID生成器 - 支持多种ID类型
class IDGenerator(DataGenerator[str]):
    """通用ID生成器

    支持多种ID类型：
    - numeric: 纯数字ID
    - uuid: UUID格式
    - sequential: 顺序ID
    - custom: 自定义格式
    """

    def _setup(self) -> None:
        """初始化设置"""
        self.id_type = self.parameters.get("type", "numeric")
        self.length = self.parameters.get("length", 10)
        self.prefix = self.parameters.get("prefix", "")
        self.suffix = self.parameters.get("suffix", "")
        self._counter = 0

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成ID"""
        if self.id_type == "numeric":
            return self._generate_numeric_id()
        elif self.id_type == "uuid":
            return self._generate_uuid_id()
        elif self.id_type == "sequential":
            return self._generate_sequential_id()
        else:
            return self._generate_numeric_id()

    def _generate_numeric_id(self) -> str:
        """生成纯数字ID"""
        digits = "".join(str(secrets.randbelow(10)) for _ in range(self.length))
        return f"{self.prefix}{digits}{self.suffix}"

    def _generate_uuid_id(self) -> str:
        """生成UUID格式ID"""
        return f"{self.prefix}{str(uuid.uuid4())}{self.suffix}"

    def _generate_sequential_id(self) -> str:
        """生成顺序ID"""
        self._counter += 1
        return f"{self.prefix}{self._counter:0{self.length}d}{self.suffix}"

    def validate(self, data: str) -> bool:
        """验证ID"""
        if not isinstance(data, str):
            return False
        if not data:
            return False

        # 检查前缀和后缀
        if self.prefix and not data.startswith(self.prefix):
            return False
        if self.suffix and not data.endswith(self.suffix):
            return False

        return True

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["type", "length", "prefix", "suffix"]


# 注册通用ID生成器
register_generator("id")(IDGenerator)
