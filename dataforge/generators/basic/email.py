"""
邮箱生成器
"""
import random
import re
from typing import Optional, Dict, Any, List
from ...core.generator import ValidatedDataGenerator, GeneratorConfig, GenerationContext, GeneratorType
from ...core.factory import register_generator


class EmailGenerator(ValidatedDataGenerator[str]):
    """邮箱地址生成器"""
    
    # 常用邮箱域名
    COMMON_DOMAINS = [
        'qq.com', '163.com', '126.com', 'sina.com', 'sohu.com',
        'gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com',
        'foxmail.com', '139.com', 'aliyun.com', 'vip.qq.com'
    ]
    
    # 企业邮箱域名
    ENTERPRISE_DOMAINS = [
        'company.com', 'corp.com.cn', 'group.com',
        'tech.com', 'business.cn', 'enterprise.net'
    ]
    
    # 用户名常用字符
    USERNAME_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'
    USERNAME_SPECIAL_CHARS = '._-'
    
    def _setup(self) -> None:
        self.domains = self.parameters.get('domains', None)  # 自定义域名列表
        self.username_length = self.parameters.get('username_length', (3, 15))  # 用户名长度范围
        self.valid = self.parameters.get('valid', True)
        self.allow_special_chars = self.parameters.get('allow_special_chars', True)
        self.email_type = self.parameters.get('type', 'COMMON')  # COMMON, ENTERPRISE, MIXED
        self.include_numbers = self.parameters.get('include_numbers', True)
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始邮箱地址"""
        if not self.valid:
            return self._generate_invalid_email()
        
        # 1. 生成用户名
        username = self._generate_username(context)
        
        # 2. 选择域名
        domain = self._select_domain()
        
        return f"{username}@{domain}"
    
    def _generate_username(self, context: Optional[GenerationContext] = None) -> str:
        """生成用户名部分"""
        # 如果上下文中有姓名，尝试基于姓名生成
        if context and hasattr(context, 'get_generated_data'):
            name_data = context.get_generated_data('name')
            if name_data:
                return self._generate_username_from_name(name_data)
        
        # 随机生成用户名
        return self._generate_random_username()
    
    def _generate_username_from_name(self, name: str) -> str:
        """基于姓名生成用户名"""
        # 提取拼音部分 (如果有括号)
        if '(' in name and ')' in name:
            # 格式如: "张三 (zhang san)"
            pinyin_part = name.split('(')[1].split(')')[0].strip()
            # 移除空格，生成用户名
            username = pinyin_part.replace(' ', '').lower()
        else:
            # 直接使用中文名称转换
            username = self._chinese_to_pinyin_simple(name)
        
        # 添加数字后缀
        if self.include_numbers and random.random() < 0.6:
            username += str(random.randint(1, 9999))
        
        # 确保长度在范围内
        min_len, max_len = self.username_length
        if len(username) < min_len:
            username += ''.join(random.choices(self.USERNAME_CHARS, k=min_len - len(username)))
        elif len(username) > max_len:
            username = username[:max_len]
        
        return username
    
    def _chinese_to_pinyin_simple(self, chinese_name: str) -> str:
        """简单的中文名转拼音（使用映射表）"""
        # 这里使用简化的映射，实际项目中可以使用 pypinyin 库
        chinese_pinyin_map = {
            '张': 'zhang', '王': 'wang', '李': 'li', '赵': 'zhao', '刘': 'liu',
            '陈': 'chen', '杨': 'yang', '黄': 'huang', '周': 'zhou', '吴': 'wu',
            '徐': 'xu', '孙': 'sun', '胡': 'hu', '朱': 'zhu', '高': 'gao',
            '林': 'lin', '何': 'he', '郭': 'guo', '马': 'ma', '罗': 'luo',
            '三': 'san', '四': 'si', '五': 'wu', '六': 'liu', '七': 'qi',
            '八': 'ba', '九': 'jiu', '十': 'shi', '一': 'yi', '二': 'er',
            '明': 'ming', '华': 'hua', '强': 'qiang', '军': 'jun', '伟': 'wei',
            '磊': 'lei', '洋': 'yang', '勇': 'yong', '刚': 'gang', '峰': 'feng'
        }
        
        result = ''
        for char in chinese_name:
            if char in chinese_pinyin_map:
                result += chinese_pinyin_map[char]
            else:
                # 未知字符用随机字母替代
                result += random.choice('abcdefghijklmnopqrstuvwxyz')
        
        return result or 'user'
    
    def _generate_random_username(self) -> str:
        """生成随机用户名"""
        min_len, max_len = self.username_length
        length = random.randint(min_len, max_len)
        
        # 生成基础用户名
        username = ''.join(random.choices(self.USERNAME_CHARS, k=length))
        
        # 可能添加特殊字符
        if self.allow_special_chars and random.random() < 0.3:
            # 在随机位置插入特殊字符
            insert_pos = random.randint(1, len(username) - 1)
            special_char = random.choice(self.USERNAME_SPECIAL_CHARS)
            username = username[:insert_pos] + special_char + username[insert_pos:]
        
        return username
    
    def _select_domain(self) -> str:
        """选择邮箱域名"""
        if self.domains:
            # 使用自定义域名
            if isinstance(self.domains, list):
                return random.choice(self.domains)
            else:
                return str(self.domains)
        
        # 根据类型选择域名
        if self.email_type == 'ENTERPRISE':
            return random.choice(self.ENTERPRISE_DOMAINS)
        elif self.email_type == 'MIXED':
            all_domains = self.COMMON_DOMAINS + self.ENTERPRISE_DOMAINS
            return random.choice(all_domains)
        else:  # COMMON
            return random.choice(self.COMMON_DOMAINS)
    
    def _generate_invalid_email(self) -> str:
        """生成无效邮箱"""
        invalid_type = random.choice([
            'no_at', 'multiple_at', 'no_domain', 'invalid_chars', 
            'starts_with_special', 'ends_with_special', 'consecutive_dots'
        ])
        
        if invalid_type == 'no_at':
            # 缺少@符号
            username = self._generate_random_username()
            domain = self._select_domain()
            return f"{username}{domain}"
        
        elif invalid_type == 'multiple_at':
            # 多个@符号
            username = self._generate_random_username()
            domain = self._select_domain()
            return f"{username}@extra@{domain}"
        
        elif invalid_type == 'no_domain':
            # 只有用户名部分
            username = self._generate_random_username()
            return f"{username}@"
        
        elif invalid_type == 'invalid_chars':
            # 包含无效字符
            username = self._generate_random_username()
            domain = self._select_domain()
            invalid_char = random.choice('!#$%&*+=?^`{|}~')
            return f"{username}{invalid_char}@{domain}"
        
        elif invalid_type == 'starts_with_special':
            # 以特殊字符开头
            username = self._generate_random_username()
            domain = self._select_domain()
            return f".{username}@{domain}"
        
        elif invalid_type == 'ends_with_special':
            # 以特殊字符结尾
            username = self._generate_random_username()
            domain = self._select_domain()
            return f"{username}.@{domain}"
        
        else:  # consecutive_dots
            # 连续的点
            username = self._generate_random_username()
            domain = self._select_domain()
            return f"{username}..test@{domain}"
    
    def validate(self, data: str) -> bool:
        """校验邮箱地址"""
        if not isinstance(data, str):
            return False
        
        # 基本的邮箱格式验证
        email_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?@[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, data):
            return False
        
        # 检查长度
        if len(data) > 254:  # RFC 5321 限制
            return False
        
        # 检查用户名部分长度
        username = data.split('@')[0]
        if len(username) > 64:  # RFC 5321 限制
            return False
        
        return True
    
    def get_domain_info(self, email: str) -> Dict[str, str]:
        """获取邮箱域名信息"""
        if not self.validate(email):
            return {'domain': 'UNKNOWN', 'type': 'INVALID'}
        
        domain = email.split('@')[1].lower()
        
        if domain in self.COMMON_DOMAINS:
            return {'domain': domain, 'type': 'COMMON', 'category': '个人邮箱'}
        elif domain in self.ENTERPRISE_DOMAINS:
            return {'domain': domain, 'type': 'ENTERPRISE', 'category': '企业邮箱'}
        else:
            return {'domain': domain, 'type': 'CUSTOM', 'category': '自定义域名'}
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC_INFO
    
    @property
    def supported_parameters(self) -> List[str]:
        return [
            'domains', 'username_length', 'valid', 'allow_special_chars', 
            'type', 'include_numbers'
        ]


@register_generator('email', ['邮箱', 'mail'])
class ChineseEmailGenerator(EmailGenerator):
    """中国邮箱生成器注册版本"""
    pass