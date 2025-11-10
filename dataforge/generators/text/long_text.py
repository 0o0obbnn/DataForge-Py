from typing import Optional
import secrets

from ...core.generator import GenerationContext

"""
长文本生成器
支持生成各种长度的文本内容，包括文章、段落等
"""


from dataforge.core.factory import register_generator
from dataforge.core.generator import DataGenerator, GeneratorType


class LongTextGenerator(DataGenerator[str]):
    """长文本生成器"""

    # 预定义文本模板
    TEXT_TEMPLATES = {
        "lorem_ipsum": [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
            "Duis aute irure dolor in reprehenderit in voluptate velit esse.",
            "Excepteur sint occaecat cupidatat non proident, sunt in culpa.",
        ],
        "technical": [
            "The system architecture follows microservices pattern with containerized deployment.",
            "API endpoints are secured with OAuth 2.0 authentication and rate limiting.",
            "Database schema optimization improves query performance and reduces latency.",
            "Continuous integration pipeline ensures code quality and automated testing.",
            "Cloud-native infrastructure provides scalability and high availability.",
        ],
        "business": [
            "Market analysis indicates strong growth potential in the digital transformation sector.",
            "Quarterly financial reports show consistent revenue growth and profitability.",
            "Strategic partnerships enable expansion into new geographic markets.",
            "Customer satisfaction metrics demonstrate improved service quality and engagement.",
            "Operational efficiency initiatives reduce costs while maintaining quality standards.",
        ],
        "news": [
            "Breaking news: Major breakthrough in renewable energy technology announced today.",
            "Economic indicators suggest stable growth despite global market uncertainties.",
            "Government policy changes impact industry regulations and compliance requirements.",
            "Technology conference showcases innovative solutions for digital transformation.",
            "Environmental initiatives gain traction as sustainability becomes priority.",
        ],
        "chinese": [
            "人工智能技术正在快速发展，为各行各业带来革命性的变革。",
            "数字化转型成为企业提升竞争力的关键战略和核心能力。",
            "云计算平台提供弹性扩展的计算资源和存储解决方案。",
            "大数据分析帮助企业从海量数据中提取有价值的商业洞察。",
            "网络安全防护体系确保信息系统和数据资产的安全可靠。",
        ],
    }

    # 连接词和过渡短语
    CONNECTORS = [
        "此外，",
        "同时，",
        "另一方面，",
        "值得注意的是，",
        "重要的是，",
        "然而，",
        "尽管如此，",
        "相比之下，",
        "与此相反，",
        " summarized,",
        " therefore,",
        " which,",
        " overall,",
        " finally,",
        " all,",
    ]

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.TEXT

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "text_type",
            "min_length",
            "max_length",
            "target_length",
            "paragraph_count",
            "sentence_count",
            "include_connectors",
            "connector_density",
            "language",
        ]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.text_type = self.parameters.get("text_type", "lorem_ipsum")
        self.min_length = self.parameters.get("min_length", 100)
        self.max_length = self.parameters.get("max_length", 1000)
        self.target_length = self.parameters.get("target_length", 500)
        self.paragraph_count = self.parameters.get("paragraph_count", 3)
        self.sentence_count = self.parameters.get("sentence_count", 5)
        self.include_connectors = self.parameters.get("include_connectors", True)
        self.connector_density = self.parameters.get("connector_density", 0.3)
        self.language = self.parameters.get("language", "english")

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成长文本"""
        paragraphs = []

        for _ in range(self.paragraph_count):
            paragraph = self._generate_paragraph()
            paragraphs.append(paragraph)

        # 组合段落
        if self.language == "chinese":
            text = "\\n\\n".join(paragraphs)
        else:
            text = "\\n\\n".join(paragraphs)

        # 确保文本长度在指定范围内
        text = self._adjust_text_length(text)

        return text

    def _generate_paragraph(self) -> str:
        """生成单个段落"""
        sentences = []
        templates = self.TEXT_TEMPLATES.get(
            self.text_type, self.TEXT_TEMPLATES["lorem_ipsum"]
        )

        for _ in range(self.sentence_count):
            sentence = secrets.choice(templates)

            # 随机添加连接词
            if self.include_connectors and (secrets.randbelow(1000000) / 1000000) < self.connector_density:
                connector = secrets.choice(self.CONNECTORS)
                sentence = connector + sentence

            sentences.append(sentence)

        # 组合句子成段落
        if self.language == "chinese":
            return "。".join(sentences) + "。"
        else:
            return ". ".join(sentences) + "."

    def _adjust_text_length(self, text: str) -> str:
        """调整文本长度到目标范围"""
        current_length = len(text)

        if current_length < self.min_length:
            # 文本太短，需要扩展
            while len(text) < self.min_length:
                additional_paragraph = self._generate_paragraph()
                text += "\\n\\n" + additional_paragraph
        elif current_length > self.max_length:
            # 文本太长，需要截断
            text = text[: self.max_length]
            # 确保截断后以完整句子结束
            if self.language == "chinese":
                last_period = text.rfind("。")
                if last_period != -1:
                    text = text[: last_period + 1]
            else:
                last_period = text.rfind(".")
                if last_period != -1:
                    text = text[: last_period + 1]

        return text

    def validate(self, data: str) -> bool:
        """验证长文本格式"""
        if not data or not isinstance(data, str):
            return False

        # 检查长度限制
        if len(data) < self.min_length or len(data) > self.max_length:
            return False

        # 检查段落结构
        paragraphs = data.split("\\n\\n")
        if len(paragraphs) < 1:
            return False

        # 检查每个段落是否包含完整的句子
        for paragraph in paragraphs:
            if self.language == "chinese":
                if not paragraph.endswith("。"):
                    return False
            else:
                if not paragraph.endswith("."):
                    return False

        return True

    def get_text_stats(self, data: str) -> dict:
        """获取文本统计信息"""
        paragraphs = data.split("\\n\\n")
        sentences = []

        for para in paragraphs:
            if self.language == "chinese":
                para_sentences = para.split("。")
            else:
                para_sentences = para.split(". ")
            sentences.extend([s for s in para_sentences if s])

        words = []
        for sentence in sentences:
            if self.language == "chinese":
                words.extend(list(sentence))
            else:
                words.extend(sentence.split())

        stats = {
            "total_length": len(data),
            "paragraph_count": len(paragraphs),
            "sentence_count": len(sentences),
            "word_count": len(words),
            "char_count": len(data.replace(" ", "").replace("\\n", "")),
            "avg_sentence_length": len(words) / len(sentences) if sentences else 0,
            "avg_paragraph_length": len(sentences) / len(paragraphs)
            if paragraphs
            else 0,
            "text_type": self.text_type,
            "language": self.language,
        }

        return stats



    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)
# 注册通用生成器
@register_generator("long_text")
class GenericLongTextGenerator(LongTextGenerator):
    """通用长文本生成器"""

    pass

