"""
DataForge 集成生成器示例
演示如何组合使用多个生成器创建复杂的数据结构
"""

import json
import os
import sys
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from dataforge import GeneratorConfig, default_factory


def basic_usage():
    """基础用法示例"""
    print("1. 基础用法示例")
    print("=" * 60)

    # 创建用户档案
    print("\n创建完整用户档案:")
    user_profile = {
        "user_id": default_factory.create_generator(
            GeneratorConfig("uuid", parameters={"version": 4})
        ).generate(),
        "personal_info": {
            "name": default_factory.create_generator(
                GeneratorConfig("name", parameters={})
            ).generate(),
            "email": default_factory.create_generator(
                GeneratorConfig("email", parameters={})
            ).generate(),
            "phone": default_factory.create_generator(
                GeneratorConfig("phone", parameters={})
            ).generate(),
            "idcard": default_factory.create_generator(
                GeneratorConfig("idcard", parameters={})
            ).generate(),
            "age": default_factory.create_generator(
                GeneratorConfig("age", parameters={})
            ).generate(),
            "gender": default_factory.create_generator(
                GeneratorConfig("gender", parameters={})
            ).generate()
        },
        "location": {
            "address": default_factory.create_generator(
                GeneratorConfig("address", parameters={})
            ).generate(),
            "coordinates": default_factory.create_generator(
                GeneratorConfig("geo_coordinates", parameters={"output_format": "dict"})
            ).generate(),
            "timezone": default_factory.create_generator(
                GeneratorConfig("timezone", parameters={})
            ).generate()
        },
        "device_info": {
            "device_id": default_factory.create_generator(
                GeneratorConfig("device_id", parameters={"type": "uuid"})
            ).generate(),
            "user_agent": default_factory.create_generator(
                GeneratorConfig("http_header", parameters={"browser": "chrome"})
            ).generate().get("User-Agent", ""),
            "ip_address": default_factory.create_generator(
                GeneratorConfig("ipaddress", parameters={"version": "ipv4"})
            ).generate()
        },
        "created_at": datetime.now().isoformat()
    }

    print("  用户档案:")
    for key, value in user_profile.items():
        if isinstance(value, dict):
            print(f"    {key}:")
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, dict):
                    print(f"      {sub_key}: {sub_value}")
                else:
                    display_value = str(sub_value)[:30] + "..." if len(str(sub_value)) > 30 else str(sub_value)
                    print(f"      {sub_key}: {display_value}")
        else:
            display_value = str(value)[:30] + "..." if len(str(value)) > 30 else str(value)
            print(f"    {key}: {display_value}")


def parameter_configuration():
    """参数配置示例"""
    print("\n\n2. 参数配置示例")
    print("=" * 60)

    # 电商订单数据
    print("\n电商订单数据:")

    # 生成订单基本信息
    order_basic = {
        "order_id": default_factory.create_generator(
            GeneratorConfig("string", parameters={"length": 12, "type": "alphanumeric", "prefix": "ORD_"})
        ).generate(),
        "customer_id": default_factory.create_generator(
            GeneratorConfig("uuid", parameters={"version": 4})
        ).generate(),
        "order_date": datetime.now().isoformat(),
        "status": default_factory.create_generator(
            GeneratorConfig("enum", parameters={"options": ["待付款", "已付款", "已发货", "已送达", "已取消"]})
        ).generate()
    }

    # 生成商品信息
    products = []
    for i in range(3):
        product = {
            "product_id": default_factory.create_generator(
                GeneratorConfig("string", parameters={"length": 8, "type": "alphanumeric", "prefix": "PROD_"})
            ).generate(),
            "name": default_factory.create_generator(
                GeneratorConfig("chinese_text", parameters={"length": 20})
            ).generate(),
            "price": default_factory.create_generator(
                GeneratorConfig("decimal", parameters={"min": 10.0, "max": 1000.0, "decimal_places": 2})
            ).generate(),
            "quantity": default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 1, "max": 10})
            ).generate(),
            "category": default_factory.create_generator(
                GeneratorConfig("enum", parameters={"options": ["电子产品", "服装", "食品", "图书", "家居"]})
            ).generate()
        }
        products.append(product)

    # 生成支付信息
    payment_info = {
        "payment_method": default_factory.create_generator(
            GeneratorConfig("enum", parameters={"options": ["支付宝", "微信支付", "银行卡", "PayPal"]})
        ).generate(),
        "transaction_id": default_factory.create_generator(
            GeneratorConfig("string", parameters={"length": 20, "type": "alphanumeric"})
        ).generate(),
        "amount": sum(p["price"] * p["quantity"] for p in products),
        "currency": "CNY",
        "paid_at": (datetime.now() - timedelta(hours=1)).isoformat()
    }

    # 生成配送信息
    shipping_info = {
        "tracking_number": default_factory.create_generator(
            GeneratorConfig("tracking_number", parameters={"company": "sf_express"})
        ).generate(),
        "carrier": "顺丰速运",
        "shipping_address": default_factory.create_generator(
            GeneratorConfig("address", parameters={})
        ).generate(),
        "estimated_delivery": (datetime.now() + timedelta(days=3)).isoformat()
    }

    # 组装完整订单
    order = {
        **order_basic,
        "products": products,
        "payment": payment_info,
        "shipping": shipping_info,
        "total_amount": payment_info["amount"],
        "metadata": {
            "source": default_factory.create_generator(
                GeneratorConfig("enum", parameters={"options": ["Web", "Mobile App", "微信小程序", "第三方平台"]})
            ).generate(),
            "ip_address": default_factory.create_generator(
                GeneratorConfig("ipaddress", parameters={"version": "ipv4"})
            ).generate(),
            "user_agent": default_factory.create_generator(
                GeneratorConfig("http_header", parameters={"browser": "chrome"})
            ).generate().get("User-Agent", "")
        }
    }

    print("  订单信息:")
    print(f"    订单ID: {order['order_id']}")
    print(f"    客户ID: {order['customer_id']}")
    print(f"    订单日期: {order['order_date'][:10]}")
    print(f"    状态: {order['status']}")

    print("  商品列表:")
    for i, product in enumerate(order['products'], 1):
        print(f"    商品 {i}: {product['name']}")
        print(f"      价格: ¥{product['price']}")
        print(f"      数量: {product['quantity']}")
        print(f"      类别: {product['category']}")

    print("  支付信息:")
    print(f"    支付方式: {order['payment']['payment_method']}")
    print(f"    交易ID: {order['payment']['transaction_id']}")
    print(f"    支付金额: ¥{order['payment']['amount']}")
    print(f"    支付时间: {order['payment']['paid_at'][:19]}")

    print("  配送信息:")
    print(f"    快递单号: {order['shipping']['tracking_number']}")
    print(f"    承运商: {order['shipping']['carrier']}")
    print(f"    配送地址: {order['shipping']['shipping_address']}")
    print(f"    预计送达: {order['shipping']['estimated_delivery'][:10]}")

    print("  元数据:")
    print(f"    来源: {order['metadata']['source']}")
    print(f"    IP地址: {order['metadata']['ip_address']}")
    print(f"    用户代理: {order['metadata']['user_agent'][:50]}...")


def batch_generation():
    """批量生成示例"""
    print("\n\n3. 批量生成示例")
    print("=" * 60)

    print("\n批量生成社交媒体数据:")

    # 生成用户列表
    users = []
    for i in range(5):
        user = {
            "user_id": default_factory.create_generator(
                GeneratorConfig("uuid", parameters={"version": 4})
            ).generate(),
            "username": default_factory.create_generator(
                GeneratorConfig("username", parameters={})
            ).generate(),
            "email": default_factory.create_generator(
                GeneratorConfig("email", parameters={})
            ).generate(),
            "profile": {
                "display_name": default_factory.create_generator(
                    GeneratorConfig("name", parameters={})
                ).generate(),
                "bio": default_factory.create_generator(
                    GeneratorConfig("chinese_text", parameters={"length": 50})
                ).generate(),
                "location": default_factory.create_generator(
                    GeneratorConfig("address", parameters={})
                ).generate(),
                "website": f"https://example.com/{default_factory.create_generator(GeneratorConfig('string', parameters={'length': 8, 'type': 'alphabetic'})).generate()}",
                "avatar": f"https://api.example.com/avatar/{default_factory.create_generator(GeneratorConfig('string', parameters={'length': 8, 'type': 'alphanumeric'})).generate()}.jpg"
            },
            "stats": {
                "followers": default_factory.create_generator(
                    GeneratorConfig("integer", parameters={"min": 0, "max": 10000})
                ).generate(),
                "following": default_factory.create_generator(
                    GeneratorConfig("integer", parameters={"min": 0, "max": 5000})
                ).generate(),
                "posts": default_factory.create_generator(
                    GeneratorConfig("integer", parameters={"min": 0, "max": 1000})
                ).generate(),
                "likes": default_factory.create_generator(
                    GeneratorConfig("integer", parameters={"min": 0, "max": 50000})
                ).generate()
            },
            "activity": {
                "last_login": (datetime.now() - timedelta(hours=default_factory.create_generator(
                    GeneratorConfig("integer", parameters={"min": 0, "max": 72})
                ).generate())).isoformat(),
                "is_online": default_factory.create_generator(
                    GeneratorConfig("boolean", parameters={"true_probability": 0.3})
                ).generate(),
                "is_verified": default_factory.create_generator(
                    GeneratorConfig("boolean", parameters={"true_probability": 0.1})
                ).generate()
            },
            "created_at": (datetime.now() - timedelta(days=default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 30, "max": 365})
            ).generate())).isoformat()
        }
        users.append(user)

    # 生成帖子列表
    posts = []
    for i in range(10):
        post = {
            "post_id": default_factory.create_generator(
                GeneratorConfig("string", parameters={"length": 12, "type": "alphanumeric", "prefix": "POST_"})
            ).generate(),
            "author_id": default_factory.create_generator(
                GeneratorConfig("uuid", parameters={"version": 4})
            ).generate(),
            "content": default_factory.create_generator(
                GeneratorConfig("chinese_text", parameters={"length": 100})
            ).generate(),
            "hashtags": [
                f"#{default_factory.create_generator(GeneratorConfig('string', parameters={'length': 5, 'type': 'alphabetic'})).generate()}"
                for _ in range(default_factory.create_generator(
                    GeneratorConfig("integer", parameters={"min": 1, "max": 5})
                ).generate())
            ],
            "media": {
                "type": default_factory.create_generator(
                    GeneratorConfig("enum", parameters={"options": ["image", "video", "link", "none"]})
                ).generate(),
                "url": f"https://cdn.example.com/media/{default_factory.create_generator(GeneratorConfig('string', parameters={'length': 10, 'type': 'alphanumeric'})).generate()}.jpg" if default_factory.create_generator(
                    GeneratorConfig("boolean", parameters={"true_probability": 0.6})
                ).generate() else None
            },
            "stats": {
                "likes": default_factory.create_generator(
                    GeneratorConfig("integer", parameters={"min": 0, "max": 1000})
                ).generate(),
                "comments": default_factory.create_generator(
                    GeneratorConfig("integer", parameters={"min": 0, "max": 100})
                ).generate(),
                "shares": default_factory.create_generator(
                    GeneratorConfig("integer", parameters={"min": 0, "max": 50})
                ).generate(),
                "views": default_factory.create_generator(
                    GeneratorConfig("integer", parameters={"min": 0, "max": 10000})
                ).generate()
            },
            "created_at": (datetime.now() - timedelta(hours=default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 0, "max": 168})
            ).generate())).isoformat()
        }
        posts.append(post)

    # 生成评论列表
    comments = []
    for i in range(20):
        comment = {
            "comment_id": default_factory.create_generator(
                GeneratorConfig("string", parameters={"length": 12, "type": "alphanumeric", "prefix": "COMM_"})
            ).generate(),
            "post_id": default_factory.create_generator(
                GeneratorConfig("uuid", parameters={"version": 4})
            ).generate(),
            "author_id": default_factory.create_generator(
                GeneratorConfig("uuid", parameters={"version": 4})
            ).generate(),
            "content": default_factory.create_generator(
                GeneratorConfig("chinese_text", parameters={"length": 50})
            ).generate(),
            "likes": default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 0, "max": 100})
            ).generate(),
            "replies": default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 0, "max": 10})
            ).generate(),
            "created_at": (datetime.now() - timedelta(hours=default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 0, "max": 72})
            ).generate())).isoformat()
        }
        comments.append(comment)

    # 打印摘要信息
    print(f"  用户数量: {len(users)}")
    print(f"  帖子数量: {len(posts)}")
    print(f"  评论数量: {len(comments)}")

    # 打印部分用户信息
    print("\n  用户示例:")
    for user in users[:3]:
        print(f"    用户名: {user['username']}")
        print(f"      显示名称: {user['profile']['display_name']}")
        print(f"      关注者: {user['stats']['followers']}")
        print(f"      帖子数: {user['stats']['posts']}")
        print(f"      在线: {'是' if user['activity']['is_online'] else '否'}")
        print(f"      已验证: {'是' if user['activity']['is_verified'] else '否'}")

    # 打印部分帖子信息
    print("\n  帖子示例:")
    for post in posts[:3]:
        print(f"    帖子ID: {post['post_id']}")
        print(f"      内容: {post['content'][:50]}...")
        print(f"      标签: {', '.join(post['hashtags'])}")
        print(f"      点赞: {post['stats']['likes']}")
        print(f"      评论: {post['stats']['comments']}")

    # 打印部分评论信息
    print("\n  评论示例:")
    for comment in comments[:3]:
        print(f"    评论ID: {comment['comment_id']}")
        print(f"      内容: {comment['content'][:40]}...")
        print(f"      点赞: {comment['likes']}")
        print(f"      回复: {comment['replies']}")


def validation_examples():
    """数据验证示例"""
    print("\n\n4. 数据验证示例")
    print("=" * 60)

    print("\n验证集成的用户数据:")

    # 创建用户数据
    user_data = {
        "user_id": default_factory.create_generator(
            GeneratorConfig("uuid", parameters={"version": 4})
        ).generate(),
        "email": default_factory.create_generator(
            GeneratorConfig("email", parameters={})
        ).generate(),
        "phone": default_factory.create_generator(
            GeneratorConfig("phone", parameters={})
        ).generate(),
        "idcard": default_factory.create_generator(
            GeneratorConfig("idcard", parameters={})
        ).generate(),
        "age": default_factory.create_generator(
            GeneratorConfig("age", parameters={})
        ).generate(),
        "bankcard": default_factory.create_generator(
            GeneratorConfig("bankcard", parameters={"type": "visa"})
        ).generate()
    }

    # 验证各个字段
    print("  验证结果:")

    # 验证UUID
    uuid_gen = default_factory.create_generator(GeneratorConfig("uuid", parameters={"version": 4}))
    is_uuid_valid = uuid_gen.validate(user_data["user_id"])
    print(f"    UUID: {'✅ 有效' if is_uuid_valid else '❌ 无效'}")

    # 验证邮箱
    email_gen = default_factory.create_generator(GeneratorConfig("email", parameters={}))
    is_email_valid = email_gen.validate(user_data["email"])
    print(f"    邮箱: {'✅ 有效' if is_email_valid else '❌ 无效'}")

    # 验证手机号
    phone_gen = default_factory.create_generator(GeneratorConfig("phone", parameters={}))
    is_phone_valid = phone_gen.validate(user_data["phone"])
    print(f"    手机号: {'✅ 有效' if is_phone_valid else '❌ 无效'}")

    # 验证身份证
    idcard_gen = default_factory.create_generator(GeneratorConfig("idcard", parameters={}))
    is_idcard_valid = idcard_gen.validate(user_data["idcard"])
    print(f"    身份证: {'✅ 有效' if is_idcard_valid else '❌ 无效'}")

    # 验证年龄
    age_gen = default_factory.create_generator(GeneratorConfig("age", parameters={}))
    is_age_valid = age_gen.validate(user_data["age"])
    print(f"    年龄: {'✅ 有效' if is_age_valid else '❌ 无效'}")

    # 验证银行卡
    card_gen = default_factory.create_generator(GeneratorConfig("bankcard", parameters={"type": "visa"}))
    is_card_valid = card_gen.validate(user_data["bankcard"])
    print(f"    银行卡: {'✅ 有效' if is_card_valid else '❌ 无效'}")

    # 整体验证结果
    all_valid = all([is_uuid_valid, is_email_valid, is_phone_valid, is_idcard_valid, is_age_valid, is_card_valid])
    print(f"\n  整体验证: {'✅ 全部有效' if all_valid else '❌ 存在无效字段'}")


def error_handling():
    """错误处理示例"""
    print("\n\n5. 错误处理示例")
    print("=" * 60)

    print("\n处理集成数据生成中的错误:")

    # 处理无效的参数组合
    print("\n处理无效的参数组合:")
    try:
        # 尝试创建年龄为负数的用户
        user = {
            "name": default_factory.create_generator(
                GeneratorConfig("name", parameters={})
            ).generate(),
            "age": default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": -10, "max": -1})
            ).generate()
        }
        print(f"  生成的用户: {user['name']}, 年龄: {user['age']}")
    except Exception as e:
        print(f"  ✅ 正确捕获了无效年龄错误: {type(e).__name__}")

    # 处理数据类型不匹配
    print("\n处理数据类型不匹配:")
    try:
        # 尝试将字符串作为整数使用
        config = GeneratorConfig("integer", parameters={})
        generator = default_factory.create_generator(config)
        result = generator.generate()
        # 这里只是演示，实际使用中应该检查类型
        print(f"  生成的整数: {result} (类型: {type(result).__name__})")
    except Exception as e:
        print(f"  ✅ 正确捕获了类型错误: {type(e).__name__}")

    # 处理依赖数据缺失
    print("\n处理依赖数据缺失:")
    try:
        # 模拟创建需要依赖关系的数据
        primary_data = {
            "id": default_factory.create_generator(
                GeneratorConfig("uuid", parameters={"version": 4})
            ).generate()
        }

        # 尝试使用不存在的依赖
        dependent_data = {
            "parent_id": primary_data.get("non_existent_id", "default_value"),
            "name": default_factory.create_generator(
                GeneratorConfig("name", parameters={})
            ).generate()
        }
        print(f"  依赖数据: {dependent_data}")
    except Exception as e:
        print(f"  ✅ 正确处理了依赖数据缺失: {type(e).__name__}")

    # 处理生成器不存在
    print("\n处理生成器不存在:")
    try:
        # 尝试使用不存在的生成器
        result = default_factory.create_generator(
            GeneratorConfig("non_existent_generator", parameters={})
        ).generate()
        print(f"  生成结果: {result}")
    except Exception as e:
        print(f"  ✅ 正确捕获了生成器不存在错误: {type(e).__name__}")


def best_practices():
    """最佳实践示例"""
    print("\n\n6. 最佳实践示例")
    print("=" * 60)

    print("\n实践1: 数据生成器工厂模式")

    # 创建一个数据生成器工厂
    class DataGeneratorFactory:
        def __init__(self):
            self.generators = {}
            self._setup_generators()

        def _setup_generators(self):
            """设置常用生成器"""
            self.generators = {
                "uuid": default_factory.create_generator(
                    GeneratorConfig("uuid", parameters={"version": 4})
                ),
                "name": default_factory.create_generator(
                    GeneratorConfig("name", parameters={})
                ),
                "email": default_factory.create_generator(
                    GeneratorConfig("email", parameters={})
                ),
                "phone": default_factory.create_generator(
                    GeneratorConfig("phone", parameters={})
                ),
                "address": default_factory.create_generator(
                    GeneratorConfig("address", parameters={})
                ),
                "company": default_factory.create_generator(
                    GeneratorConfig("company_name", parameters={})
                )
            }

        def generate_user(self):
            """生成用户数据"""
            return {
                "id": self.generators["uuid"].generate(),
                "name": self.generators["name"].generate(),
                "email": self.generators["email"].generate(),
                "phone": self.generators["phone"].generate(),
                "address": self.generators["address"].generate()
            }

        def generate_company(self):
            """生成公司数据"""
            return {
                "id": self.generators["uuid"].generate(),
                "name": self.generators["company"].generate(),
                "address": self.generators["address"].generate()
            }

    # 使用工厂生成数据
    factory = DataGeneratorFactory()

    print("  使用工厂生成用户数据:")
    for i in range(3):
        user = factory.generate_user()
        print(f"    用户 {i+1}: {user['name']} - {user['email']}")

    print("  使用工厂生成公司数据:")
    for i in range(3):
        company = factory.generate_company()
        print(f"    公司 {i+1}: {company['name']}")

    print("\n实践2: 数据关联生成")

    # 生成有关联的数据
    print("  生成有关联的订单和客户数据:")

    # 先生成客户
    customer = {
        "customer_id": default_factory.create_generator(
            GeneratorConfig("uuid", parameters={"version": 4})
        ).generate(),
        "name": default_factory.create_generator(
            GeneratorConfig("name", parameters={})
        ).generate(),
        "email": default_factory.create_generator(
            GeneratorConfig("email", parameters={})
        ).generate()
    }

    # 生成该客户的订单
    orders = []
    for i in range(3):
        order = {
            "order_id": default_factory.create_generator(
                GeneratorConfig("string", parameters={"length": 12, "type": "alphanumeric", "prefix": "ORD_"})
            ).generate(),
            "customer_id": customer["customer_id"],  # 关联客户ID
            "order_date": (datetime.now() - timedelta(days=i)).isoformat(),
            "amount": default_factory.create_generator(
                GeneratorConfig("decimal", parameters={"min": 100.0, "max": 1000.0, "decimal_places": 2})
            ).generate(),
            "status": default_factory.create_generator(
                GeneratorConfig("enum", parameters={"options": ["待付款", "已付款", "已发货", "已完成"]})
            ).generate()
        }
        orders.append(order)

    print(f"    客户: {customer['name']} ({customer['email']})")
    print("    订单列表:")
    for order in orders:
        print(f"      订单 {order['order_id']}: ¥{order['amount']} - {order['status']} ({order['order_date'][:10]})")

    print("\n实践3: 批量数据导出")

    # 生成批量数据并导出
    print("  生成批量用户数据并导出为JSON:")

    batch_data = []
    for i in range(5):
        user_data = {
            "user_id": default_factory.create_generator(
                GeneratorConfig("uuid", parameters={"version": 4})
            ).generate(),
            "profile": {
                "name": default_factory.create_generator(
                    GeneratorConfig("name", parameters={})
                ).generate(),
                "age": default_factory.create_generator(
                    GeneratorConfig("age", parameters={})
                ).generate(),
                "gender": default_factory.create_generator(
                    GeneratorConfig("gender", parameters={})
                ).generate()
            },
            "contact": {
                "email": default_factory.create_generator(
                    GeneratorConfig("email", parameters={})
                ).generate(),
                "phone": default_factory.create_generator(
                    GeneratorConfig("phone", parameters={})
                ).generate(),
                "address": default_factory.create_generator(
                    GeneratorConfig("address", parameters={})
                ).generate()
            },
            "identifiers": {
                "idcard": default_factory.create_generator(
                    GeneratorConfig("idcard", parameters={})
                ).generate(),
                "passport": default_factory.create_generator(
                    GeneratorConfig("passport", parameters={"country": "CN"})
                ).generate(),
                "bankcard": default_factory.create_generator(
                    GeneratorConfig("bankcard", parameters={"type": "visa"})
                ).generate()
            },
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "source": "integration_demo",
                "version": "1.0"
            }
        }
        batch_data.append(user_data)

    print("  JSON格式输出 (前2条):")
    print(json.dumps(batch_data[:2], ensure_ascii=False, indent=2))


def integration_demo():
    """集成演示"""
    print("\n\n7. 集成演示")
    print("=" * 60)

    print("\n生成完整的电商平台数据:")

    # 生成平台数据
    platform_data = {
        "platform": {
            "name": "DataForge商城",
            "version": "2.0.0",
            "created_at": "2023-01-01T00:00:00Z"
        },
        "users": [],
        "products": [],
        "orders": [],
        "reviews": []
    }

    # 生成用户数据
    print("  生成用户数据...")
    for i in range(10):
        user = {
            "user_id": default_factory.create_generator(
                GeneratorConfig("uuid", parameters={"version": 4})
            ).generate(),
            "username": default_factory.create_generator(
                GeneratorConfig("username", parameters={})
            ).generate(),
            "email": default_factory.create_generator(
                GeneratorConfig("email", parameters={})
            ).generate(),
            "profile": {
                "name": default_factory.create_generator(
                    GeneratorConfig("name", parameters={})
                ).generate(),
                "age": default_factory.create_generator(
                    GeneratorConfig("age", parameters={})
                ).generate(),
                "gender": default_factory.create_generator(
                    GeneratorConfig("gender", parameters={})
                ).generate(),
                "location": default_factory.create_generator(
                    GeneratorConfig("address", parameters={})
                ).generate()
            },
            "stats": {
                "total_orders": default_factory.create_generator(
                    GeneratorConfig("integer", parameters={"min": 0, "max": 50})
                ).generate(),
                "total_spent": default_factory.create_generator(
                    GeneratorConfig("decimal", parameters={"min": 0, "max": 10000, "decimal_places": 2})
                ).generate(),
                "avg_rating": default_factory.create_generator(
                    GeneratorConfig("decimal", parameters={"min": 3.0, "max": 5.0, "decimal_places": 1})
                ).generate()
            },
            "registered_at": (datetime.now() - timedelta(days=default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 30, "max": 365})
            ).generate())).isoformat()
        }
        platform_data["users"].append(user)

    # 生成商品数据
    print("  生成商品数据...")
    categories = ["电子产品", "服装", "食品", "图书", "家居", "运动", "美妆", "玩具"]
    for i in range(20):
        product = {
            "product_id": default_factory.create_generator(
                GeneratorConfig("string", parameters={"length": 10, "type": "alphanumeric", "prefix": "PROD_"})
            ).generate(),
            "name": default_factory.create_generator(
                GeneratorConfig("chinese_text", parameters={"length": 20})
            ).generate(),
            "description": default_factory.create_generator(
                GeneratorConfig("chinese_text", parameters={"length": 100})
            ).generate(),
            "category": default_factory.create_generator(
                GeneratorConfig("enum", parameters={"options": categories})
            ).generate(),
            "price": default_factory.create_generator(
                GeneratorConfig("decimal", parameters={"min": 10.0, "max": 1000.0, "decimal_places": 2})
            ).generate(),
            "stock": default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 0, "max": 1000})
            ).generate(),
            "brand": default_factory.create_generator(
                GeneratorConfig("string", parameters={"length": 10, "type": "alphabetic"})
            ).generate(),
            "rating": default_factory.create_generator(
                GeneratorConfig("decimal", parameters={"min": 3.0, "max": 5.0, "decimal_places": 1})
            ).generate(),
            "reviews_count": default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 0, "max": 500})
            ).generate(),
            "created_at": (datetime.now() - timedelta(days=default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 1, "max": 365})
            ).generate())).isoformat()
        }
        platform_data["products"].append(product)

    # 生成订单数据
    print("  生成订单数据...")
    for i in range(30):
        # 随机选择用户
        user_ids = [u["user_id"] for u in platform_data["users"]]
        user = default_factory.create_generator(
            GeneratorConfig("enum", parameters={"options": user_ids})
        ).generate()

        # 随机选择商品
        product_ids = [p["product_id"] for p in platform_data["products"]]
        products_in_order = []
        num_products = default_factory.create_generator(
            GeneratorConfig("integer", parameters={"min": 1, "max": 5})
        ).generate()

        total_amount = 0
        for _ in range(num_products):
            product = default_factory.create_generator(
                GeneratorConfig("enum", parameters={"options": product_ids})
            ).generate()
            quantity = default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 1, "max": 3})
            ).generate()

            # 找到商品价格
            product_info = next((p for p in platform_data["products"] if p["product_id"] == product), None)
            if product_info:
                amount = product_info["price"] * quantity
                total_amount += amount
            else:
                # 如果找不到商品，使用默认价格
                amount = default_factory.create_generator(
                    GeneratorConfig("decimal", parameters={"min": 10.0, "max": 1000.0, "decimal_places": 2})
                ).generate() * quantity
                total_amount += amount

            products_in_order.append({
                "product_id": product,
                "quantity": quantity,
                "price": product_info["price"] if product_info else (amount / quantity if quantity > 0 else 0),
                "amount": amount
            })

        order = {
            "order_id": default_factory.create_generator(
                GeneratorConfig("string", parameters={"length": 12, "type": "alphanumeric", "prefix": "ORD_"})
            ).generate(),
            "user_id": user,
            "products": products_in_order,
            "total_amount": total_amount,
            "status": default_factory.create_generator(
                GeneratorConfig("enum", parameters={"options": ["待付款", "已付款", "已发货", "已送达", "已取消"]})
            ).generate(),
            "payment_method": default_factory.create_generator(
                GeneratorConfig("enum", parameters={"options": ["支付宝", "微信支付", "银行卡", "PayPal"]})
            ).generate(),
            "shipping_address": default_factory.create_generator(
                GeneratorConfig("address", parameters={})
            ).generate(),
            "order_date": (datetime.now() - timedelta(days=default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 0, "max": 30})
            ).generate())).isoformat(),
            "created_at": datetime.now().isoformat()
        }
        platform_data["orders"].append(order)

    # 生成评价数据
    print("  生成评价数据...")
    for i in range(50):
        # 随机选择订单
        delivered_orders = [o["order_id"] for o in platform_data["orders"] if o["status"] in ["已送达"]]
        if delivered_orders:
            order = default_factory.create_generator(
                GeneratorConfig("enum", parameters={"options": delivered_orders})
            ).generate()
        else:
            order = default_factory.create_generator(
                GeneratorConfig("string", parameters={"length": 12, "type": "alphanumeric", "prefix": "ORD_"})
            ).generate()

        # 随机选择商品
        product_ids = [p["product_id"] for p in platform_data["products"]]
        if product_ids:
            product = default_factory.create_generator(
                GeneratorConfig("enum", parameters={"options": product_ids})
            ).generate()
        else:
            product = default_factory.create_generator(
                GeneratorConfig("string", parameters={"length": 10, "type": "alphanumeric", "prefix": "PROD_"})
            ).generate()

        # 找到商品价格
        try:
            product_info = next((p for p in platform_data["products"] if p["product_id"] == product), None)
            product_price = product_info["price"] if product_info else default_factory.create_generator(
                GeneratorConfig("decimal", parameters={"min": 10.0, "max": 1000.0, "decimal_places": 2})
            ).generate()
        except StopIteration:
            product_price = default_factory.create_generator(
                GeneratorConfig("decimal", parameters={"min": 10.0, "max": 1000.0, "decimal_places": 2})
            ).generate()

        review = {
            "review_id": default_factory.create_generator(
                GeneratorConfig("string", parameters={"length": 12, "type": "alphanumeric", "prefix": "REV_"})
            ).generate(),
            "order_id": order,
            "product_id": product,
            "rating": default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 1, "max": 5})
            ).generate(),
            "title": default_factory.create_generator(
                GeneratorConfig("chinese_text", parameters={"length": 20})
            ).generate(),
            "content": default_factory.create_generator(
                GeneratorConfig("chinese_text", parameters={"length": 100})
            ).generate(),
            "helpful": default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 0, "max": 100})
            ).generate(),
            "verified": default_factory.create_generator(
                GeneratorConfig("boolean", parameters={"true_probability": 0.8})
            ).generate(),
            "created_at": (datetime.now() - timedelta(days=default_factory.create_generator(
                GeneratorConfig("integer", parameters={"min": 0, "max": 30})
            ).generate())).isoformat()
        }
        platform_data["reviews"].append(review)

    # 打印统计信息
    print("\n  平台数据统计:")
    print(f"    用户数量: {len(platform_data['users'])}")
    print(f"    商品数量: {len(platform_data['products'])}")
    print(f"    订单数量: {len(platform_data['orders'])}")
    print(f"    评价数量: {len(platform_data['reviews'])}")

    # 计算总销售额
    total_sales = sum(order["total_amount"] for order in platform_data["orders"] if order["status"] != "已取消")
    print(f"    总销售额: ¥{total_sales:.2f}")

    # 计算平均评分
    if platform_data["reviews"]:
        avg_rating = sum(review["rating"] for review in platform_data["reviews"]) / len(platform_data["reviews"])
        print(f"    平均评分: {avg_rating:.1f}")

    # 保存数据到文件
    output_file = os.path.join(os.path.dirname(__file__), "platform_data.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(platform_data, f, ensure_ascii=False, indent=2)

    print(f"\n  数据已保存到: {output_file}")


def main():
    """主函数"""
    print("🔗 DataForge 集成生成器示例")
    print("本示例展示了如何组合使用多个生成器创建复杂的数据结构\n")

    try:
        basic_usage()
        parameter_configuration()
        batch_generation()
        validation_examples()
        error_handling()
        best_practices()
        integration_demo()

        print("\n" + "=" * 60)
        print("✅ 示例演示完成")
        print("=" * 60)
        print("🎉 所有集成生成器示例已成功运行！")

        print("\n📚 相关文档:")
        print("  • 查看 examples/utility/utility_demo.py 了解实用工具示例")
        print("  • 查看 examples/comprehensive_demo.py 了解所有生成器概览")

    except Exception as e:
        print(f"\n❌ 运行示例时发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
