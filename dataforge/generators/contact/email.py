"""
电子邮件生成器
"""

import re
import secrets
import string

from ...core.factory import register_generator
from ...core.generator import (
    DataGenerator,
    GenerationContext,
)
from ...core.protocols import Validator
from ...core.types import GeneratorType
from ...resources.name_config_loader import load_pinyin_map


class EmailValidator(Validator):
    """RFC 5321标准邮箱验证器"""

    def validate(self, data: str) -> bool:
        """校验邮箱地址"""
        if not isinstance(data, str):
            return False

        # 支持中文字符的邮箱格式验证
        email_pattern = r"^[\w\u4e00-\u9fff]([a-zA-Z0-9\u4e00-\u9fff._-]*[a-zA-Z0-9\u4e00-\u9fff])?@[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$"

        if not re.match(email_pattern, data):
            return False

        # 检查长度 (RFC 5321 限制)
        if len(data) > 254:
            return False

        # 检查用户名部分长度
        username = data.split("@")[0]
        if len(username) > 64:
            return False

        return True

    @property
    def error_message(self) -> str:
        return "Invalid email address format (RFC 5321)"


class EmailGenerator(DataGenerator[str]):
    """电子邮件生成器，生成符合中国用户习惯的电子邮件地址"""

    def _setup(self) -> None:
        """初始化生成器参数"""
        self.domain_type = self.parameters.get(
            "domain_type", "RANDOM"
        )  # RANDOM, REAL, ENTERPRISE, CUSTOM
        # 支持domains和custom_domains两种参数名
        self.custom_domains = self.parameters.get(
            "domains", None
        ) or self.parameters.get("custom_domains", None)
        self.include_subdomain = self.parameters.get("include_subdomain", True)
        self.username_length = self.parameters.get("username_length", (5, 10))
        self.include_chinese = self.parameters.get(
            "include_chinese", False
        )  # 是否包含中文字符
        self.valid = self.parameters.get("valid", True)  # 是否生成有效邮箱
        self.allow_name_based = self.parameters.get(
            "allow_name_based", True
        )  # 是否允许基于姓名生成

        # 初始化验证器
        self.validator = EmailValidator()

        # 真实域名列表 - 包括更多中国常用邮箱服务
        self.real_domains = [
            # 中国常用邮箱
            "163.com",
            "qq.com",
            "sina.com",
            "sohu.com",
            "yahoo.cn",
            "126.com",
            "yeah.net",
            "vip.163.com",
            "vip.qq.com",
            "vip.sina.com",
            "vip.sohu.com",
            "vip.yahoo.cn",
            "139.com",  # 中国移动邮箱
            "foxmail.com",  # 腾讯企业邮箱
            "aliyun.com",  # 阿里云邮箱
            # 国际邮箱
            "gmail.com",
            "hotmail.com",
            "outlook.com",
            "icloud.com",
            "example.com",
            "test.com",
            "demo.org",
            "sample.net",
        ]

        # 企业邮箱域名
        self.enterprise_domains = [
            "company.com",
            "corp.com.cn",
            "group.com",
            "tech.com",
            "business.cn",
            "enterprise.net",
        ]

        # 常见顶级域名
        self.tlds = [".com", ".org", ".net", ".cn", ".com.cn", ".gov", ".edu"]

    def _generate_raw(self, context: GenerationContext | None = None) -> str:
        """生成原始电子邮件地址"""
        # 如果要生成无效邮箱
        if not self.valid:
            return self._generate_invalid_email()

        # 生成用户名
        username = self._generate_username(context)

        # 生成域名
        domain = self._generate_domain()

        return f"{username}@{domain}"

    def _generate_username(self, context: GenerationContext | None = None) -> str:
        """生成用户名"""
        # 如果允许基于姓名生成且上下文中有姓名数据
        if self.allow_name_based and context and context.related_data:
            name_data = context.related_data.get("name")
            if name_data:
                return self._generate_username_from_name(name_data)

        # 随机生成用户名
        length = (
            secrets.randbelow(self.username_length[1] - self.username_length[0] + 1)
            + self.username_length[0]
        )

        # 基础字符集
        chars = string.ascii_lowercase + string.digits + "_-."

        # 如果允许中文字符，则添加常用中文字符
        if self.include_chinese:
            chars += "张王李赵钱孙杨周吴徐黄赵朱秦尤许沈周胡何郭林罗史钟曹严华蒋韩冯马侯龙万罗梁宋郑谢韩邓萧曹袁邓许韩邓萧叶潘杜戴夏钟汪田任姜范方石姚韩冯叶潘杜戴夏钟汪田任姜范方石姚"

        # 确保首字符不是特殊字符
        if self.include_chinese and secrets.randbelow(2):  # 50%概率使用中文用户名
            chinese_chars = "张王李赵钱孙杨周吴徐黄赵朱秦尤许沈周胡何郭林罗史钟曹严华蒋韩冯马侯龙万罗梁宋郑谢韩邓萧曹袁邓许韩邓萧叶潘杜戴夏钟汪田任姜范方石姚"
            first_char = secrets.choice(chinese_chars)
            rest_chars = "".join(secrets.choice(chars) for _ in range(length - 1))
            username = first_char + rest_chars
        else:
            first_char = secrets.choice(string.ascii_lowercase + string.digits)
            rest_chars = "".join(secrets.choice(chars) for _ in range(length - 1))
            username = first_char + rest_chars

        # 确保用户名不以特殊字符结尾（修复验证失败问题）
        while username and username[-1] in "._-":
            username = username[:-1]
            if not username:
                # 如果变成空字符串，生成一个简单的用户名
                username = secrets.choice(string.ascii_lowercase) + secrets.choice(
                    string.digits
                )

        return username

    def _generate_username_from_name(self, name: str) -> str:
        """基于姓名生成用户名"""
        # 提取拼音部分 (如果有括号)
        if "(" in name and ")" in name:
            # 格式如: "张三 (zhang san)"
            pinyin_part = name.split("(")[1].split(")")[0].strip()
            # 移除空格，生成用户名
            username = pinyin_part.replace(" ", "").lower()
        else:
            # 直接使用中文名称转换
            username = self._chinese_to_pinyin_simple(name)

        # 添加数字后缀
        if secrets.randbelow(10) < 6:  # 60%概率
            username += str(secrets.randbelow(10000))

        # 确保长度在范围内
        min_len, max_len = self.username_length
        if len(username) < min_len:
            username += "".join(
                secrets.choice(string.ascii_lowercase + string.digits)
                for _ in range(min_len - len(username))
            )
        elif len(username) > max_len:
            username = username[:max_len]

        return username

    def _chinese_to_pinyin_simple(self, chinese_name: str) -> str:
        """简单的中文名转拼音（使用映射表）"""
        maps = load_pinyin_map()
        surname_map = maps["surname"]
        given_map = maps["given_char"]

        if not chinese_name:
            return "user"

        result = ""
        # 简单拆分：首字当姓，其余当名
        surname_char = chinese_name[0]
        given_chars = chinese_name[1:]

        if surname_char in surname_map:
            result += surname_map[surname_char]
        else:
            result += secrets.choice(string.ascii_lowercase)

        for char in given_chars:
            if char in given_map:
                result += given_map[char]
            elif char.strip():
                result += secrets.choice(string.ascii_lowercase)

        return result or "user"

    def _generate_domain(self) -> str:
        """生成域名"""
        if self.custom_domains:
            if isinstance(self.custom_domains, list):
                domain = secrets.choice(self.custom_domains)
            else:
                # 如果是单个字符串域名，直接返回
                domain = str(self.custom_domains)
        elif self.domain_type.upper() == "ENTERPRISE":
            domain = secrets.choice(self.enterprise_domains)
        elif self.domain_type.upper() == "REAL":
            domain = secrets.choice(self.real_domains)
        else:  # RANDOM
            domain = self._generate_word()
            tld = secrets.choice(self.tlds)

            # 添加子域名的概率
            if self.include_subdomain and secrets.randbelow(10) < 3:  # 30%概率
                subdomain = self._generate_word()
                domain = f"{subdomain}.{domain}{tld}"
            else:
                domain = f"{domain}{tld}"

        return domain

    def _generate_word(self, length_range=(3, 8)) -> str:
        """生成域名部分的随机单词"""
        length = (
            secrets.randbelow(length_range[1] - length_range[0] + 1) + length_range[0]
        )
        return "".join(secrets.choice(string.ascii_lowercase) for _ in range(length))

    def _generate_invalid_email(self) -> str:
        """生成无效邮箱"""
        invalid_type = secrets.choice(
            [
                "no_at",
                "multiple_at",
                "no_domain",
                "invalid_chars",
                "starts_with_special",
                "ends_with_special",
                "consecutive_dots",
            ]
        )

        # 对于无效邮箱，我们使用固定的测试域名
        test_domain = "test.com"
        username = self._generate_word((5, 10))

        if invalid_type == "no_at":
            # 缺少@符号
            return f"{username}{test_domain}"

        elif invalid_type == "multiple_at":
            # 多个@符号
            return f"{username}@extra@{test_domain}"

        elif invalid_type == "no_domain":
            # 只有用户名部分
            return f"{username}@"

        elif invalid_type == "invalid_chars":
            # 包含无效字符
            invalid_char = secrets.choice("!#$%&*+=?^`{|}~")
            return f"{username}{invalid_char}@{test_domain}"

        elif invalid_type == "starts_with_special":
            # 以特殊字符开头
            return f".{username}@{test_domain}"

        elif invalid_type == "ends_with_special":
            # 以特殊字符结尾
            return f"{username}.@{test_domain}"

        else:  # consecutive_dots
            # 连续的点
            return f"{username}..test@{test_domain}"

    def validate(self, data: str) -> bool:
        """校验电子邮件地址"""
        return self.validator.validate(data)

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.CONTACT

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "domain_type",
            "domains",
            "custom_domains",
            "include_subdomain",
            "username_length",
            "include_chinese",
            "valid",
            "allow_name_based",
        ]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项 - TODO: Implement generation logic"""
        return self._generate_raw(context)


@register_generator("email", ["e-mail", "电子邮件", "邮箱"])
class GenericEmailGenerator(EmailGenerator):
    """通用电子邮件生成器注册版本"""

    pass
