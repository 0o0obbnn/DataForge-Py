"""
优化的姓名生成器
使用缓存系统和惰性加载优化性能
"""

import random
import secrets
from typing import Any

from ...core.cache import LazyDataLoader, get_data_file_path
from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
)
from ...core.types import GeneratorType


class OptimizedNameGenerator(DataGenerator[str]):
    """优化的中文姓名生成器"""

    def _setup(self) -> None:
        self.name_type = self.parameters.get("type", "BOTH")  # CN, EN, BOTH
        self.gender = self.parameters.get("gender", "ANY")  # MALE, FEMALE, ANY
        self.surname_file = self.parameters.get("surname_file", None)
        self.givenname_file = self.parameters.get("givenname_file", None)
        self.include_pinyin = self.parameters.get("include_pinyin", False)
        self.compound_surname_ratio = self.parameters.get("compound_surname_ratio", 0.1)

        # 使用惰性加载器加载姓名数据
        self._setup_lazy_loaders()

    def _setup_lazy_loaders(self):
        """设置惰性数据加载器"""
        # 设置姓氏数据加载器
        surnames_path = self.surname_file or get_data_file_path("chinese/surnames.json")
        self._surnames_loader = LazyDataLoader(surnames_path)

        # 设置名字数据加载器
        givennames_path = self.givenname_file or get_data_file_path(
            "chinese/givennames.json"
        )
        self._givennames_loader = LazyDataLoader(givennames_path)

    @property
    def surnames_data(self):
        """获取姓氏数据（惰性加载）"""
        try:
            return self._surnames_loader.data
        except (FileNotFoundError, RuntimeError):
            return self._get_default_surnames_data()

    @property
    def givennames_data(self):
        """获取名字数据（惰性加载）"""
        try:
            return self._givennames_loader.data
        except (FileNotFoundError, RuntimeError):
            return self._get_default_givennames_data()

    @property
    def common_surnames(self):
        """获取常见姓氏"""
        data = self.surnames_data.get("common_surnames", [])
        return data if isinstance(data, list) else []

    @property
    def rare_surnames(self):
        """获取罕见姓氏"""
        data = self.surnames_data.get("rare_surnames", [])
        return data if isinstance(data, list) else []

    @property
    def male_names(self):
        """获取男性名字"""
        data = self.givennames_data.get("male_names", [])
        return data if isinstance(data, list) else []

    @property
    def female_names(self):
        """获取女性名字"""
        data = self.givennames_data.get("female_names", [])
        return data if isinstance(data, list) else []

    @property
    def neutral_names(self):
        """获取中性名字"""
        data = self.givennames_data.get("neutral_names", [])
        return data if isinstance(data, list) else []

    def _get_default_surnames_data(self):
        """获取默认姓氏数据"""
        return {
            "common_surnames": [
                {"surname": "王", "pinyin": "wang", "frequency": 0.0693},
                {"surname": "李", "pinyin": "li", "frequency": 0.0636},
                {"surname": "张", "pinyin": "zhang", "frequency": 0.0626},
                {"surname": "刘", "pinyin": "liu", "frequency": 0.0520},
                {"surname": "陈", "pinyin": "chen", "frequency": 0.0451},
                {"surname": "杨", "pinyin": "yang", "frequency": 0.0384},
                {"surname": "赵", "pinyin": "zhao", "frequency": 0.0302},
                {"surname": "黄", "pinyin": "huang", "frequency": 0.0279},
                {"surname": "周", "pinyin": "zhou", "frequency": 0.0245},
                {"surname": "吴", "pinyin": "wu", "frequency": 0.0226},
            ],
            "rare_surnames": [
                {"surname": "欧阳", "pinyin": "ouyang", "frequency": 0.001},
                {"surname": "太史", "pinyin": "taishi", "frequency": 0.0005},
                {"surname": "端木", "pinyin": "duanmu", "frequency": 0.0003},
                {"surname": "上官", "pinyin": "shangguan", "frequency": 0.0002},
            ],
        }

    def _get_default_givennames_data(self):
        """获取默认名字数据"""
        return {
            "male_names": [
                {"name": "伟", "pinyin": "wei"},
                {"name": "强", "pinyin": "qiang"},
                {"name": "明", "pinyin": "ming"},
                {"name": "军", "pinyin": "jun"},
                {"name": "建华", "pinyin": "jianhua"},
                {"name": "志强", "pinyin": "zhiqiang"},
                {"name": "国华", "pinyin": "guohua"},
                {"name": "建国", "pinyin": "jianguo"},
            ],
            "female_names": [
                {"name": "丽", "pinyin": "li"},
                {"name": "娟", "pinyin": "juan"},
                {"name": "敏", "pinyin": "min"},
                {"name": "静", "pinyin": "jing"},
                {"name": "美丽", "pinyin": "meili"},
                {"name": "秀英", "pinyin": "xiuying"},
                {"name": "淑华", "pinyin": "shuhua"},
                {"name": "玉兰", "pinyin": "yulan"},
            ],
            "neutral_names": [
                {"name": "华", "pinyin": "hua"},
                {"name": "平", "pinyin": "ping"},
                {"name": "安", "pinyin": "an"},
                {"name": "宁", "pinyin": "ning"},
            ],
        }

    def _generate_raw(self, context: GenerationContext | None = None) -> str:
        """生成原始姓名"""
        if self.name_type == "EN":
            return self._generate_english_name()
        elif self.name_type == "CN":
            return self._generate_chinese_name(context)
        else:  # BOTH
            return (
                self._generate_chinese_name(context)
                if (secrets.randbelow(1000000) / 1000000) < 0.8
                else self._generate_english_name()
            )

    def _generate_chinese_name(
        self, context: GenerationContext | None = None
    ) -> str:
        """生成中文姓名"""
        # 1. 选择姓氏
        surname_info = self._select_surname()
        surname = surname_info["surname"]

        # 2. 确定性别（如果有关联数据）
        gender = self._determine_gender(context)

        # 3. 选择名字
        given_name = self._select_given_name(gender)

        # 4. 组合姓名
        full_name = surname + given_name

        # 5. 如果需要拼音
        if self.include_pinyin:
            surname_pinyin = surname_info.get("pinyin", "")
            given_pinyin = self._get_given_name_pinyin(given_name)
            if surname_pinyin and given_pinyin:
                full_name = f"{full_name} ({surname_pinyin} {given_pinyin})"

        return full_name

    def _select_surname(self) -> dict[str, Any]:
        """选择姓氏"""
        # 是否选择复姓
        if (
            secrets.randbelow(1000000) / 1000000
        ) < self.compound_surname_ratio and self.rare_surnames:
            return secrets.choice(self.rare_surnames)

        # 根据频率加权选择常见姓氏
        surnames = self.common_surnames
        if not surnames:
            return {"surname": "王", "pinyin": "wang", "frequency": 1.0}

        weights = [s.get("frequency", 1.0) for s in surnames]
        return random.choices(surnames, weights=weights)[0]

    def _determine_gender(self, context: GenerationContext | None = None) -> str:
        """确定性别"""
        # 如果有关联数据中的性别信息
        if context and context.related_data and "gender" in context.related_data:
            related_gender = context.related_data["gender"]
            if related_gender in ["MALE", "FEMALE"]:
                return related_gender

        # 如果参数指定了性别
        if self.gender in ["MALE", "FEMALE"]:
            return self.gender

        # 随机选择性别
        return secrets.choice(["MALE", "FEMALE"])

    def _select_given_name(self, gender: str) -> str:
        """选择名字"""
        if gender == "MALE":
            name_pool = self.male_names
        elif gender == "FEMALE":
            name_pool = self.female_names
        else:
            # 随机选择男名、女名或中性名
            all_pools = [self.male_names, self.female_names, self.neutral_names]
            name_pool = secrets.choice([pool for pool in all_pools if pool])

        if not name_pool:
            return "明"  # 默认名字

        name_info = secrets.choice(name_pool)

        if isinstance(name_info, dict):

            name = name_info.get("name")

            return str(name) if name is not None else str(name_info)

        else:

            return str(name_info)

    def _get_given_name_pinyin(self, given_name: str) -> str:
        """获取名字的拼音"""
        # 在所有名字中查找对应的拼音
        all_names = self.male_names + self.female_names + self.neutral_names
        for name_info in all_names:
            if isinstance(name_info, dict) and name_info.get("name") == given_name:
                return name_info.get("pinyin", "")
        return ""

    def _generate_english_name(self) -> str:
        """生成英文姓名"""
        first_names = [
            "John",
            "Jane",
            "Michael",
            "Emily",
            "David",
            "Sarah",
            "Robert",
            "Lisa",
        ]
        last_names = [
            "Smith",
            "Johnson",
            "Williams",
            "Brown",
            "Jones",
            "Garcia",
            "Miller",
            "Davis",
        ]

        first_name = secrets.choice(first_names)
        last_name = secrets.choice(last_names)

        return f"{first_name} {last_name}"

    @property
    def generator_type(self) -> GeneratorType:

        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "type",
            "gender",
            "surname_file",
            "givenname_file",
            "include_pinyin",
            "compound_surname_ratio",
        ]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项 - Implemented generation logic"""
        return self._generate_raw(context)

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        return isinstance(data, str) and len(data) > 0


# 注册优化的生成器


@register_generator("name_optimized", ["姓名优化", "name_fast", "cached_name"])
class OptimizedNameGeneratorRegistered(OptimizedNameGenerator):

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""

        # 直接调用父类方法

        return self._generate_raw(context)

    def validate(self, data: str) -> bool:
        """验证生成的数据"""

        # 简单验证：检查是否为非空字符串
        return isinstance(data, str) and bool(data.strip())


@register_generator("optimized_name", ["optimized-name"])
class GenericOptimizedNameGenerator(OptimizedNameGenerator):
    """通用optimized_name生成器注册版本"""

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)
