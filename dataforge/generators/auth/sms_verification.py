"""
短信验证码生成器
SMS verification code generator for mobile authentication.
"""

import random
import string
from datetime import datetime, timedelta
from typing import Any

from dataforge.core.factory import register_generator
from dataforge.core.generator import DataGenerator, GenerationContext, GeneratorType


@register_generator("sms_verification", ["sms_code"])
class SMSVerificationGenerator(DataGenerator[Any]):
    """
    短信验证码生成器

    功能特性：
    - 生成4-6位数字验证码
    - 支持运营商特定格式
    - 包含防刷机制
    - 支持语音验证码格式

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
            "carrier",
            "format",
            "include_timestamp",
            "anti_brute_force",
            "string_only",
        ]

    def _setup(self) -> None:
        """初始化设置"""
        self.default_config = {
            "length": 6,
            "expiry_minutes": 5,
            "carrier": "CMCC",
            "format": "text",
            "template": "SMS_123456789",
            "include_country_code": False,
            "rate_limit": 3,
            "string_only": True,  # 默认返回字符串
        }

    def _get_effective_config(self) -> dict[str, Any]:
        """获取有效配置（合并默认配置和用户参数）"""
        config = self.default_config.copy()
        config.update(self.parameters)
        return config

    def _generate_raw(
        self, context: GenerationContext | None = None
    ) -> str | dict[str, Any]:
        """生成原始短信验证码数据"""
        config = self._get_effective_config()

        length = config["length"]
        carrier = config["carrier"]
        format_type = config["format"]
        template = config["template"]
        string_only = config.get("string_only", True)

        # 生成纯数字验证码
        code = "".join(random.choices(string.digits, k=length))

        # 如果只需要字符串，直接返回验证码
        if string_only:
            return code

        # 生成过期时间（短信通常有效期较短）
        expiry_time = datetime.now() + timedelta(minutes=config["expiry_minutes"])

        # 生成请求ID（用于防重放攻击）
        request_id = f"SMS_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"

        result = {
            "code": code,
            "phone_number": None,  # 需要配合phone生成器使用
            "expiry_time": expiry_time.isoformat(),
            "request_id": request_id,
            "carrier": carrier,
            "format": format_type,
            "template": template,
            "length": length,
            "is_used": False,
            "attempts": 0,
            "max_attempts": 3,
            "rate_limit": config["rate_limit"],
            "generated_at": datetime.now().isoformat(),
        }

        # 根据运营商添加特定格式
        if carrier == "CMCC":
            result["carrier_name"] = "中国移动"
        elif carrier == "CUCC":
            result["carrier_name"] = "中国联通"
        elif carrier == "CTCC":
            result["carrier_name"] = "中国电信"

        # 语音验证码特殊处理
        if format_type == "voice":
            result["voice_template"] = f"您的验证码是：{code}，请在5分钟内使用。"
            result["repeat_count"] = 3

        return result

    def validate(self, data: str | dict[str, Any]) -> bool:
        """验证短信验证码数据的有效性"""
        # 如果是字符串，直接验证格式
        if isinstance(data, str):
            return data.isdigit() and len(data) >= 4

        # 如果是字典，验证完整数据
        if not isinstance(data, dict):
            return False

        code = data.get("code")
        if not code or not isinstance(code, str):
            return False

        # 检查是否为纯数字
        if not code.isdigit():
            return False

        # 检查长度
        length = data.get("length", 6)
        if len(code) != length:
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
        """验证输入的短信验证码"""
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
        if stored_code == input_code:
            verification_data["is_used"] = True
            return {"valid": True, "reason": "success", "message": "验证成功"}
        else:
            verification_data["attempts"] = attempts + 1
            return {"valid": False, "reason": "invalid_code", "message": "验证码错误"}

    def get_sms_content(self, verification_data: dict[str, Any]) -> str:
        """获取短信发送内容"""
        if not self.validate(verification_data):
            return ""

        code = verification_data.get("code", "")
        template = verification_data.get("template", "SMS_123456789")

        # 标准短信模板
        templates = {
            "SMS_123456789": f"【DataForge】您的验证码是：{code}，请在5分钟内使用。如非本人操作请忽略。",
            "SMS_LOGIN": f"【DataForge】登录验证码：{code}，有效期5分钟。请勿泄露给他人。",
            "SMS_REGISTER": f"【DataForge】注册验证码：{code}，有效期5分钟。完成注册后请删除此短信。",
        }

        return templates.get(template, templates["SMS_123456789"])

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        # 使用_generate_raw方法生成验证码数据
        verification_data = self._generate_raw(context)
        # 如果是字符串，直接返回
        if isinstance(verification_data, str):
            return verification_data
        # 如果是字典，返回code字段
        return verification_data.get("code", "")
