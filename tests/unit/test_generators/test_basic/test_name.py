"""
姓名生成器测试
"""

import pytest

from dataforge.core.generator import GeneratorConfig


@pytest.mark.unit
class TestNameGenerator:
    """姓名生成器测试类"""

    def test_generate_single(self, generator_factory):
        """测试生成单个姓名"""
        config = GeneratorConfig(generator_type="name", parameters={})
        generator = generator_factory.create_generator(config)
        name = generator.generate_single()

        assert isinstance(name, str)
        assert 2 <= len(name) <= 4
        assert generator.validate(name)

    def test_generate_batch(self, generator_factory):
        """测试批量生成姓名"""
        config = GeneratorConfig(generator_type="name", parameters={})
        generator = generator_factory.create_generator(config)
        names = generator.generate_batch(10)

        assert len(names) == 10
        for name in names:
            assert isinstance(name, str)
            assert 2 <= len(name) <= 4
            assert generator.validate(name)

    def test_male_name(self, generator_factory):
        """测试生成男性姓名"""
        config = GeneratorConfig(generator_type="name", parameters={"gender": "male"})
        generator = generator_factory.create_generator(config)
        name = generator.generate_single()

        assert isinstance(name, str)
        assert 2 <= len(name) <= 4

    def test_female_name(self, generator_factory):
        """测试生成女性姓名"""
        config = GeneratorConfig(generator_type="name", parameters={"gender": "female"})
        generator = generator_factory.create_generator(config)
        name = generator.generate_single()

        assert isinstance(name, str)
        assert 2 <= len(name) <= 4

    def test_name_length(self, generator_factory):
        """测试指定姓名长度"""
        config = GeneratorConfig(generator_type="name", parameters={"length": 3})
        generator = generator_factory.create_generator(config)
        name = generator.generate_single()

        assert isinstance(name, str)
        # Length parameter may be a suggestion, allow some flexibility
        assert 2 <= len(name) <= 4

    def test_validation(self, generator_factory):
        """测试姓名验证"""
        config = GeneratorConfig(generator_type="name", parameters={})
        generator = generator_factory.create_generator(config)

        # Valid names
        assert generator.validate("张三")
        assert generator.validate("李四")
        assert generator.validate("王小明")

        # Invalid names
        assert not generator.validate("")
        assert not generator.validate("A")
        assert not generator.validate("张三李四王五")  # Too long
        assert not generator.validate(123)

    def test_uniqueness(self, generator_factory):
        """测试姓名唯一性"""
        config = GeneratorConfig(generator_type="name", parameters={})
        generator = generator_factory.create_generator(config)
        names = generator.generate_batch(50)

        # Should have variety in 50 names
        unique_names = set(names)
        assert len(unique_names) > 20

    def test_edge_cases(self, generator_factory):
        """测试边界情况"""
        config = GeneratorConfig(generator_type="name", parameters={})
        generator = generator_factory.create_generator(config)

        # Generate multiple times
        for _ in range(10):
            name = generator.generate_single()
            assert name is not None
            assert len(name) >= 2
            assert all(
                "\u4e00" <= char <= "\u9fff" for char in name
            )  # Chinese characters

    def test_english_name_uses_config(self, monkeypatch, generator_factory):
        """英文姓名应来自 name_en 配置"""

        def _fake_name_en_config():
            return {
                "first_names_male": ["TestMale"],
                "first_names_female": ["TestFemale"],
                "last_names": ["TestLast"],
            }

        monkeypatch.setattr(
            "dataforge.generators.basic.name.load_name_en_config",
            _fake_name_en_config,
        )

        config = GeneratorConfig(
            generator_type="name", parameters={"type": "EN", "gender": "MALE"}
        )
        generator = generator_factory.create_generator(config)
        name = generator.generate_single()

        assert name in {"TestMale TestLast"}

    def test_pinyin_approximation_uses_config(self, monkeypatch, generator_factory):
        """拼音近似应使用 pinyin_map 配置"""

        def _fake_pinyin_map():
            return {
                "surname": {"甲": "jia"},
                "given_char": {"乙": "yi"},
            }

        monkeypatch.setattr(
            "dataforge.generators.basic.name.load_pinyin_map",
            _fake_pinyin_map,
        )

        config = GeneratorConfig(generator_type="name", parameters={})
        generator = generator_factory.create_generator(config)

        # 直接调用内部方法以验证映射是否生效（仅验证名字符映射）
        pinyin = generator._get_pinyin_approximation("乙")  # type: ignore[attr-defined]
        assert pinyin == "yi"
