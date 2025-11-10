import secrets
import re
from typing import Optional

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorType,
)
from ...data.loader import load_json


class PhoneNumberGenerator(DataGenerator[str]):
    """中国电话号码生成器，支持手机、固话、400热线"""

    def _setup(self) -> None:
        """初始化生成器参数"""
        self.number_type = self.parameters.get(
            "type", "MOBILE"
        )  # MOBILE, LANDLINE, TOLL_FREE, MIXED
        self.format_style = self.parameters.get(
            "format", "COMPACT"
        )  # STANDARD, COMPACT, INTERNATIONAL
        self.include_extension = self.parameters.get("include_extension", False)
        self.region = self.parameters.get("region", None)  # 区号或省份
        self.operator = self.parameters.get("operator", None)  # 运营商代码 (CMCC, CUCC, CTCC)
        self.valid = self.parameters.get("valid", True)  # 是否生成有效号码

        # 加载手机号段数据from配置文件
        try:
            phone_data = load_json("phone_prefixes.json")
            self._load_mobile_prefixes_from_config(phone_data)
        except:
            # 如果配置文件不存在，使用硬编码的前缀
            self._use_hardcoded_mobile_prefixes()

        # 固定电话区号
        self.area_codes = {
            "北京": "010",
            "上海": "021",
            "广州": "020",
            "深圳": "0755",
            "南京": "025",
            "杭州": "0571",
            "武汉": "027",
            "成都": "028",
            "重庆": "023",
            "沈阳": "024",
            "济南": "0531",
            "西安": "029",
            "长沙": "0731",
            "福州": "0591",
            "厦门": "0592",
            "合肥": "0551",
            "郑州": "0371",
            "石家庄": "0311",
            "哈尔滨": "0451",
            "长春": "0431",
            "南昌": "0791",
            "贵阳": "0851",
            "昆明": "0871",
            "南宁": "0771",
            "海口": "0898",
            "乌鲁木齐": "0991",
            "兰州": "0931",
            "西宁": "0971",
            "银川": "0951",
            "拉萨": "0891",
            "呼和浩特": "0471",
            "大连": "0411",
            "青岛": "0532",
            "宁波": "0574",
        }

        # 400服务热线前缀
        self.toll_free_prefixes = ["4006", "4007", "4008", "4009"]

        # 无效前缀 (用于生成无效号码)
        self.invalid_prefixes = ["120", "121", "122", "100", "101", "102"]

    def _load_mobile_prefixes_from_config(self, phone_data: dict) -> None:
        """从配置文件加载手机号段"""
        self.mobile_operator_prefixes = {}
        self.operator_info = {}

        # 加载三大运营商号段
        for operator in phone_data.get("mobile_operators", []):
            self.mobile_operator_prefixes[operator["code"]] = operator["prefixes"]
            self.operator_info[operator["code"]] = {
                "name": operator["name"],
                "generations": operator.get("generations", {}),
            }

        # 加载虚拟运营商号段
        virtual_prefixes = []
        for operator in phone_data.get("virtual_operators", []):
            virtual_prefixes.extend(operator["prefixes"])
            self.operator_info[operator["code"]] = {
                "name": operator["name"],
                "generations": {},
            }

        if virtual_prefixes:
            self.mobile_operator_prefixes["VIRTUAL"] = virtual_prefixes

        # 保存无效前缀
        self.invalid_prefixes = phone_data.get("invalid_prefixes", self.invalid_prefixes)

    def _use_hardcoded_mobile_prefixes(self) -> None:
        """使用硬编码的手机号前缀 (配置文件不可用时的fallback)"""
        self.mobile_operator_prefixes = {
            "CMCC": ["134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "157", "158", "159", "182", "183", "184", "187", "188", "178", "198"],
            "CUCC": ["130", "131", "132", "145", "155", "156", "166", "171", "175", "176", "185", "186"],
            "CTCC": ["133", "149", "153", "173", "177", "180", "181", "189", "191", "199"],
            "VIRTUAL": ["170", "171"],
        }
        self.operator_info = {
            "CMCC": {"name": "中国移动", "generations": {}},
            "CUCC": {"name": "中国联通", "generations": {}},
            "CTCC": {"name": "中国电信", "generations": {}},
            "VIRTUAL": {"name": "虚拟运营商", "generations": {}},
        }

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个电话号码"""
        # 如果要生成无效号码
        if not self.valid:
            return self._generate_invalid_phone()

        # 选择号码类型
        if self.number_type == "MIXED":
            number_types = ["MOBILE", "LANDLINE", "TOLL_FREE"]
            actual_type = secrets.choice(number_types)
        else:
            actual_type = self.number_type

        # 生成号码
        if actual_type == "MOBILE":
            number = self._generate_mobile_number()
        elif actual_type == "LANDLINE":
            number = self._generate_landline_number()
        elif actual_type == "TOLL_FREE":
            number = self._generate_toll_free_number()
        else:
            number = self._generate_mobile_number()  # 默认生成手机号

        # 添加分机号
        if self.include_extension and actual_type in ["LANDLINE", "TOLL_FREE"]:
            extension = secrets.randbelow(9900) + 100  # 100-9999
            number += f" ext.{extension}"

        return number

    def _generate_mobile_number(self) -> str:
        """生成手机号码"""
        # 选择运营商前缀
        if self.operator and self.operator in self.mobile_operator_prefixes:
            prefix = secrets.choice(self.mobile_operator_prefixes[self.operator])
        else:
            # 随机选择所有前缀
            all_prefixes = [p for prefixes in self.mobile_operator_prefixes.values() for p in prefixes]
            prefix = secrets.choice(all_prefixes)

        # 生成后8位
        suffix = "".join(secrets.choice("0123456789") for _ in range(8))

        # 格式化输出
        if self.format_style == "STANDARD":
            return f"{prefix} {suffix[:4]} {suffix[4:]}"
        elif self.format_style == "INTERNATIONAL":
            return f"+86 {prefix} {suffix[:4]} {suffix[4:]}"
        else:  # COMPACT
            return f"{prefix}{suffix}"

    def _generate_landline_number(self) -> str:
        """生成固定电话号码"""
        # 选择区号
        if self.region and self.region in self.area_codes:
            area_code = self.area_codes[self.region]
        else:
            area_code = secrets.choice(list(self.area_codes.values()))

        # 生成本地号码
        if area_code.startswith("0"):
            area_digits = area_code[1:]  # 去掉前导0
            if len(area_digits) == 2:  # 如010 -> 10
                local_number = f"{secrets.randbelow(8) + 2}{secrets.randbelow(9000) + 1000}{secrets.randbelow(900) + 100}"
            else:  # 如0755 -> 755
                local_number = f"{secrets.randbelow(8) + 2}{secrets.randbelow(90000) + 10000}"
        else:
            area_digits = area_code
            local_number = f"{secrets.randbelow(8) + 2}{secrets.randbelow(90000) + 10000}"

        # 组装号码
        if self.format_style == "INTERNATIONAL":
            return f"+86 {area_digits} {local_number}"
        elif self.format_style == "COMPACT":
            return f"{area_digits}{local_number}"
        else:  # STANDARD
            return f"{area_code}-{local_number}"

    def _generate_toll_free_number(self) -> str:
        """生成400服务热线号码"""
        prefix = secrets.choice(self.toll_free_prefixes)
        # 生成7位数字
        number = "".join(secrets.choice("0123456789") for _ in range(7))

        # 组装号码
        if self.format_style == "STANDARD":
            return f"{prefix} {number[:3]} {number[3:]}"
        elif self.format_style == "INTERNATIONAL":
            return f"+86 {prefix} {number[:3]} {number[3:]}"
        else:  # COMPACT
            return f"{prefix}{number}"

    def _generate_invalid_phone(self) -> str:
        """生成无效电话号码"""
        invalid_type = secrets.choice(["wrong_length", "wrong_prefix", "wrong_format"])

        if invalid_type == "wrong_length":
            # 错误长度
            wrong_length = secrets.choice([9, 10, 12, 13])
            return "".join(secrets.choice("0123456789") for _ in range(wrong_length))
        elif invalid_type == "wrong_prefix":
            # 错误前缀（不是有效的手机号段）
            prefix = secrets.choice(self.invalid_prefixes)
            suffix = "".join(secrets.choice("0123456789") for _ in range(8))
            return prefix + suffix
        else:  # wrong_format
            # 包含字母或特殊字符
            invalid_phone = "".join(
                secrets.choice("0123456789ABCDEF-() ") for _ in range(11)
            )
            return invalid_phone

    def validate(self, data: str) -> bool:
        """校验电话号码"""
        if not isinstance(data, str):
            return False

        # 移除分机号部分
        main_number = data.split(" ext.")[0]
        # 移除所有非数字字符
        main_number = re.sub(r"[^\d]", "", main_number)

        # 检查是否为空
        if not main_number:
            return False

        # 处理国际格式的号码（以86开头但没有+）
        if main_number.startswith("86") and len(main_number) > 2:
            main_number = main_number[2:]

        # 根据号码类型进行校验
        if self.number_type == "MOBILE":
            return self._validate_mobile(main_number)
        elif self.number_type == "LANDLINE":
            return self._validate_landline(main_number)
        elif self.number_type == "TOLL_FREE":
            return self._validate_toll_free(main_number)
        else:
            # 综合校验
            return (
                self._validate_mobile(main_number)
                or self._validate_landline(main_number)
                or self._validate_toll_free(main_number)
            )

    def _validate_mobile(self, number: str) -> bool:
        """校验手机号码"""
        if len(number) != 11:
            return False

        prefix = number[:3]
        all_prefixes = [p for prefixes in self.mobile_operator_prefixes.values() for p in prefixes]
        return prefix in all_prefixes

    def _validate_landline(self, number: str) -> bool:
        """校验固定电话号码"""
        # 固定电话：以0开头，长度为9-11位
        return (
            re.match(r"^0\d{2,3}\d{6,8}$", number) is not None
            and len(number) <= 11
        )

    def _validate_toll_free(self, number: str) -> bool:
        """校验400号码"""
        # 400号码：4006-4009开头，后面跟7位数字
        return re.match(r"^(4006|4007|4008|4009)\d{7}$", number) is not None

    def get_number_type(self, number: str) -> str:
        """获取号码类型"""
        # 移除分机号部分并提取纯数字
        number = re.sub(r"[^\d]", "", number.split(" ext.")[0])

        # 处理国际格式的号码（以86开头但没有+）
        if number.startswith("86") and len(number) > 2:
            number = number[2:]

        if not number:
            return "UNKNOWN"

        if self._validate_mobile(number):
            return "MOBILE"
        elif self._validate_landline(number):
            return "LANDLINE"
        elif self._validate_toll_free(number):
            return "TOLL_FREE"
        else:
            return "UNKNOWN"

    def get_operator_info(self, phone: str) -> dict[str, str]:
        """获取手机号运营商信息"""
        # 提取纯数字
        number = re.sub(r"[^\d]", "", phone.split(" ext.")[0])

        # 处理国际格式
        if number.startswith("86") and len(number) > 2:
            number = number[2:]

        if not self._validate_mobile(number):
            return {"operator": "UNKNOWN", "type": "INVALID"}

        prefix = number[:3]

        # 查找运营商
        for op_code, prefixes in self.mobile_operator_prefixes.items():
            if prefix in prefixes:
                op_info = self.operator_info.get(op_code, {})
                return {
                    "operator": op_code,
                    "name": op_info.get("name", "未知"),
                    "generations": op_info.get("generations", {}),
                }

        return {"operator": "UNKNOWN", "name": "未知"}

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.CONTACT

    @property
    def supported_parameters(self) -> list[str]:
        return ["type", "format", "include_extension", "region", "operator", "valid"]


@register_generator("phone", ["telephone", "mobile", "手机号", "电话", "手机号码"])
class GenericPhoneNumberGenerator(PhoneNumberGenerator):
    """通用电话号码生成器注册版本"""

    pass


# 别名，用于向后兼容
PhoneGenerator = PhoneNumberGenerator
