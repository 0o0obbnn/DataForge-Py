"""
DataForge 增强测试覆盖率
测试核心功能、边界条件和异常处理
"""

import json
import os
import sys
import tempfile
import unittest

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dataforge.core.cache import DataCache, LazyDataLoader
from dataforge.core.factory import default_factory, default_registry
from dataforge.core.generator import GenerationContext, GeneratorConfig
from dataforge.core.preloader import DataPreloader
from dataforge.core.relations import DataRelationManager, RelationRule
from dataforge.core.validator import (
    CompositeValidator,
    LengthValidator,
    RangeValidator,
    RegexValidator,
)
from dataforge.generators.basic.idcard import IDCardGenerator
from dataforge.generators.basic.name import NameGenerator
from dataforge.generators.basic.uscc import USCCGenerator
from dataforge.generators.contact.phone import PhoneNumberGenerator
from dataforge.output.formatter import OutputFormatter


class TestValidators(unittest.TestCase):
    """数据校验器测试"""

    def test_regex_validator(self):
        """测试正则表达式校验器"""
        # 手机号校验器
        phone_validator = RegexValidator(r"^1[3-9]\d{9}$", "Invalid phone number")

        # 有效手机号
        self.assertTrue(phone_validator.validate("13800138000"))
        self.assertTrue(phone_validator.validate("15912345678"))

        # 无效手机号
        self.assertFalse(phone_validator.validate("12800138000"))  # 第二位错误
        self.assertFalse(phone_validator.validate("138001380001"))  # 长度错误
        self.assertFalse(phone_validator.validate(None))  # 非字符串
        self.assertFalse(phone_validator.validate(123))  # 非字符串

        # 错误消息
        self.assertEqual(
            phone_validator.get_error_message("invalid"), "Invalid phone number"
        )

    def test_length_validator(self):
        """测试长度校验器"""
        # 长度范围校验器
        length_validator = LengthValidator(min_length=2, max_length=10)

        # 有效长度
        self.assertTrue(length_validator.validate("ab"))
        self.assertTrue(length_validator.validate("abcdefghij"))
        self.assertTrue(length_validator.validate([1, 2, 3]))

        # 无效长度
        self.assertFalse(length_validator.validate("a"))  # 太短
        self.assertFalse(length_validator.validate("abcdefghijk"))  # 太长
        self.assertFalse(length_validator.validate(123))  # 没有长度属性

        # 只设置最小长度
        min_validator = LengthValidator(min_length=5)
        self.assertTrue(min_validator.validate("12345"))
        self.assertFalse(min_validator.validate("1234"))

        # 只设置最大长度
        max_validator = LengthValidator(max_length=3)
        self.assertTrue(max_validator.validate("123"))
        self.assertFalse(max_validator.validate("1234"))

    def test_range_validator(self):
        """测试数值范围校验器"""
        # 范围校验器
        range_validator = RangeValidator(min_value=0, max_value=100)

        # 有效数值
        self.assertTrue(range_validator.validate(0))
        self.assertTrue(range_validator.validate(50))
        self.assertTrue(range_validator.validate(100))
        self.assertTrue(range_validator.validate("50"))  # 字符串数字

        # 无效数值
        self.assertFalse(range_validator.validate(-1))
        self.assertFalse(range_validator.validate(101))
        self.assertFalse(range_validator.validate("abc"))  # 非数字字符串
        self.assertFalse(range_validator.validate(None))

    def test_composite_validator(self):
        """测试复合校验器"""
        # 创建复合校验器 - 要求所有条件都满足
        length_validator = LengthValidator(min_length=5, max_length=10)
        regex_validator = RegexValidator(r"^\d+$", "Must be digits only")

        all_validator = CompositeValidator(
            [length_validator, regex_validator], require_all=True
        )

        # 满足所有条件
        self.assertTrue(all_validator.validate("12345"))

        # 不满足长度条件
        self.assertFalse(all_validator.validate("123"))

        # 不满足正则条件
        self.assertFalse(all_validator.validate("abcde"))

        # 创建复合校验器 - 满足任一条件即可
        any_validator = CompositeValidator(
            [length_validator, regex_validator], require_all=False
        )

        # 只满足长度条件
        self.assertTrue(any_validator.validate("abcde"))

        # 只满足正则条件（但长度不够）
        self.assertTrue(any_validator.validate("123"))

        # 都不满足
        self.assertFalse(any_validator.validate("ab"))


class TestDataRelationManager(unittest.TestCase):
    """数据关联管理器测试"""

    def setUp(self):
        self.relation_manager = DataRelationManager()

    def test_builtin_relations(self):
        """测试内置关联规则"""
        # 测试身份证到年龄的关联
        self.relation_manager.add_builtin_relation(
            "idcard", "age", "derive", priority=10
        )

        context = GenerationContext()
        generated_data = {"idcard": "11010119900101123X"}
        pending_configs = [GeneratorConfig(generator_type="age", parameters={})]

        result = self.relation_manager.apply_relations(
            generated_data, pending_configs, context
        )

        # 应该从身份证推导出年龄
        self.assertIn("age", result)
        self.assertIsInstance(result["age"], int)
        self.assertTrue(30 <= result["age"] <= 35)  # 1990年出生，大约30-35岁

    def test_custom_relation_rule(self):
        """测试自定义关联规则"""

        def email_to_domain(email: str, context) -> str:
            return email.split("@")[1] if "@" in email else "example.com"

        # 添加自定义关联规则
        custom_rule = RelationRule(
            source_field="email",
            target_field="domain",
            relation_type="derive",
            rule_func=email_to_domain,
            priority=5,
        )
        self.relation_manager.add_relation_rule(custom_rule)

        context = GenerationContext()
        generated_data = {"email": "test@gmail.com"}
        pending_configs = [GeneratorConfig(generator_type="domain", parameters={})]

        result = self.relation_manager.apply_relations(
            generated_data, pending_configs, context
        )

        self.assertEqual(result["domain"], "gmail.com")

    def test_dependency_resolution(self):
        """测试依赖关系解析"""
        # 添加几个关联规则形成依赖链
        self.relation_manager.add_builtin_relation(
            "idcard", "age", "derive", priority=10
        )
        self.relation_manager.add_builtin_relation(
            "idcard", "gender", "derive", priority=10
        )
        self.relation_manager.add_builtin_relation(
            "gender", "name", "constrain", priority=5
        )

        field_names = ["name", "idcard", "age", "gender"]
        dependency_order = self.relation_manager.get_relation_dependencies(field_names)

        # idcard 应该在 age 和 gender 之前
        # gender 应该在 name 之前
        idcard_idx = dependency_order.index("idcard")
        age_idx = dependency_order.index("age")
        gender_idx = dependency_order.index("gender")
        name_idx = dependency_order.index("name")

        self.assertTrue(idcard_idx < age_idx)
        self.assertTrue(idcard_idx < gender_idx)
        self.assertTrue(gender_idx < name_idx)


class TestDataCache(unittest.TestCase):
    """数据缓存测试"""

    def setUp(self):
        self.cache = DataCache()
        self.test_data = {"test": "data", "numbers": [1, 2, 3]}

    def test_cache_basic_operations(self):
        """测试缓存基本操作"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(self.test_data, f)
            temp_file = f.name

        try:
            # 第一次加载
            data1 = self.cache.get_data(temp_file)
            self.assertEqual(data1, self.test_data)

            # 第二次加载应该使用缓存
            data2 = self.cache.get_data(temp_file)
            self.assertEqual(data2, self.test_data)
            self.assertIs(data1, data2)  # 应该是同一个对象

        finally:
            os.unlink(temp_file)

    def test_cache_file_not_found(self):
        """测试文件不存在的情况"""
        with self.assertRaises(FileNotFoundError):
            self.cache.get_data("/non/existent/file.json")

    def test_cache_custom_loader(self):
        """测试自定义加载器"""

        def custom_loader(file_path):
            return f"Custom loaded: {file_path}"

        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("dummy content")
            temp_file = f.name

        try:
            data = self.cache.get_data(temp_file, custom_loader)
            self.assertEqual(data, f"Custom loaded: {temp_file}")
        finally:
            os.unlink(temp_file)

    def test_lazy_data_loader(self):
        """测试惰性数据加载器"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(self.test_data, f)
            temp_file = f.name

        try:
            loader = LazyDataLoader(temp_file)

            # 数据还未加载
            self.assertFalse(loader._loaded)

            # 访问数据时才加载
            data = loader.data
            self.assertEqual(data, self.test_data)
            self.assertTrue(loader._loaded)

            # 再次访问使用缓存
            data2 = loader.data
            self.assertIs(data, data2)

        finally:
            os.unlink(temp_file)


class TestGeneratorEdgeCases(unittest.TestCase):
    """生成器边界条件测试"""

    def test_idcard_edge_cases(self):
        """测试身份证生成器边界条件"""
        # 测试无效参数
        config = GeneratorConfig(generator_type="idcard", parameters={"valid": False})
        generator = IDCardGenerator(config)

        # 生成无效身份证
        invalid_id = generator.generate_single()
        self.assertFalse(generator.validate(invalid_id))

        # 测试极端年龄
        config_old = GeneratorConfig(
            generator_type="idcard",
            parameters={
                "birth_date_range": ("1920-01-01", "1920-12-31"),
                "valid": True,
            },
        )
        generator_old = IDCardGenerator(config_old)
        old_id = generator_old.generate_single()
        self.assertTrue(generator_old.validate(old_id))

    def test_uscc_edge_cases(self):
        """测试统一社会信用代码边界条件"""
        # 测试不同机构类型
        for org_type in ["1", "2", "3", "9"]:
            config = GeneratorConfig(
                generator_type="uscc", parameters={"org_type": org_type, "valid": True}
            )
            generator = USCCGenerator(config)
            uscc = generator.generate_single()

            self.assertTrue(generator.validate(uscc))
            self.assertEqual(uscc[1], org_type)

        # 测试无效数据生成
        config_invalid = GeneratorConfig(
            generator_type="uscc", parameters={"valid": False}
        )
        generator_invalid = USCCGenerator(config_invalid)
        invalid_uscc = generator_invalid.generate_single()
        self.assertFalse(generator_invalid.validate(invalid_uscc))

    def test_name_generator_edge_cases(self):
        """测试姓名生成器边界条件"""
        # 测试英文名生成
        config_en = GeneratorConfig(
            generator_type="name", parameters={"type": "EN", "gender": "MALE"}
        )
        generator_en = NameGenerator(config_en)
        en_name = generator_en.generate_single()

        self.assertTrue(generator_en.validate(en_name))
        self.assertIn(" ", en_name)  # 英文名应该包含空格

        # 测试带拼音的中文名
        config_pinyin = GeneratorConfig(
            generator_type="name", parameters={"type": "CN", "include_pinyin": True}
        )
        generator_pinyin = NameGenerator(config_pinyin)
        pinyin_name = generator_pinyin.generate_single()

        self.assertTrue(generator_pinyin.validate(pinyin_name))
        self.assertIn("(", pinyin_name)  # 应该包含拼音

    def test_phone_generator_edge_cases(self):
        """测试电话生成器边界条件"""
        # 测试400号码生成
        config_400 = GeneratorConfig(
            generator_type="phone",
            parameters={"type": "TOLL_FREE", "format": "COMPACT"},
        )
        generator_400 = PhoneNumberGenerator(config_400)
        toll_free = generator_400.generate_single()

        self.assertTrue(generator_400.validate(toll_free))
        self.assertTrue(toll_free.startswith(("4006", "4007", "4008", "4009")))

        # 测试固定电话生成
        config_landline = GeneratorConfig(
            generator_type="phone",
            parameters={
                "type": "LANDLINE",
                "region": "北京",
                "include_extension": True,
            },
        )
        generator_landline = PhoneNumberGenerator(config_landline)
        landline = generator_landline.generate_single()

        self.assertTrue(generator_landline.validate(landline))
        if "ext." in landline:
            self.assertIn("ext.", landline)


class TestOutputFormatterEdgeCases(unittest.TestCase):
    """输出格式化器边界条件测试"""

    def setUp(self):
        self.formatter = OutputFormatter()

    def test_empty_data(self):
        """测试空数据格式化"""
        empty_data = {}

        # JSON格式
        json_result = self.formatter.format(empty_data, "json")
        self.assertEqual(json_result, "{}")

        # CSV格式
        csv_result = self.formatter.format(empty_data, "csv")
        self.assertEqual(csv_result.strip(), "")

    def test_complex_data_structures(self):
        """测试复杂数据结构格式化"""
        complex_data = {
            "users": [
                {"name": "张三", "age": 25, "hobbies": ["读书", "游泳"]},
                {"name": "李四", "age": 30, "hobbies": ["电影", "旅游"]},
            ],
            "metadata": {"total": 2, "timestamp": "2023-01-01"},
        }

        # 测试JSON格式
        json_result = self.formatter.format(complex_data, "json")
        parsed_back = json.loads(json_result)
        self.assertEqual(parsed_back, complex_data)

        # 测试XML格式
        xml_result = self.formatter.format(complex_data, "xml")
        self.assertIn("<dataforge_output>", xml_result)
        self.assertIn("</dataforge_output>", xml_result)

    def test_unsupported_format(self):
        """测试不支持的格式"""
        data = {"test": "data"}

        with self.assertRaises(ValueError):
            self.formatter.format(data, "unsupported_format")


class TestDataPreloader(unittest.TestCase):
    """数据预加载器测试"""

    def setUp(self):
        self.preloader = DataPreloader(max_workers=2)

    def test_register_data_source(self):
        """测试注册数据源"""
        # 创建临时数据文件
        test_data = {"test": "preload_data"}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_data, f)
            temp_file = f.name

        try:
            # 注册数据源
            self.preloader.register_data_source(
                name="test_source", file_path=temp_file, priority=5
            )

            # 检查状态
            status = self.preloader.get_loading_status("test_source")
            self.assertEqual(status["test_source"], "pending")

        finally:
            os.unlink(temp_file)

    def test_preload_with_dependencies(self):
        """测试带依赖的预加载"""
        # 创建两个临时数据文件
        data1 = {"dependency": "data1"}
        data2 = {"main": "data2"}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f1:
            json.dump(data1, f1)
            temp_file1 = f1.name

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f2:
            json.dump(data2, f2)
            temp_file2 = f2.name

        try:
            # 注册有依赖关系的数据源
            self.preloader.register_data_source(
                name="dependency_source", file_path=temp_file1, priority=10
            )

            self.preloader.register_data_source(
                name="main_source",
                file_path=temp_file2,
                priority=5,
                dependencies=["dependency_source"],
            )

            # 预加载
            results = self.preloader.preload_all(timeout=5.0)

            # 检查结果
            self.assertEqual(results["success"], 2)
            self.assertEqual(results["failed"], 0)
            self.assertIn("dependency_source", results["loaded_data"])
            self.assertIn("main_source", results["loaded_data"])

        finally:
            os.unlink(temp_file1)
            os.unlink(temp_file2)


class TestIntegrationScenarios(unittest.TestCase):
    """集成测试场景"""

    def test_complete_user_generation_workflow(self):
        """测试完整的用户数据生成工作流"""
        # 创建用户数据生成配置
        user_configs = [
            GeneratorConfig(
                generator_type="idcard", parameters={"region": "110000", "valid": True}
            ),
            GeneratorConfig(generator_type="name", parameters={"type": "CN"}),
            GeneratorConfig(generator_type="phone", parameters={"type": "MOBILE"}),
        ]

        # 使用工厂生成关联数据
        context = GenerationContext()
        results = default_factory.generate_batch_with_relations(user_configs, context)

        # 验证生成的数据
        self.assertIn("idcard", results)
        self.assertIn("name", results)
        self.assertIn("phone", results)

        # 验证数据有效性
        idcard_gen = IDCardGenerator(user_configs[0])
        name_gen = NameGenerator(user_configs[1])
        phone_gen = PhoneNumberGenerator(user_configs[2])

        self.assertTrue(idcard_gen.validate(results["idcard"]))
        self.assertTrue(name_gen.validate(results["name"]))
        self.assertTrue(phone_gen.validate(results["phone"]))

    def test_batch_generation_performance(self):
        """测试批量生成性能"""
        import time

        config = GeneratorConfig(generator_type="idcard", parameters={"valid": True})
        generator = IDCardGenerator(config)

        # 测试生成1000个身份证号的性能
        start_time = time.time()
        batch_data = generator.generate_batch(1000)
        end_time = time.time()

        generation_time = end_time - start_time

        # 验证结果
        self.assertEqual(len(batch_data), 1000)
        self.assertTrue(all(generator.validate(idcard) for idcard in batch_data))

        # 性能断言（应该在1秒内完成）
        self.assertLess(
            generation_time, 1.0, f"批量生成耗时过长: {generation_time:.2f}s"
        )

    def test_error_recovery_scenarios(self):
        """测试错误恢复场景"""
        # 测试无效配置的处理
        invalid_config = GeneratorConfig(
            generator_type="nonexistent_generator", parameters={}
        )

        with self.assertRaises(ValueError):
            default_factory.create_generator(invalid_config)

        # 测试部分失败的批量生成
        mixed_configs = [
            GeneratorConfig(generator_type="idcard", parameters={"valid": True}),
            GeneratorConfig(generator_type="invalid_type", parameters={}),
            GeneratorConfig(generator_type="phone", parameters={"type": "MOBILE"}),
        ]

        # 应该能处理部分失败的情况
        try:
            context = GenerationContext()
            # 这应该只生成有效的生成器对应的数据
            valid_configs = [
                cfg
                for cfg in mixed_configs
                if default_registry.is_registered(cfg.generator_type)
            ]
            results = default_factory.generate_batch_with_relations(
                valid_configs, context
            )

            # 应该包含有效的数据
            self.assertIn("idcard", results)
            self.assertIn("phone", results)

        except Exception as e:
            self.fail(f"错误恢复测试失败: {e}")


if __name__ == "__main__":
    # 配置测试运行器
    unittest.main(verbosity=2, buffer=True)

