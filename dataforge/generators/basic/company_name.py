"""
企业名称生成器
"""

import secrets
from typing import Optional

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
)
from ...core.types import GeneratorType


class CompanyNameGenerator(DataGenerator[str]):
    """企业名称生成器"""

    def _setup(self) -> None:
        self.industry = self.parameters.get(
            "industry", "ANY"
        )  # IT, FINANCE, RETAIL, ANY
        self.company_type = self.parameters.get(
            "type", "ANY"
        )  # CO_LTD, GROUP, INSTITUTE, ANY
        self.prefix_region = self.parameters.get(
            "prefix_region", True
        )  # 是否加地区前缀

        # 地区前缀
        self.regions = [
            "北京",
            "上海",
            "深圳",
            "广州",
            "杭州",
            "苏州",
            "成都",
            "武汉",
            "西安",
            "南京",
            "天津",
            "重庆",
            "青岛",
            "大连",
            "宁波",
            "厦门",
            "长沙",
            "郑州",
            "无锡",
            "佛山",
            "东莞",
            "合肥",
            "昆明",
            "福州",
            "哈尔滨",
            "济南",
            "长春",
            "石家庄",
            "常州",
            "嘉兴",
        ]

        # 行业关键词
        self.industry_keywords = {
            "IT": [
                "科技",
                "信息",
                "网络",
                "软件",
                "数据",
                "云计算",
                "智能",
                "互联网",
                "电子",
                "通信",
                "技术",
                "系统",
                "平台",
                "数字",
                "创新",
                "智慧",
            ],
            "FINANCE": [
                "金融",
                "投资",
                "资本",
                "财富",
                "基金",
                "证券",
                "银行",
                "保险",
                "资产",
                "理财",
                "信托",
                "租赁",
                "担保",
                "小贷",
                "支付",
                "金服",
            ],
            "RETAIL": [
                "商贸",
                "贸易",
                "销售",
                "零售",
                "批发",
                "商城",
                "购物",
                "百货",
                "超市",
                "连锁",
                "专卖",
                "代理",
                "经销",
                "营销",
                "电商",
                "商业",
            ],
            "MANUFACTURING": [
                "制造",
                "生产",
                "工业",
                "机械",
                "设备",
                "加工",
                "装备",
                "重工",
                "轻工",
                "化工",
                "材料",
                "能源",
                "环保",
                "新材料",
                "精密",
                "自动化",
            ],
            "EDUCATION": [
                "教育",
                "培训",
                "学校",
                "学院",
                "大学",
                "研究",
                "科研",
                "学术",
                "文化",
                "艺术",
                "体育",
                "健康",
                "医疗",
                "咨询",
                "服务",
                "管理",
            ],
            "REAL_ESTATE": [
                "房地产",
                "地产",
                "置业",
                "物业",
                "建设",
                "建筑",
                "工程",
                "装饰",
                "设计",
                "规划",
                "开发",
                "投资",
                "置地",
                "城建",
                "基建",
                "园区",
            ],
        }

        # 通用关键词
        self.general_keywords = [
            "华",
            "中",
            "国",
            "民",
            "天",
            "地",
            "人",
            "和",
            "信",
            "诚",
            "德",
            "正",
            "金",
            "银",
            "宝",
            "珠",
            "玉",
            "龙",
            "凤",
            "麒",
            "麟",
            "鹤",
            "鹏",
            "燕",
            "东",
            "西",
            "南",
            "北",
            "中",
            "上",
            "下",
            "大",
            "小",
            "新",
            "老",
            "古",
            "春",
            "夏",
            "秋",
            "冬",
            "晨",
            "晚",
            "阳",
            "月",
            "星",
            "云",
            "海",
            "山",
            "兴",
            "发",
            "达",
            "通",
            "顺",
            "盛",
            "昌",
            "泰",
            "安",
            "康",
            "富",
            "贵",
            "美",
            "好",
            "优",
            "佳",
            "精",
            "品",
            "质",
            "高",
            "尚",
            "雅",
            "洁",
            "净",
        ]

        # 公司类型后缀
        self.company_types = {
            "CO_LTD": ["有限公司", "有限责任公司"],
            "GROUP": ["集团", "集团有限公司", "控股集团"],
            "INSTITUTE": ["研究所", "研究院", "技术研究院"],
            "CORP": ["公司", "企业", "实业"],
            "TECH": ["科技有限公司", "技术有限公司"],
            "TRADING": ["贸易有限公司", "商贸有限公司"],
            "INVESTMENT": ["投资有限公司", "资本管理有限公司"],
        }

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始企业名称，确保最小长度要求"""
        parts = []

        # 1. 地区前缀
        if self.prefix_region:
            if (secrets.randbelow(1000000) / 1000000) < 0.7:  # 70%概率加地区前缀
                region = secrets.choice(self.regions)
                parts.append(region)

        # 2. 核心名称 - 确保最小长度
        core_name = self._generate_core_name()
        parts.append(core_name)

        # 3. 公司类型后缀
        company_suffix = self._generate_company_suffix()
        parts.append(company_suffix)

        result = "".join(parts)

        # 智能长度保证：确保最小长度为4个字符
        min_length = 4
        if len(result) < min_length:
            # 计算需要补充的字符数
            needed = min_length - len(result)

            # 从通用关键词中选择合适的补充内容
            supplement_candidates = [
                word for word in self.general_keywords if len(word) <= needed
            ]

            if supplement_candidates:
                supplement = secrets.choice(supplement_candidates)
                # 在核心名称后插入补充内容
                if len(parts) >= 2:
                    parts.insert(-1, supplement)
                else:
                    parts.append(supplement)
                result = "".join(parts)
            else:
                # 如果没有合适的补充词，使用通用字符
                result = result + "科技"[:needed]

        return result

    def _generate_core_name(self) -> str:
        """生成核心名称"""
        # 根据行业选择关键词
        if self.industry != "ANY" and self.industry in self.industry_keywords:
            industry_words = self.industry_keywords[self.industry]
            if (secrets.randbelow(1000000) / 1000000) < 0.8:  # 80%概率使用行业关键词
                core_parts = [secrets.choice(industry_words)]
            else:
                core_parts = [secrets.choice(self.general_keywords)]
        else:
            # 混合使用行业关键词和通用关键词
            all_industry_words = []
            for words in self.industry_keywords.values():
                all_industry_words.extend(words)

            if (secrets.randbelow(1000000) / 1000000) < 0.6:
                core_parts = [secrets.choice(all_industry_words)]
            else:
                core_parts = [secrets.choice(self.general_keywords)]

        # 可能添加第二个词
        if (secrets.randbelow(1000000) / 1000000) < 0.4:  # 40%概率添加第二个词
            if (secrets.randbelow(1000000) / 1000000) < 0.5:
                core_parts.append(secrets.choice(self.general_keywords))
            else:
                # 根据行业添加相关词
                if self.industry != "ANY" and self.industry in self.industry_keywords:
                    core_parts.append(
                        secrets.choice(self.industry_keywords[self.industry])
                    )
                else:
                    core_parts.append(secrets.choice(self.general_keywords))

        return "".join(core_parts)

    def _generate_company_suffix(self) -> str:
        """生成公司类型后缀"""
        if self.company_type != "ANY" and self.company_type in self.company_types:
            return secrets.choice(self.company_types[self.company_type])
        else:
            # 根据行业倾向选择合适的后缀
            if self.industry == "IT":
                suffix_types = ["CO_LTD", "TECH"]
            elif self.industry == "FINANCE":
                suffix_types = ["CO_LTD", "INVESTMENT", "GROUP"]
            elif self.industry == "RETAIL":
                suffix_types = ["CO_LTD", "TRADING"]
            elif self.industry == "EDUCATION":
                suffix_types = ["CO_LTD", "INSTITUTE"]
            else:
                suffix_types = list(self.company_types.keys())

            chosen_type = secrets.choice(suffix_types)
            return secrets.choice(self.company_types[chosen_type])

    def validate(self, data: str) -> bool:
        """校验企业名称"""
        if not isinstance(data, str) or len(data.strip()) == 0:
            return False

        # 基本长度检查
        if len(data) < 3 or len(data) > 100:
            return False

        # 检查是否包含公司类型后缀（中文）
        all_suffixes = []
        for suffixes in self.company_types.values():
            all_suffixes.extend(suffixes)

        has_chinese_suffix = any(data.endswith(suffix) for suffix in all_suffixes)

        # 检查英文公司后缀
        english_suffixes = [
            "Inc",
            "Corp",
            "LLC",
            "Ltd",
            "Co",
            "Group",
            "International",
            "Inc.",
            "Corp.",
            "Ltd.",
        ]
        has_english_suffix = any(suffix in data for suffix in english_suffixes)

        # 检查是否包含公司相关词汇
        company_keywords = [
            "Solutions",
            "Systems",
            "Technologies",
            "Enterprises",
            "Services",
            "Partners",
        ]
        has_company_keyword = any(keyword in data for keyword in company_keywords)

        return has_chinese_suffix or has_english_suffix or has_company_keyword

    def get_company_info(self, company_name: str) -> dict:
        """解析企业名称信息"""
        result = {
            "original": company_name,
            "region": "",
            "core_name": "",
            "company_type": "",
            "industry_hint": "",
        }

        # 检测地区前缀
        for region in self.regions:
            if company_name.startswith(region):
                result["region"] = region
                company_name = company_name[len(region) :]
                break

        # 检测公司类型后缀
        for _type_key, suffixes in self.company_types.items():
            for suffix in suffixes:
                if company_name.endswith(suffix):
                    result["company_type"] = suffix
                    result["core_name"] = company_name[: -len(suffix)]
                    break
            if result["company_type"]:
                break

        # 推测行业
        for industry, keywords in self.industry_keywords.items():
            for keyword in keywords:
                if keyword in result["core_name"]:
                    result["industry_hint"] = industry
                    break
            if result["industry_hint"]:
                break

        return result

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO

    @property
    def supported_parameters(self) -> list[str]:
        return ["industry", "type", "prefix_region"]

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        # 支持language参数
        language = self.parameters.get("language", "").lower()

        if language == "english":
            return self._generate_english_name()

        return self._generate_raw(context)

    def _generate_english_name(self) -> str:
        """生成英文公司名"""
        # 英文公司名前缀
        prefixes = [
            "Global",
            "International",
            "United",
            "Advanced",
            "Premier",
            "Elite",
            "Prime",
            "Superior",
            "Innovative",
            "Dynamic",
            "Strategic",
            "Quantum",
            "Digital",
            "Smart",
            "Tech",
            "Cyber",
            "Cloud",
            "Data",
            "Net",
            "Web",
        ]

        # 英文公司名核心词
        core_words = [
            "Solutions",
            "Systems",
            "Technologies",
            "Innovations",
            "Enterprises",
            "Industries",
            "Services",
            "Group",
            "Partners",
            "Associates",
            "Ventures",
            "Capital",
            "Holdings",
            "Networks",
            "Dynamics",
            "Labs",
            "Studios",
            "Works",
            "Media",
            "Digital",
        ]

        # 英文公司后缀
        suffixes = ["Inc", "Corp", "LLC", "Ltd", "Co", "Group", "International"]

        # 生成公司名
        parts = []

        # 40%概率添加前缀
        if secrets.randbelow(100) < 40:
            parts.append(secrets.choice(prefixes))

        # 核心词
        parts.append(secrets.choice(core_words))

        # 60%概率添加后缀
        if secrets.randbelow(100) < 60:
            suffix = secrets.choice(suffixes)
            return f"{' '.join(parts)} {suffix}."

        return " ".join(parts)


@register_generator("company_name", ["company", "企业名称", "公司名称"])
class ChineseCompanyNameGenerator(CompanyNameGenerator):
    """中国企业名称生成器注册版本"""

    pass

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        # 调用父类的_generate_raw方法
        return super()._generate_raw(context)

    def validate(self, data: str) -> bool:
        """验证生成的数据"""
        # 简单验证：检查是否为非空字符串
        return isinstance(data, str) and bool(data.strip())

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        # 继承父类的参数列表
        return ["industry", "type", "prefix_region"]


@register_generator("company_name", ["company-name"])
class GenericCompanyNameGenerator(CompanyNameGenerator):
    """通用company_name生成器注册版本"""

    pass
