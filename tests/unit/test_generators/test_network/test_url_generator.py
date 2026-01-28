"""
URL生成器测试用例
"""

from urllib.parse import urlparse

import pytest

from dataforge.generators.network.url_generator import GenericURLGenerator, URLGenerator


class TestURLGenerator:
    """测试URL生成器"""

    def test_basic_url_generation(self):
        """测试基础URL生成"""
        generator = URLGenerator()
        url = generator.generate()

        assert isinstance(url, str)
        assert url.startswith("https://")
        assert len(url) > 10

    def test_http_protocol(self):
        """测试HTTP协议"""
        generator = URLGenerator(protocol="http")
        url = generator.generate()

        assert url.startswith("http://")

    def test_custom_domain(self):
        """测试自定义域名"""
        generator = URLGenerator(
            custom_base_url="example.com",
            include_path=False,
            include_query=False,
            include_fragment=False,
        )
        url = generator.generate()

        assert url == "https://example.com"

    def test_url_with_path(self):
        """测试带路径的URL"""
        generator = URLGenerator(
            include_path=True,
            include_query=False,
            include_fragment=False,
            path_length=(2, 3),
        )
        url = generator.generate()

        parsed = urlparse(url)
        assert parsed.path.count("/") >= 2

    def test_url_with_query(self):
        """测试带查询参数的URL"""
        generator = URLGenerator(
            include_path=True,
            include_query=True,
            include_fragment=False,
            query_params_count=(2, 3),
        )
        url = generator.generate()

        parsed = urlparse(url)
        assert "?" in url
        assert len(parsed.query) > 0

    def test_url_with_fragment(self):
        """测试带片段标识符的URL"""
        generator = URLGenerator(
            include_path=True, include_fragment=True, include_query=False
        )
        url = generator.generate()

        parsed = urlparse(url)
        assert "#" in url
        assert len(parsed.fragment) > 0

    def test_restful_path_generation(self):
        """测试RESTful路径生成"""
        generator = URLGenerator(path_style="RESTFUL", path_length=(2, 3))
        url = generator.generate()

        parsed = urlparse(url)
        path_parts = [p for p in parsed.path.split("/") if p]
        assert len(path_parts) >= 2

    def test_keyword_query_generation(self):
        """测试关键词查询参数生成"""
        generator = URLGenerator(
            include_query=True, query_style="KEYWORD", query_params_count=(2, 2)
        )
        url = generator.generate()

        parsed = urlparse(url)
        query_params = parsed.query.split("&")
        # 过滤空字符串（当query为空时split会返回['']）
        query_params = [p for p in query_params if p]
        assert len(query_params) == 2

    def test_url_validation(self):
        """测试URL验证"""
        generator = URLGenerator()

        # 有效URL
        assert generator.validate("https://example.com/path")
        assert generator.validate("http://test.com/path?query=value")

        # 无效URL
        assert not generator.validate("invalid-url")
        assert not generator.validate(123)

    def test_url_info_parsing(self):
        """测试URL信息解析"""
        generator = URLGenerator()
        url = "https://example.com/api/users?page=1&limit=10#section"

        info = generator.get_url_info(url)

        assert info["protocol"] == "https"
        assert info["domain"] == "example.com"
        assert info["path"] == "/api/users"
        assert "page" in info["query"]
        assert info["fragment"] == "section"
        assert info["is_secure"] is True

    def test_country_domain_generation(self):
        """测试国家域名生成"""
        generator = URLGenerator(domain_type="COUNTRY", include_path=False)
        url = generator.generate()

        parsed = urlparse(url)
        domain = parsed.netloc
        assert any(domain.endswith(tld) for tld in [".cn", ".us", ".uk", ".de", ".jp"])

    def test_ftp_protocol(self):
        """测试FTP协议"""
        generator = URLGenerator(protocol="ftp")
        url = generator.generate()

        assert url.startswith("ftp://")

    def test_no_encoding_query(self):
        """测试不编码的查询参数"""
        generator = URLGenerator(
            include_query=True, encode_special_chars=False, query_params_count=(1, 1)
        )
        url = generator.generate()

        assert "?" in url


class TestGenericURLGenerator:
    """测试注册的通用URL生成器"""

    def test_basic_functionality(self):
        """测试基本功能"""
        generator = GenericURLGenerator()
        url = generator.generate()

        assert isinstance(url, str)
        assert len(url) > 0


if __name__ == "__main__":
    pytest.main([__file__])
