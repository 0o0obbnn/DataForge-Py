"""
统一社会信用代码生成器
支持生成符合GB 32100-2015标准的18位统一社会信用代码
"""

import random
from typing import Optional

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    GenerationContext,
    GeneratorType,
    ValidatedDataGenerator,
)


@register_generator("uscc", ["统一社会信用代码", "信用代码"])
class USCCGenerator(ValidatedDataGenerator):
    """统一社会信用代码生成器"""

    # 登记管理部门代码
    DEPT_CODES = {
        "1": "机构编制",
        "5": "民政", 
        "9": "工商",
        "A": "全国组织机构",
        "Y": "其他"
    }

    # 机构类别代码
    ORG_TYPE_CODES = {
        "enterprise": {
            "1": "企业",
            "2": "个体工商户", 
            "3": "农民专业合作社"
        },
        "institution": {
            "4": "机关",
            "5": "事业单位",
            "6": "社会团体"
        },
        "other": {
            "9": "其他组织"
        }
    }

    # 省份代码（同身份证前两位）
    PROVINCE_CODES = {
        "北京": "11", "天津": "12", "河北": "13", "山西": "14", "内蒙古": "15",
        "辽宁": "21", "吉林": "22", "黑龙江": "23",
        "上海": "31", "江苏": "32", "浙江": "33", "安徽": "34", "福建": "35", "江西": "36", "山东": "37",
        "河南": "41", "湖北": "42", "湖南": "43", "广东": "44", "广西": "45", "海南": "46",
        "重庆": "50", "四川": "51", "贵州": "52", "云南": "53", "西藏": "54",
        "陕西": "61", "甘肃": "62", "青海": "63", "宁夏": "64", "新疆": "65"
    }

    # 校验码字符集
    CHECK_CHARS = "0123456789ABCDEFGHJKLMNPQRTUWXY"
    
    # 加权因子
    WEIGHTS = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BUSINESS

    @property
    def supported_parameters(self) -> list[str]:
        return ["org_type", "region", "dept_code", "valid", "province", "city"]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.org_type = self.parameters.get("org_type", "enterprise")
        self.region = self.parameters.get("region", None)
        self.dept_code = self.parameters.get("dept_code", None)
        self.valid = self.parameters.get("valid", True)
        self.province = self.parameters.get("province", None)
        self.city = self.parameters.get("city", None)

    def _get_dept_code(self) -> str:
        """获取登记管理部门代码（第1位）"""
        if self.dept_code and self.dept_code in self.DEPT_CODES:
            return self.dept_code
        
        # 根据机构类型选择合适的部门代码
        if self.org_type == "enterprise":
            return random.choice(["9", "1"])  # 工商或机构编制
        elif self.org_type == "institution":
            return random.choice(["1", "5"])  # 机构编制或民政
        else:
            return random.choice(list(self.DEPT_CODES.keys()))

    def _get_org_type_code(self) -> str:
        """获取机构类别代码（第2位）"""
        org_types = self.ORG_TYPE_CODES.get(self.org_type, self.ORG_TYPE_CODES["enterprise"])
        return random.choice(list(org_types.keys()))

    def _get_region_code(self) -> str:
        """获取登记管理机关行政区划码（第3-8位）"""
        # 选择省份代码
        if self.province and self.province in self.PROVINCE_CODES:
            province_code = self.PROVINCE_CODES[self.province]
        elif self.region and self.region in self.PROVINCE_CODES:
            province_code = self.PROVINCE_CODES[self.region]
        else:
            province_code = random.choice(list(self.PROVINCE_CODES.values()))
        
        # 生成市县代码（4位）
        city_code = f"{random.randint(1, 99):02d}{random.randint(1, 99):02d}"
        
        return province_code + city_code

    def _get_main_body_code(self) -> str:
        """获取主体标识码（第9-17位）"""
        # 生成9位组织机构代码
        code_chars = []
        for _ in range(9):
            code_chars.append(random.choice(self.CHECK_CHARS))
        return ''.join(code_chars)

    def _calculate_check_code(self, uscc_17: str) -> str:
        """计算校验码（第18位）"""
        if not self.valid:
            return random.choice(self.CHECK_CHARS)
        
        # 将字符转换为对应的数值
        char_values = {}
        for i, char in enumerate(self.CHECK_CHARS):
            char_values[char] = i
        
        # 计算加权和
        sum_val = 0
        for i in range(17):
            char = uscc_17[i]
            if char in char_values:
                sum_val += char_values[char] * self.WEIGHTS[i]
            else:
                # 如果字符不在字符集中，使用0
                sum_val += 0
        
        # 计算校验码
        check_code_index = 31 - (sum_val % 31)
        if check_code_index == 31:
            check_code_index = 0
        
        return self.CHECK_CHARS[check_code_index]

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成统一社会信用代码"""
        # 第1位：登记管理部门代码
        dept_code = self._get_dept_code()
        
        # 第2位：机构类别代码
        org_type_code = self._get_org_type_code()
        
        # 第3-8位：登记管理机关行政区划码
        region_code = self._get_region_code()
        
        # 第9-17位：主体标识码
        main_body_code = self._get_main_body_code()
        
        # 前17位
        uscc_17 = dept_code + org_type_code + region_code + main_body_code
        
        # 第18位：校验码
        check_code = self._calculate_check_code(uscc_17)
        
        return uscc_17 + check_code

    def validate(self, data: str) -> bool:
        """验证统一社会信用代码"""
        import re
        
        # 基本格式检查
        if not re.match(r'^[0-9A-Z]{18}$', data):
            return False
        
        # 检查字符集
        for char in data:
            if char not in self.CHECK_CHARS:
                return False
        
        # 校验码验证
        uscc_17 = data[:17]
        check_code = data[17]
        
        expected_check = self._calculate_check_code(uscc_17)
        return check_code == expected_check

    def extract_info(self, uscc: str) -> dict:
        """从统一社会信用代码中提取信息"""
        if not self.validate(uscc):
            return {"valid": False}
        
        # 提取各部分信息
        dept_code = uscc[0]
        org_type_code = uscc[1]
        province_code = uscc[2:4]
        region_code = uscc[2:8]
        main_body_code = uscc[8:17]
        check_code = uscc[17]
        
        # 解析信息
        dept_name = self.DEPT_CODES.get(dept_code, "未知")
        
        # 查找机构类型
        org_type_name = "未知"
        for category, types in self.ORG_TYPE_CODES.items():
            if org_type_code in types:
                org_type_name = types[org_type_code]
                break
        
        # 查找省份名称
        province_name = None
        for name, code in self.PROVINCE_CODES.items():
            if code == province_code:
                province_name = name
                break
        
        return {
            "valid": True,
            "dept_code": dept_code,
            "dept_name": dept_name,
            "org_type_code": org_type_code,
            "org_type_name": org_type_name,
            "province_code": province_code,
            "province_name": province_name,
            "region_code": region_code,
            "main_body_code": main_body_code,
            "check_code": check_code
        }

    def generate_by_company_name(self, company_name: str) -> str:
        """根据公司名称生成对应的统一社会信用代码"""
        # 从公司名称中推断地区和类型
        inferred_region = None
        inferred_type = "enterprise"
        
        # 检查地区
        for region in self.PROVINCE_CODES.keys():
            if region in company_name:
                inferred_region = region
                break
        
        # 检查类型
        if "有限公司" in company_name or "股份" in company_name:
            inferred_type = "enterprise"
        elif "合作社" in company_name:
            inferred_type = "enterprise"  # 农民专业合作社也属于企业类
        
        # 临时设置参数
        original_region = self.region
        original_org_type = self.org_type
        
        try:
            if inferred_region:
                self.region = inferred_region
            self.org_type = inferred_type
            
            return self.generate()
        finally:
            # 恢复原始参数
            self.region = original_region
            self.org_type = original_org_type
