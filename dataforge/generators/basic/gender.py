"""
性别生成器
"""

import secrets
from typing import Any

from ...core.context import ExtendedGenerationContext
from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
)
from ...core.types import GeneratorType


class GenderGenerator(DataGenerator[str]):
    """性别生成器"""

    # 性别选项定义
    GENDER_OPTIONS = {
        "BINARY": ["MALE", "FEMALE"],
        "EXTENDED": ["MALE", "FEMALE", "OTHER", "NON_BINARY", "PREFER_NOT_TO_SAY"],
        "CHINESE": ["男", "女"],
        "CHINESE_EXTENDED": ["男", "女", "其他", "不便透露"],
        "ENGLISH": ["Male", "Female"],
        "ENGLISH_EXTENDED": [
            "Male",
            "Female",
            "Other",
            "Non-binary",
            "Prefer not to say",
        ],
        "SYMBOL": ["M", "F"],
        "SYMBOL_EXTENDED": ["M", "F", "O", "N", "X"],
        "NUMERIC": ["0", "1"],  # 0=女, 1=男
        "NUMERIC_EXTENDED": ["0", "1", "2"],  # 0=女, 1=男, 2=其他
    }

    # 性别权重映射（用于现实比例）
    DEFAULT_WEIGHTS = {
        "MALE": 0.51,  # 男性比例稍高
        "FEMALE": 0.49,  # 女性比例
        "OTHER": 0.005,  # 其他性别
        "NON_BINARY": 0.003,
        "PREFER_NOT_TO_SAY": 0.002,
    }

    def _setup(self) -> None:
        self.gender_type = self.parameters.get("type", "BINARY")  # 性别类型
        self.male_ratio = self.parameters.get("male_ratio", 0.51)  # 男性比例
        self.format_style = self.parameters.get("format", "ENGLISH")  # 输出格式
        self.custom_options = self.parameters.get("custom_options", None)  # 自定义选项
        self.use_realistic_weights = self.parameters.get("realistic_weights", True)
        self.allow_unknown = self.parameters.get("allow_unknown", False)

    def _generate_raw(self, context: GenerationContext | None = None) -> str:
        """生成原始性别数据"""
        # 获取性别选项
        options = self._get_gender_options()

        # 如果上下文中有相关数据，尝试保持一致性
        if context:
            # 检查是否已有性别相关数据
            existing_gender = self._extract_gender_from_context(context)
            if existing_gender and existing_gender in options:
                return existing_gender

        # 根据权重选择性别
        if self.use_realistic_weights and len(options) <= 3:
            return self._weighted_choice(options)
        else:
            return secrets.choice(options)

    def _get_gender_options(self) -> list[str]:
        """获取性别选项列表"""
        if self.custom_options:
            return self.custom_options

        # 根据格式样式选择选项
        if self.format_style.upper() == "CHINESE":
            base_key = (
                "CHINESE_EXTENDED" if self.gender_type == "EXTENDED" else "CHINESE"
            )
        elif self.format_style.upper() == "SYMBOL":
            base_key = "SYMBOL_EXTENDED" if self.gender_type == "EXTENDED" else "SYMBOL"
        elif self.format_style.upper() == "NUMERIC":
            base_key = (
                "NUMERIC_EXTENDED" if self.gender_type == "EXTENDED" else "NUMERIC"
            )
        elif self.format_style.upper() == "ENGLISH":
            base_key = (
                "ENGLISH_EXTENDED" if self.gender_type == "EXTENDED" else "ENGLISH"
            )
        else:  # 默认使用标准格式
            base_key = "EXTENDED" if self.gender_type == "EXTENDED" else "BINARY"

        options = self.GENDER_OPTIONS.get(
            base_key, self.GENDER_OPTIONS["BINARY"]
        ).copy()

        # 如果允许未知值，添加相应选项
        if self.allow_unknown:
            if self.format_style.upper() == "CHINESE":
                options.append("未知")
            elif self.format_style.upper() == "SYMBOL":
                options.append("U")
            elif self.format_style.upper() == "NUMERIC":
                options.append("9")
            else:
                options.append("UNKNOWN")

        return options

    def _weighted_choice(self, options: list[str]) -> str:
        """根据权重选择性别"""
        if len(options) == 2:  # 二元性别
            return (
                options[0]
                if (secrets.randbelow(1000000) / 1000000) < self.male_ratio
                else options[1]
            )

        # 多元性别，使用默认权重
        weights = []
        total_weight: float = 0.0

        for option in options:
            # 映射选项到标准权重
            standard_option = self._map_to_standard_gender(option)
            weight = self.DEFAULT_WEIGHTS.get(standard_option, 0.001)

            # 调整男女比例
            if standard_option == "MALE":
                weight = self.male_ratio
            elif standard_option == "FEMALE":
                weight = (
                    1
                    - self.male_ratio
                    - sum(
                        self.DEFAULT_WEIGHTS.get(k, 0)
                        for k in self.DEFAULT_WEIGHTS
                        if k not in ["MALE", "FEMALE"]
                    )
                )

            weights.append(weight)
            total_weight += weight

        # 标准化权重
        weights = [w / total_weight for w in weights]

        # 随机选择
        rand = secrets.randbelow(1000000) / 1000000
        cumulative: float = 0.0
        for i, weight in enumerate(weights):
            cumulative += weight
            if rand <= cumulative:
                return options[i]

        return options[-1]  # 兜底

    def _map_to_standard_gender(self, option: str) -> str:
        """将选项映射到标准性别"""
        option_upper = option.upper()

        # 男性映射
        if option_upper in ["MALE", "M", "男", "1"]:
            return "MALE"
        # 女性映射
        elif option_upper in ["FEMALE", "F", "女", "0"]:
            return "FEMALE"
        # 其他映射
        elif option_upper in ["OTHER", "O", "其他", "2"]:
            return "OTHER"
        # 非二元映射
        elif option_upper in ["NON_BINARY", "NON-BINARY", "N", "X"]:
            return "NON_BINARY"
        # 不透露映射
        elif option_upper in ["PREFER_NOT_TO_SAY", "PREFER NOT TO SAY", "不便透露"]:
            return "PREFER_NOT_TO_SAY"
        else:
            return "OTHER"

    def _extract_gender_from_context(self, context: GenerationContext) -> str | None:
        """从上下文中提取性别信息（兼容扩展上下文与related_data）"""
        idcard: str | None = None
        name: str | None = None

        # 优先从扩展上下文取值
        if isinstance(context, ExtendedGenerationContext):
            idcard = context.get("idcard")
            name = context.get("name")
        else:
            # 回退到 related_data
            if context.related_data and isinstance(context.related_data, dict):
                idcard = context.related_data.get("idcard")  # type: ignore[assignment]
                name = context.related_data.get("name")  # type: ignore[assignment]

        # 检查身份证号中的性别信息
        if idcard and len(idcard) >= 17 and idcard[16].isdigit():
            gender_digit = int(idcard[16])
            if gender_digit % 2 == 1:
                return self._convert_to_format("MALE")
            else:
                return self._convert_to_format("FEMALE")

        # 检查姓名中的性别暗示（基于常见名字）
        if name:
            return self._infer_gender_from_name(name)

        return None

    def _convert_to_format(self, standard_gender: str) -> str:
        """将标准性别转换为指定格式"""
        options = self._get_gender_options()

        if standard_gender == "MALE":
            male_options = ["MALE", "Male", "M", "男", "1"]
        else:  # FEMALE
            male_options = ["FEMALE", "Female", "F", "女", "0"]

        for opt in options:
            if opt in male_options:
                return opt

        return options[0] if options else standard_gender

    def _infer_gender_from_name(self, name: str) -> str | None:
        """从姓名推断性别（简单实现）"""
        # 移除拼音部分
        if "(" in name:
            name = name.split("(")[0].strip()

        # 常见女性名字特征
        female_chars = [
            "娜",
            "丽",
            "美",
            "红",
            "燕",
            "芳",
            "敏",
            "静",
            "莉",
            "秀",
            "霞",
            "玲",
            "琳",
            "萍",
            "华",
            "慧",
            "月",
            "雪",
            "梅",
            "兰",
            "蕾",
            "薇",
            "婷",
            "颖",
            "洁",
            "雅",
            "琴",
            "欣",
            "馨",
            "怡",
        ]

        # 常见男性名字特征
        male_chars = [
            "伟",
            "强",
            "磊",
            "军",
            "洋",
            "勇",
            "刚",
            "峰",
            "超",
            "杰",
            "涛",
            "明",
            "辉",
            "鹏",
            "华",
            "斌",
            "宇",
            "浩",
            "凯",
            "健",
        ]

        female_score = sum(1 for char in name if char in female_chars)
        male_score = sum(1 for char in name if char in male_chars)

        if female_score > male_score:
            return self._convert_to_format("FEMALE")
        elif male_score > female_score:
            return self._convert_to_format("MALE")

        return None

    def validate(self, data: str) -> bool:
        """校验性别数据

        验证是否为有效的性别值（支持常用格式，但不包括单字母缩写）
        """
        if not isinstance(data, str):
            return False

        # 定义有效的性别值（排除单字母缩写如M/F）
        valid_genders = {
            # 英文
            "Male",
            "Female",
            "MALE",
            "FEMALE",
            # 中文
            "男",
            "女",
            # 扩展选项
            "Other",
            "OTHER",
            "其他",
            "Non-binary",
            "NON_BINARY",
            "Prefer not to say",
            "PREFER_NOT_TO_SAY",
            "不便透露",
        }

        # 添加未知选项（如果允许）
        if self.allow_unknown:
            valid_genders.update(["未知", "UNKNOWN", "U", "9"])

        return data in valid_genders

    def convert_format(self, gender: str, target_format: str) -> str:
        """转换性别格式"""
        # 先映射到标准格式
        standard = self._map_to_standard_gender(gender)

        # 根据目标格式选择输出
        format_map = {
            "CHINESE": {"MALE": "男", "FEMALE": "女", "OTHER": "其他"},
            "ENGLISH": {"MALE": "Male", "FEMALE": "Female", "OTHER": "Other"},
            "SYMBOL": {"MALE": "M", "FEMALE": "F", "OTHER": "O"},
            "NUMERIC": {"MALE": "1", "FEMALE": "0", "OTHER": "2"},
            "STANDARD": {"MALE": "MALE", "FEMALE": "FEMALE", "OTHER": "OTHER"},
        }

        mapping = format_map.get(target_format.upper(), format_map["STANDARD"])
        return mapping.get(standard, gender)

    def get_statistics(self, data_list: list[str]) -> dict[str, Any]:
        """获取性别数据统计"""
        if not data_list:
            return {}

        stats = {}
        total = len(data_list)

        # 统计各性别数量
        gender_counts: dict[str, int] = {}
        for gender in data_list:
            standard = self._map_to_standard_gender(gender)
            gender_counts[standard] = gender_counts.get(standard, 0) + 1

        # 计算比例
        for gender, count in gender_counts.items():
            stats[gender] = {
                "count": count,
                "percentage": round(count / total * 100, 2),
            }

        # 计算男女比例
        male_count = gender_counts.get("MALE", 0)
        female_count = gender_counts.get("FEMALE", 0)

        if male_count + female_count > 0:
            stats["gender_ratio"] = {
                "male_female_ratio": round(male_count / (male_count + female_count), 3)
            }

        return stats

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "type",
            "male_ratio",
            "format",
            "custom_options",
            "realistic_weights",
            "allow_unknown",
        ]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项 - Implemented generation logic"""
        return self._generate_raw(context)


@register_generator("gender", ["性别", "sex"])
class ChineseGenderGenerator(GenderGenerator):
    """中国性别生成器注册版本"""

    pass


@register_generator("gender", ["性别"])
class GenericGenderGenerator(GenderGenerator):
    """通用gender生成器注册版本"""

    pass
