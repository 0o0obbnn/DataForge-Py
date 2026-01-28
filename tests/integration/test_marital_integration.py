"""
婚姻状况生成器完整测试

测试婚姻状况生成器的所有功能，包括中国和国际婚姻状况选项、
年龄相关权重、数据生成和验证等。
"""

import os
import sys

import pytest

# 确保能够导入项目模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from typing import cast

from dataforge.core.generator import GenerationContext, GeneratorConfig
from dataforge.generators.basic.marital_status import MaritalStatusGenerator


class TestMaritalStatusGenerator:
    """测试婚姻状况生成器的核心功能"""

    def test_china_options(self) -> None:
        """测试中国婚姻状况选项"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "china"}
        )
        generator = cast(MaritalStatusGenerator, MaritalStatusGenerator(config))
        options: list[str] = generator.get_marital_status_options()
        expected: list[str] = ["未婚", "已婚", "离异", "丧偶", "再婚"]
        assert options == expected

    def test_international_options(self) -> None:
        """测试国际婚姻状况选项"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "us"}
        )
        generator = cast(MaritalStatusGenerator, MaritalStatusGenerator(config))
        options: list[str] = generator.get_marital_status_options()
        expected: list[str] = ["single", "married", "divorced", "widowed", "separated"]
        assert options == expected

    def test_age_based_weights_young(self) -> None:
        """测试年轻人权重分布"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status", parameters={"include_age_factor": True}
        )
        generator = cast(MaritalStatusGenerator, MaritalStatusGenerator(config))
        weights: list[float] = generator.get_age_based_weights(18)
        assert weights[0] > 0.8  # 未婚率应该很高

    def test_age_based_weights_middle(self) -> None:
        """测试中年人权重分布"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status", parameters={"include_age_factor": True}
        )
        generator = cast(MaritalStatusGenerator, MaritalStatusGenerator(config))
        weights: list[float] = generator.get_age_based_weights(35)
        assert weights[1] > 0.6  # 已婚率应该很高

    def test_age_based_weights_old(self) -> None:
        """测试老年人权重分布"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status", parameters={"include_age_factor": True}
        )
        generator = cast(MaritalStatusGenerator, MaritalStatusGenerator(config))
        weights: list[float] = generator.get_age_based_weights(60)
        assert weights[3] > 0.05  # 丧偶率应该增加

    def test_default_weights(self) -> None:
        """测试默认权重分布"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status", parameters={"include_age_factor": False}
        )
        generator = cast(MaritalStatusGenerator, MaritalStatusGenerator(config))
        weights: list[float] = generator.get_age_based_weights(None)
        total_weight: float = sum(weights)
        assert abs(total_weight - 1.0) < 0.001  # 权重总和应该为1

    def test_generate_with_age_context(self) -> None:
        """测试带有年龄上下文的数据生成"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status",
            parameters={"region": "china", "include_age_factor": True},
        )
        generator = cast(MaritalStatusGenerator, MaritalStatusGenerator(config))
        valid_options: list[str] = generator.get_marital_status_options()

        # 测试不同年龄段的生成
        test_ages: list[int] = [20, 30, 40, 50]
        for age in test_ages:
            context: GenerationContext = GenerationContext(related_data={"age": age})
            result: str = generator.generate_single(context)
            assert result in valid_options

    def test_generate_with_birth_year_context(self) -> None:
        """测试带有出生年份上下文的数据生成"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status",
            parameters={"region": "china", "include_age_factor": True},
        )
        generator = cast(MaritalStatusGenerator, MaritalStatusGenerator(config))
        valid_options: list[str] = generator.get_marital_status_options()

        context: GenerationContext = GenerationContext(
            related_data={"birth_year": 1990}
        )
        result: str = generator.generate_single(context)
        assert result in valid_options

    def test_validate_china(self) -> None:
        """测试中国婚姻状况数据验证"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "china"}
        )
        generator = cast(MaritalStatusGenerator, MaritalStatusGenerator(config))

        # 测试有效值
        valid_values: list[str] = ["未婚", "已婚", "离异", "丧偶", "再婚"]
        for value in valid_values:
            assert generator.validate(value) is True

        # 测试无效值
        invalid_values: list[str] = ["single", "invalid", "", "   "]
        for value in invalid_values:
            assert generator.validate(value) is False

    def test_validate_international(self) -> None:
        """测试国际婚姻状况数据验证"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "us"}
        )
        generator = cast(MaritalStatusGenerator, MaritalStatusGenerator(config))

        # 测试有效值
        valid_values: list[str] = [
            "single",
            "married",
            "divorced",
            "widowed",
            "separated",
        ]
        for value in valid_values:
            assert generator.validate(value) is True

        # 测试无效值
        invalid_values: list[str] = ["未婚", "invalid", "", "   "]
        for value in invalid_values:
            assert generator.validate(value) is False


class TestMaritalStatusGeneratorAdvanced:
    """测试婚姻状况生成器的高级功能"""

    def test_setup_default(self) -> None:
        """测试默认配置的生成器设置"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status", parameters={}
        )
        generator = cast(MaritalStatusGenerator, MaritalStatusGenerator(config))
        assert generator is not None
        assert generator.region == "china"  # 默认为中国
        assert generator.include_age_factor is True  # 默认包含年龄因子

    def test_setup_custom(self) -> None:
        """测试自定义配置的生成器设置"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status",
            parameters={"region": "us", "include_age_factor": False},
        )
        generator = cast(MaritalStatusGenerator, MaritalStatusGenerator(config))
        assert generator is not None
        assert generator.region == "us"
        assert generator.include_age_factor is False

    def test_generate_without_context(self) -> None:
        """测试无上下文的数据生成"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "china"}
        )
        generator = cast(MaritalStatusGenerator, MaritalStatusGenerator(config))
        valid_options: list[str] = generator.get_marital_status_options()

        result: str = generator.generate_single()
        assert isinstance(result, str)
        assert result in valid_options

    def test_generate_with_empty_context(self) -> None:
        """测试空上下文的数据生成"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "china"}
        )
        generator: MaritalStatusGenerator = MaritalStatusGenerator(config)
        valid_options: list[str] = generator.get_marital_status_options()

        context: GenerationContext = GenerationContext(related_data={})
        result: str = generator.generate_single(context)
        assert isinstance(result, str)
        assert result in valid_options

    def test_validate_edge_cases(self) -> None:
        """测试验证功能的边界情况"""
        config: GeneratorConfig = GeneratorConfig(
            generator_type="marital_status", parameters={"region": "china"}
        )
        generator: MaritalStatusGenerator = MaritalStatusGenerator(config)

        # 测试生成的数据能通过验证
        for _ in range(10):
            result: str = generator.generate_single()
            assert generator.validate(result) is True

        # 测试非字符串类型
        assert generator.validate(123) is False  # type: ignore[arg-type]
        assert generator.validate(None) is False  # type: ignore[arg-type]
        assert generator.validate([]) is False  # type: ignore[arg-type]


if __name__ == "__main__":
    # 运行测试时忽略未使用的调用结果警告
    _ = pytest.main([__file__, "-v"])
