"""
联系/通信类生成器
"""
import random
import re
import string
from typing import Optional, Dict, Any, List
from ...core.generator import ValidatedDataGenerator, GeneratorConfig, GenerationContext, GeneratorType
from ...core.factory import register_generator


class VerificationCodeGenerator(ValidatedDataGenerator[str]):
    """验证码生成器"""
    
    def _setup(self) -> None:
        self.length = self.parameters.get('length', 6)
        self.code_type = self.parameters.get('type', 'NUMERIC')  # NUMERIC, ALPHA, ALPHANUMERIC, MIXED
        self.exclude_similar = self.parameters.get('exclude_similar', True)  # 排除易混淆字符
        self.case_sensitive = self.parameters.get('case_sensitive', False)
        self.custom_charset = self.parameters.get('custom_charset', None)
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始验证码"""
        chars = self._get_character_set()
        
        if not chars:
            raise ValueError("字符集为空，无法生成验证码")
        
        return ''.join(random.choices(chars, k=self.length))
    
    def _get_character_set(self) -> List[str]:
        """获取字符集"""
        if self.custom_charset:
            return list(self.custom_charset)
        
        if self.code_type.upper() == 'NUMERIC':
            chars = list('0123456789')
        elif self.code_type.upper() == 'ALPHA':
            chars = list(string.ascii_uppercase if not self.case_sensitive else string.ascii_letters)
        elif self.code_type.upper() == 'ALPHANUMERIC':
            base = string.ascii_uppercase + string.digits
            if self.case_sensitive:
                base = string.ascii_letters + string.digits
            chars = list(base)
        elif self.code_type.upper() == 'MIXED':
            chars = list(string.ascii_letters + string.digits + '!@#$%^&*')
        else:
            chars = list(string.digits)
        
        # 排除易混淆字符
        if self.exclude_similar:
            similar_chars = set('0O1lI')
            chars = [c for c in chars if c not in similar_chars]
        
        return chars
    
    def validate(self, data: str) -> bool:
        """校验验证码"""
        if not isinstance(data, str):
            return False
        
        if len(data) != self.length:
            return False
        
        valid_chars = set(self._get_character_set())
        return all(c in valid_chars for c in data)
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.CONTACT
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['length', 'type', 'exclude_similar', 'case_sensitive', 'custom_charset']


class FaxNumberGenerator(ValidatedDataGenerator[str]):
    """传真号码生成器"""
    
    def _setup(self) -> None:
        self.country_code = self.parameters.get('country_code', '+86')
        self.area_code = self.parameters.get('area_code', None)
        self.format_style = self.parameters.get('format', 'STANDARD')  # STANDARD, COMPACT, INTERNATIONAL
        self.include_extension = self.parameters.get('include_extension', False)
        
        # 中国主要城市区号
        self.china_area_codes = [
            '010',  # 北京
            '021',  # 上海
            '020',  # 广州
            '0755', # 深圳
            '025',  # 南京
            '0571', # 杭州
            '027',  # 武汉
            '028',  # 成都
            '023',  # 重庆
            '024',  # 沈阳
            '0531', # 济南
            '029',  # 西安
        ]
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始传真号码"""
        # 选择区号
        if self.area_code:
            area = self.area_code
        else:
            area = random.choice(self.china_area_codes)
        
        # 生成本地号码
        if area.startswith('0'):
            # 去掉前导0
            area_digits = area[1:]
            if len(area_digits) == 2:  # 如010 -> 10
                local_length = 8
            else:  # 如0755 -> 755
                local_length = 7
        else:
            area_digits = area
            local_length = 7
        
        # 生成本地号码（第一位不能是0）
        first_digit = random.randint(2, 9)
        remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(local_length - 1)])
        local_number = str(first_digit) + remaining_digits
        
        # 组合号码
        if self.format_style.upper() == 'INTERNATIONAL':
            fax_number = f"{self.country_code} {area_digits} {local_number}"
        elif self.format_style.upper() == 'COMPACT':
            fax_number = f"{area_digits}{local_number}"
        else:  # STANDARD
            fax_number = f"{area}-{local_number}"
        
        # 添加分机号
        if self.include_extension:
            extension = random.randint(100, 9999)
            fax_number += f" ext.{extension}"
        
        return fax_number
    
    def validate(self, data: str) -> bool:
        """校验传真号码"""
        if not isinstance(data, str):
            return False
        
        # 移除分机号部分
        main_number = data.split(' ext.')[0]
        
        # 基本格式检查
        if self.format_style.upper() == 'INTERNATIONAL':
            pattern = r'^\+\d{1,3}\s\d{2,4}\s\d{6,8}$'
        elif self.format_style.upper() == 'COMPACT':
            pattern = r'^\d{9,12}$'
        else:  # STANDARD
            pattern = r'^\d{2,4}-\d{6,8}$'
        
        return bool(re.match(pattern, main_number))
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.CONTACT
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['country_code', 'area_code', 'format', 'include_extension']


class URLGenerator(ValidatedDataGenerator[str]):
    """URL生成器"""
    
    def _setup(self) -> None:
        self.scheme = self.parameters.get('scheme', 'https')  # http, https, ftp
        self.domain_type = self.parameters.get('domain_type', 'RANDOM')  # RANDOM, REAL, CUSTOM
        self.custom_domains = self.parameters.get('domains', None)
        self.include_path = self.parameters.get('include_path', True)
        self.include_query = self.parameters.get('include_query', False)
        self.include_fragment = self.parameters.get('include_fragment', False)
        self.path_depth = self.parameters.get('path_depth', (1, 3))
        
        # 真实域名列表
        self.real_domains = [
            'example.com', 'test.com', 'demo.org', 'sample.net',
            'github.com', 'stackoverflow.com', 'wikipedia.org',
            'google.com', 'microsoft.com', 'amazon.com', 'apple.com'
        ]
        
        # TLD列表
        self.tlds = ['.com', '.org', '.net', '.cn', '.com.cn', '.gov', '.edu']
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始URL"""
        # 构建基础URL
        domain = self._generate_domain()
        url = f"{self.scheme}://{domain}"
        
        # 添加路径
        if self.include_path:
            path = self._generate_path()
            url += path
        
        # 添加查询参数
        if self.include_query:
            query = self._generate_query_string()
            url += f"?{query}"
        
        # 添加片段标识符
        if self.include_fragment:
            fragment = self._generate_fragment()
            url += f"#{fragment}"
        
        return url
    
    def _generate_domain(self) -> str:
        """生成域名"""
        if self.custom_domains:
            return random.choice(self.custom_domains)
        elif self.domain_type.upper() == 'REAL':
            return random.choice(self.real_domains)
        else:  # RANDOM
            # 生成随机域名
            subdomain = ''
            if random.random() < 0.3:  # 30%概率有子域名
                subdomain = self._generate_word() + '.'
            
            domain_name = self._generate_word()
            tld = random.choice(self.tlds)
            
            return f"{subdomain}{domain_name}{tld}"
    
    def _generate_word(self, length_range=(3, 8)) -> str:
        """生成单词"""
        length = random.randint(*length_range)
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    
    def _generate_path(self) -> str:
        """生成路径"""
        depth = random.randint(*self.path_depth)
        path_parts = []
        
        for _ in range(depth):
            part = self._generate_word()
            path_parts.append(part)
        
        # 可能添加文件扩展名
        if random.random() < 0.4:
            extensions = ['.html', '.php', '.jsp', '.asp', '.json', '.xml']
            path_parts[-1] += random.choice(extensions)
        
        return '/' + '/'.join(path_parts)
    
    def _generate_query_string(self) -> str:
        """生成查询字符串"""
        param_count = random.randint(1, 4)
        params = []
        
        for _ in range(param_count):
            key = self._generate_word((2, 6))
            value = self._generate_word((2, 10))
            params.append(f"{key}={value}")
        
        return '&'.join(params)
    
    def _generate_fragment(self) -> str:
        """生成片段标识符"""
        return self._generate_word((3, 8))
    
    def validate(self, data: str) -> bool:
        """校验URL"""
        if not isinstance(data, str):
            return False
        
        # 基本URL格式验证
        url_pattern = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
        return bool(re.match(url_pattern, data))
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.CONTACT
    
    @property
    def supported_parameters(self) -> List[str]:
        return [
            'scheme', 'domain_type', 'domains', 'include_path', 
            'include_query', 'include_fragment', 'path_depth'
        ]


class FilePathGenerator(ValidatedDataGenerator[str]):
    """文件路径生成器"""
    
    def _setup(self) -> None:
        self.path_type = self.parameters.get('type', 'UNIX')  # UNIX, WINDOWS, MIXED
        self.absolute = self.parameters.get('absolute', True)
        self.depth = self.parameters.get('depth', (1, 4))
        self.include_filename = self.parameters.get('include_filename', True)
        self.file_extensions = self.parameters.get('extensions', ['.txt', '.log', '.json', '.xml', '.csv'])
        self.common_dirs = self.parameters.get('common_dirs', None)
        
        # 常见目录名
        self.default_common_dirs = [
            'home', 'usr', 'var', 'etc', 'tmp', 'opt', 'bin', 'lib',
            'Documents', 'Downloads', 'Pictures', 'Videos', 'Music',
            'projects', 'src', 'test', 'data', 'logs', 'config'
        ]
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始文件路径"""
        path_parts = []
        
        # 根据系统类型设置分隔符
        if self.path_type.upper() == 'WINDOWS':
            separator = '\\'
            if self.absolute:
                path_parts.append('C:')
        else:  # UNIX or MIXED
            separator = '/'
            if self.absolute:
                path_parts.append('')  # 开头的空字符串会产生前导/
        
        # 生成目录结构
        dir_depth = random.randint(*self.depth)
        dirs = self.common_dirs or self.default_common_dirs
        
        for _ in range(dir_depth):
            if random.random() < 0.7:  # 70%概率使用常见目录名
                dir_name = random.choice(dirs)
            else:  # 30%概率生成随机目录名
                dir_name = self._generate_name()
            path_parts.append(dir_name)
        
        # 添加文件名
        if self.include_filename:
            filename = self._generate_filename()
            path_parts.append(filename)
        
        return separator.join(path_parts)
    
    def _generate_name(self, length_range=(3, 10)) -> str:
        """生成名称"""
        length = random.randint(*length_range)
        chars = string.ascii_lowercase + string.digits + '_-'
        return ''.join(random.choices(chars, k=length))
    
    def _generate_filename(self) -> str:
        """生成文件名"""
        base_name = self._generate_name((3, 15))
        
        if self.file_extensions and random.random() < 0.8:  # 80%概率有扩展名
            extension = random.choice(self.file_extensions)
            return base_name + extension
        
        return base_name
    
    def validate(self, data: str) -> bool:
        """校验文件路径"""
        if not isinstance(data, str):
            return False
        
        # 基本路径格式检查
        if self.path_type.upper() == 'WINDOWS':
            # Windows路径检查
            if self.absolute and not (data.startswith('C:\\') or data.startswith('D:\\')):
                return False
            # 检查非法字符
            illegal_chars = '<>:"|?*'
            if any(char in data for char in illegal_chars):
                return False
        else:  # UNIX
            if self.absolute and not data.startswith('/'):
                return False
        
        return len(data) > 0
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.CONTACT
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['type', 'absolute', 'depth', 'include_filename', 'extensions', 'common_dirs']


class MimeTypeGenerator(ValidatedDataGenerator[str]):
    """MIME类型生成器"""
    
    def _setup(self) -> None:
        self.category = self.parameters.get('category', 'ALL')  # ALL, TEXT, IMAGE, AUDIO, VIDEO, APPLICATION
        self.common_only = self.parameters.get('common_only', True)
        
        # MIME类型定义
        self.mime_types = {
            'TEXT': [
                'text/plain', 'text/html', 'text/css', 'text/javascript',
                'text/csv', 'text/xml', 'text/markdown', 'text/yaml'
            ],
            'IMAGE': [
                'image/jpeg', 'image/png', 'image/gif', 'image/bmp',
                'image/webp', 'image/svg+xml', 'image/tiff', 'image/ico'
            ],
            'AUDIO': [
                'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/aac',
                'audio/flac', 'audio/mp4', 'audio/webm'
            ],
            'VIDEO': [
                'video/mp4', 'video/avi', 'video/quicktime', 'video/webm',
                'video/ogg', 'video/3gpp', 'video/x-msvideo'
            ],
            'APPLICATION': [
                'application/json', 'application/xml', 'application/pdf',
                'application/zip', 'application/gzip', 'application/octet-stream',
                'application/x-www-form-urlencoded', 'application/javascript',
                'application/msword', 'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ]
        }
        
        # 常见MIME类型
        self.common_mime_types = [
            'text/html', 'text/plain', 'text/css', 'text/javascript',
            'image/jpeg', 'image/png', 'image/gif',
            'application/json', 'application/pdf', 'application/zip',
            'video/mp4', 'audio/mpeg'
        ]
    
    def _generate_raw(self, context: Optional[GenerationContext] = None) -> str:
        """生成原始MIME类型"""
        if self.common_only:
            return random.choice(self.common_mime_types)
        
        if self.category.upper() == 'ALL':
            # 从所有类别中选择
            all_types = []
            for types in self.mime_types.values():
                all_types.extend(types)
            return random.choice(all_types)
        else:
            # 从指定类别中选择
            category_types = self.mime_types.get(self.category.upper(), self.common_mime_types)
            return random.choice(category_types)
    
    def validate(self, data: str) -> bool:
        """校验MIME类型"""
        if not isinstance(data, str):
            return False
        
        # 基本MIME类型格式检查
        mime_pattern = r'^[a-zA-Z][a-zA-Z0-9][a-zA-Z0-9\!\#\$\&\-\^]*\/[a-zA-Z0-9][a-zA-Z0-9\!\#\$\&\-\^]*$'
        return bool(re.match(mime_pattern, data))
    
    def get_category(self, mime_type: str) -> str:
        """获取MIME类型的类别"""
        for category, types in self.mime_types.items():
            if mime_type in types:
                return category
        return 'UNKNOWN'
    
    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.CONTACT
    
    @property
    def supported_parameters(self) -> List[str]:
        return ['category', 'common_only']


@register_generator('verification_code', ['验证码', 'captcha'])
class GenericVerificationCodeGenerator(VerificationCodeGenerator):
    """通用验证码生成器注册版本"""
    pass


@register_generator('fax', ['传真'])
class GenericFaxNumberGenerator(FaxNumberGenerator):
    """通用传真号码生成器注册版本"""
    pass


@register_generator('url', ['网址'])
class GenericURLGenerator(URLGenerator):
    """通用URL生成器注册版本"""
    pass


@register_generator('file_path', ['path', '文件路径'])
class GenericFilePathGenerator(FilePathGenerator):
    """通用文件路径生成器注册版本"""
    pass


@register_generator('mime_type', ['content_type'])
class GenericMimeTypeGenerator(MimeTypeGenerator):
    """通用MIME类型生成器注册版本"""
    pass