"""
婚姻状况生成器测试
"""

import pytest

from dataforge.core.generator import GenerationContext, GeneratorConfig, GeneratorType
from dataforge.generators.basic.marital_status import (
    MaritalStatusGenerator,
)


class TestMaritalStatusGenerator:
    """婚姻状况生成器测试类"""

    def test_china_options(self):
        """测试中国婚姻状况选项"""
        config = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "china"}
        )
        generator = MaritalStatusGenerator(config)
        options = generator._get_marital_status_options()
        expected = ["未婚", "已婚", "离异", "丧偶", "再婚"]
        assert options == expected

    def test_international_options(self):
        """测试国际婚姻状况选项"""
        config = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "us"}
        )
        generator = MaritalStatusGenerator(config)
        options = generator._get_marital_status_options()
        expected = ["single", "married", "divorced", "widowed", "separated"]
        assert options == expected

    def test_age_based_weights_young(self):
        """测试年轻人婚姻状况权重"""
        config = GeneratorConfig(
            generator_type="marital_status", parameters={"include_age_factor": True}
        )
        generator = MaritalStatusGenerator(config)
        weights = generator._age_based_weights(18)
        assert weights[0] > 0.8  # 未婚权重应该很高

    def test_age_based_weights_middle(self):
        """测试中年人婚姻状况权重"""
        config = GeneratorConfig(
            generator_type="marital_status", parameters={"include_age_factor": True}
        )
        generator = MaritalStatusGenerator(config)
        weights = generator._age_based_weights(35)
        assert weights[1] > 0.6  # 已婚权重应该很高

    def test_age_based_weights_senior(self):
        """测试老年人婚姻状况权重"""
        config = GeneratorConfig(
            generator_type="marital_status", parameters={"include_age_factor": True}
        )
        generator = MaritalStatusGenerator(config)
        weights = generator._age_based_weights(60)
        assert weights[3] > 0.05  # 丧偶权重应该增加

    def test_generate_single(self):
        """测试单个生成"""
        config = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "china"}
        )
        generator = MaritalStatusGenerator(config)
        result = generator.generate_single()
        assert result in ["未婚", "已婚", "离异", "丧偶", "再婚"]

    def test_generate_with_age_context(self):
        """测试带年龄上下文的生成"""
        config = GeneratorConfig(
            generator_type="marital_status",
            parameters={"region": "china", "include_age_factor": True},
        )
        generator = MaritalStatusGenerator(config)
        context = GenerationContext(related_data={"age": 25})
        result = generator.generate_single(context)
        assert result in ["未婚", "已婚", "离异", "丧偶", "再婚"]

    def test_generate_with_birth_year_context(self):
        """测试带出生年份上下文的生成"""
        config = GeneratorConfig(
            generator_type="marital_status",
            parameters={"region": "china", "include_age_factor": True},
        )
        generator = MaritalStatusGenerator(config)
        context = GenerationContext(related_data={"birth_year": 1990})
        result = generator.generate_single(context)
        assert result in ["未婚", "已婚", "离异", "丧偶", "再婚"]

    def test_validate_valid_china(self):
        """测试有效中国婚姻状况验证"""
        config = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "china"}
        )
        generator = MaritalStatusGenerator(config)
        assert generator.validate("已婚") is True
        assert generator.validate("离异") is True

    def test_validate_invalid_china(self):
        """测试无效中国婚姻状况验证"""
        config = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "china"}
        )
        generator = MaritalStatusGenerator(config)
        assert generator.validate("married") is False
        assert generator.validate("invalid") is False

    def test_validate_valid_international(self):
        """测试有效国际婚姻状况验证"""
        config = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "us"}
        )
        generator = MaritalStatusGenerator(config)
        assert generator.validate("married") is True
        assert generator.validate("single") is True

    def test_validate_invalid_international(self):
        """测试无效国际婚姻状况验证"""
        config = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "us"}
        )
        generator = MaritalStatusGenerator(config)
        assert generator.validate("已婚") is False
        assert generator.validate("invalid") is False

    def test_generator_type(self):
        """测试生成器类型"""
        config = GeneratorConfig(generator_type="marital_status", parameters={})
        generator = MaritalStatusGenerator(config)
        assert generator.generator_type == GeneratorType.BASIC

    def test_supported_parameters(self):
        """测试支持的参数"""
        config = GeneratorConfig(generator_type="marital_status", parameters={})
        generator = MaritalStatusGenerator(config)
        params = generator.supported_parameters
        assert "region" in params
        assert "include_age_factor" in params


class TestGenericMaritalStatusGenerator:
    """通用婚姻状况生成器测试类"""

    def test_setup_default(self):
        """测试默认设置"""
        config = GeneratorConfig(generator_type="marital_status", parameters={})
        generator = MaritalStatusGenerator(config)
        assert generator.region == "china"
        assert generator.include_age_factor is True

    def test_setup_custom(self):
        """测试自定义设置"""
        config = GeneratorConfig(
            generator_type="marital_status",
            parameters={"region": "us", "include_age_factor": False},
        )
        generator = MaritalStatusGenerator(config)
        assert generator.region == "us"
        assert generator.include_age_factor is False

    def test_generate_raw(self):
        """测试原始生成"""
        config = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "china"}
        )
        generator = MaritalStatusGenerator(config)
        result = generator.generate_single()
        assert result in ["未婚", "已婚", "离异", "丧偶", "再婚"]

    def test_validate(self):
        """测试验证"""
        config = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "china"}
        )
        generator = MaritalStatusGenerator(config)
        assert generator.validate("已婚") is True
        assert generator.validate("invalid") is False


if __name__ == "__main__":
    pytest.main([__file__])
