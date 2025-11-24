"""
DataForge 设备标识生成器示例
演示设备ID、地理位置、HTTP头、会话令牌、时区等生成器的使用方法
"""

import os
import sys
import json
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from dataforge import GeneratorConfig, default_factory


def basic_usage():
    """基础用法示例"""
    print("1. 基础用法示例")
    print("=" * 60)
    
    # 设备ID生成器
    print("\n设备ID生成器 (device_id):")
    config = GeneratorConfig("device_id", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        device_id = generator.generate()
        print(f"  示例 {i+1}: {device_id}")
    
    # 地理坐标生成器
    print("\n地理坐标生成器 (geo_coordinates):")
    config = GeneratorConfig("geo_coordinates", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        coords = generator.generate()
        print(f"  示例 {i+1}: {coords}")
    
    # HTTP头生成器
    print("\nHTTP头生成器 (http_header):")
    config = GeneratorConfig("http_header", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        headers = generator.generate()
        print(f"  示例 {i+1}: {json.dumps(headers, ensure_ascii=False, indent=2)}")
    
    # 会话令牌生成器
    print("\n会话令牌生成器 (session_token):")
    config = GeneratorConfig("session_token", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        token = generator.generate()
        print(f"  示例 {i+1}: {token}")
    
    # 时区生成器
    print("\n时区生成器 (timezone):")
    config = GeneratorConfig("timezone", parameters={})
    generator = default_factory.create_generator(config)
    for i in range(3):
        tz = generator.generate()
        print(f"  示例 {i+1}: {tz}")


def parameter_configuration():
    """参数配置示例"""
    print("\n\n2. 参数配置示例")
    print("=" * 60)
    
    # 设备ID - 不同类型
    print("\n设备ID生成器 - 类型配置:")
    device_types = [{}, {"type": "uuid"}, {"type": "android"}, {"type": "ios"}]
    for i, params in enumerate(device_types, 1):
        config = GeneratorConfig("device_id", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # 地理坐标 - 不同地区
    print("\n地理坐标生成器 - 地区配置:")
    regions = [
        {"country": "CN", "city": "Beijing"},
        {"country": "US", "city": "New York"},
        {"country": "JP", "city": "Tokyo"},
        {"bounds": {"lat": (-90, 90), "lng": (-180, 180)}}
    ]
    for i, params in enumerate(regions, 1):
        config = GeneratorConfig("geo_coordinates", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # HTTP头 - 不同浏览器
    print("\nHTTP头生成器 - 浏览器配置:")
    browsers = [{}, {"browser": "chrome"}, {"browser": "firefox"}, {"browser": "safari"}]
    for i, params in enumerate(browsers, 1):
        config = GeneratorConfig("http_header", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        user_agent = result.get('User-Agent', 'N/A')
        print(f"  配置 {i}: {params}")
        print(f"    User-Agent: {user_agent[:80]}...")
    
    # 会话令牌 - 不同格式
    print("\n会话令牌生成器 - 格式配置:")
    token_formats = [
        {"length": 16},
        {"length": 32, "prefix": "sess_"},
        {"format": "jwt"},
        {"format": "base64"}
    ]
    for i, params in enumerate(token_formats, 1):
        config = GeneratorConfig("session_token", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")
    
    # 时区 - 不同类型
    print("\n时区生成器 - 类型配置:")
    tz_types = [
        {"type": "popular"},
        {"type": "all"},
        {"region": "Asia"},
        {"offset": 8}  # UTC+8
    ]
    for i, params in enumerate(tz_types, 1):
        config = GeneratorConfig("timezone", parameters=params)
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  配置 {i}: {params}")
        print(f"    结果: {result}")


def batch_generation():
    """批量生成示例"""
    print("\n\n3. 批量生成示例")
    print("=" * 60)
    
    print("\n批量生成设备信息:")
    devices = []
    
    # 生成设备基本信息
    device_id_config = GeneratorConfig("device_id", parameters={"type": "uuid"})
    device_id_gen = default_factory.create_generator(device_id_config)
    
    geo_config = GeneratorConfig("geo_coordinates", parameters={"country": "CN", "output_format": "dict"})
    geo_gen = default_factory.create_generator(geo_config)
    
    header_config = GeneratorConfig("http_header", parameters={"browser": "chrome"})
    header_gen = default_factory.create_generator(header_config)
    
    token_config = GeneratorConfig("session_token", parameters={"length": 32, "prefix": "dev_"})
    token_gen = default_factory.create_generator(token_config)
    
    tz_config = GeneratorConfig("timezone", parameters={"type": "popular"})
    tz_gen = default_factory.create_generator(tz_config)
    
    # 生成5个设备信息
    for i in range(5):
        device = {
            "device_id": device_id_gen.generate(),
            "location": geo_gen.generate(),
            "headers": header_gen.generate(),
            "session_token": token_gen.generate(),
            "timezone": tz_gen.generate(),
            "last_seen": datetime.now().isoformat()
        }
        devices.append(device)
    
    # 打印设备信息
    print("-" * 80)
    print(f"{'设备ID':<36} | {'位置':<20} | {'时区':<15} | {'会话令牌'}")
    print("-" * 80)
    for device in devices:
        device_id = device['device_id'][:34] + "..." if len(device['device_id']) > 34 else device['device_id']
        location = f"{device['location']['lat']:.2f},{device['location']['lng']:.2f}"
        tz = device['timezone'][:13] + ".." if len(device['timezone']) > 15 else device['timezone']
        token = device['session_token'][:20] + "..." if len(device['session_token']) > 20 else device['session_token']
        print(f"{device_id:<36} | {location:<20} | {tz:<15} | {token}")
    print("-" * 80)


def validation_examples():
    """数据验证示例"""
    print("\n\n4. 数据验证示例")
    print("=" * 60)
    
    # 设备ID验证
    print("\n设备ID格式验证:")
    config = GeneratorConfig("device_id", parameters={"type": "uuid"})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        device_id = generator.generate()
        is_valid = generator.validate(device_id)
        print(f"  {i+1}. {device_id}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
    
    # 地理坐标验证
    print("\n地理坐标验证:")
    config = GeneratorConfig("geo_coordinates", parameters={"output_format": "dict"})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        coords = generator.generate()
        lat, lng = coords['lat'], coords['lng']
        is_valid_lat = -90 <= lat <= 90
        is_valid_lng = -180 <= lng <= 180
        print(f"  {i+1}. 纬度: {lat}, 经度: {lng}")
        print(f"     纬度验证: {'✅ 有效' if is_valid_lat else '❌ 无效'}")
        print(f"     经度验证: {'✅ 有效' if is_valid_lng else '❌ 无效'}")
    
    # 会话令牌验证
    print("\n会话令牌验证:")
    config = GeneratorConfig("session_token", parameters={"length": 32})
    generator = default_factory.create_generator(config)
    
    for i in range(3):
        token = generator.generate()
        is_valid = generator.validate(token)
        print(f"  {i+1}. {token}")
        print(f"     验证结果: {'✅ 有效' if is_valid else '❌ 无效'}")
        print(f"     长度检查: {'✅ 符合' if len(token) == 32 else '❌ 不符合'}")


def error_handling():
    """错误处理示例"""
    print("\n\n5. 错误处理示例")
    print("=" * 60)
    
    # 处理无效的设备类型
    print("\n处理无效的设备类型:")
    try:
        config = GeneratorConfig("device_id", parameters={"type": "invalid_type"})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的设备ID: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效设备类型错误: {type(e).__name__}")
    
    # 处理无效的地理坐标范围
    print("\n处理无效的地理坐标范围:")
    try:
        config = GeneratorConfig("geo_coordinates", parameters={"bounds": {"lat": (100, 200)}})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的坐标: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效坐标范围错误: {type(e).__name__}")
    
    # 处理无效的会话令牌长度
    print("\n处理无效的会话令牌长度:")
    try:
        config = GeneratorConfig("session_token", parameters={"length": -1})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        print(f"  生成的令牌: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效令牌长度错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print("\n\n6. 最佳实践示例")
    print("=" * 60)
    
    # 实践1: 生成完整的设备指纹
    print("\n实践1: 生成完整的设备指纹")
    device_fingerprint = {
        "device_id": default_factory.create_generator(
            GeneratorConfig("device_id", parameters={"type": "uuid"})
        ).generate(),
        "user_agent": default_factory.create_generator(
            GeneratorConfig("http_header", parameters={"browser": "chrome"})
        ).generate().get("User-Agent", ""),
        "screen_resolution": "1920x1080",
        "timezone": default_factory.create_generator(
            GeneratorConfig("timezone", parameters={"region": "Asia"})
        ).generate(),
        "language": "zh-CN",
        "platform": "Win32",
        "location": default_factory.create_generator(
            GeneratorConfig("geo_coordinates", parameters={"country": "CN"})
        ).generate()
    }
    
    print("  设备指纹信息:")
    for key, value in device_fingerprint.items():
        if isinstance(value, dict):
            print(f"    {key}: {json.dumps(value, ensure_ascii=False)}")
        else:
            display_value = str(value)[:80] + "..." if len(str(value)) > 80 else str(value)
            print(f"    {key}: {display_value}")
    
    # 实践2: 批量导出设备数据
    print("\n实践2: 批量导出设备数据 (JSON格式)")
    devices_data = []
    
    for i in range(3):
        device_data = {
            "device_id": default_factory.create_generator(
                GeneratorConfig("device_id", parameters={"type": "android"})
            ).generate(),
            "location": default_factory.create_generator(
                GeneratorConfig("geo_coordinates", parameters={"output_format": "dict"})
            ).generate(),
            "session_info": {
                "token": default_factory.create_generator(
                    GeneratorConfig("session_token", parameters={"length": 24})
                ).generate(),
                "headers": default_factory.create_generator(
                    GeneratorConfig("http_header", parameters={"browser": "mobile"})
                ).generate()
            },
            "timezone": default_factory.create_generator(
                GeneratorConfig("timezone", parameters={"type": "popular"})
            ).generate()
        }
        devices_data.append(device_data)
    
    print("  JSON格式输出:")
    print(json.dumps(devices_data, ensure_ascii=False, indent=2))


def device_tracking_demo():
    """设备追踪演示"""
    print("\n\n7. 设备追踪演示")
    print("=" * 60)
    
    print("\n设备移动轨迹模拟:")
    
    # 生成设备ID
    device_id_gen = default_factory.create_generator(
        GeneratorConfig("device_id", parameters={"type": "uuid"})
    )
    device_id = device_id_gen.generate()
    
    # 生成移动轨迹（北京地区）
    beijing_bounds = {
        "lat": (39.8, 40.2),
        "lng": (116.3, 116.7)
    }
    
    # Add output_format to beijing_bounds
    beijing_bounds_with_format = beijing_bounds.copy()
    beijing_bounds_with_format["output_format"] = "dict"
    
    geo_gen = default_factory.create_generator(
        GeneratorConfig("geo_coordinates", parameters=beijing_bounds_with_format)
    )
    
    # 生成时间戳和位置
    trajectory = []
    base_time = datetime.now().timestamp()
    
    for i in range(5):
        location = geo_gen.generate()
        trajectory.append({
            "timestamp": datetime.fromtimestamp(base_time + i * 3600).isoformat(),
            "location": location,
            "accuracy": 10 + (i * 2)  # 模拟精度变化
        })
    
    print(f"  设备ID: {device_id}")
    print("  移动轨迹:")
    for point in trajectory:
        print(f"    时间: {point['timestamp'][:19]}")
        print(f"    位置: {point['location']['lat']:.6f}, {point['location']['lng']:.6f}")
        print(f"    精度: ±{point['accuracy']}米")
        print()


def main():
    """主函数"""
    print("🎯 DataForge 设备标识生成器示例")
    print("本示例展示了设备相关生成器的各种使用方法\n")
    
    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        device_tracking_demo()
        
        print("\n" + "=" * 60)
        print("✅ 示例演示完成")
        print("=" * 60)
        print("🎉 所有设备相关生成器示例已成功运行！")
        
        print("\n📚 相关文档:")
        print("  • 查看 examples/network/ip_demo.py 了解IP地址相关生成器")
        print("  • 查看 examples/network/web_demo.py 了解Web相关生成器")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")
        
    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()