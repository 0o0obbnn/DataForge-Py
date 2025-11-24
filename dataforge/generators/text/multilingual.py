"""
多语言文本生成器
支持生成中文、英文、日文等多种语言的文本内容
"""

import secrets
from typing import Optional

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorType,
)


class MultilingualTextGenerator(DataGenerator):
    """多语言文本生成器"""

    # 预定义语言语料库
    LANGUAGE_CORPORA = {
        "chinese": {
            "words": [
                "数据",
                "生成",
                "测试",
                "开发",
                "系统",
                "应用",
                "程序",
                "网络",
                "安全",
                "性能",
                "用户",
                "界面",
                "功能",
                "模块",
                "接口",
                "服务",
                "平台",
                "框架",
                "算法",
                "结构",
            ],
            "sentences": [
                "这是一个测试句子用于数据生成。",
                "多语言文本生成器可以创建各种语言的文本内容。",
                "数据伪造工具用于测试和开发目的。",
                "系统需要支持多种语言的数据生成。",
                "这是一个中文测试句子，用于验证文本生成功能。",
            ],
        },
        "english": {
            "words": [
                "data",
                "generate",
                "test",
                "develop",
                "system",
                "application",
                "program",
                "network",
                "security",
                "performance",
                "user",
                "interface",
                "function",
                "module",
                "interface",
                "service",
                "platform",
                "framework",
                "algorithm",
                "structure",
            ],
            "sentences": [
                "This is a test sentence for data generation.",
                "Multilingual text generator can create text in various languages.",
                "Data forge tool is used for testing and development purposes.",
                "The system needs to support multilingual data generation.",
                "This is an English test sentence to verify text generation functionality.",
            ],
        },
        "japanese": {
            "words": [
                "データ",
                "生成",
                "テスト",
                "開発",
                "システム",
                "アプリケーション",
                "プログラム",
                "ネットワーク",
                "セキュリティ",
                "パフォーマンス",
                "ユーザー",
                "インターフェース",
                "機能",
                "モジュール",
                "インターフェース",
                "サービス",
                "プラットフォーム",
                "フレームワーク",
                "アルゴリズム",
                "構造",
            ],
            "sentences": [
                "これはデータ生成のためのテスト文です。",
                "多言語テキストジェネレーターは様々な言語のテキストを作成できます。",
                "データ偽造ツールはテストと開発の目的で使用されます。",
                "システムは多言語データ生成をサポートする必要があります。",
                "これはテキスト生成機能を検証するための日本語のテスト文です。",
            ],
        },
        "korean": {
            "words": [
                "데이터",
                "생성",
                "테스트",
                "개발",
                "시스템",
                "애플리케이션",
                "프로그램",
                "네트워크",
                "보안",
                "성능",
                "사용자",
                "인터페이스",
                "기능",
                "모듈",
                "인터페이스",
                "서비스",
                "플랫폼",
                "프레임워크",
                "알고리즘",
                "구조",
            ],
            "sentences": [
                "이것은 데이터 생성을 위한 테스트 문장입니다.",
                "다국어 텍스트 생성기는 다양한 언어의 텍스트를 생성할 수 있습니다.",
                "데이터 위조 도구는 테스트 및 개발 목적으로 사용됩니다.",
                "시스템은 다국어 데이터 생성을 지원해야 합니다.",
                "이것은 텍스트 생성 기능을 검증하기 위한 한국어 테스트 문장입니다.",
            ],
        },
        "spanish": {
            "words": [
                "datos",
                "generar",
                "prueba",
                "desarrollar",
                "sistema",
                "aplicación",
                "programa",
                "red",
                "seguridad",
                "rendimiento",
                "usuario",
                "interfaz",
                "función",
                "módulo",
                "interfaz",
                "servicio",
                "plataforma",
                "marco",
                "algoritmo",
                "estructura",
            ],
            "sentences": [
                "Esta es una oración de prueba para la generación de datos.",
                "El generador de texto multilingüe puede crear texto en varios idiomas.",
                "La herramienta de falsificación de datos se utiliza para fines de prueba y desarrollo.",
                "El sistema necesita admitir la generación de datos multilingües.",
                "Esta es una oración de prueba en español para verificar la funcionalidad de generación de texto.",
            ],
        },
    }

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.TEXT

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "language",
            "text_type",
            "min_length",
            "max_length",
            "word_count",
            "sentence_count",
            "include_punctuation",
            "mixed_ratio",
        ]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.language = self.parameters.get("language", "chinese")
        self.text_type = self.parameters.get("text_type", "sentence")
        self.min_length = self.parameters.get("min_length", 10)
        self.max_length = self.parameters.get("max_length", 200)
        self.mixed_ratio = self.parameters.get("mixed_ratio", 0.3)

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成多语言文本"""
        corpus = self.LANGUAGE_CORPORA.get(
            self.language, self.LANGUAGE_CORPORA["chinese"]
        )

        # 生成长度
        target_length = (
            secrets.randbelow(self.max_length - self.min_length + 1) + self.min_length
        )

        if self.text_type == "word":
            # 生成单个词汇
            words = corpus.get("words", ["test"])
            return secrets.choice(words)

        elif self.text_type == "sentence":
            # 生成句子
            sentences = corpus.get("sentences", ["This is a test sentence."])

            if sentences and (secrets.randbelow(1000000) / 1000000) < 0.8:
                return secrets.choice(sentences)
            else:
                # 动态生成句子
                words = corpus.get("words", ["test", "data", "generate"])
                word_count = secrets.randbelow(6) + 3
                sentence_parts = [secrets.choice(words) for _ in range(word_count)]
                sentence = " ".join(sentence_parts)

                # 添加标点
                punctuations = [".", "!", "?", "，", "。", "！", "？"]
                sentence += secrets.choice(punctuations)

                return sentence[: self.max_length]

        else:  # paragraph
            # 生成段落
            sentences = corpus.get("sentences", ["This is a test sentence."])
            words = corpus.get("words", ["test", "data", "generate"])

            result_parts = []
            current_length = 0

            while current_length < target_length:
                # 随机选择生成方式
                if sentences and (secrets.randbelow(1000000) / 1000000) < 0.6:
                    text = secrets.choice(sentences)
                else:
                    # 生成短语
                    word_count = secrets.randbelow(4) + 2
                    phrase_parts = [secrets.choice(words) for _ in range(word_count)]
                    text = " ".join(phrase_parts)

                if result_parts:
                    result_parts.append(" ")
                result_parts.append(text)
                current_length += len(text)

                if current_length >= target_length:
                    break

            result = "".join(result_parts)[:target_length]

            # 确保结果不为空
            if not result.strip():
                result = secrets.choice(sentences) if sentences else "test"

            return result.strip()

    def validate(self, data: str) -> bool:
        """验证文本格式"""
        if not data or not isinstance(data, str):
            return False

        # 检查长度限制
        if len(data) < self.min_length or len(data) > self.max_length:
            return False

        # 根据文本类型进行验证
        if self.text_type == "word":
            # 单词应该不包含空格
            if " " in data:
                return False
        elif self.text_type == "sentence":
            # 句子应该包含有意义的字符
            if len(data.strip()) == 0:
                return False
        elif self.text_type == "paragraph":
            # 段落应该包含多个句子
            if data.count(".") + data.count("!") + data.count("?") < 2:
                return False

        return True

    def get_text_info(self, data: str) -> dict:
        """获取文本信息"""
        info = {
            "language": self.language,
            "text_type": self.text_type,
            "length": len(data),
            "word_count": len(data.split()),
            "sentence_count": data.count(".") + data.count("!") + data.count("?"),
            "contains_mixed_languages": self.language == "mixed",
        }

        # 检测实际语言（简化版）
        detected_langs = []
        for lang, corpus in self.LANGUAGE_CORPORA.items():
            if any(word in data for word in corpus["words"]):
                detected_langs.append(lang)

        if detected_langs:
            info["detected_languages"] = detected_langs

        return info

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self._generate_raw(context)


# 注册通用生成器
@register_generator("multilingual_text")
class GenericMultilingualTextGenerator(MultilingualTextGenerator):
    """通用多语言文本生成器"""

    pass
