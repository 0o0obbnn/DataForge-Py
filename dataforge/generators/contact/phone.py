"""
中国手机号码生成器
支持生成符合中国三大运营商号段规则的手机号码
"""

import random
from typing import Optional

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    GenerationContext,
    GeneratorType,
    ValidatedDataGenerator,
)


@register_generator("phone", ["手机", "手机号码", "移动电话"])
class ChinesePhoneGenerator(ValidatedDataGenerator):
    """中国手机号码生成器"""

    # 中国移动号段
    CHINA_MOBILE_PREFIXES = [
        "134", "135", "136", "137", "138", "139",  # 2G/3G
        "147", "150", "151", "152", "157", "158", "159",  # 3G/4G
        "172", "178", "182", "183", "184", "187", "188",  # 4G
        "195", "197", "198"  # 5G
    ]

    # 中国联通号段
    CHINA_UNICOM_PREFIXES = [
        "130", "131", "132", "155", "156",  # 2G/3G
        "145", "166", "167", "171", "175", "176", "185", "186",  # 4G
        "196"  # 5G
    ]

    # 中国电信号段
    CHINA_TELECOM_PREFIXES = [
        "133", "149", "153", "173", "174", "177", "180", "181", "189",  # 3G/4G
        "190", "191", "193", "199"  # 5G
    ]

    # 虚拟运营商号段
    MVNO_PREFIXES = [
        "162", "165", "167", "170", "171", "192"
    ]

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.CONTACT

    @property
    def supported_parameters(self) -> list[str]:
        return ["carrier", "area_code", "generation", "format_type", "include_country_code"]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.carrier = self.parameters.get("carrier", None)  # mobile, unicom, telecom, mvno, random
        self.area_code = self.parameters.get("area_code", None)  # 区号（用于特定地区号段）
        self.generation = self.parameters.get("generation", "any")  # 2g, 3g, 4g, 5g, any
        self.format_type = self.parameters.get("format_type", "plain")  # plain, dash, space, international
        self.include_country_code = self.parameters.get("include_country_code", False)

    def _get_carrier_prefixes(self) -> list[str]:
        """根据运营商获取号段"""
        if self.carrier == "mobile":
            return self.CHINA_MOBILE_PREFIXES
        elif self.carrier == "unicom":
            return self.CHINA_UNICOM_PREFIXES
        elif self.carrier == "telecom":
            return self.CHINA_TELECOM_PREFIXES
        elif self.carrier == "mvno":
            return self.MVNO_PREFIXES
        else:
            # 随机选择运营商
            all_prefixes = (
                self.CHINA_MOBILE_PREFIXES +
                self.CHINA_UNICOM_PREFIXES +
                self.CHINA_TELECOM_PREFIXES
            )
            return all_prefixes

    def _filter_by_generation(self, prefixes: list[str]) -> list[str]:
        """根据网络制式过滤号段"""
        if self.generation == "any":
            return prefixes
        
        # 简化的制式分类（实际情况更复杂）
        generation_mapping = {
            "2g": ["134", "135", "136", "137", "138", "139", "130", "131", "132"],
            "3g": ["150", "151", "152", "157", "158", "159", "155", "156", "133", "153", "189"],
            "4g": ["172", "178", "182", "183", "184", "187", "188", "145", "166", "171", "175", "176", "185", "186", "173", "174", "177", "180", "181"],
            "5g": ["195", "197", "198", "196", "190", "191", "193", "199"]
        }
        
        target_prefixes = generation_mapping.get(self.generation, prefixes)
        return [p for p in prefixes if p in target_prefixes]

    def _generate_suffix(self) -> str:
        """生成8位后缀"""
        # 避免生成全相同数字
        while True:
            suffix = f"{random.randint(10000000, 99999999)}"
            # 检查是否为连续数字或全相同数字
            if not (len(set(suffix)) == 1 or self._is_sequential(suffix)):
                return suffix
            # 如果生成了不合适的号码，重新生成（但避免无限循环）
            if random.random() < 0.9:  # 90%的概率接受，避免完全循环
                return suffix

    def _is_sequential(self, number: str) -> bool:
        """检查是否为连续数字"""
        for i in range(len(number) - 1):
            if int(number[i+1]) != int(number[i]) + 1:
                return False
        return True

    def _format_number(self, number: str) -> str:
        """格式化手机号码"""
        if self.include_country_code:
            number = "+86" + number
        
        if self.format_type == "dash":
            # 例：138-1234-5678 或 +86-138-1234-5678
            if number.startswith("+86"):
                return f"{number[:3]}-{number[3:6]}-{number[6:10]}-{number[10:]}"
            else:
                return f"{number[:3]}-{number[3:7]}-{number[7:]}"
        elif self.format_type == "space":
            # 例：138 1234 5678 或 +86 138 1234 5678
            if number.startswith("+86"):
                return f"{number[:3]} {number[3:6]} {number[6:10]} {number[10:]}"
            else:
                return f"{number[:3]} {number[3:7]} {number[7:]}"
        elif self.format_type == "international":
            # 例：+86 138 1234 5678
            if not number.startswith("+86"):
                number = "+86" + number
            return f"{number[:3]} {number[3:6]} {number[6:10]} {number[10:]}"
        else:
            # 默认无格式：13812345678
            return number

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成手机号码"""
        # 获取可用号段
        prefixes = self._get_carrier_prefixes()
        
        # 根据制式过滤
        prefixes = self._filter_by_generation(prefixes)
        
        if not prefixes:
            # 如果过滤后没有可用号段，使用默认号段
            prefixes = ["138", "139", "186", "188"]
        
        # 选择前缀
        prefix = random.choice(prefixes)
        
        # 生成后缀
        suffix = self._generate_suffix()
        
        # 组合完整号码
        full_number = prefix + suffix
        
        # 格式化
        return self._format_number(full_number)

    def validate(self, data: str) -> bool:
        """验证手机号码格式"""
        import re
        
        # 移除格式化字符
        clean_number = re.sub(r'[\s\-\+]', '', data)
        
        # 移除国家代码
        if clean_number.startswith('86'):
            clean_number = clean_number[2:]
        
        # 检查长度
        if len(clean_number) != 11:
            return False
        
        # 检查是否全为数字
        if not clean_number.isdigit():
            return False
        
        # 检查前缀是否有效
        prefix = clean_number[:3]
        all_prefixes = (
            self.CHINA_MOBILE_PREFIXES +
            self.CHINA_UNICOM_PREFIXES +
            self.CHINA_TELECOM_PREFIXES +
            self.MVNO_PREFIXES
        )
        
        return prefix in all_prefixes

    def get_carrier_info(self, phone: str) -> dict:
        """获取手机号码的运营商信息"""
        import re
        
        # 清理号码
        clean_number = re.sub(r'[\s\-\+]', '', phone)
        if clean_number.startswith('86'):
            clean_number = clean_number[2:]
        
        if not self.validate(phone):
            return {"valid": False}
        
        prefix = clean_number[:3]
        
        # 判断运营商
        if prefix in self.CHINA_MOBILE_PREFIXES:
            carrier = "中国移动"
            carrier_en = "China Mobile"
        elif prefix in self.CHINA_UNICOM_PREFIXES:
            carrier = "中国联通"
            carrier_en = "China Unicom"
        elif prefix in self.CHINA_TELECOM_PREFIXES:
            carrier = "中国电信"
            carrier_en = "China Telecom"
        elif prefix in self.MVNO_PREFIXES:
            carrier = "虚拟运营商"
            carrier_en = "MVNO"
        else:
            carrier = "未知"
            carrier_en = "Unknown"
        
        return {
            "valid": True,
            "prefix": prefix,
            "carrier": carrier,
            "carrier_en": carrier_en,
            "full_number": clean_number
        }
