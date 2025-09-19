"""
中文公司名称生成器
支持生成各种类型的中文公司名称
"""

import random
from typing import Optional

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    GenerationContext,
    GeneratorType,
    ValidatedDataGenerator,
)


@register_generator("company_name", ["公司名称", "企业名称"])
class ChineseCompanyNameGenerator(ValidatedDataGenerator):
    """中文公司名称生成器"""

    # 地区前缀
    REGIONS = {
        "一线城市": ["北京", "上海", "广州", "深圳"],
        "新一线": ["成都", "杭州", "重庆", "武汉", "西安", "苏州", "天津", "南京", "长沙", "郑州", "东莞", "青岛", "沈阳", "宁波", "昆明"],
        "二线城市": ["无锡", "佛山", "合肥", "大连", "福州", "厦门", "哈尔滨", "济南", "温州", "南宁", "长春", "泉州", "石家庄", "贵阳", "南昌"],
        "全国": ["中国", "华夏", "神州", "九州", "中华", "华北", "华南", "华东", "华西", "东方", "西部", "南方", "北方"]
    }

    # 行业相关词汇
    INDUSTRY_WORDS = {
        "tech": {
            "核心词": ["科技", "技术", "信息", "网络", "数据", "智能", "数字", "电子", "软件", "系统"],
            "修饰词": ["创新", "先进", "高新", "前沿", "领先", "尖端", "智慧", "未来", "新兴", "现代"],
            "后缀词": ["科技", "技术", "信息技术", "网络科技", "数据科技", "智能科技"]
        },
        "finance": {
            "核心词": ["金融", "投资", "资本", "财富", "基金", "证券", "银行", "保险", "信托", "资产"],
            "修饰词": ["稳健", "安全", "专业", "权威", "可靠", "诚信", "优质", "精品", "卓越", "领先"],
            "后缀词": ["金融", "投资", "资本", "财富管理", "基金管理", "资产管理"]
        },
        "manufacturing": {
            "核心词": ["制造", "工业", "机械", "设备", "生产", "加工", "装备", "器械", "工程", "重工"],
            "修饰词": ["精密", "重型", "先进", "现代", "智能", "自动", "高效", "节能", "环保", "优质"],
            "后缀词": ["制造", "工业", "机械", "设备", "重工"]
        },
        "trade": {
            "核心词": ["贸易", "商务", "进出口", "国际", "商业", "经贸", "流通", "供应链", "物流", "采购"],
            "修饰词": ["国际", "全球", "专业", "综合", "现代", "高效", "便捷", "快速", "安全", "可靠"],
            "后缀词": ["贸易", "商务", "进出口", "国际贸易", "商业"]
        },
        "service": {
            "核心词": ["服务", "咨询", "管理", "顾问", "策划", "营销", "广告", "传媒", "文化", "教育"],
            "修饰词": ["专业", "优质", "高端", "精品", "一流", "卓越", "权威", "领先", "创新", "高效"],
            "后缀词": ["服务", "咨询", "管理", "顾问"]
        },
        "real_estate": {
            "核心词": ["地产", "房地产", "置业", "建设", "开发", "投资", "物业", "建筑", "工程", "装饰"],
            "修饰词": ["优质", "精品", "高端", "豪华", "现代", "绿色", "生态", "智慧", "舒适", "宜居"],
            "后缀词": ["地产", "房地产", "置业", "开发", "建设"]
        },
        "mixed": {
            "核心词": ["实业", "集团", "控股", "投资", "发展", "建设", "创业", "企业", "产业", "商贸"],
            "修饰词": ["综合", "多元", "现代", "创新", "发展", "兴业", "繁荣", "昌盛", "宏图", "伟业"],
            "后缀词": ["实业", "集团", "控股", "投资", "发展"]
        }
    }

    # 公司类型后缀
    COMPANY_TYPES = {
        "有限公司": 0.6,
        "股份有限公司": 0.15,
        "有限责任公司": 0.2,
        "集团有限公司": 0.03,
        "控股有限公司": 0.02
    }

    # 特殊字符组合
    SPECIAL_COMBINATIONS = {
        "tech": ["云计算", "大数据", "人工智能", "物联网", "区块链", "5G", "AI", "VR", "AR", "互联网+"],
        "finance": ["金融科技", "数字金融", "普惠金融", "绿色金融", "供应链金融"],
        "new_energy": ["新能源", "清洁能源", "太阳能", "风能", "电池", "储能", "充电桩"]
    }

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BUSINESS

    @property
    def supported_parameters(self) -> list[str]:
        return ["type", "region", "size", "style", "include_region", "length"]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.company_type = self.parameters.get("type", "mixed")
        self.region = self.parameters.get("region", None)
        self.size = self.parameters.get("size", "medium")  # small, medium, large
        self.style = self.parameters.get("style", "modern")  # traditional, modern, creative
        self.include_region = self.parameters.get("include_region", True)
        self.length = self.parameters.get("length", "medium")  # short, medium, long

    def _get_region_prefix(self) -> str:
        """获取地区前缀"""
        if not self.include_region:
            return ""
        
        if self.region:
            # 如果指定了具体地区
            if self.region in [item for sublist in self.REGIONS.values() for item in sublist]:
                return self.region
            else:
                # 如果不在列表中，直接使用
                return self.region
        
        # 根据公司规模选择地区
        if self.size == "large":
            region_type = random.choice(["一线城市", "全国"])
        elif self.size == "medium":
            region_type = random.choice(["一线城市", "新一线", "全国"])
        else:
            region_type = random.choice(["新一线", "二线城市"])
        
        return random.choice(self.REGIONS[region_type])

    def _get_core_name(self) -> str:
        """获取公司核心名称"""
        industry_data = self.INDUSTRY_WORDS.get(self.company_type, self.INDUSTRY_WORDS["mixed"])
        
        # 根据长度选择组合方式
        if self.length == "short":
            # 短名称：修饰词 + 核心词
            modifier = random.choice(industry_data["修饰词"])
            core = random.choice(industry_data["核心词"])
            return modifier + core
        elif self.length == "long":
            # 长名称：修饰词 + 核心词 + 后缀词
            modifier = random.choice(industry_data["修饰词"])
            core = random.choice(industry_data["核心词"])
            suffix = random.choice(industry_data["后缀词"])
            
            # 避免重复
            if core == suffix:
                suffix = random.choice([w for w in industry_data["后缀词"] if w != core])
            
            return modifier + core + suffix
        else:
            # 中等长度：核心词 + 后缀词 或 修饰词 + 核心词
            if random.random() < 0.7:
                core = random.choice(industry_data["核心词"])
                suffix = random.choice(industry_data["后缀词"])
                return core + suffix if core != suffix else core
            else:
                modifier = random.choice(industry_data["修饰词"])
                core = random.choice(industry_data["核心词"])
                return modifier + core

    def _add_special_elements(self, name: str) -> str:
        """添加特殊元素"""
        if self.style == "creative" and random.random() < 0.3:
            # 创意风格，可能添加特殊组合
            special_words = self.SPECIAL_COMBINATIONS.get(self.company_type, [])
            if special_words and random.random() < 0.5:
                special = random.choice(special_words)
                return special + name
        
        return name

    def _get_company_type_suffix(self) -> str:
        """获取公司类型后缀"""
        # 根据权重随机选择
        rand = random.random()
        cumulative = 0
        
        for company_type, weight in self.COMPANY_TYPES.items():
            cumulative += weight
            if rand <= cumulative:
                return company_type
        
        return "有限公司"  # 默认

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成公司名称"""
        # 地区前缀
        region_prefix = self._get_region_prefix()
        
        # 核心名称
        core_name = self._get_core_name()
        
        # 添加特殊元素
        core_name = self._add_special_elements(core_name)
        
        # 公司类型后缀
        type_suffix = self._get_company_type_suffix()
        
        # 组合完整名称
        full_name = region_prefix + core_name + type_suffix
        
        return full_name

    def validate(self, data: str) -> bool:
        """验证公司名称格式"""
        import re
        
        # 基本格式检查：包含中文字符，以公司类型结尾
        if not re.search(r'[\u4e00-\u9fff]', data):
            return False
        
        # 检查是否以合法的公司类型结尾
        valid_endings = list(self.COMPANY_TYPES.keys())
        return any(data.endswith(ending) for ending in valid_endings)

    def generate_batch(self, count: int, **kwargs) -> list[str]:
        """批量生成公司名称"""
        # 临时更新参数
        original_params = self.parameters.copy()
        self.parameters.update(kwargs)
        self._setup()
        
        try:
            names = []
            for _ in range(count):
                name = self.generate()
                # 确保不重复
                while name in names:
                    name = self.generate()
                names.append(name)
            return names
        finally:
            # 恢复原始参数
            self.parameters = original_params
            self._setup()
