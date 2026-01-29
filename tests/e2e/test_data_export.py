"""
数据导出端到端测试
"""

import csv
import io
import json

import pytest

from dataforge.core.factory import GeneratorFactory, GeneratorRegistry
from dataforge.core.generator import GeneratorConfig


@pytest.mark.e2e
class TestDataExport:
    """数据导出端到端测试类"""

    def test_json_export(self):
        """测试JSON格式导出"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 注册所需的生成器
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.contact.email import EmailGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("email", EmailGenerator)

        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
        }

        # 生成数据
        users = []
        for _ in range(10):
            user = {
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
                "email": generators["email"].generate_single(),
            }
            users.append(user)

        # 导出为JSON
        json_data = json.dumps(users, ensure_ascii=False, indent=2)

        # 验证导出
        assert json_data is not None
        assert len(json_data) > 0

        # 验证可以重新解析
        parsed_users = json.loads(json_data)
        assert len(parsed_users) == len(users)
        assert parsed_users[0]["name"] == users[0]["name"]

        print("\nJSON导出:")
        print(f"  记录数: {len(users)}")
        print(f"  数据大小: {len(json_data)}字节")

    def test_csv_export(self):
        """测试CSV格式导出"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 注册所需的生成器
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.contact.email import EmailGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("email", EmailGenerator)

        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
        }

        # 生成数据
        users = []
        for _ in range(10):
            user = {
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
                "email": generators["email"].generate_single(),
            }
            users.append(user)

        # 导出为CSV
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["name", "age", "email"])
        writer.writeheader()
        writer.writerows(users)
        csv_data = output.getvalue()

        # 验证导出
        assert csv_data is not None
        assert len(csv_data) > 0
        assert "name,age,email" in csv_data

        # 验证可以重新解析
        input_stream = io.StringIO(csv_data)
        reader = csv.DictReader(input_stream)
        parsed_users = list(reader)
        assert len(parsed_users) == len(users)

        print("\nCSV导出:")
        print(f"  记录数: {len(users)}")
        print(f"  数据大小: {len(csv_data)}字节")

    def test_sql_export(self):
        """测试SQL格式导出"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 注册所需的生成器
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.name import NameGenerator
        from dataforge.generators.contact.email import EmailGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)
        registry.register("email", EmailGenerator)

        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
            "email": factory.create_generator(GeneratorConfig("email", {})),
        }

        # 生成数据
        users = []
        for _ in range(10):
            user = {
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
                "email": generators["email"].generate_single(),
            }
            users.append(user)

        # 导出为SQL INSERT语句
        sql_statements = []
        for user in users:
            sql = f"INSERT INTO users (name, age, email) VALUES ('{user['name']}', {user['age']}, '{user['email']}');"
            sql_statements.append(sql)

        sql_data = "\n".join(sql_statements)

        # 验证导出
        assert sql_data is not None
        assert len(sql_data) > 0
        assert "INSERT INTO users" in sql_data
        assert len(sql_statements) == len(users)

        print("\nSQL导出:")
        print(f"  记录数: {len(users)}")
        print(f"  SQL语句数: {len(sql_statements)}")

    def test_large_dataset_export(self):
        """测试大数据集导出"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 注册所需的生成器
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)

        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
        }

        # 生成大数据集
        batch_size = 1000
        users = []
        for _ in range(batch_size):
            user = {
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
            }
            users.append(user)

        # 导出为JSON
        json_data = json.dumps(users, ensure_ascii=False)

        # 验证导出
        assert len(users) == batch_size
        assert len(json_data) > 0

        print("\n大数据集导出:")
        print(f"  记录数: {len(users)}")
        print(f"  JSON大小: {len(json_data)/1024:.2f} KB")

    def test_multi_format_export(self):
        """测试多格式导出"""
        registry = GeneratorRegistry()
        factory = GeneratorFactory(registry)

        # 注册所需的生成器
        from dataforge.generators.basic.age import AgeGenerator
        from dataforge.generators.basic.name import NameGenerator

        registry.register("name", NameGenerator)
        registry.register("age", AgeGenerator)

        # 创建生成器
        generators = {
            "name": factory.create_generator(GeneratorConfig("name", {})),
            "age": factory.create_generator(GeneratorConfig("age", {})),
        }

        # 生成数据
        users = []
        for _ in range(10):
            user = {
                "name": generators["name"].generate_single(),
                "age": generators["age"].generate_single(),
            }
            users.append(user)

        # 导出为多种格式
        formats = {}

        # JSON格式
        formats["json"] = json.dumps(users, ensure_ascii=False)

        # CSV格式
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["name", "age"])
        writer.writeheader()
        writer.writerows(users)
        formats["csv"] = output.getvalue()

        # 验证所有格式
        assert all(len(data) > 0 for data in formats.values())

        print("\n多格式导出:")
        for fmt, data in formats.items():
            print(f"  {fmt.upper()}: {len(data)}字节")
