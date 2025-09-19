"""
中文姓名生成器
支持生成真实的中文姓名，包括性别、字数等参数控制
"""

import random
from typing import Optional

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    GenerationContext,
    GeneratorType,
    ValidatedDataGenerator,
)


@register_generator("name", ["姓名", "中文姓名"])
class ChineseNameGenerator(ValidatedDataGenerator):
    """中文姓名生成器"""

    # 常见姓氏 (Top 100 Chinese surnames)
    SURNAMES = [
        "王", "李", "张", "刘", "陈", "杨", "黄", "赵", "周", "吴",
        "徐", "孙", "朱", "马", "胡", "郭", "林", "何", "高", "梁",
        "郑", "罗", "宋", "谢", "唐", "韩", "曹", "许", "邓", "萧",
        "冯", "曾", "程", "蔡", "彭", "潘", "袁", "于", "董", "余",
        "苏", "叶", "吕", "魏", "蒋", "田", "杜", "丁", "沈", "姜",
        "范", "江", "傅", "钟", "卢", "汪", "戴", "崔", "任", "陆",
        "廖", "姚", "方", "金", "邱", "夏", "谭", "韦", "贾", "邹",
        "石", "熊", "孟", "秦", "阎", "薛", "侯", "雷", "白", "龙",
        "段", "郝", "孔", "邵", "史", "毛", "常", "万", "顾", "赖",
        "武", "康", "贺", "严", "尹", "钱", "施", "牛", "洪", "龚"
    ]

    # 男性常用名字
    MALE_NAMES = [
        "伟", "强", "军", "勇", "磊", "涛", "明", "超", "峰", "华",
        "建", "国", "志", "鹏", "杰", "斌", "龙", "辉", "飞", "宇",
        "浩", "凯", "亮", "博", "文", "武", "东", "南", "北", "中",
        "海", "山", "林", "森", "天", "地", "人", "和", "平", "安",
        "康", "健", "乐", "福", "禄", "寿", "喜", "财", "富", "贵",
        "荣", "华", "昌", "盛", "兴", "旺", "发", "达", "成", "功",
        "德", "仁", "义", "礼", "智", "信", "忠", "孝", "廉", "耻",
        "雄", "英", "豪", "杰", "俊", "才", "学", "识", "渊", "博"
    ]

    # 女性常用名字
    FEMALE_NAMES = [
        "丽", "娜", "敏", "静", "秀", "红", "梅", "芳", "燕", "雪",
        "莹", "晶", "欣", "颖", "蕾", "佳", "慧", "琳", "婷", "雯",
        "萍", "霞", "玲", "艳", "洁", "倩", "君", "宁", "薇", "涵",
        "月", "花", "草", "春", "夏", "秋", "冬", "雨", "雷", "电",
        "云", "霞", "虹", "彩", "光", "明", "亮", "星", "辰", "露",
        "珠", "玉", "金", "银", "钻", "宝", "贝", "珍", "琪", "瑶",
        "琴", "棋", "书", "画", "诗", "词", "歌", "舞", "音", "韵",
        "美", "丽", "雅", "优", "柔", "温", "馨", "香", "甜", "蜜"
    ]

    # 中性常用名字
    NEUTRAL_NAMES = [
        "安", "平", "和", "乐", "欢", "喜", "悦", "爱", "情", "心",
        "思", "想", "念", "忆", "梦", "希", "望", "愿", "祈", "求",
        "天", "地", "人", "神", "仙", "佛", "道", "德", "善", "美",
        "真", "诚", "实", "正", "直", "公", "义", "理", "智", "慧",
        "学", "问", "知", "识", "见", "闻", "听", "说", "读", "写"
    ]

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.PERSON

    @property
    def supported_parameters(self) -> list[str]:
        return ["gender", "length", "surname", "given_name"]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.gender = self.parameters.get("gender", "random").lower()
        self.length = self.parameters.get("length", 2)  # 2 or 3 characters for given name
        self.surname = self.parameters.get("surname", None)  # 指定姓氏
        self.given_name = self.parameters.get("given_name", None)  # 指定名字

    def _generate_surname(self) -> str:
        """生成姓氏"""
        if self.surname:
            return self.surname
        return random.choice(self.SURNAMES)

    def _generate_given_name(self) -> str:
        """生成名字"""
        if self.given_name:
            return self.given_name

        # 选择名字字符池
        if self.gender == "male":
            name_pool = self.MALE_NAMES
        elif self.gender == "female":
            name_pool = self.FEMALE_NAMES
        else:  # random or neutral
            name_pool = self.MALE_NAMES + self.FEMALE_NAMES + self.NEUTRAL_NAMES

        # 生成指定长度的名字
        if self.length == 1:
            return random.choice(name_pool)
        elif self.length == 2:
            return random.choice(name_pool) + random.choice(name_pool)
        elif self.length == 3:
            return (
                random.choice(name_pool)
                + random.choice(name_pool)
                + random.choice(name_pool)
            )
        else:
            # 默认2个字
            return random.choice(name_pool) + random.choice(name_pool)

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成中文姓名"""
        surname = self._generate_surname()
        given_name = self._generate_given_name()
        return surname + given_name

    def validate(self, data: str) -> bool:
        """验证中文姓名格式"""
        import re
        
        # 检查是否为中文字符
        pattern = r"^[\u4e00-\u9fff]{2,4}$"
        return bool(re.match(pattern, data))
