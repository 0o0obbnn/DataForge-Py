"""
中国地址信息生成器
支持生成中国大陆地区的详细地址信息
"""

import random
from typing import Optional, Dict, List

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    GenerationContext,
    GeneratorType,
    ValidatedDataGenerator,
)


@register_generator("address", ["地址", "住址", "通讯地址"])
class ChineseAddressGenerator(ValidatedDataGenerator):
    """中国地址生成器"""

    # 省级行政区
    PROVINCES = {
        "北京市": {"cities": ["东城区", "西城区", "朝阳区", "丰台区", "石景山区", "海淀区", "门头沟区", "房山区", "通州区", "顺义区", "昌平区", "大兴区", "怀柔区", "平谷区", "密云区", "延庆区"], "postal_prefix": "10"},
        "上海市": {"cities": ["黄浦区", "徐汇区", "长宁区", "静安区", "普陀区", "虹口区", "杨浦区", "闵行区", "宝山区", "嘉定区", "浦东新区", "金山区", "松江区", "青浦区", "奉贤区", "崇明区"], "postal_prefix": "20"},
        "广东省": {"cities": ["广州市", "深圳市", "珠海市", "汕头市", "佛山市", "韶关市", "湛江市", "肇庆市", "江门市", "茂名市", "惠州市", "梅州市", "汕尾市", "河源市", "阳江市", "清远市", "东莞市", "中山市", "潮州市", "揭阳市", "云浮市"], "postal_prefix": "51"},
        "江苏省": {"cities": ["南京市", "无锡市", "徐州市", "常州市", "苏州市", "南通市", "连云港市", "淮安市", "盐城市", "扬州市", "镇江市", "泰州市", "宿迁市"], "postal_prefix": "21"},
        "浙江省": {"cities": ["杭州市", "宁波市", "温州市", "嘉兴市", "湖州市", "绍兴市", "金华市", "衢州市", "舟山市", "台州市", "丽水市"], "postal_prefix": "31"},
        "山东省": {"cities": ["济南市", "青岛市", "淄博市", "枣庄市", "东营市", "烟台市", "潍坊市", "济宁市", "泰安市", "威海市", "日照市", "临沂市", "德州市", "聊城市", "滨州市", "菏泽市"], "postal_prefix": "25"},
        "河南省": {"cities": ["郑州市", "开封市", "洛阳市", "平顶山市", "安阳市", "鹤壁市", "新乡市", "焦作市", "濮阳市", "许昌市", "漯河市", "三门峡市", "南阳市", "商丘市", "信阳市", "周口市", "驻马店市", "济源市"], "postal_prefix": "45"},
        "四川省": {"cities": ["成都市", "自贡市", "攀枝花市", "泸州市", "德阳市", "绵阳市", "广元市", "遂宁市", "内江市", "乐山市", "南充市", "眉山市", "宜宾市", "广安市", "达州市", "雅安市", "巴中市", "资阳市"], "postal_prefix": "61"},
        "湖北省": {"cities": ["武汉市", "黄石市", "十堰市", "宜昌市", "襄阳市", "鄂州市", "荆门市", "孝感市", "荆州市", "黄冈市", "咸宁市", "随州市"], "postal_prefix": "43"},
        "湖南省": {"cities": ["长沙市", "株洲市", "湘潭市", "衡阳市", "邵阳市", "岳阳市", "常德市", "张家界市", "益阳市", "郴州市", "永州市", "怀化市", "娄底市"], "postal_prefix": "41"}
    }

    # 常见街道类型
    STREET_TYPES = ["路", "街", "大道", "大街", "巷", "弄", "胡同", "里", "坊"]

    # 街道名称元素
    STREET_ELEMENTS = {
        "方位": ["东", "南", "西", "北", "中", "内", "外", "上", "下"],
        "数字": ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"],
        "常用词": ["人民", "建设", "解放", "和平", "友谊", "团结", "胜利", "光明", "新华", "文化", "学府", "科技", "工业", "商业", "金融", "花园", "公园", "广场", "中心"]
    }

    # 建筑类型
    BUILDING_TYPES = {
        "住宅": ["小区", "花园", "苑", "城", "家园", "公寓", "大厦", "广场", "中心", "新村"],
        "商业": ["商城", "购物中心", "商业广场", "写字楼", "商务大厦", "金融中心", "国际大厦"],
        "工业": ["工业园", "科技园", "开发区", "产业园", "厂区"]
    }

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.CONTACT

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "province", "city", "district", "detail_level", 
            "include_postal_code", "address_type", "format_style"
        ]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.province = self.parameters.get("province", None)
        self.city = self.parameters.get("city", None)
        self.district = self.parameters.get("district", None)
        self.detail_level = self.parameters.get("detail_level", "detailed")  # simple, detailed, full
        self.include_postal_code = self.parameters.get("include_postal_code", False)
        self.address_type = self.parameters.get("address_type", "residential")  # residential, commercial, industrial
        self.format_style = self.parameters.get("format_style", "standard")  # standard, formal, casual

    def _select_region(self) -> Dict[str, str]:
        """选择省市区"""
        # 选择省份
        if self.province and self.province in self.PROVINCES:
            selected_province = self.province
        else:
            selected_province = random.choice(list(self.PROVINCES.keys()))
        
        province_info = self.PROVINCES[selected_province]
        
        # 选择城市
        if self.city and self.city in province_info["cities"]:
            selected_city = self.city
        else:
            selected_city = random.choice(province_info["cities"])
        
        # 如果是直辖市，区就是城市
        if selected_province in ["北京市", "上海市", "天津市", "重庆市"]:
            selected_district = selected_city
            selected_city = selected_province
        else:
            # 生成区县名称
            if self.district:
                selected_district = self.district
            else:
                district_suffixes = ["区", "县", "市"]
                district_prefix = random.choice(["东", "西", "南", "北", "中", "新", "老", "上", "下"])
                selected_district = district_prefix + random.choice(["城", "关", "郊", "山", "河", "湖"]) + random.choice(district_suffixes)
        
        return {
            "province": selected_province,
            "city": selected_city,
            "district": selected_district,
            "postal_prefix": province_info["postal_prefix"]
        }

    def _generate_street_name(self) -> str:
        """生成街道名称"""
        # 选择街道元素
        elements = []
        
        # 可能添加方位
        if random.random() < 0.4:
            elements.append(random.choice(self.STREET_ELEMENTS["方位"]))
        
        # 添加主要名称
        if random.random() < 0.3:
            elements.append(random.choice(self.STREET_ELEMENTS["数字"]))
        
        elements.append(random.choice(self.STREET_ELEMENTS["常用词"]))
        
        # 添加街道类型
        street_type = random.choice(self.STREET_TYPES)
        
        return ''.join(elements) + street_type

    def _generate_building_info(self) -> str:
        """生成建筑信息"""
        building_types = self.BUILDING_TYPES.get(
            "住宅" if self.address_type == "residential" else
            "商业" if self.address_type == "commercial" else "工业"
        )
        
        # 生成建筑名称
        building_prefix = random.choice(["阳光", "花园", "金色", "银河", "星光", "海景", "山景", "湖景", "绿地", "蓝天", "彩虹", "梦想"])
        building_suffix = random.choice(building_types)
        building_name = building_prefix + building_suffix
        
        # 添加楼栋和房间号
        if self.detail_level in ["detailed", "full"]:
            building_num = random.randint(1, 30)
            unit_num = random.randint(1, 6)
            room_num = f"{random.randint(1, 30):02d}{random.randint(1, 8)}"
            
            return f"{building_name}{building_num}号楼{unit_num}单元{room_num}室"
        else:
            return building_name

    def _generate_postal_code(self, postal_prefix: str) -> str:
        """生成邮政编码"""
        # 生成6位邮政编码
        suffix = f"{random.randint(1000, 9999)}"
        return postal_prefix + suffix

    def _format_address(self, components: Dict[str, str]) -> str:
        """格式化地址"""
        if self.format_style == "formal":
            # 正式格式：省份 城市 区县 街道 建筑
            address_parts = [
                components["province"],
                components["city"],
                components["district"],
                components["street"],
                components["building"]
            ]
            
            if self.include_postal_code:
                address_parts.append(f"邮编：{components['postal_code']}")
                
        elif self.format_style == "casual":
            # 简洁格式
            address_parts = [
                components["city"],
                components["district"],
                components["street"],
                components["building"]
            ]
        else:
            # 标准格式
            address_parts = []
            
            # 根据详细程度决定包含的信息
            if self.detail_level == "simple":
                address_parts = [components["city"], components["district"]]
            elif self.detail_level == "detailed":
                address_parts = [
                    components["province"],
                    components["city"],
                    components["district"],
                    components["street"]
                ]
            else:  # full
                address_parts = [
                    components["province"],
                    components["city"],
                    components["district"],
                    components["street"],
                    components["building"]
                ]
            
            if self.include_postal_code and self.detail_level == "full":
                address_parts.append(components["postal_code"])
        
        return "".join(address_parts)

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成地址"""
        # 选择地区
        region = self._select_region()
        
        # 生成街道
        street = self._generate_street_name()
        street_number = random.randint(1, 999)
        full_street = f"{street}{street_number}号"
        
        # 生成建筑信息
        building = self._generate_building_info()
        
        # 生成邮政编码
        postal_code = self._generate_postal_code(region["postal_prefix"])
        
        # 组装地址组件
        components = {
            "province": region["province"],
            "city": region["city"],
            "district": region["district"],
            "street": full_street,
            "building": building,
            "postal_code": postal_code
        }
        
        return self._format_address(components)

    def validate(self, data: str) -> bool:
        """验证地址格式"""
        # 基本检查：包含中文字符，有一定长度
        import re
        
        if not re.search(r'[\u4e00-\u9fff]', data):
            return False
        
        if len(data) < 5 or len(data) > 200:
            return False
        
        # 检查是否包含常见的地址元素
        address_indicators = ["省", "市", "区", "县", "路", "街", "巷", "号", "室", "栋", "楼"]
        has_indicator = any(indicator in data for indicator in address_indicators)
        
        return has_indicator

    def generate_coordinates(self, address: str) -> Dict[str, float]:
        """生成地址对应的大概坐标（模拟）"""
        # 这里只是示例，实际应用中需要使用地理编码服务
        # 根据省份生成大概的坐标范围
        coordinate_ranges = {
            "北京市": {"lat": (39.4, 40.4), "lng": (115.7, 117.4)},
            "上海市": {"lat": (30.7, 31.8), "lng": (120.9, 122.1)},
            "广东省": {"lat": (20.2, 25.5), "lng": (109.7, 117.2)},
            "江苏省": {"lat": (30.7, 35.3), "lng": (116.4, 121.9)},
            "浙江省": {"lat": (27.0, 31.4), "lng": (118.0, 123.0)}
        }
        
        # 简单的省份匹配
        for province, coords in coordinate_ranges.items():
            if province in address:
                lat_range = coords["lat"]
                lng_range = coords["lng"]
                
                lat = random.uniform(lat_range[0], lat_range[1])
                lng = random.uniform(lng_range[0], lng_range[1])
                
                return {
                    "latitude": round(lat, 6),
                    "longitude": round(lng, 6)
                }
        
        # 默认返回中国中心位置附近的坐标
        return {
            "latitude": round(random.uniform(35.0, 40.0), 6),
            "longitude": round(random.uniform(103.0, 120.0), 6)
        }
