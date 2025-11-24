#!/usr/bin/env python3
"""
DataForge 网络生成器示例 - IP地址相关

这个文件展示了DataForge项目中网络相关生成器的使用方法，包括：
- IP地址 (ipaddress)
- MAC地址 (mac_address)
- 域名 (domain)
- URL (url)
- 端口号 (port)

作者: DataForge Team
日期: 2025-11-10
"""

import sys
import os
import json
import re
import ipaddress
from typing import Dict, List, Any

# 设置环境
sys.path.insert(0, '.')
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'

from dataforge.core.factory import default_registry
from dataforge.core.generator import GeneratorConfig, GenerationContext


def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_subsection(title: str):
    """打印子章节标题"""
    print(f"\n{'─'*40}")
    print(f"  {title}")
    print(f"{'─'*40}")


def basic_usage():
    """基础用法示例"""
    print_section("1. 基础用法示例")
    
    # 演示IP地址生成
    print_subsection("IP地址生成器 (ipaddress)")
    try:
        config = GeneratorConfig('ipaddress', {}, count=5)
        generator_class = default_registry.get_generator_class('ipaddress')
        generator = generator_class(config)
        ip_addresses = generator.generate_batch(5)
        
        for i, ip in enumerate(ip_addresses, 1):
            print(f"  示例 {i}: {ip}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # 演示MAC地址生成
    print_subsection("MAC地址生成器 (mac_address)")
    try:
        config = GeneratorConfig('mac_address', {}, count=5)
        generator_class = default_registry.get_generator_class('mac_address')
        generator = generator_class(config)
        mac_addresses = generator.generate_batch(5)
        
        for i, mac in enumerate(mac_addresses, 1):
            print(f"  示例 {i}: {mac}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # 演示域名生成
    print_subsection("域名生成器 (domain)")
    try:
        config = GeneratorConfig('domain', {}, count=5)
        generator_class = default_registry.get_generator_class('domain')
        generator = generator_class(config)
        domains = generator.generate_batch(5)
        
        for i, domain in enumerate(domains, 1):
            print(f"  示例 {i}: {domain}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # 演示URL生成
    print_subsection("URL生成器 (url)")
    try:
        config = GeneratorConfig('url', {}, count=5)
        generator_class = default_registry.get_generator_class('url')
        generator = generator_class(config)
        urls = generator.generate_batch(5)
        
        for i, url in enumerate(urls, 1):
            print(f"  示例 {i}: {url}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # 演示端口号生成
    print_subsection("端口号生成器 (port)")
    try:
        config = GeneratorConfig('port', {}, count=5)
        generator_class = default_registry.get_generator_class('port')
        generator = generator_class(config)
        ports = generator.generate_batch(5)
        
        for i, port in enumerate(ports, 1):
            print(f"  示例 {i}: {port}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")


def parameter_configuration():
    """参数配置示例"""
    print_section("2. 参数配置示例")
    
    # IP地址生成器参数配置
    print_subsection("IP地址生成器 - 版本配置")
    try:
        # 尝试不同的IP版本配置
        configs = [
            {},  # 默认配置
            {"version": "ipv4"},  # IPv4地址
            {"version": "ipv6"},  # IPv6地址
            {"version": "private"},  # 私有IP地址
        ]
        
        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig('ipaddress', params, count=3)
            generator_class = default_registry.get_generator_class('ipaddress')
            generator = generator_class(config)
            ip_addresses = generator.generate_batch(3)
            
            for j, ip in enumerate(ip_addresses, 1):
                print(f"    结果 {j}: {ip}")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # MAC地址生成器参数配置
    print_subsection("MAC地址生成器 - 厂商配置")
    try:
        configs = [
            {},  # 默认配置
            {"vendor": "cisco"},  # 思科
            {"vendor": "hp"},     # 惠普
            {"vendor": "dell"},   # 戴尔
        ]
        
        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig('mac_address', params, count=3)
            generator_class = default_registry.get_generator_class('mac_address')
            generator = generator_class(config)
            mac_addresses = generator.generate_batch(3)
            
            for j, mac in enumerate(mac_addresses, 1):
                print(f"    结果 {j}: {mac}")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")
    
    # 域名生成器参数配置
    print_subsection("域名生成器 - 域名类型配置")
    try:
        configs = [
            {},  # 默认配置
            {"domain_type": "com"},   # .com域名
            {"domain_type": "cn"},    # .cn域名
            {"domain_type": "org"},   # .org域名
        ]
        
        for i, params in enumerate(configs, 1):
            print(f"  配置 {i}: {params}")
            config = GeneratorConfig('domain', params, count=3)
            generator_class = default_registry.get_generator_class('domain')
            generator = generator_class(config)
            domains = generator.generate_batch(3)
            
            for j, domain in enumerate(domains, 1):
                print(f"    结果 {j}: {domain}")
            print()
    except Exception as e:
        print(f"  ❌ 错误: {e}")


def batch_generation():
    """批量生成示例"""
    print_section("3. 批量生成示例")
    
    # 批量生成网络信息
    print_subsection("批量生成网络信息")
    try:
        network_generators = ['ipaddress', 'mac_address', 'domain', 'url', 'port']
        batch_size = 5
        
        print(f"  生成 {batch_size} 个网络设备信息:")
        print("  " + "-" * 120)
        print("  序号 | IP地址       | MAC地址        | 域名              | URL                        | 端口")
        print("  " + "-" * 120)
        
        for i in range(batch_size):
            network_info = []
            
            # 生成网络信息
            for generator_name in network_generators:
                try:
                    config = GeneratorConfig(generator_name, {}, count=1)
                    generator_class = default_registry.get_generator_class(generator_name)
                    generator = generator_class(config)
                    result = generator.generate_single()
                    network_info.append(str(result))
                except:
                    network_info.append("N/A")
            
            # 格式化输出
            ip = network_info[0][:15].ljust(15)
            mac = network_info[1][:15].ljust(15)
            domain = network_info[2][:18].ljust(18)
            url = network_info[3][:25].ljust(25)
            port = network_info[4][:8].ljust(8)
            
            print(f"  {i+1:2d}    | {ip} | {mac} | {domain} | {url} | {port}")
        
        print("  " + "-" * 120)
        
    except Exception as e:
        print(f"  ❌ 批量生成失败: {e}")


def validation_examples():
    """数据验证示例"""
    print_section("4. 数据验证示例")
    
    # 验证IP地址格式
    print_subsection("IP地址格式验证")
    try:
        config = GeneratorConfig('ipaddress', {}, count=5)
        generator_class = default_registry.get_generator_class('ipaddress')
        generator = generator_class(config)
        ip_addresses = generator.generate_batch(5)
        
        print("  生成的IP地址:")
        for i, ip in enumerate(ip_addresses, 1):
            print(f"    {i}. {ip}")
            
            try:
                # 使用ipaddress库验证
                ip_obj = ipaddress.ip_address(ip)
                print(f"       格式验证: ✅ 有效 ({ip_obj.version})")
                
                # 检查是否为私有地址
                is_private = ip_obj.is_private
                print(f"       私有地址: {'是' if is_private else '否'}")
                
            except ValueError:
                print(f"       格式验证: ❌ 无效")
        
    except Exception as e:
        print(f"  ❌ IP地址验证失败: {e}")
    
    # 验证MAC地址格式
    print_subsection("MAC地址格式验证")
    try:
        config = GeneratorConfig('mac_address', {}, count=5)
        generator_class = default_registry.get_generator_class('mac_address')
        generator = generator_class(config)
        mac_addresses = generator.generate_batch(5)
        
        print("  生成的MAC地址:")
        mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$')
        
        for i, mac in enumerate(mac_addresses, 1):
            print(f"    {i}. {mac}")
            
            # 验证MAC地址格式
            is_valid = bool(mac_pattern.match(mac))
            print(f"       格式验证: {'✅ 有效' if is_valid else '❌ 无效'}")
            
            # 验证MAC地址长度
            length_valid = len(mac.replace(':', '')) == 12
            print(f"       长度验证: {'✅ 有效' if length_valid else '❌ 无效'}")
        
    except Exception as e:
        print(f"  ❌ MAC地址验证失败: {e}")


def error_handling():
    """错误处理示例"""
    print_section("5. 错误处理示例")
    
    # 处理不存在的IP版本
    print_subsection("处理不存在的IP版本")
    try:
        config = GeneratorConfig('ipaddress', {"version": "不存在的版本"}, count=1)
        generator_class = default_registry.get_generator_class('ipaddress')
        generator = generator_class(config)
        ip = generator.generate_single()
        print(f"  生成的IP地址: {ip}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效IP版本错误: {type(e).__name__}")
    
    # 处理无效的域名类型
    print_subsection("处理无效的域名类型")
    try:
        config = GeneratorConfig('domain', {"domain_type": "不存在的类型"}, count=1)
        generator_class = default_registry.get_generator_class('domain')
        generator = generator_class(config)
        domain = generator.generate_single()
        print(f"  生成的域名: {domain}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效域名类型错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print_section("6. 最佳实践示例")
    
    # 实践1: 生成关联的网络设备信息
    print_subsection("实践1: 生成关联的网络设备信息")
    try:
        # 生成一个网络设备的完整信息
        device_info = {}
        
        # 生成IP地址
        ip_config = GeneratorConfig('ipaddress', {"version": "ipv4"}, count=1)
        ip_class = default_registry.get_generator_class('ipaddress')
        ip_gen = ip_class(ip_config)
        device_info['ip_address'] = ip_gen.generate_single()
        
        # 生成关联的MAC地址
        mac_config = GeneratorConfig('mac_address', {"vendor": "cisco"}, count=1)
        mac_class = default_registry.get_generator_class('mac_address')
        mac_gen = mac_class(mac_config)
        device_info['mac_address'] = mac_gen.generate_single()
        
        # 生成主机名
        domain_config = GeneratorConfig('domain', {"domain_type": "com"}, count=1)
        domain_class = default_registry.get_generator_class('domain')
        domain_gen = domain_class(domain_config)
        device_info['domain'] = domain_gen.generate_single()
        
        print("  生成的网络设备信息:")
        for key, value in device_info.items():
            print(f"    {key}: {value}")
        
        print("\n  💡 建议：使用相同厂商的IP和MAC地址生成更真实的设备信息")
        
    except Exception as e:
        print(f"  ❌ 关联网络信息生成失败: {e}")
    
    # 实践2: 批量导出格式化数据
    print_subsection("实践2: 批量导出格式化数据")
    try:
        network_data = []
        
        # 生成多条网络设备信息
        for i in range(3):
            record = {}
            
            # 生成网络信息
            for field in ['ipaddress', 'mac_address', 'domain', 'url', 'port']:
                config = GeneratorConfig(field, {}, count=1)
                generator_class = default_registry.get_generator_class(field)
                generator = generator_class(config)
                record[field] = generator.generate_single()
            
            # 添加设备信息
            name_config = GeneratorConfig('name', {}, count=1)
            name_class = default_registry.get_generator_class('name')
            name_gen = name_class(name_config)
            record['device_name'] = name_gen.generate_single()
            
            # 添加设备类型
            device_types = ['路由器', '交换机', '防火墙', '服务器', '负载均衡器']
            record['device_type'] = device_types[i % len(device_types)]
            
            network_data.append(record)
        
        # 导出为JSON格式
        json_output = json.dumps(network_data, ensure_ascii=False, indent=2)
        print("  JSON格式输出:")
        print(json_output)
        
    except Exception as e:
        print(f"  ❌ 格式化导出失败: {e}")


def network_topology_demo():
    """网络拓扑演示"""
    print_section("7. 网络拓扑演示")
    
    # 演示网络拓扑数据
    print_subsection("网络拓扑数据生成")
    try:
        # 生成网络拓扑信息
        topology_data = []
        
        for i in range(3):
            topology = {
                "topology_id": f"TOPOLOGY_{i+1:03d}",
                "network_name": f"企业网络_{i+1}",
                "subnet": f"192.168.{i+1}.0.0/24",
                "gateway": f"192.168.{i+1}.0.1",
                "dns_servers": [f"8.8.8.8", f"8.8.4.4"],
                "devices": [],
                "created_at": f"2025-11-10T{i+9:02d}:00:00"
            }
            
            # 生成设备列表
            device_count = 5
            for j in range(device_count):
                device = {
                    "device_id": f"DEV_{i+1:03d}_{j+1:03d}",
                    "device_name": f"设备{i+1}-{j+1}",
                    "device_type": ["路由器", "交换机", "防火墙", "服务器"][j % 4],
                    "ip_address": f"192.168.{i+1}.{j+1}.{j+1}",
                    "mac_address": f"00:1B:44:11:{i+1:02d}:{j+1:02d}:{j+1:02d}",
                    "status": "online"
                }
                topology["devices"].append(device)
            
            topology_data.append(topology)
        
        print("  网络拓扑信息:")
        for topology in topology_data:
            print(f"\n  拓扑ID: {topology['topology_id']}")
            print(f"    网络名称: {topology['network_name']}")
            print(f"    子网: {topology['subnet']}")
            print(f"    网关: {topology['gateway']}")
            print(f"    DNS服务器: {', '.join(topology['dns_servers'])}")
            print(f"    设备数量: {len(topology['devices'])}")
            print(f"    设备列表:")
            
            for device in topology['devices'][:3]:  # 只显示前3个设备
                print(f"      - {device['device_name']} ({device['device_type']})")
                print(f"        IP: {device['ip_address']}")
                print(f"        MAC: {device['mac_address']}")
                print(f"        状态: {device['status']}")
        
    except Exception as e:
        print(f"  ❌ 网络拓扑演示失败: {e}")


def main():
    """主函数，运行所有示例"""
    print("🎯 DataForge 网络生成器示例 - IP地址相关")
    print("本示例展示了网络相关生成器的各种使用方法")
    
    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        network_topology_demo()
        
        print_section("✅ 示例演示完成")
        print("🎉 所有网络相关生成器示例已成功运行！")
        print("\n📚 相关文档:")
        print("  • 查看 examples/network/device_demo.py 了解设备标识相关生成器")
        print("  • 查看 examples/network/web_demo.py 了解Web相关生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")
        
    except Exception as e:
        print(f"\n❌ 示例运行出现错误: {e}")
        print("请检查DataForge环境配置是否正确")


if __name__ == "__main__":
    main()