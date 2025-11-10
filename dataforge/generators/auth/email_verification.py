"""
邮箱验证码生成器
Email verification code generator for account authentication.
"""

import random
import string
from datetime import datetime, timedelta
from typing import Any, Optional

from dataforge.core.factory import register_generator
from dataforge.core.generator import DataGenerator, GenerationContext, GeneratorType


@register_generator("email_verification", ["email_code"])
class EmailVerificationGenerator(DataGenerator[str]):
    """
    邮箱验证码生成器

    功能特性：
    - 生成6-8位数字验证码
    - 支持自定义长度和有效期
    - 包含时间戳和过期验证
    - 支持防暴力破解的复杂度设置
    
    返回类型：
    - 默认返回字符串（仅验证码）
    - 设置 string_only=False 返回完整字典
    """

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.AUTH

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "length",
            "expires_in",
            "complexity",
            "prefix",
            "include_timestamp",
            "case_sensitive",
            "max_attempts",
            "string_only",
        ]

    def _setup(self) -> None:
        """初始化设置"""
        self.default_config = {
            "length": 6,
            "expires_in": 1800,
            "complexity": "numeric",
            "include_timestamp": True,
            "subject": "邮箱验证码",
            "template": "default",
            "prefix": "",
            "case_sensitive": False,
            "max_attempts": 3,
            "string_only": True,  # 默认返回字符串
        }

    def _get_effective_config(self) -> dict[str, Any]:
        """获取有效配置（合并默认配置和用户参数）"""
        config = self.default_config.copy()
        config.update(self.parameters)
        return config

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始邮箱验证码数据"""
        config = self._get_effective_config()

        length = config["length"]
        complexity = config["complexity"]
        prefix = config.get("prefix", "")
        include_timestamp = config.get("include_timestamp", True)
        string_only = config.get("string_only", True)

        # 根据复杂度选择字符集
        if complexity == "simple" or complexity == "numeric":
            charset = string.digits
        elif complexity == "medium":
            charset = string.digits + string.ascii_uppercase
        else:  # strong
            charset = string.digits + string.ascii_letters + "!@#$%^&*"

        # 生成验证码
        code = "".join(random.choices(charset, k=length))
        if prefix:
            code = f"{prefix}{code}"

        # 如果只需要字符串，直接返回验证码
        if string_only:
            return code

        # 计算过期时间 - 使用expires_in秒数
        expires_in = config.get("expires_in", 1800)
        expiry_time = datetime.now() + timedelta(seconds=expires_in)

        result = {
            "code": code,
            "expiry_time": expiry_time.isoformat(),
            "length": length,
            "complexity": complexity,
            "is_used": False,
            "attempts": 0,
            "max_attempts": config.get("max_attempts", 3),
        }

        if include_timestamp:
            result["generated_at"] = datetime.now().isoformat()

        return result

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证验证码数据的有效性"""
        # 如果是字符串，直接验证长度
        if isinstance(data, str):
            return len(data) >= 4  # 最小长度4位
        
        # 如果是字典，验证完整数据
        if not isinstance(data, dict):
            return False

        code = data.get("code")
        if not code or not isinstance(code, str):
            return False

        # 检查格式
        length = data.get("length", 6)
        if len(code) < length:
            return False

        # 检查过期时间
        expiry_str = data.get("expiry_time")
        if expiry_str:
            try:
                expiry_time = datetime.fromisoformat(expiry_str)
                if datetime.now() > expiry_time:
                    return False
            except ValueError:
                return False

        return True

    def is_expired(self, verification_data: dict[str, Any]) -> bool:
        """检查验证码是否过期"""
        expiry_str = verification_data.get("expiry_time")
        if not expiry_str:
            return True

        try:
            expiry_time = datetime.fromisoformat(expiry_str)
            return datetime.now() > expiry_time
        except ValueError:
            return True

    def verify_code(
        self, verification_data: dict[str, Any], input_code: str
    ) -> dict[str, Any]:
        """验证输入的验证码"""
        if not self.validate(verification_data):
            return {
                "valid": False,
                "reason": "invalid_data_format",
                "message": "验证码数据格式无效",
            }

        if self.is_expired(verification_data):
            return {"valid": False, "reason": "expired", "message": "验证码已过期"}

        if verification_data.get("is_used", False):
            return {
                "valid": False,
                "reason": "already_used",
                "message": "验证码已被使用",
            }

        # 检查尝试次数
        attempts = verification_data.get("attempts", 0)
        max_attempts = verification_data.get("max_attempts", 3)

        if attempts >= max_attempts:
            return {
                "valid": False,
                "reason": "max_attempts_exceeded",
                "message": "尝试次数过多",
            }

        # 验证代码
        stored_code = verification_data.get("code", "")
        case_sensitive = self._get_effective_config().get("case_sensitive", False)

        if not case_sensitive:
            stored_code = stored_code.upper()
            input_code = input_code.upper()

        if stored_code == input_code:
            verification_data["is_used"] = True
            return {"valid": True, "reason": "success", "message": "验证成功"}
        else:
            verification_data["attempts"] = attempts + 1
            return {"valid": False, "reason": "invalid_code", "message": "验证码错误"}



    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        # 使用_generate_raw方法生成验证码数据
        verification_data = self._generate_raw(context)
        # 如果是字符串，直接返回
        if isinstance(verification_data, str):
            return verification_data
        # 如果是字典，返回code字段
        return verification_data.get("code", "")
