"""
中文文本生成器
支持生成不同长度、主题领域的中文文本内容
"""

import secrets

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorType,
)


@register_generator("chinese_text")
class ChineseTextGenerator(DataGenerator[str]):
    """中文文本生成器 - 支持不同长度、主题领域"""

    def _setup(self) -> None:
        self.theme = self.parameters.get("theme", "general")
        self.text_type = self.parameters.get("text_type", "sentence")
        self.min_length = self.parameters.get("min_length", 30)
        self.max_length = self.parameters.get("max_length", 100)

    def _generate_raw(self, context: GenerationContext | None = None) -> str:
        # 主题词库
        themes = {
            "general": {
                "words": [
                    "数据",
                    "系统",
                    "技术",
                    "信息",
                    "平台",
                    "服务",
                    "用户",
                    "功能",
                    "应用",
                    "方案",
                ],
                "sentences": [
                    "这是一个测试句子。",
                    "数据生成器正在运行。",
                    "系统功能正常可用。",
                    "信息处理完成。",
                    "平台服务稳定可靠。",
                ],
                "paragraphs": [
                    "这是一个测试段落，用于生成中文文本内容。该段落包含多个句子，可以测试长文本生成功能。",
                    "数据生成器是现代软件开发中的重要工具，可以帮助开发者快速创建测试数据，提高开发效率。",
                ],
            },
            "business": {
                "words": [
                    "合同",
                    "项目",
                    "投资",
                    "收益",
                    "成本",
                    "利润",
                    "市场",
                    "客户",
                    "产品",
                    "服务",
                ],
                "sentences": [
                    "项目投资回报率达到预期目标。",
                    "成本控制在合理范围内。",
                    "客户满意度持续提升。",
                    "市场份额稳步增长。",
                    "产品竞争力不断增强。",
                ],
                "paragraphs": [
                    "本季度项目投资回报率显著提升，成本控制措施取得良好效果。客户满意度调查显示，整体服务水平得到市场认可。",
                    "通过持续的市场分析和产品优化，公司在目标市场的份额稳步提升，产品竞争力得到显著增强。",
                ],
            },
            "technical": {
                "words": [
                    "算法",
                    "架构",
                    "接口",
                    "模块",
                    "组件",
                    "配置",
                    "部署",
                    "监控",
                    "日志",
                    "性能",
                ],
                "sentences": [
                    "算法优化提升系统性能。",
                    "架构设计满足扩展需求。",
                    "接口调用响应时间正常。",
                    "模块功能测试通过验证。",
                    "组件配置参数设置正确。",
                ],
                "paragraphs": [
                    "通过算法优化和架构调整，系统整体性能得到显著提升。接口设计遵循RESTful规范，确保良好的扩展性和兼容性。",
                    "模块化设计使得系统组件可以独立部署和维护，配置管理工具确保环境一致性，监控日志提供完整的运行状态信息。",
                ],
            },
        }

        # 根据主题和文本类型选择内容
        theme_data = themes.get(self.theme, themes["general"])

        if self.text_type == "word":
            words = theme_data["words"]
            return secrets.choice(words)
        elif self.text_type == "sentence":
            sentences = theme_data["sentences"]
            # 生成更长的句子，组合多个句子
            num_sentences = secrets.randbelow(3) + 4  # 4-6个句子
            selected = [secrets.choice(sentences) for _ in range(num_sentences)]
            return "".join(selected)
        elif self.text_type == "paragraph":
            paragraphs = theme_data["paragraphs"]
            # 生成更长的段落，组合多个段落
            num_paragraphs = secrets.randbelow(2) + 3  # 3-4个段落
            selected = [secrets.choice(paragraphs) for _ in range(num_paragraphs)]
            return "".join(selected)
        else:
            # 默认生成随机文本
            sentences = theme_data["sentences"]
            num_sentences = secrets.randbelow(4) + 5  # 5-8个句子
            selected = [secrets.choice(sentences) for _ in range(num_sentences)]
            return "".join(selected)

    def validate(self, data: str) -> bool:
        return isinstance(data, str) and len(data) > 0

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.TEXT

    @property
    def supported_parameters(self) -> list[str]:
        return ["theme", "text_type", "min_length", "max_length"]

    def generate(self, context: GenerationContext | None = None) -> str:
        return self._generate_raw(context)

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)


@register_generator("english_text")
class EnglishTextGenerator(DataGenerator[str]):
    """英文文本生成器 - 支持lorem ipsum变体、专业术语"""

    def _setup(self) -> None:
        self.theme = self.parameters.get("theme", "lorem")
        self.text_type = self.parameters.get("text_type", "sentence")
        self.min_length = self.parameters.get("min_length", 5)
        self.max_length = self.parameters.get("max_length", 50)

    def _generate_raw(self, context: GenerationContext | None = None) -> str:
        # 英文语料库
        themes = {
            "lorem": {
                "words": [
                    "lorem",
                    "ipsum",
                    "dolor",
                    "sit",
                    "amet",
                    "consectetur",
                    "adipiscing",
                    "elit",
                ],
                "sentences": [
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                    "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
                ],
            },
            "general": {
                "words": [
                    "data",
                    "system",
                    "application",
                    "technology",
                    "platform",
                    "service",
                    "user",
                    "function",
                ],
                "sentences": [
                    "This is a test sentence for English text generation.",
                    "The data generator is working properly.",
                    "System functionality has been verified successfully.",
                ],
            },
        }

        theme_data = themes.get(self.theme, themes["lorem"])

        if self.text_type == "word":
            words = theme_data["words"]
            return secrets.choice(words)
        elif self.text_type == "sentence":
            sentences = theme_data["sentences"]
            return secrets.choice(sentences)
        else:
            # 生成随机英文文本
            length = (
                secrets.randbelow(self.max_length - self.min_length + 1)
                + self.min_length
            )
            words = [
                "test",
                "data",
                "generate",
                "system",
                "application",
                "verify",
                "function",
            ]
            return " ".join(secrets.choice(words) for _ in range(length // 4 + 1))

    def validate(self, data: str) -> bool:
        return isinstance(data, str) and len(data) > 0

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.TEXT

    @property
    def supported_parameters(self) -> list[str]:
        return ["theme", "text_type", "min_length", "max_length"]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)


# 已通过装饰器完成注册
