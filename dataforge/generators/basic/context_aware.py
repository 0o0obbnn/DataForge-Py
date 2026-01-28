"""
上下文感知的基础数据生成器

提供支持数据关联性的基础生成器实现
"""

import random  # Keep for random.choices
import secrets
import string
from datetime import datetime, timedelta
from typing import Any

from dataforge.core.context import ContextAwareGenerator, ExtendedGenerationContext
from dataforge.core.factory import register_generator
from dataforge.core.generator import DataGenerator, GenerationContext, GeneratorConfig
from dataforge.core.types import GeneratorType

from ...data.loader import load_json


class ContextAwareNameGenerator(ContextAwareGenerator, DataGenerator):
    """上下文感知的姓名生成器"""

    def __init__(
        self,
        config: GeneratorConfig,
        context: ExtendedGenerationContext | None = None,
    ):
        # DataGenerator需要config参数
        DataGenerator.__init__(self, config)
        # ContextAwareGenerator需要context参数
        ContextAwareGenerator.__init__(self, context)
        self._load_name_data()

    def _load_name_data(self) -> None:
        """从数据文件加载姓名数据"""
        try:
            # 加载姓氏数据
            surnames_data = load_json("surnames.json")
            self._last_names = [
                item["surname"] for item in surnames_data.get("common_surnames", [])
            ]

            # 加载名字数据
            givennames_data = load_json("givennames.json")
            male_names_data = givennames_data.get("male_names", {})
            female_names_data = givennames_data.get("female_names", {})

            # 组合单字和双字名字
            self._first_names = {
                "male": (
                    male_names_data.get("single_char", [])
                    + male_names_data.get("double_char", [])
                ),
                "female": (
                    female_names_data.get("single_char", [])
                    + female_names_data.get("double_char", [])
                ),
            }

            # 如果数据文件加载失败，使用默认值作为fallback
            if not self._last_names:
                self._last_names = [
                    "王",
                    "李",
                    "张",
                    "刘",
                    "陈",
                    "杨",
                    "赵",
                    "黄",
                    "周",
                    "吴",
                    "徐",
                    "孙",
                    "胡",
                    "朱",
                    "高",
                    "林",
                    "何",
                    "郭",
                    "罗",
                    "梁",
                ]

            if not self._first_names.get("male"):
                self._first_names["male"] = [
                    "张伟",
                    "王强",
                    "李军",
                    "刘洋",
                    "陈勇",
                    "杨帆",
                    "赵磊",
                    "黄旭",
                    "周杰",
                    "吴磊",
                    "徐浩",
                    "孙宇",
                    "朱华",
                    "胡斌",
                    "高翔",
                    "林涛",
                    "何明",
                    "郭峰",
                    "罗刚",
                    "梁宇",
                ]

            if not self._first_names.get("female"):
                self._first_names["female"] = [
                    "王丽",
                    "李娜",
                    "张敏",
                    "刘静",
                    "陈丽",
                    "杨芳",
                    "赵雪",
                    "黄莉",
                    "周婷",
                    "吴倩",
                    "徐颖",
                    "孙燕",
                    "朱琳",
                    "胡霞",
                    "高媛",
                    "林娜",
                    "何晶",
                    "郭莉",
                    "罗娟",
                    "梁芳",
                ]
        except (FileNotFoundError, KeyError, Exception) as e:
            # 如果数据文件不存在或加载失败，使用默认值
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                f"Failed to load name data from files: {e}, using default values"
            )

            self._last_names = [
                "王",
                "李",
                "张",
                "刘",
                "陈",
                "杨",
                "赵",
                "黄",
                "周",
                "吴",
                "徐",
                "孙",
                "胡",
                "朱",
                "高",
                "林",
                "何",
                "郭",
                "罗",
                "梁",
            ]
            self._first_names = {
                "male": [
                    "张伟",
                    "王强",
                    "李军",
                    "刘洋",
                    "陈勇",
                    "杨帆",
                    "赵磊",
                    "黄旭",
                    "周杰",
                    "吴磊",
                    "徐浩",
                    "孙宇",
                    "朱华",
                    "胡斌",
                    "高翔",
                    "林涛",
                    "何明",
                    "郭峰",
                    "罗刚",
                    "梁宇",
                ],
                "female": [
                    "王丽",
                    "李娜",
                    "张敏",
                    "刘静",
                    "陈丽",
                    "杨芳",
                    "赵雪",
                    "黄莉",
                    "周婷",
                    "吴倩",
                    "徐颖",
                    "孙燕",
                    "朱琳",
                    "胡霞",
                    "高媛",
                    "林娜",
                    "何晶",
                    "郭莉",
                    "罗娟",
                    "梁芳",
                ],
            }

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成姓名，支持上下文关联"""
        # 若传入扩展上下文，则使用该上下文实例
        if isinstance(context, ExtendedGenerationContext):
            self.context = context

        self.ensure_dependencies()

        # 优先从上下文获取，其次从配置参数获取
        gender = self.get_context_value("gender") or self.parameters.get("gender")

        # 从上下文中获取年龄信息
        age = self.get_context_value("age")

        last_name = secrets.choice(self._last_names)

        if gender:
            first_name = secrets.choice(
                self._first_names.get(gender, self._first_names["male"])
            )
        else:
            # 随机选择性别和对应的名字
            gender = secrets.choice(["male", "female"])
            first_name = secrets.choice(self._first_names[gender])
            # 将性别信息存入上下文
            self.set_context_value("gender", gender)

        full_name = f"{last_name}{first_name}"

        # 将姓名信息存入上下文
        self.set_context_value(
            "name",
            full_name,
            {
                "last_name": last_name,
                "first_name": first_name,
                "gender": gender,
                "age_context": age,
            },
        )

        return full_name

    def validate(self, data: Any) -> bool:
        """验证姓名格式"""
        if not isinstance(data, str):
            return False

        # 中文姓名验证
        if len(data) < 2 or len(data) > 4:
            return False

        # 检查是否包含中文
        chinese_chars = sum(1 for char in data if "\u4e00" <= char <= "\u9fff")
        return chinese_chars >= 2

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


class ContextAwareAgeGenerator(ContextAwareGenerator, DataGenerator):
    """上下文感知的年龄生成器"""

    def __init__(
        self,
        config: GeneratorConfig,
        context: ExtendedGenerationContext | None = None,
    ):
        # DataGenerator需要config参数
        DataGenerator.__init__(self, config)
        # ContextAwareGenerator需要context参数
        ContextAwareGenerator.__init__(self, context)

    def generate_single(self, context: GenerationContext | None = None) -> int:
        """生成年龄，支持上下文关联"""
        # 若传入扩展上下文，则使用该上下文实例
        if isinstance(context, ExtendedGenerationContext):
            self.context = context

        min_age = self.parameters.get("min_age", 18)
        max_age = self.parameters.get("max_age", 80)

        # 从上下文中获取姓名信息
        name_info = self.get_context_value("name")

        # 基于姓名信息调整年龄分布
        if name_info and isinstance(name_info, dict):
            gender = name_info.get("gender")
            if gender == "male":
                # 男性年龄稍微偏大一些
                age_bias = secrets.randbelow(6)
            elif gender == "female":
                # 女性年龄稍微偏小一些
                age_bias = secrets.randbelow(6) - 5
            else:
                age_bias = 0

            age = max(
                min_age,
                min(
                    max_age,
                    secrets.randbelow(max_age - min_age + 1) + min_age + age_bias,
                ),
            )
        else:
            age = secrets.randbelow(max_age - min_age + 1) + min_age

        # 将年龄信息存入上下文
        self.set_context_value(
            "age",
            age,
            {
                "min_age": min_age,
                "max_age": max_age,
                "age_group": self._get_age_group(age),
            },
        )

        return age

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

    def validate(self, data: Any) -> bool:
        """验证年龄"""
        return isinstance(data, int) and 0 <= data <= 120

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


class ContextAwareIDCardGenerator(ContextAwareGenerator, DataGenerator):
    """上下文感知的身份证生成器"""

    def __init__(
        self,
        config: GeneratorConfig,
        context: ExtendedGenerationContext | None = None,
    ):
        # DataGenerator需要config参数
        DataGenerator.__init__(self, config)
        # ContextAwareGenerator需要context参数
        ContextAwareGenerator.__init__(self, context)

        # 地区代码（部分示例）
        self._region_codes = [
            "110101",
            "110102",
            "110105",
            "110106",  # 北京
            "310101",
            "310104",
            "310105",
            "310106",  # 上海
            "440103",
            "440104",
            "440105",
            "440106",  # 广州
            "420102",
            "420103",
            "420104",
            "420105",  # 武汉
            "510104",
            "510105",
            "510106",
            "510107",  # 成都
        ]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成身份证号码，支持上下文关联"""
        # 若传入扩展上下文，则使用该上下文实例
        if isinstance(context, ExtendedGenerationContext):
            self.context = context

        self.add_dependency("age", "gender")
        self.ensure_dependencies()

        # 从上下文中获取年龄和性别
        age = self.get_context_value("age")
        name_info = self.get_context_value("name")
        gender = name_info.get("gender") if isinstance(name_info, dict) else None

        # 地区代码
        region_code = secrets.choice(self._region_codes)

        # 出生日期
        if age:
            birth_date = self._calculate_birth_date(age)
        else:
            birth_date = self._generate_random_birth_date()

        # 顺序码（基于性别调整）
        sequence = secrets.randbelow(999) + 1
        if gender == "male" and sequence % 2 == 0:
            sequence += 1  # 男性奇数
        elif gender == "female" and sequence % 2 == 1:
            sequence += 1  # 女性偶数

        sequence_str = f"{sequence:03d}"

        # 前17位
        id_17 = f"{region_code}{birth_date}{sequence_str}"

        # 计算校验位
        check_digit = self._calculate_check_digit(id_17)

        id_card = f"{id_17}{check_digit}"

        # 将身份证信息存入上下文
        self.set_context_value(
            "id_card",
            id_card,
            {
                "region_code": region_code,
                "birth_date": birth_date,
                "sequence": sequence_str,
                "check_digit": check_digit,
                "gender": gender,
                "age": age,
            },
        )

        return id_card

    def _calculate_birth_date(self, age: int) -> str:
        """根据年龄计算出生日期"""
        today = datetime.now()
        birth_year = today.year - age

        # 随机月份和日期
        month = secrets.randbelow(12) + 1
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = secrets.randbelow(31) + 1
        elif month in [4, 6, 9, 11]:
            day = secrets.randbelow(30) + 1
        else:  # 2月
            if (birth_year % 4 == 0 and birth_year % 100 != 0) or (
                birth_year % 400 == 0
            ):
                day = secrets.randbelow(29) + 1
            else:
                day = secrets.randbelow(28) + 1

        return f"{birth_year:04d}{month:02d}{day:02d}"

    def _generate_random_birth_date(self) -> str:
        """生成随机出生日期"""
        start_date = datetime(1950, 1, 1)
        end_date = datetime(2005, 12, 31)

        random_date = start_date + timedelta(
            days=secrets.randbelow((end_date - start_date).days + 1)
        )

        return f"{random_date.year:04d}{random_date.month:02d}{random_date.day:02d}"

    def _calculate_check_digit(self, id_17: str) -> str:
        """计算身份证校验位"""
        weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        check_digits = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]

        total = sum(int(id_17[i]) * weights[i] for i in range(17))
        return check_digits[total % 11]

    def validate(self, data: Any) -> bool:
        """验证身份证号码"""
        if not isinstance(data, str) or len(data) != 18:
            return False

        # 基本格式验证
        if not data[:-1].isdigit():
            return False

        # 校验位验证
        return data[-1].upper() == self._calculate_check_digit(data[:-1])

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


class ContextAwareEmailGenerator(ContextAwareGenerator, DataGenerator):
    """上下文感知的邮箱生成器"""

    def __init__(
        self,
        config: GeneratorConfig,
        context: ExtendedGenerationContext | None = None,
    ):
        # DataGenerator需要config参数
        DataGenerator.__init__(self, config)
        # ContextAwareGenerator需要context参数
        ContextAwareGenerator.__init__(self, context)

        self._domains = [
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

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成邮箱地址，支持上下文关联"""
        # 若传入扩展上下文，则使用该上下文实例
        if isinstance(context, ExtendedGenerationContext):
            self.context = context

        self.add_dependency("name")
        self.ensure_dependencies()

        # 从上下文中获取姓名
        name_info = self.get_context_value("name")

        # 生成用户名
        if name_info and isinstance(name_info, dict):
            last_name = name_info.get("last_name", "")
            first_name = name_info.get("first_name", "")

            # 基于姓名生成用户名
            username_patterns = [
                f"{last_name.lower()}{first_name.lower()}",
                f"{first_name.lower()}{last_name.lower()}",
                f"{last_name.lower()}.{first_name.lower()}",
                f"{first_name.lower()}{secrets.randbelow(900) + 100}",
                f"{last_name.lower()}{secrets.randbelow(900) + 100}",
            ]
            username = secrets.choice(username_patterns)
        else:
            # 随机用户名
            username = "".join(
                random.choices(
                    string.ascii_lowercase + string.digits, k=secrets.randbelow(7) + 6
                )
            )

        # 选择域名
        domain = secrets.choice(self._domains)

        email = f"{username}@{domain}"

        # 将邮箱信息存入上下文
        self.set_context_value(
            "email",
            email,
            {"username": username, "domain": domain, "name_based": bool(name_info)},
        )

        return email

    def validate(self, data: Any) -> bool:
        """验证邮箱地址"""
        if not isinstance(data, str) or "@" not in data:
            return False

        username, domain = data.split("@", 1)

        if not username or not domain:
            return False

        # 基本格式验证
        return username.replace(".", "").replace("_", "").replace("-", "").isalnum()

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


class ContextAwarePhoneGenerator(ContextAwareGenerator, DataGenerator):
    """上下文感知的手机号生成器"""

    def __init__(
        self,
        config: GeneratorConfig,
        context: ExtendedGenerationContext | None = None,
    ):
        # DataGenerator需要config参数
        DataGenerator.__init__(self, config)
        # ContextAwareGenerator需要context参数
        ContextAwareGenerator.__init__(self, context)

        # 中国大陆手机号段
        self._prefixes = [
            "130",
            "131",
            "132",
            "133",
            "134",
            "135",
            "136",
            "137",
            "138",
            "139",
            "150",
            "151",
            "152",
            "153",
            "155",
            "156",
            "157",
            "158",
            "159",
            "170",
            "176",
            "177",
            "178",
            "180",
            "181",
            "182",
            "183",
            "184",
            "185",
            "186",
            "187",
            "188",
            "189",
            "190",
            "191",
            "192",
            "193",
            "195",
            "196",
            "197",
            "198",
            "199",
        ]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成手机号，支持上下文关联"""
        # 若传入扩展上下文，则使用该上下文实例
        if isinstance(context, ExtendedGenerationContext):
            self.context = context

        # 从上下文中获取姓名和年龄信息
        name_info = self.get_context_value("name")
        age = self.get_context_value("age")

        # 选择号段
        prefix = secrets.choice(self._prefixes)

        # 生成后8位
        suffix = "".join(random.choices("0123456789", k=8))

        phone = f"{prefix}{suffix}"

        # 将手机号信息存入上下文
        self.set_context_value(
            "phone",
            phone,
            {
                "prefix": prefix,
                "suffix": suffix,
                "region": "CN",
                "age_context": age,
                "name_context": bool(name_info),
            },
        )

        return phone

    def validate(self, data: Any) -> bool:
        """验证手机号"""
        if not isinstance(data, str) or len(data) != 11:
            return False

        return data.isdigit() and data.startswith(tuple(self._prefixes))

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return []


@register_generator("context_aware_name", ["context-aware-name", "can"])
class GenericContextAwareNameGenerator(ContextAwareNameGenerator):
    """通用context_aware_name生成器注册版本"""

    pass


@register_generator("context_aware_age", ["context-aware-age", "caa"])
class GenericContextAwareAgeGenerator(ContextAwareAgeGenerator):
    """通用context_aware_age生成器注册版本"""

    pass


@register_generator("context_aware_id_card", ["context-aware-id-card", "caic"])
class GenericContextAwareIDCardGenerator(ContextAwareIDCardGenerator):
    """通用context_aware_id_card生成器注册版本"""

    pass


@register_generator("context_aware_email", ["context-aware-email", "cae"])
class GenericContextAwareEmailGenerator(ContextAwareEmailGenerator):
    """通用context_aware_email生成器注册版本"""

    pass


@register_generator("context_aware_phone", ["context-aware-phone", "cap"])
class GenericContextAwarePhoneGenerator(ContextAwarePhoneGenerator):
    """通用context_aware_phone生成器注册版本"""

    pass
