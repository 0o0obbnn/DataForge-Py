"""
身份证号码生成器
"""

import secrets
from datetime import date, datetime, timedelta
from typing import Optional, cast

import pandas as pd

from ...core.factory import register_generator
from ...core.generator import DataGenerator, GenerationContext, GeneratorConfig
from ...core.protocols import Validator
from ...core.types import GeneratorType
from ...data.loader import load_regions_df


class IDCardValidator(Validator):
    """Validator for Chinese ID cards."""

    ID_WEIGHTS: list[int] = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    ID_CHECK_CODES: list[str] = ["1", "0", "X", "9", "8", "7", "6", "5", "4", "3", "2"]

    def __init__(self) -> None:
        self.regions_df: pd.DataFrame = load_regions_df()
        self.all_district_codes: list[str] = self.regions_df["district_code"].tolist()

    def validate(self, data: str) -> bool:
        """
        校验一个身份证号码是否有效。

        :param data: 待校验的身份证号码。
        :return: 如果有效则为True，否则为False。
        """
        if not isinstance(data, str) or not data.isalnum() or len(data) != 18:
            return False

        if not data[:17].isdigit():
            return False

        if data[17].upper() not in self.ID_CHECK_CODES:
            return False

        # 校验地区代码（基本格式检查）
        region_code = data[:6]
        # 只检查地区代码是否为6位数字，不强制要求在数据库中
        # 因为数据库可能不包含所有历史或特殊地区代码
        if not region_code.isdigit():
            return False

        # 校验出生日期
        try:
            birth_date = datetime.strptime(data[6:14], "%Y%m%d").date()
            if not (date(1900, 1, 1) < birth_date < date.today()):
                return False
        except ValueError:
            return False

        # 校验校验位
        return self._calculate_check_digit(data[:17]) == data[17].upper()

    def _calculate_check_digit(self, id_17: str) -> str:
        """
        根据前17位计算校验位。

        :param id_17: 身份证号的前17位。
        :return: 1位校验码字符串。
        """
        total = sum(int(id_17[i]) * self.ID_WEIGHTS[i] for i in range(17))
        return self.ID_CHECK_CODES[total % 11]

    @property
    def error_message(self) -> str:
        return "Invalid ID card number"


@register_generator("idcard", aliases=["身份证", "id_card"])
class IDCardGenerator(DataGenerator[str]):
    """
    中国大陆居民身份证号码生成器。
    """

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.regions_df: pd.DataFrame = load_regions_df()
        self.all_district_codes: list[str] = self.regions_df["district_code"].tolist()
        self.validator = IDCardValidator()

    def _setup(self) -> None:
        """
        初始化配置参数。
        """
        self.region: Optional[str] = self.parameters.get("region")
        self.birth_date_range: tuple[str, str] = self.parameters.get(
            "birth_date_range", ("1980-01-01", "2000-12-31")
        )
        self.gender: str = self.parameters.get(
            "gender", "ANY"
        ).upper()  # MALE, FEMALE, ANY
        self.valid: bool = self.parameters.get("valid", True)

        try:
            start_str, end_str = self.birth_date_range
            self.start_date: date = datetime.strptime(start_str, "%Y-%m-%d").date()
            self.end_date: date = datetime.strptime(end_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            self.start_date = date(1980, 1, 1)
            self.end_date = date(2000, 12, 31)

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """
        生成一个有效的18位身份证号码。

        :param context: 生成上下文，用于处理数据关联。
        :return: 生成的身份证号码字符串。
        """
        if not self.valid:
            return self._generate_invalid_idcard()

        region_code = self._get_region_code()
        birth_date_obj = self._get_random_birth_date(context)
        birth_str = birth_date_obj.strftime("%Y%m%d")
        sequence_code = self._get_sequence_code()

        id_17 = f"{region_code}{birth_str}{sequence_code}"
        check_digit = self.validator._calculate_check_digit(id_17)

        return f"{id_17}{check_digit}"

    def validate(self, data: str) -> bool:
        """验证生成的身份证号码

        Args:
            data: 待验证的身份证号码

        Returns:
            bool: 身份证号码是否有效
        """
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型

        Returns:
            GeneratorType: 生成器类型为BASIC
        """
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表

        Returns:
            list[str]: 支持的参数名称列表
        """
        return ["region", "birth_date_range", "gender", "valid"]

    def _get_region_code(self) -> str:
        """
        根据配置获取一个有效的6位行政区划代码。

        :return: 6位地区代码字符串。
        """
        if self.region:
            # 如果是6位数字代码
            if len(self.region) == 6 and self.region.isdigit():
                if self.region in self.all_district_codes:
                    return self.region
            # 如果是省份或城市名称
            else:
                filtered_df = self.regions_df[
                    self.regions_df["province_name"].str.startswith(self.region)
                    | self.regions_df["city_name"].str.startswith(self.region)
                    | self.regions_df["district_name"].str.startswith(self.region)
                ]
                if not filtered_df.empty:
                    return cast(str, filtered_df["district_code"].sample(n=1).iloc[0])

        # 默认随机选择一个
        return secrets.choice(self.all_district_codes)

    def _get_random_birth_date(
        self, context: Optional[GenerationContext] = None
    ) -> date:
        """
        获取一个随机的出生日期。
        如果上下文中存在'age'，则根据年龄计算出生日期。

        :param context: 生成上下文。
        :return: date对象。
        """
        if context and context.related_data and "age" in context.related_data:
            try:
                age = int(context.related_data["age"])
                today = date.today()
                birth_year = today.year - age
                # 计算该年份的第一天和最后一天
                start_of_year = date(birth_year, 1, 1)
                end_of_year = date(birth_year, 12, 31)
                # 确保生成的日期能让年龄有效
                if today.month < end_of_year.month or (
                    today.month == end_of_year.month and today.day < end_of_year.day
                ):
                    start_of_year = date(birth_year - 1, today.month, today.day)
                else:
                    start_of_year = date(birth_year, today.month, today.day)

                total_days = (end_of_year - start_of_year).days
                random_days = secrets.randbelow(total_days + 1)
                return start_of_year + timedelta(days=random_days)
            except (ValueError, TypeError):
                pass  # Fallback to default range if age is invalid

        total_days = (self.end_date - self.start_date).days
        random_days = secrets.randbelow(total_days + 1)
        return self.start_date + timedelta(days=random_days)

    def _get_sequence_code(self) -> str:
        """
        获取3位顺序码，其中最后一位根据性别确定。

        :return: 3位顺序码字符串。
        """
        first_two = f"{secrets.randbelow(100):02d}"

        if self.gender == "MALE":
            third_digit = str(secrets.choice([1, 3, 5, 7, 9]))
        elif self.gender == "FEMALE":
            third_digit = str(secrets.choice([0, 2, 4, 6, 8]))
        else:
            third_digit = str(secrets.randbelow(10))

        return f"{first_two}{third_digit}"

    def _generate_invalid_idcard(self) -> str:
        """
        生成一个无效的身份证号码用于测试。
        """
        invalid_type = secrets.choice(
            ["wrong_length", "wrong_check", "invalid_date", "wrong_format"]
        )

        if invalid_type == "wrong_length":
            return "".join(
                [str(secrets.randbelow(10)) for _ in range(secrets.choice([15, 17, 19]))]
            )

        if invalid_type == "wrong_check":
            valid_id = self.generate_single(None)
            original_check = valid_id[-1]
            wrong_check = secrets.choice(
                [c for c in self.validator.ID_CHECK_CODES if c != original_check]
            )
            return f"{valid_id[:-1]}{wrong_check}"

        if invalid_type == "invalid_date":
            region_code = self._get_region_code()
            # 生成一个不存在的日期，如2月30日或13月
            invalid_date_str = f"{secrets.randbelow(21) + 1980}{secrets.choice(['13', '02'])}{secrets.choice(['32', '30'])}"
            sequence_code = self._get_sequence_code()
            id_17 = f"{region_code}{invalid_date_str}{sequence_code}"
            return f"{id_17}{self.validator._calculate_check_digit(id_17)}"

        # wrong_format (default)
        return "".join([secrets.choice("0123456789ABCXYZ") for _ in range(18)])
