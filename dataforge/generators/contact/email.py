"""
电子邮箱地址生成器
支持生成各种格式的电子邮箱地址
"""

import random
from typing import Optional

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    GenerationContext,
    GeneratorType,
    ValidatedDataGenerator,
)


@register_generator("email", ["邮箱", "电子邮箱", "邮件地址"])
class EmailGenerator(ValidatedDataGenerator):
    """电子邮箱地址生成器"""

    # 常见邮箱域名
    EMAIL_DOMAINS = {
        "common": [
            "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
            "163.com", "126.com", "qq.com", "sina.com", "sohu.com"
        ],
        "chinese": [
            "qq.com", "163.com", "126.com", "sina.com", "sohu.com",
            "139.com", "wo.com.cn", "189.cn", "21cn.com", "aliyun.com"
        ],
        "international": [
            "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
            "aol.com", "icloud.com", "protonmail.com", "yandex.com"
        ],
        "business": [
            "company.com", "corp.com", "enterprise.com", "business.com",
            "firm.com", "group.com", "inc.com", "ltd.com"
        ],
        "education": [
            "edu.cn", "student.edu.cn", "mail.edu.cn", "university.edu",
            "college.edu", "school.edu", "academic.edu"
        ]
    }

    # 用户名生成元素
    USERNAME_ELEMENTS = {
        "prefixes": [
            "user", "admin", "test", "demo", "info", "contact",
            "support", "service", "hello", "mail", "web", "dev"
        ],
        "words": [
            "cool", "smart", "happy", "lucky", "sunny", "star",
            "dream", "hope", "love", "life", "blue", "red",
            "green", "gold", "silver", "diamond", "pearl", "moon"
        ],
        "numbers": [
            "123", "888", "666", "999", "2023", "2024",
            "88", "66", "99", "100", "520", "1314"
        ],
        "separators": [".", "_", "-", ""]
    }

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.CONTACT

    @property
    def supported_parameters(self) -> list[str]:
        return [
            "domain_type", "custom_domain", "username_style", 
            "include_numbers", "include_dots", "min_length", "max_length"
        ]

    def _setup(self) -> None:
        """配置生成器参数"""
        self.domain_type = self.parameters.get("domain_type", "common")
        self.custom_domain = self.parameters.get("custom_domain", None)
        self.username_style = self.parameters.get("username_style", "mixed")  # simple, mixed, business, random
        self.include_numbers = self.parameters.get("include_numbers", True)
        self.include_dots = self.parameters.get("include_dots", True)
        self.min_length = self.parameters.get("min_length", 5)
        self.max_length = self.parameters.get("max_length", 20)

    def _get_domain(self) -> str:
        """获取邮箱域名"""
        if self.custom_domain:
            return self.custom_domain
        
        domains = self.EMAIL_DOMAINS.get(self.domain_type, self.EMAIL_DOMAINS["common"])
        return random.choice(domains)

    def _generate_simple_username(self) -> str:
        """生成简单用户名"""
        base = random.choice(self.USERNAME_ELEMENTS["words"])
        
        if self.include_numbers and random.random() < 0.7:
            number = random.choice(self.USERNAME_ELEMENTS["numbers"])
            separator = random.choice(self.USERNAME_ELEMENTS["separators"])
            return base + separator + number
        
        return base

    def _generate_mixed_username(self) -> str:
        """生成混合用户名"""
        parts = []
        
        # 添加前缀（可选）
        if random.random() < 0.3:
            parts.append(random.choice(self.USERNAME_ELEMENTS["prefixes"]))
        
        # 添加主要词汇
        parts.append(random.choice(self.USERNAME_ELEMENTS["words"]))
        
        # 添加第二个词汇（可选）
        if random.random() < 0.5:
            parts.append(random.choice(self.USERNAME_ELEMENTS["words"]))
        
        # 添加数字（可选）
        if self.include_numbers and random.random() < 0.8:
            parts.append(random.choice(self.USERNAME_ELEMENTS["numbers"]))
        
        # 选择分隔符
        separator = random.choice(self.USERNAME_ELEMENTS["separators"])
        username = separator.join(parts)
        
        return username

    def _generate_business_username(self) -> str:
        """生成商务用户名"""
        business_prefixes = ["admin", "info", "contact", "support", "service", "sales", "hr", "finance"]
        prefix = random.choice(business_prefixes)
        
        if random.random() < 0.3:
            # 添加部门或数字
            suffix = random.choice(["dept", "team", "01", "02", "03"])
            separator = random.choice([".", "_", "-"])
            return prefix + separator + suffix
        
        return prefix

    def _generate_random_username(self) -> str:
        """生成随机用户名"""
        import string
        
        # 生成随机字母组合
        length = random.randint(self.min_length, min(self.max_length, 15))
        chars = string.ascii_lowercase
        
        username = ''.join(random.choice(chars) for _ in range(length))
        
        # 可能添加数字
        if self.include_numbers and random.random() < 0.6:
            numbers = ''.join(random.choice(string.digits) for _ in range(random.randint(1, 3)))
            username += numbers
        
        return username

    def _generate_username(self) -> str:
        """生成用户名"""
        if self.username_style == "simple":
            username = self._generate_simple_username()
        elif self.username_style == "business":
            username = self._generate_business_username()
        elif self.username_style == "random":
            username = self._generate_random_username()
        else:  # mixed
            username = self._generate_mixed_username()
        
        # 确保长度在范围内
        if len(username) < self.min_length:
            # 如果太短，添加数字
            username += random.choice(self.USERNAME_ELEMENTS["numbers"])
        elif len(username) > self.max_length:
            # 如果太长，截断
            username = username[:self.max_length]
        
        return username.lower()

    def _add_dots_and_formatting(self, username: str) -> str:
        """添加点和格式化"""
        if not self.include_dots or len(username) < 6:
            return username
        
        # 随机在中间添加点
        if random.random() < 0.3:
            mid = len(username) // 2
            # 避免在开头或结尾添加点
            pos = random.randint(2, max(2, len(username) - 2))
            username = username[:pos] + "." + username[pos:]
        
        return username

    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成电子邮箱地址"""
        # 生成用户名
        username = self._generate_username()
        
        # 添加格式化
        username = self._add_dots_and_formatting(username)
        
        # 获取域名
        domain = self._get_domain()
        
        # 组合完整邮箱
        email = f"{username}@{domain}"
        
        return email

    def validate(self, data: str) -> bool:
        """验证电子邮箱格式"""
        import re
        
        # 基本邮箱格式验证
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, data):
            return False
        
        # 检查是否有连续的点
        if '..' in data:
            return False
        
        # 检查是否以点开头或结尾
        username = data.split('@')[0]
        if username.startswith('.') or username.endswith('.'):
            return False
        
        return True

    def generate_batch(self, count: int, **kwargs) -> list[str]:
        """批量生成邮箱地址"""
        # 临时更新参数
        original_params = self.parameters.copy()
        self.parameters.update(kwargs)
        self._setup()
        
        try:
            emails = set()  # 使用集合确保唯一性
            while len(emails) < count:
                email = self.generate()
                emails.add(email)
                
                # 防止无限循环
                if len(emails) > count * 10:  # 如果尝试次数过多，停止
                    break
            
            return list(emails)[:count]
        finally:
            # 恢复原始参数
            self.parameters = original_params
            self._setup()

    def generate_corporate_emails(self, company_domain: str, departments: list[str] = None) -> list[str]:
        """为企业生成邮箱地址"""
        if not departments:
            departments = ["admin", "info", "contact", "support", "sales", "hr", "finance", "marketing"]
        
        emails = []
        for dept in departments:
            # 设置企业邮箱参数
            original_params = self.parameters.copy()
            self.parameters.update({
                "custom_domain": company_domain,
                "username_style": "business"
            })
            self._setup()
            
            try:
                # 生成部门邮箱
                email = f"{dept}@{company_domain}"
                emails.append(email)
                
                # 生成变体
                if random.random() < 0.5:
                    variant = f"{dept}.service@{company_domain}"
                    emails.append(variant)
                    
            finally:
                self.parameters = original_params
                self._setup()
        
        return emails
