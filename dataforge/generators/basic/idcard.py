"""
中国身份证号码生成器
支持生成符合GB 11643-1999标准的18位身份证号码
"""

import random
from datetime import datetime, timedelta
from typing import Optional, Tuple

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    GenerationContext,
    GeneratorType,
    ValidatedDataGenerator,
)


@register_generator("idcard", ["身份证", "身份证号码"])
class ChineseIDCardGenerator(ValidatedDataGenerator):
    """中国身份证号码生成器"""

    # 省份代码映射
    PROVINCE_CODES = {
        "北京": "11", "天津": "12", "河北": "13", "山西": "14", "内蒙古": "15",
        "辽宁": "21", "吉林": "22", "黑龙江": "23",
        "上海": "31", "江苏": "32", "浙江": "33", "安徽": "34", "福建": "35", "江西": "36", "山东": "37",
        "河南": "41", "湖北": "42", "湖南": "43", "广东": "44", "广西": "45", "海南": "46",
        "重庆": "50", "四川": "51", "贵州": "52", "云南": "53", "西藏": "54",
        "陕西": "61", "甘肃": "62", "青海": "63", "宁夏": "64", "新疆": "65",
        "台湾": "71", "香港": "81", "澳门": "82"
    }

    # 校验码对应表
    CHECK_CODES = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    
    # 权重系数
    WEIGHTS = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.PERSON

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "region", "birth_date_range", "gender", "valid", 
            "province", "city", "county", "birth_year", "birth_month", "birth_day"
        ]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.region = self.parameters.get("region", None)
        self.birth_date_range = self.parameters.get(
            "birth_date_range", ("1960-01-01", "2005-12-31")
        )
        self.gender = self.parameters.get("gender", "ANY").upper()
        self.valid = self.parameters.get("valid", True)
        
        # 更细粒度的地区控制
        self.province = self.parameters.get("province", None)
        self.city = self.parameters.get("city", None)
        self.county = self.parameters.get("county", None)
        
        # 具体出生日期控制
        self.birth_year = self.parameters.get("birth_year", None)
        self.birth_month = self.parameters.get("birth_month", None)
        self.birth_day = self.parameters.get("birth_day", None)

    def _get_region_code(self) -> str:
        """获取地区代码（前6位）"""
        # 如果指定了省份，使用省份代码
        if self.province and self.province in self.PROVINCE_CODES:
            province_code = self.PROVINCE_CODES[self.province]
        elif self.region and self.region in self.PROVINCE_CODES:
            province_code = self.PROVINCE_CODES[self.region]
        else:
            # 随机选择省份
            province_code = random.choice(list(self.PROVINCE_CODES.values()))
        
        # 生成市县代码（4位）
        if self.city:
            # 如果指定了城市，可以在这里添加城市代码映射
            # 现在简单生成随机代码
            city_code = f"{random.randint(1, 99):02d}"
        else:
            city_code = f"{random.randint(1, 99):02d}"
        
        if self.county:
            # 如果指定了县区，可以在这里添加县区代码映射
            county_code = f"{random.randint(1, 99):02d}"
        else:
            county_code = f"{random.randint(1, 99):02d}"
        
        return province_code + city_code + county_code

    def _get_birth_date(self) -> str:
        """获取出生日期（8位YYYYMMDD）"""
        if self.birth_year and self.birth_month and self.birth_day:
            # 使用指定的出生日期
            return f"{self.birth_year:04d}{self.birth_month:02d}{self.birth_day:02d}"
        
        # 解析日期范围
        start_date_str, end_date_str = self.birth_date_range
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        
        # 生成随机日期
        days_between = (end_date - start_date).days
        random_days = random.randint(0, days_between)
        random_date = start_date + timedelta(days=random_days)
        
        return random_date.strftime("%Y%m%d")

    def _get_sequence_code(self, gender_digit: int) -> str:
        """获取顺序码（3位），最后一位表示性别"""
        # 前两位随机
        first_two = random.randint(10, 99)
        
        # 第三位根据性别确定（奇数男性，偶数女性）
        if self.gender == "MALE":
            # 确保是奇数
            third_digit = random.choice([1, 3, 5, 7, 9])
        elif self.gender == "FEMALE":
            # 确保是偶数
            third_digit = random.choice([0, 2, 4, 6, 8])
        else:
            # 随机性别
            third_digit = random.randint(0, 9)
        
        return f"{first_two}{third_digit}"

    def _calculate_check_code(self, id_17: str) -> str:
        """计算校验码"""
        if not self.valid:
            # 如果不需要有效的校验码，随机返回
            return random.choice(self.CHECK_CODES)
        
        # 计算加权和
        sum_val = sum(int(id_17[i]) * self.WEIGHTS[i] for i in range(17))
        
        # 计算校验码
        remainder = sum_val % 11
        return self.CHECK_CODES[remainder]

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成身份证号码"""
        # 地区代码（6位）
        region_code = self._get_region_code()
        
        # 出生日期（8位）
        birth_date = self._get_birth_date()
        
        # 顺序码（3位）
        sequence_code = self._get_sequence_code(int(birth_date[-1]))
        
        # 前17位
        id_17 = region_code + birth_date + sequence_code
        
        # 校验码（1位）
        check_code = self._calculate_check_code(id_17)
        
        return id_17 + check_code

    def validate(self, data: str) -> bool:
        """验证身份证号码"""
        import re
        
        # 基本格式检查
        if not re.match(r'^\d{17}[\dX]$', data):
            return False
        
        # 校验码验证
        id_17 = data[:17]
        check_code = data[17]
        
        try:
            sum_val = sum(int(id_17[i]) * self.WEIGHTS[i] for i in range(17))
            expected_check = self.CHECK_CODES[sum_val % 11]
            return check_code == expected_check
        except (ValueError, IndexError):
            return False

    def extract_info(self, idcard: str) -> dict:
        """从身份证号码中提取信息"""
        if not self.validate(idcard):
            return {"valid": False}
        
        # 提取各部分信息
        province_code = idcard[:2]
        birth_date = idcard[6:14]
        gender_digit = int(idcard[16])
        
        # 查找省份名称
        province_name = None
        for name, code in self.PROVINCE_CODES.items():
            if code == province_code:
                province_name = name
                break
        
        # 解析出生日期
        try:
            birth_year = int(birth_date[:4])
            birth_month = int(birth_date[4:6])
            birth_day = int(birth_date[6:8])
            birth_date_obj = datetime(birth_year, birth_month, birth_day)
            
            # 计算年龄
            today = datetime.now()
            age = today.year - birth_year
            if today.month < birth_month or (today.month == birth_month and today.day < birth_day):
                age -= 1
        except ValueError:
            birth_date_obj = None
            age = None
        
        # 判断性别
        gender = "男" if gender_digit % 2 == 1 else "女"
        
        return {
            "valid": True,
            "province_code": province_code,
            "province_name": province_name,
            "birth_date": birth_date_obj.strftime("%Y-%m-%d") if birth_date_obj else None,
            "age": age,
            "gender": gender,
            "gender_code": gender_digit
        }
