"""
婚姻状况生成器最终测试
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

import pytest

from dataforge.generators.basic.marital_status import (
    GenericMaritalStatusGenerator,
    MaritalStatusGenerator,
)


class TestMaritalStatusGenerator:
    """测试婚姻状况生成器"""

    def test_china_options(self):
        """测试中国婚姻状况选项"""
        generator = MaritalStatusGenerator({"region": "china"})
        options = generator._get_marital_status_options()
        expected = ["未婚", "已婚", "离异", "丧偶", "再婚"]
        assert options == expected

    def test_international_options(self):
        """测试国际婚姻状况选项"""
        generator = MaritalStatusGenerator({"region": "us"})
        options = generator._get_marital_status_options()
        expected = ["single", "married", "divorced", "widowed", "separated"]
        assert options == expected

    def test_age_based_weights_young(self):
        """测试年轻人权重"""
        generator = MaritalStatusGenerator({"include_age_factor": True})
        weights = generator._age_based_weights(18)
        assert weights[0] > 0.8  # 未婚率应该很高

    def test_age_based_weights_middle(self):
        """测试中年人权重"""
        generator = MaritalStatusGenerator({"include_age_factor": True})
        weights = generator._age_based_weights(35)
        assert weights[1] > 0.6  # 已婚率应该很高

    def test_age_based_weights_old(self):
        """测试老年人权重"""
        generator = MaritalStatusGenerator({"include_age_factor": True})
        weights = generator._age_based_weights(60)
        assert weights[3] > 0.05  # 丧偶率应该增加

    def test_default_weights(self):
        """测试默认权重"""
        generator = MaritalStatusGenerator({"include_age_factor": False})
        weights = generator._age_based_weights(None)
        assert sum(weights) == 1.0

    def test_generate_with_age_context(self):
        """测试带有年龄上下文的生成"""
        generator = MaritalStatusGenerator({"region": "china", "include_age_factor": True})

        class MockContext:
            def __init__(self, age):
                self.related_data = {"age": age}

        # 测试不同年龄
        for age in [20, 30, 40, 50]:
            context = MockContext(age)
            result = generator._generate_raw(context)
            assert result in generator._get_marital_status_options()

    def test_generate_with_birth_year_context(self):
        """测试带有出生年份上下文的生成"""
        generator = MaritalStatusGenerator({"region": "china", "include_age_factor": True})

        class MockContext:
            def __init__(self, birth_year):
                self.related_data = {"birth_year": birth_year}

        context = MockContext(1990)
        result = generator._generate_raw(context)
        assert result in generator._get_marital_status_options()

    def test_validate_china(self):
        """测试中国婚姻状况验证"""
        generator = MaritalStatusGenerator({"region": "china"})

        # 有效值
        valid_values = ["未婚", "已婚", "离异", "丧偶", "再婚"]
        for value in valid_values:
            assert generator.validate(value) is True

        # 无效值
        invalid_values = ["single", "invalid", ""]
        for value in invalid_values:
            assert generator.validate(value) is False

    def test_validate_international(self):
        """测试国际婚姻状况验证"""
        generator = MaritalStatusGenerator({"region": "us"})

        # 有效值
        valid_values = ["single", "married", "divorced", "widowed", "separated"]
        for value in valid_values:
            assert generator.validate(value) is True

        # 无效值
        invalid_values = ["未婚", "invalid", ""]
        for value in invalid_values:
            assert generator.validate(value) is False

class TestGenericMaritalStatusGenerator:
    """测试通用婚姻状况生成器"""

    def test_setup_default(self):
        """测试默认设置"""
        generator = GenericMaritalStatusGenerator({})
        assert generator.region == "international"
        assert generator.include_age_factor is True

    def test_setup_custom(self):
        """测试自定义设置"""
        generator = GenericMaritalStatusGenerator({
            "region": "china",
            "include_age_factor": False
        })
        assert generator.region == "china"
        assert generator.include_age_factor is False

    def test_generate_raw(self):
        """测试原始生成"""
        generator = GenericMaritalStatusGenerator({"region": "china"})

        class MockContext:
            def __init__(self):
                self.related_data = {"age": 30}

        context = MockContext()
        result = generator._generate_raw(context)
        assert result in generator._get_marital_status_options()

    def test_validate(self):
        """测试验证"""
        generator = GenericMaritalStatusGenerator({"region": "china"})

        # 有效值
        assert generator.validate("未婚") is True
        assert generator.validate("已婚") is True

        # 无效值
        assert generator.validate("invalid") is False

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
