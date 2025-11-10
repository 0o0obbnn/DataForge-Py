from ...core.types import GeneratorType

"""
驾驶证号生成器

生成符合中国公安部标准的驾驶证号码
支持不同省份的驾驶证号生成规则
"""

import random  # TODO: Convert to secrets
import secrets
import re
from dataclasses import dataclass
from typing import Optional, Union

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
)
from ...core.protocols import Validator

# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary



@dataclass
class DriverLicenseInfo:
    """驾驶证信息数据模型"""
    license_number: str
    province_code: str
    issue_date: str
    expiry_date: str
    license_class: str
    holder_name: str


class DriverLicenseValidator(Validator):
    """Validator for driver's licenses."""

    def __init__(self, province_codes: dict):
        self.province_codes = province_codes

    def validate(self, data: dict[str, Union[str, int]]) -> bool:
        """验证生成的驾驶证数据"""
        if "license_number" not in data:
            return False

        license_number = data["license_number"]

        # 确保license_number是字符串类型
        if not isinstance(license_number, str):
            return False

        # 验证驾驶证号码格式：18位数字
        if not re.match(r'^\d{18}$', license_number):
            return False

        # 验证省份代码
        province_code = license_number[:2]
        valid_province_codes = {code[:2] for code in self.province_codes.values()}
        if province_code not in valid_province_codes:
            return False

        return True

    @property
    def error_message(self) -> str:
        return "Invalid driver's license format"


class DriverLicenseGenerator(DataGenerator[dict[str, Union[str, int]]]):
    """中国驾驶证号码生成器

    功能特性：
    - 生成符合公安部标准的18位驾驶证号码
    - 支持全国各省份驾驶证号规则
    - 包含驾驶证类型、有效期等信息
    """

    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.province = self.parameters.get("province", "北京")
        self.license_class = self.parameters.get("license_class", "C1").upper()
        self.include_dates = self.parameters.get("include_dates", True)
        self.include_name = self.parameters.get("include_name", False)

        # 省份代码映射
        self.province_codes = {
            "北京": "110000", "天津": "120000", "河北": "130000", "山西": "140000", "内蒙古": "150000",
            "辽宁": "210000", "吉林": "220000", "黑龙江": "230000", "上海": "310000", "江苏": "320000",
            "浙江": "330000", "安徽": "340000", "福建": "350000", "江西": "360000", "山东": "370000",
            "河南": "410000", "湖北": "420000", "湖南": "430000", "广东": "440000", "广西": "450000",
            "海南": "460000", "重庆": "500000", "四川": "510000", "贵州": "520000", "云南": "530000",
            "西藏": "540000", "陕西": "610000", "甘肃": "620000", "青海": "630000", "宁夏": "640000",
            "新疆": "650000",
        }
        self.validator = DriverLicenseValidator(self.province_codes)

        # 驾驶证类型
        self.license_classes = {
            "A1": "大型客车", "A2": "牵引车", "A3": "城市公交车",
            "B1": "中型客车", "B2": "大型货车",
            "C1": "小型汽车", "C2": "小型自动挡汽车", "C3": "低速载货汽车",
            "C4": "三轮汽车", "C5": "残疾人专用小型自动挡载客汽车",
            "D": "普通三轮摩托车", "E": "普通二轮摩托车", "F": "轻便摩托车",
        }

        # 中国常见姓氏
        self.chinese_surnames = [
            "张", "王", "李", "赵", "刘", "陈", "杨", "黄", "周", "吴",
            "徐", "孙", "胡", "朱", "高", "林", "何", "郭", "马", "罗",
        ]

        # 常见名字
        self.chinese_names = [
            "伟", "芳", "娜", "秀英", "敏", "静", "丽", "强", "磊", "军",
            "洋", "勇", "艳", "杰", "娟", "涛", "明", "超", "秀兰", "霞",
        ]

    def _setup(self) -> None:
        """初始化驾驶证生成器参数"""
        self.province = self.parameters.get("province", "北京")
        self.license_class = self.parameters.get("license_class", "C1").upper()
        self.include_dates = self.parameters.get("include_dates", True)
        self.include_name = self.parameters.get("include_name", False)

    def _get_province_code(self, province: str) -> str:
        """获取省份代码"""
        # 如果输入的是省份名称，返回对应代码
        if province in self.province_codes:
            return self.province_codes[province][:2]  # 取前两位

        # 如果输入的是代码，直接使用
        if province.isdigit() and len(province) >= 2:
            return province[:2]

        # 默认返回北京
        return "11"

    def _generate_license_number(self, province_code: str) -> str:
        """生成18位驾驶证号码"""
        # 驾驶证号码格式：省份代码(2位) + 8位数字 + 8位顺序码
        province_prefix = self._get_province_code(province_code)

        # 8位数字（可以包含年份信息）
        year_digits = str(secrets.randbelow(15) + 2010)
        random_digits = ''.join(str(secrets.randbelow(10)) for _ in range(4))
        middle_part = year_digits + random_digits

        # 8位顺序码
        sequence = ''.join(str(secrets.randbelow(10)) for _ in range(8))

        license_number = f"{province_prefix}{middle_part}{sequence}"

        # 确保18位
        if len(license_number) > 18:
            license_number = license_number[:18]
        elif len(license_number) < 18:
            license_number = license_number.ljust(18, '0')

        return license_number

    def _generate_dates(self) -> tuple[str, str]:
        """生成驾驶证签发和有效期"""
        import datetime

        # 随机生成签发日期（过去5年内）
        today = datetime.date.today()
        max_days = 365 * 5
        random_days = secrets.randbelow(max_days + 1)
        issue_date = today - datetime.timedelta(days=random_days)

        # 驾驶证有效期：C类6年，A/B类10年
        if self.license_class.startswith("C"):
            validity_years = 6
        elif self.license_class.startswith(("A", "B")):
            validity_years = 10
        else:
            validity_years = 6

        expiry_date = issue_date + datetime.timedelta(days=365 * validity_years)

        return (
            issue_date.strftime("%Y-%m-%d"),
            expiry_date.strftime("%Y-%m-%d")
        )

    def _generate_chinese_name(self) -> str:
        """生成中文姓名"""
        surname = secrets.choice(self.chinese_surnames)

        # 50%概率生成单名，50%概率生成双名
        if (secrets.randbelow(1000000) / 1000000) < 0.5:
            given_name = secrets.choice(self.chinese_names)
        else:
            given_name = ''.join(secrets.choice(self.chinese_names) for _ in range(2))

        return f"{surname}{given_name}"

    def generate(self, context: Optional[GenerationContext] = None) -> Union[str, dict[str, Union[str, int]]]:
        """生成驾驶证数据
        
        Returns:
            如果string_only=True，返回驾驶证号码字符串
            否则返回包含完整信息的字典
        """
        # 获取省份代码
        province_code = self._get_province_code(self.province)

        # 生成驾驶证号码
        license_number = self._generate_license_number(province_code)

        # 如果只需要字符串，直接返回
        if self.parameters.get('string_only', False):
            return license_number

        # 生成签发和有效期
        issue_date, expiry_date = self._generate_dates()

        # 生成持有人姓名
        holder_name = self._generate_chinese_name()

        result = {
            "license_number": license_number,
            "province": self.province,
            "province_code": province_code,
            "license_class": self.license_class,
            "license_class_name": self.license_classes.get(self.license_class, "未知类型"),
        }

        if self.include_dates:
            validity_years = 6 if self.license_class.startswith("C") else 10
            result.update({
                "issue_date": issue_date,
                "expiry_date": expiry_date,
                "validity_years": validity_years,
            })

        if self.include_name:
            result["holder_name"] = holder_name

        return result

    def generate_single(self, context: Optional[GenerationContext] = None) -> Union[str, dict[str, Union[str, int]]]:
        """生成单个数据项
        
        默认返回驾驶证号码字符串，除非明确设置string_only=False
        """
        # 如果没有明确设置string_only，默认为True（返回字符串）
        if 'string_only' not in self.parameters:
            self.parameters['string_only'] = True
        
        return self.generate(context)

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.IDENTIFIER

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return ["include_dates", "include_name", "license_class", "province"]

    def validate(self, data: Union[str, dict[str, Union[str, int]]]) -> bool:
        """验证生成的数据
        
        Args:
            data: 驾驶证号码字符串或包含完整信息的字典
        """
        # 类型检查
        if not isinstance(data, (str, dict)):
            return False
            
        # 如果是字符串，转换为dict格式进行验证
        if isinstance(data, str):
            data = {"license_number": data}
        
        if hasattr(self, 'validator') and hasattr(self.validator, 'validate'):
            return self.validator.validate(data)
        return True



@register_generator("generic_driver_license", aliases=["驾驶证", "driver_license"])
class GenericDriverLicenseGenerator(DriverLicenseGenerator):
    """通用驾驶证生成器注册版本"""

    def generate_single(self, context: Optional[GenerationContext] = None) -> dict[str, Union[str, int]]:
        """生成单个数据项"""
        return self.generate(context)


# 添加别名以支持测试导入
DriversLicenseGenerator = DriverLicenseGenerator
