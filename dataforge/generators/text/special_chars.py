"""
特殊字符和Unicode符号生成器
支持生成各种特殊字符、emoji、Unicode符号等
"""

import random  # TODO: Convert to secrets
import secrets
from ...core.types import (
GeneratorType
)
from typing import Optional

from dataforge.core.factory import register_generator
from dataforge.core.generator import (

# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   secrets.randbelow(b - a + 1) + a → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary


# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review
# Conversion patterns:
#   secrets.randbelow(b - a + 1) + a → secrets.randbelow(b - a + 1) + a
#   random.randrange(n) → secrets.randbelow(n)
#   For statistical distributions, consider if CSPRNG is necessary

    DataGenerator,
    GenerationContext,
    GeneratorType,
)


class SpecialCharGenerator(DataGenerator[str]):
    """特殊字符生成器"""

    # Unicode特殊字符集合
    SPECIAL_CHARS: dict[str, list[str]] = {
        "math": [
            "∞",
            "∑",
            "∏",
            "∫",
            "∂",
            "∇",
            "√",
            "∛",
            "∜",
            "∠",
            "∡",
            "∢",
            "∥",
            "∦",
            "⊥",
            "⊤",
            "±",
            "∓",
            "×",
            "÷",
            "≠",
            "≤",
            "≥",
            "≈",
            "≡",
            "≪",
            "≫",
            "⊕",
            "⊗",
            "⊖",
            "⊘",
            "⊙",
            "∧",
            "∨",
            "∩",
            "∪",
            "⊂",
            "⊃",
            "⊆",
            "⊇",
            "∈",
            "∉",
            "∋",
            "∌",
            "∅",
            "ℕ",
            "ℤ",
            "ℚ",
            "ℝ",
            "ℂ",
            "ℍ",
            "ℙ",
            "ℵ",
            "ℶ",
            "ℷ",
            "ℸ",
            "⅓",
            "⅔",
            "⅕",
            "⅖",
            "⅗",
            "⅘",
            "⅙",
            "⅚",
        ],
        "currency": [
            "¥",
            "$",
            "€",
            "£",
            "₤",
            "₣",
            "₧",
            "₨",
            "₩",
            "₪",
            "₫",
            "₭",
            "₮",
            "₯",
            "₰",
            "₱",
            "₲",
            "₳",
            "₴",
            "₵",
            "₶",
            "₷",
            "₸",
            "₹",
            "₺",
            "₻",
            "₼",
            "₽",
            "₾",
            "₿",
            "¤",
            "¢",
        ],
        "arrows": [
            "←",
            "↑",
            "→",
            "↓",
            "↔",
            "↕",
            "↖",
            "↗",
            "↘",
            "↙",
            "↚",
            "↛",
            "↜",
            "↝",
            "↞",
            "↟",
            "↠",
            "↡",
            "↢",
            "↣",
            "↤",
            "↥",
            "↦",
            "↧",
            "↨",
            "↩",
            "↪",
            "↫",
            "↬",
            "↭",
            "↮",
            "↯",
            "⇐",
            "⇑",
            "⇒",
            "⇓",
            "⇔",
            "⇕",
            "⇖",
            "⇗",
            "⇘",
            "⇙",
            "⇚",
            "⇛",
            "⇜",
            "⇝",
            "⇞",
            "⇟",
        ],
        "geometric": [
            "■",
            "□",
            "▢",
            "▣",
            "▤",
            "▥",
            "▦",
            "▧",
            "▨",
            "▩",
            "▪",
            "▫",
            "▬",
            "▭",
            "▮",
            "▯",
            "▰",
            "▱",
            "▲",
            "△",
            "▴",
            "▵",
            "▶",
            "▷",
            "▸",
            "▹",
            "►",
            "▻",
            "▼",
            "▽",
            "▾",
            "▿",
            "◀",
            "◁",
            "◂",
            "◃",
            "◄",
            "◅",
            "◆",
            "◇",
            "◈",
            "◉",
            "◊",
            "○",
            "◌",
            "◍",
            "◎",
            "●",
        ],
        "punctuation": [
            "¡",
            "¿",
            "‽",
            "⁇",
            "⁈",
            "⁉",
            "․",
            "‥",
            "…",
            "‧",
            "‰",
            "‱",
            "‴",
            "‵",
            "‶",
            "‷",
            "‸",
            "‹",
            "›",
            "※",
            "‼",
            "‽",
            "‾",
            "‿",
            "⁀",
            "⁁",
            "⁂",
            "⁃",
            "⁄",
            "⁅",
            "⁆",
            "⁇",
        ],
    }

    # Emoji表情集合
    EMOJI_CATEGORIES: dict[str, list[str]] = {
        "faces": [
            "😀",
            "😃",
            "😄",
            "😁",
            "😆",
            "😅",
            "😂",
            "🤣",
            "😊",
            "😇",
            "🙂",
            "🙃",
            "😉",
            "😌",
            "😍",
            "🥰",
            "😘",
            "😗",
            "😙",
            "😚",
            "😋",
            "😛",
            "😝",
            "😜",
            "🤪",
            "🤨",
            "🧐",
            "🤓",
            "😎",
            "🤩",
            "🥳",
            "😏",
            "😒",
            "😞",
            "😔",
            "😟",
            "😕",
            "🙁",
            "☹️",
            "😣",
            "😖",
            "😫",
            "😩",
            "🥺",
            "😢",
            "😭",
            "😤",
            "😠",
        ],
        "animals": [
            "🐶",
            "🐱",
            "🐭",
            "🐹",
            "🐰",
            "🦊",
            "🐻",
            "🐼",
            "🐨",
            "🐯",
            "🦁",
            "🐮",
            "🐷",
            "🐸",
            "🐵",
            "🙈",
            "🙉",
            "🙊",
            "🐒",
            "🐔",
            "🐧",
            "🐦",
            "🐤",
            "🐣",
            "🐥",
            "🦆",
            "🦅",
            "🦉",
            "🐺",
            "🐗",
            "🐴",
            "🦄",
            "🐝",
            "🐛",
            "🦋",
            "🐌",
            "🐞",
            "🐜",
            "🦗",
            "🕷️",
            "🦂",
            "🐢",
            "🐍",
            "🦎",
            "🦖",
            "🦕",
            "🐙",
            "🦑",
        ],
        "food": [
            "🍏",
            "🍎",
            "🍐",
            "🍊",
            "🍋",
            "🍌",
            "🍉",
            "🍇",
            "🍓",
            "🍈",
            "🍒",
            "🍑",
            "🥭",
            "🍍",
            "🥥",
            "🥝",
            "🍅",
            "🍆",
            "🥑",
            "🥦",
            "🥒",
            "🍄",
            "🥕",
            "🌽",
            "🌶️",
            "🥔",
            "🍠",
            "🥐",
            "🥖",
            "🍞",
            "🥨",
            "🧀",
            "🥚",
            "🍳",
            "🥓",
            "🥩",
            "🍔",
            "🍟",
            "🍕",
            "🌭",
            "🥪",
            "🌮",
            "🌯",
            "🥗",
            "🥘",
            "🥙",
            "🍝",
            "🍜",
        ],
        "symbols": [
            "❤️",
            "🧡",
            "💛",
            "💚",
            "💙",
            "💜",
            "🖤",
            "🤍",
            "🤎",
            "💔",
            "❣️",
            "💕",
            "💞",
            "💓",
            "💗",
            "💖",
            "💘",
            "💝",
            "💟",
            "☮️",
            "✝️",
            "☪️",
            "🕉️",
            "☸️",
            "✡️",
            "🔯",
            "🕎",
            "☯️",
            "☦️",
            "🛐",
            "⛎",
            "♈",
            "♉",
            "♊",
            "♋",
            "♌",
            "♍",
            "♎",
            "♏",
            "♐",
            "♑",
            "♒",
            "♓",
            "🆔",
            "⚛️",
            "🉑",
            "☢️",
            "☣️",
        ],
        "objects": [
            "⌚",
            "📱",
            "📲",
            "💻",
            "⌨️",
            "🖥️",
            "🖨️",
            "🖱️",
            "🖲️",
            "🕹️",
            "💽",
            "💾",
            "💿",
            "📀",
            "📼",
            "📷",
            "📸",
            "📹",
            "🎥",
            "📽️",
            "🎞️",
            "📞",
            "☎️",
            "📟",
            "📠",
            "📺",
            "📻",
            "🎙️",
            "🎚️",
            "🎛️",
            "⏱️",
            "⏲️",
            "⏰",
            "🕰️",
            "⌛",
            "⏳",
            "📡",
            "🔋",
            "🔌",
            "💡",
            "🔦",
            "🕯️",
            "🗑️",
            "🛢️",
            "💸",
            "💵",
            "💴",
            "💶",
        ],
    }

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.TEXT

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "category",
            "count",
            "include_emoji",
            "include_special",
            "unicode_range",
            "custom_chars",
        ]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.category: str = self.parameters.get("category", "symbols")
        self.count: int = self.parameters.get("count", 1)
        self.include_emoji: bool = self.parameters.get("include_emoji", True)
        self.include_special: bool = self.parameters.get("include_special", True)
        self.unicode_range: Optional[str] = self.parameters.get("unicode_range", None)
        self.custom_chars: Optional[list[str]] = self.parameters.get("custom_chars", None)

    def _get_special_chars(self) -> list[str]:
        """获取特殊字符集合"""
        if self.custom_chars:
            return list(self.custom_chars)

        chars = []

        if self.include_special and self.category in self.SPECIAL_CHARS:
            chars.extend(self.SPECIAL_CHARS[self.category])

        if self.include_emoji:
            # 添加emoji
            for emoji_list in self.EMOJI_CATEGORIES.values():
                chars.extend(emoji_list)

        if not chars:
            # 默认返回常用特殊字符
            chars = ["★", "☆", "●", "○", "■", "□", "▲", "△", "♠", "♣", "♥", "♦"]

        return chars

    def generate(self, context: Optional[GenerationContext] = None) -> str:
        """生成特殊字符"""
        chars = self._get_special_chars()

        if not chars:
            return "★"

        if self.count == 1:
            return secrets.choice(chars)
        else:
            return "".join(random.choices(chars, k=min(self.count, 100)))

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始特殊字符数据"""
        return self.generate(context)

    def validate(self, data: str) -> bool:
        """验证生成的特殊字符"""
        return isinstance(data, str) and len(data.strip()) > 0

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self.generate(context)



class UnicodeSymbolGenerator(DataGenerator[str]):
    """Unicode符号生成器"""

    # Unicode范围定义
    UNICODE_RANGES: dict[str, tuple[int, int]] = {
        "basic_latin": (0x0020, 0x007F),  # 基本拉丁字符
        "latin_supplement": (0x0080, 0x00FF),  # 拉丁字符补充
        "cyrillic": (0x0400, 0x04FF),  # 西里尔字符
        "greek": (0x0370, 0x03FF),  # 希腊字符
        "arabic": (0x0600, 0x06FF),  # 阿拉伯字符
        "hindi": (0x0900, 0x097F),  # 天城文
        "cjk_symbols": (0x3000, 0x303F),  # CJK符号
        "hiragana": (0x3040, 0x309F),  # 平假名
        "katakana": (0x30A0, 0x30FF),  # 片假名
        "cjk_unified": (0x4E00, 0x9FFF),  # CJK统一汉字
        "emoticons": (0x1F600, 0x1F64F),  # 表情符号
        "symbols": (0x2600, 0x26FF),  # 杂项符号
        "dingbats": (0x2700, 0x27BF),  # 装饰符号
        "arrows": (0x2190, 0x21FF),  # 箭头符号
        "math_operators": (0x2200, 0x22FF),  # 数学运算符
    }

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.TEXT

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "unicode_range",
            "character_count",
            "exclude_ascii",
            "include_control",
            "custom_range_start",
            "custom_range_end",
        ]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.unicode_range: str = self.parameters.get("unicode_range", "symbols")
        self.character_count: int = self.parameters.get("character_count", 1)
        self.exclude_ascii: bool = self.parameters.get("exclude_ascii", True)
        self.include_control: bool = self.parameters.get("include_control", False)
        self.custom_range_start: Optional[int] = self.parameters.get("custom_range_start", None)
        self.custom_range_end: Optional[int] = self.parameters.get("custom_range_end", None)

    def _get_unicode_range(self) -> tuple[int, int]:
        """获取Unicode范围"""
        if self.custom_range_start is not None and self.custom_range_end is not None:
            return (self.custom_range_start, self.custom_range_end)

        if (
            isinstance(self.unicode_range, str)
            and self.unicode_range in self.UNICODE_RANGES
        ):
            return self.UNICODE_RANGES[self.unicode_range]

        # 默认返回符号范围
        return self.UNICODE_RANGES["symbols"]

    def _is_valid_char(self, char_code: int) -> bool:
        """检查字符是否有效"""
        if not self.include_control and char_code < 32:
            return False

        if self.exclude_ascii and 32 <= char_code <= 126:
            return False

        return True

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成Unicode符号"""
        start, end = self._get_unicode_range()

        # 确保范围合理
        start = max(32, start)
        end = min(0x10FFFF, end)

        if start >= end:
            return "★"

        chars = []
        for _ in range(min(self.character_count, 100)):
            char_code = secrets.randbelow(end - start + 1) + start

            # 确保字符有效
            attempts = 0
            while not self._is_valid_char(char_code) and attempts < 10:
                char_code = secrets.randbelow(end - start + 1) + start
                attempts += 1

            if attempts < 10:
                try:
                    chars.append(chr(char_code))
                except ValueError:
                    chars.append("★")

        return "".join(chars)

    def validate(self, data: str) -> bool:
        """验证生成的Unicode符号"""
        return isinstance(data, str) and len(data.strip()) > 0

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项 - TODO: Implement generation logic"""
        return self._generate_raw(context)



# 注册生成器
register_generator("special_chars")(SpecialCharGenerator)
register_generator("unicode_symbols")(UnicodeSymbolGenerator)
