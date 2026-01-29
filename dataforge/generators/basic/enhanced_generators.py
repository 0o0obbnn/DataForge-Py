"""
增强版基础数据生成器

支持上下文关联和数据依赖的高级生成器
"""

import random  # Keep for any remaining uses
import secrets
import string
from datetime import datetime
from typing import Any

from dataforge.core.context import ExtendedGenerationContext, GenerationContext
from dataforge.core.factory import register_generator
from dataforge.core.generator import GeneratorConfig
from dataforge.core.types import GeneratorType
from dataforge.generators.basic.age import AgeGenerator
from dataforge.generators.basic.idcard import IDCardGenerator, IDCardValidator
from dataforge.generators.basic.name import NameGenerator, NameValidator
from dataforge.generators.contact.email import EmailGenerator
from dataforge.generators.contact.phone import PhoneNumberGenerator


class EnhancedNameGenerator(NameGenerator):
    """增强版姓名生成器，支持上下文关联"""

    # 类型注解，使 Pylance 识别父类 __init__ 中赋值的属性
    validator: NameValidator

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.context: ExtendedGenerationContext | None = None

    def set_context(self, context: ExtendedGenerationContext):
        """设置上下文"""
        self.context = context

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成姓名并存储到上下文"""
        name = super().generate_single(context)

        if self.context:
            # 提取姓名信息
            last_name = name[0] if len(name) > 0 else ""
            first_name = name[1:] if len(name) > 1 else ""

            # 确定性别（基于名字特征）
            gender = (
                "female"
                if any(
                    c in first_name
                    for c in ["丽", "娜", "芳", "霞", "莉", "琳", "娟", "雪"]
                )
                else "male"
            )

            self.context.set(
                "name",
                name,
                {
                    "last_name": last_name,
                    "first_name": first_name,
                    "gender": gender,
                    "generator": "EnhancedNameGenerator",
                },
            )
            self.context.add_generation_order("name")

        return name

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        return super().validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


class EnhancedAgeGenerator(AgeGenerator):
    """增强版年龄生成器，支持上下文关联"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.context: ExtendedGenerationContext | None = None

    def set_context(self, context: ExtendedGenerationContext):
        """设置上下文"""
        self.context = context

    def generate_single(self, context: GenerationContext | None = None) -> int:
        """生成年龄并考虑上下文信息"""
        # 从上下文中获取姓名信息
        name_info = None
        if self.context:
            name_info = self.context.get("name")

        # 根据姓名信息调整年龄分布
        age_bias = 0
        if name_info and isinstance(name_info, dict):
            gender = name_info.get("gender")
            if gender == "male":
                age_bias = secrets.randbelow(4)  # 男性年龄稍大
            elif gender == "female":
                age_bias = secrets.randbelow(4) - 3  # 女性年龄稍小

        # 生成基础年龄
        base_age = super().generate_single(context)
        adjusted_age = max(18, min(80, base_age + age_bias))

        if self.context:
            self.context.set(
                "age",
                adjusted_age,
                {
                    "age_group": self._get_age_group(adjusted_age),
                    "name_context": bool(name_info),
                    "generator": "EnhancedAgeGenerator",
                },
            )
            self.context.add_generation_order("age")

        return adjusted_age

    def _get_age_group(self, age: int) -> str:
        """获取年龄组"""
        if age < 18:
            return "youth"
        elif age < 35:
            return "young_adult"
        elif age < 50:
            return "middle_aged"
        else:
            return "senior"

    def validate(self, data: int) -> bool:
        """验证生成的数据"""
        return super().validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


class EnhancedIDCardGenerator(IDCardGenerator):
    """增强版身份证生成器，支持上下文关联"""

    # 类型注解，引用父类 __init__ 中设置的属性
    all_district_codes: list[str]
    validator: IDCardValidator

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.context: ExtendedGenerationContext | None = None

    def set_context(self, context: ExtendedGenerationContext):
        """设置上下文"""
        self.context = context

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成身份证号码并考虑上下文信息"""
        # 从上下文中获取姓名和年龄
        name_info = None
        age = None
        gender = None

        # 优先使用传入的 extended context，否则使用实例的 extended context
        current_context: ExtendedGenerationContext | None = (
            context if isinstance(context, ExtendedGenerationContext) else self.context
        )

        if current_context:
            name_info = current_context.get("name")
            age = current_context.get("age")

            if name_info and isinstance(name_info, dict):
                gender = name_info.get("gender")

        # 如果上下文中有年龄信息，基于年龄生成身份证
        if age and isinstance(age, int):
            # 基于年龄计算出生年份
            current_year = datetime.now().year
            birth_year = current_year - age

            # 生成出生日期（随机月份和日期）
            month = secrets.randbelow(12) + 1
            if month in [1, 3, 5, 7, 8, 10, 12]:
                day = secrets.randbelow(31) + 1
            elif month in [4, 6, 9, 11]:
                day = secrets.randbelow(30) + 1
            else:  # 2月
                day = secrets.randbelow(28) + 1

            birth_date = f"{birth_year:04d}{month:02d}{day:02d}"

            # 生成地区代码（使用父类初始化的地区代码列表）
            region_code = secrets.choice(self.all_district_codes)

            # 生成顺序码（基于性别）
            if gender == "female":
                sequence = secrets.randbelow(1000) * 2  # 偶数
            elif gender == "male":
                sequence = secrets.randbelow(1000) * 2 + 1  # 奇数
            else:
                sequence = secrets.randbelow(1000)

            sequence_str = f"{sequence:03d}"

            # 生成前17位
            id_17 = region_code + birth_date + sequence_str

            # 计算校验位
            check_digit = self._calculate_check_digit(id_17)

            id_card = id_17 + check_digit
        else:
            # 生成基础身份证号码
            id_card = super().generate_single(context)

        # 如果上下文可用，存储额外信息
        if self.context:
            # 解析身份证信息
            region_code = id_card[:6]
            birth_date_from_id = id_card[6:14]
            sequence_str = id_card[14:17]
            check_digit = id_card[17]

            # 计算年龄
            birth_year = int(birth_date_from_id[:4])
            calculated_age = datetime.now().year - birth_year

            # 确定性别
            sequence = int(sequence_str[-1])
            calculated_gender = "male" if sequence % 2 == 1 else "female"

            self.context.set(
                "id_card",
                id_card,
                {
                    "region_code": region_code,
                    "birth_date": birth_date_from_id,
                    "sequence": sequence,
                    "check_digit": check_digit,
                    "calculated_age": calculated_age,
                    "calculated_gender": calculated_gender,
                    "context_age": age,
                    "context_gender": gender,
                    "generator": "EnhancedIDCardGenerator",
                },
            )
            self.context.add_generation_order("id_card")

        return id_card

    def _calculate_check_digit(self, id_17: str) -> str:
        """计算身份证校验位"""
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_codes = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]

        total = sum(int(id_17[i]) * weights[i] for i in range(17))
        return check_codes[total % 11]

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        return super().validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


class EnhancedPhoneGenerator(PhoneNumberGenerator):
    """增强版手机号生成器，支持上下文关联"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.context: ExtendedGenerationContext | None = None

    def set_context(self, context: ExtendedGenerationContext):
        """设置上下文"""
        self.context = context

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成手机号并考虑上下文信息"""
        phone = super().generate_single(context)

        if self.context:
            # 从上下文中获取姓名和年龄
            name_info = self.context.get("name")
            age = self.context.get("age")

            self.context.set(
                "phone",
                phone,
                {
                    "prefix": phone[:3],
                    "suffix": phone[3:],
                    "region": "CN",
                    "context_age": age,
                    "context_name": bool(name_info),
                    "generator": "EnhancedPhoneGenerator",
                },
            )
            self.context.add_generation_order("phone")

        return phone

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        return super().validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.CONTACT

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


class EnhancedEmailGenerator(EmailGenerator):
    """增强版邮箱生成器，支持上下文关联"""

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.context: ExtendedGenerationContext | None = None

    def set_context(self, context: ExtendedGenerationContext):
        """设置上下文"""
        self.context = context

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成邮箱并考虑上下文信息"""
        # 从上下文中获取姓名
        name_info = None
        if self.context:
            name_info = self.context.get("name")

        # 自定义邮箱生成逻辑
        if name_info and isinstance(name_info, dict):
            last_name = name_info.get("last_name", "")
            first_name = name_info.get("first_name", "")

            # 基于姓名生成用户名
            patterns = [
                f"{last_name.lower()}{first_name.lower()}",
                f"{first_name.lower()}{last_name.lower()}",
                f"{last_name.lower()}.{first_name.lower()}",
                f"{first_name.lower()}{secrets.randbelow(900) + 100}",
                f"{last_name.lower()}{secrets.randbelow(900) + 100}",
            ]
            username = secrets.choice(patterns)
        else:
            # 使用基础生成逻辑
            username = "".join(
                random.choices(
                    string.ascii_lowercase + string.digits, k=secrets.randbelow(7) + 6
                )
            )

        # 选择域名
        domains = [
            "gmail.com",
            "yahoo.com",
            "outlook.com",
            "qq.com",
            "163.com",
            "126.com",
            "sina.com",
            "hotmail.com",
            "icloud.com",
            "protonmail.com",
        ]
        domain = secrets.choice(domains)

        email = f"{username}@{domain}"

        if self.context:
            self.context.set(
                "email",
                email,
                {
                    "username": username,
                    "domain": domain,
                    "name_based": bool(name_info),
                    "generator": "EnhancedEmailGenerator",
                },
            )
            self.context.add_generation_order("email")

        return email

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        return super().validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.CONTACT

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


class PersonDataGenerator:
    """个人数据综合生成器"""

    # 声明generators类型
    generators: dict[str, Any]  # type: ignore[assignment]

    def __init__(self, external_context: ExtendedGenerationContext | None = None):
        """
        初始化个人数据生成器

        Args:
            external_context: 可选的外部上下文，用于继承已有数据
        """
        # 使用外部上下文或创建新的
        self.context = (
            external_context if external_context else ExtendedGenerationContext()
        )

        # 创建基础配置
        base_config = GeneratorConfig(generator_type="enhanced", parameters={})

        self.generators = {
            "name": EnhancedNameGenerator(base_config),
            "age": EnhancedAgeGenerator(base_config),
            "id_card": EnhancedIDCardGenerator(base_config),
            "phone": EnhancedPhoneGenerator(base_config),
            "email": EnhancedEmailGenerator(base_config),
        }

        # 为所有生成器设置上下文
        for generator in self.generators.values():
            if hasattr(generator, "set_context"):
                generator.set_context(self.context)

    def set_context(self, context: ExtendedGenerationContext):
        """设置新的上下文"""
        self.context = context
        for generator in self.generators.values():
            if hasattr(generator, "set_context"):
                generator.set_context(context)

    def generate_person(self, **kwargs) -> dict[str, Any]:
        """生成完整的个人数据"""
        # 按依赖顺序生成数据
        data = {}

        # 检查上下文中是否已有数据
        existing_name = self.context.get("name")
        existing_age = self.context.get("age")

        # 只生成缺失的数据
        if not existing_name:
            data["name"] = self.generators["name"].generate_single()
        else:
            data["name"] = existing_name

        if not existing_age:
            data["age"] = self.generators["age"].generate_single()
        else:
            data["age"] = existing_age

        # 生成身份证（基于姓名和年龄）
        # 确保身份证生成器使用当前上下文
        data["id_card"] = self.generators["id_card"].generate_single(self.context)

        # 生成手机号
        data["phone"] = self.generators["phone"].generate_single(self.context)

        # 生成邮箱
        data["email"] = self.generators["email"].generate_single(self.context)

        # 返回包含上下文的数据
        return {
            "data": data,
            "context": self.context.snapshot(),
            "generation_order": self.context.get_generation_order(),
        }

    def generate_batch(self, count: int, **kwargs) -> list[dict[str, Any]]:
        """批量生成个人数据"""
        results = []

        # 保存原始上下文引用
        original_context = self.context

        for i in range(count):
            # 检查是否使用外部上下文
            if original_context is None:
                # 没有外部上下文，创建新的
                self.context = ExtendedGenerationContext()
                # 重新为生成器设置新的上下文
                for generator in self.generators.values():
                    if hasattr(generator, "set_context"):
                        generator.set_context(self.context)
            else:
                # 使用外部上下文，但创建独立的工作副本
                # 这里我们使用原始上下文，但确保每个批次都是独立的
                pass

            # 设置批次信息
            self.context.set("batch_id", i)
            self.context.set("batch_size", count)

            person_data = self.generate_person(**kwargs)
            results.append(person_data)

            # 如果是内部创建的上下文，清除数据
            if original_context is None:
                self.context.clear()

        # 恢复原始上下文
        if original_context is not None:
            self.context = original_context
            # 恢复生成器上下文引用
            for generator in self.generators.values():
                if hasattr(generator, "set_context"):
                    generator.set_context(self.context)

        return results


@register_generator("enhanced_email", ["enhanced-email"])
class GenericEnhancedEmailGenerator(EnhancedEmailGenerator):
    """通用enhanced_email生成器注册版本"""

    pass
