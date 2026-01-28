"""
DataForge Web相关生成器示例
演示URL、HTTP头等Web相关生成器的使用方法
"""

import json
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from dataforge import GeneratorConfig, default_factory


def basic_usage():
    """基础用法示例"""
    print("1. 基础用法示例")
    print("=" * 60)

    # URL生成器
    print("\nURL生成器 (url):")
    config = GeneratorConfig("url", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        url = generator.generate()
        print(f"  示例 {i+1}: {url}")

    # HTTP头生成器
    print("\nHTTP头生成器 (http_header):")
    config = GeneratorConfig("http_header", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        headers = generator.generate()
        user_agent = headers.get("User-Agent", "N/A")
        print(f"  示例 {i+1}: {user_agent[:80]}...")

    # 域名生成器
    print("\n域名生成器 (domain):")
    config = GeneratorConfig("domain", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        domain = generator.generate()
        print(f"  示例 {i+1}: {domain}")


def parameter_configuration():
    """参数配置示例"""
    print("\n\n2. 参数配置示例")
    print("=" * 60)

    # URL - 不同协议
    print("\nURL生成器 - 协议配置:")
    protocols = [
        {"protocol": "https"},
        {"protocol": "http"},
        {"protocol": ["http", "https"]},
        {"include_path": False},
        {"include_query": True},
        {"include_fragment": True}
    ]
    for i, params in enumerate(protocols, 1):
        config = GeneratorConfig("url", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")

    # HTTP头 - 不同浏览器
    print("\nHTTP头生成器 - 浏览器配置:")
    browsers = [
        {"browser": "chrome"},
        {"browser": "firefox"},
        {"browser": "safari"},
        {"browser": "edge"},
        {"include_cookies": True}
    ]
    for i, params in enumerate(browsers, 1):
        config = GeneratorConfig("http_header", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        user_agent = result.get("User-Agent", "N/A")
        print(f"  配置 {i}: {params}")
        print(f"    User-Agent: {user_agent[:80]}...")

    # 域名 - 不同类型
    print("\n域名生成器 - 类型配置:")
    domain_types = [
        {"domain_type": "com"},
        {"domain_type": "country"},
        {"subdomain_levels": (2, 3)},
        {"use_real_words": False},
        {"custom_tlds": [".tech", ".app", ".dev"]}
    ]
    for i, params in enumerate(domain_types, 1):
        config = GeneratorConfig("domain", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")


def batch_generation():
    """批量生成示例"""
    print("\n\n3. 批量生成示例")
    print("=" * 60)

    print("\n批量生成Web资源:")

    # 生成URL
    url_config = GeneratorConfig("url", parameters={
        "include_path": True,
        "include_query": True,
        "path_length": (2, 4)
    })
    url_gen = default_factory.create_generator(url_config)

    # 生成域名
    domain_config = GeneratorConfig("domain", parameters={
        "domain_type": "com",
        "subdomain_levels": (0, 2)
    })
    domain_gen = default_factory.create_generator(domain_config)

    # 生成HTTP头
    header_config = GeneratorConfig("http_header", parameters={
        "browser": "chrome",
        "include_cookies": True
    })
    header_gen = default_factory.create_generator(header_config)

    # 生成5个Web资源
    web_resources = []
    for i in range(5):
        resource = {
            "url": url_gen.generate(),
            "domain": domain_gen.generate(),
            "headers": header_gen.generate(),
            "resource_type": "web_page"
        }
        web_resources.append(resource)

    # 打印资源信息
    print("-" * 100)
    print(f"{'URL':<50} | {'域名':<25} | {'类型'}")
    print("-" * 100)
    for resource in web_resources:
        url = resource['url'][:47] + "..." if len(resource['url']) > 50 else resource['url']
        domain = resource['domain'][:22] + "..." if len(resource['domain']) > 25 else resource['domain']
        resource_type = resource['resource_type']
        print(f"{url:<50} | {domain:<25} | {resource_type}")
    print("-" * 100)


def validation_examples():
    """数据验证示例"""
    print("\n\n4. 数据验证示例")
    print("=" * 60)

    # URL验证
    print("\nURL格式验证:")
    config = GeneratorConfig("url", parameters={"include_query": True})
    generator = default_factory.create_generator(config)

    for i in range(3):
        url = generator.generate()
        is_valid = generator.validate(url)
        print(f"  {i+1}. {url}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")

    # HTTP头验证
    print("\nHTTP头验证:")
    config = GeneratorConfig("http_header", parameters={"include_cookies": True})
    generator = default_factory.create_generator(config)

    for i in range(3):
        headers = generator.generate()
        is_valid = generator.validate(headers)
        print(f"  {i+1}. 包含 {len(headers)} 个头的HTTP头")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     包含Cookie: {'✅ 是' if 'Cookie' in headers else '❌ 否'}")

    # 域名验证
    print("\n域名格式验证:")
    config = GeneratorConfig("domain", parameters={"subdomain_levels": (1, 2)})
    generator = default_factory.create_generator(config)

    for i in range(3):
        domain = generator.generate()
        is_valid = generator.validate(domain)
        print(f"  {i+1}. {domain}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     子域名数量: {domain.count('.')}")


def error_handling():
    """错误处理示例"""
    print("\n\n5. 错误处理示例")
    print("=" * 60)

    # 处理无效的协议
    print("\n处理无效的协议:")
    try:
        config = GeneratorConfig("url", parameters={"protocol": "invalid"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的URL: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效协议错误: {type(e).__name__}")

    # 处理无效的域名类型
    print("\n处理无效的域名类型:")
    try:
        config = GeneratorConfig("domain", parameters={"domain_type": "invalid"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的域名: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效域名类型错误: {type(e).__name__}")

    # 处理无效的浏览器类型
    print("\n处理无效的浏览器类型:")
    try:
        config = GeneratorConfig("http_header", parameters={"browser": "invalid"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的HTTP头: 包含 {len(result)} 个字段")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效浏览器类型错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print("\n\n6. 最佳实践示例")
    print("=" * 60)

    # 实践1: 生成完整的网站信息
    print("\n实践1: 生成完整的网站信息")
    website_info = {
        "url": default_factory.create_generator(
            GeneratorConfig("url", parameters={
                "protocol": "https",
                "include_path": True,
                "include_query": True,
                "path_style": "RESTFUL"
            })
        ).generate(),
        "domain": default_factory.create_generator(
            GeneratorConfig("domain", parameters={
                "domain_type": "com",
                "subdomain_levels": (1, 2),
                "use_real_words": True
            })
        ).generate(),
        "headers": default_factory.create_generator(
            GeneratorConfig("http_header", parameters={
                "browser": "chrome",
                "include_cookies": True,
                "include_auth": False
            })
        ).generate(),
        "ssl_info": {
            "protocol": "TLSv1.3",
            "cipher_suite": "TLS_AES_256_GCM_SHA384",
            "certificate": "self-signed"
        }
    }

    print("  网站信息:")
    for key, value in website_info.items():
        if isinstance(value, dict):
            print(f"    {key}:")
            for sub_key, sub_value in value.items():
                print(f"      {sub_key}: {sub_value}")
        else:
            display_value = str(value)[:80] + "..." if len(str(value)) > 80 else str(value)
            print(f"    {key}: {display_value}")

    # 实践2: 批量导出Web数据
    print("\n实践2: 批量导出Web数据 (JSON格式)")
    web_data = []

    for i in range(3):
        web_item = {
            "request": {
                "url": default_factory.create_generator(
                    GeneratorConfig("url", parameters={
                        "protocol": "https",
                        "include_path": True,
                        "include_query": True
                    })
                ).generate(),
                "method": "GET",
                "headers": default_factory.create_generator(
                    GeneratorConfig("http_header", parameters={
                        "browser": "chrome",
                        "include_cookies": True
                    })
                ).generate()
            },
            "response": {
                "status_code": 200,
                "content_type": "text/html; charset=utf-8",
                "server": "nginx/1.18.0"
            }
        }
        web_data.append(web_item)

    print("  JSON格式输出:")
    print(json.dumps(web_data, ensure_ascii=False, indent=2))


def web_crawling_demo():
    """Web爬虫演示"""
    print("\n\n7. Web爬虫演示")
    print("=" * 60)

    print("\n模拟爬虫请求信息:")

    # 生成多个URL
    url_config = GeneratorConfig("url", parameters={
        "protocol": "https",
        "path_style": "REALISTIC",
        "include_query": True
    })
    url_gen = default_factory.create_generator(url_config)

    # 生成不同的User-Agent
    ua_config = GeneratorConfig("http_header", parameters={
        "browser": "chrome",
        "min_headers": 5,
        "max_headers": 8
    })
    ua_gen = default_factory.create_generator(ua_config)

    # 生成爬虫请求
    crawl_requests = []
    for i in range(5):
        request = {
            "url": url_gen.generate(),
            "headers": ua_gen.generate(),
            "method": "GET",
            "delay": 1 + (i * 0.5),  # 模拟延迟
            "retry_count": 0
        }
        crawl_requests.append(request)

    print("  爬虫请求列表:")
    for i, req in enumerate(crawl_requests, 1):
        print(f"    请求 {i}:")
        print(f"      URL: {req['url']}")
        print(f"      方法: {req['method']}")
        print(f"      延迟: {req['delay']}秒")
        user_agent = req['headers'].get('User-Agent', 'N/A')
        print(f"      User-Agent: {user_agent[:60]}...")
        print()


def main():
    """主函数"""
    print("🎯 DataForge Web相关生成器示例")
    print("本示例展示了Web相关生成器的各种使用方法\n")

    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        web_crawling_demo()

        print("\n" + "=" * 60)
        print("✅ 示例演示完成")
        print("=" * 60)
        print("🎉 所有Web相关生成器示例已成功运行！")

        print("\n📚 相关文档:")
        print("  • 查看 examples/network/ip_demo.py 了解IP地址相关生成器")
        print("  • 查看 examples/network/device_demo.py 了解设备标识相关生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")

    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
