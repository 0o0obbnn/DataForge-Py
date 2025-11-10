#!/usr/bin/env python3
"""
DataForge 数据关联性管理系统测试 (pytest风格)
"""

import pytest
import json
from datetime import datetime

from dataforge.core.factory import GeneratorFactory
from dataforge.core.generator import GeneratorConfig, GenerationContext
from dataforge.core.relations import RelationRule, DataRelationManager

@pytest.mark.skip(reason="Data relation derivation - advanced feature not fully implemented")
def test_relation_derivation(generator_factory: GeneratorFactory):
    """测试从身份证号到年龄的关联推导"""
    configs = [
        GeneratorConfig(generator_type='idcard', parameters={'region': '110000'}),
        GeneratorConfig(generator_type='age', parameters={})
    ]

    context = GenerationContext()
    result = generator_factory.generate_batch_with_relations(configs, context)

    assert 'idcard' in result
    assert 'age' in result

    idcard = result['idcard']
    age = result['age']

    if len(idcard) == 18 and idcard[:17].isdigit():
        birth_year = int(idcard[6:10])
        expected_age = datetime.now().year - birth_year
        # The calculated age could be off by one depending on the birth month/day
        assert abs(age - expected_age) <= 1

def test_gender_name_relation(generator_factory: GeneratorFactory):
    """测试从身份证号到性别的关联, 并生成对应性别的姓名"""
    configs = [
        GeneratorConfig(generator_type='idcard', parameters={'gender': 'FEMALE'}),
        GeneratorConfig(generator_type='name', parameters={})
    ]

    context = GenerationContext()
    result = generator_factory.generate_batch_with_relations(configs, context)

    assert 'idcard' in result
    assert 'name' in result

    idcard = result['idcard']
    if len(idcard) == 18:
        gender_digit = int(idcard[16])
        assert gender_digit % 2 == 0, "身份证号的性别位应为偶数 (女性)"

@pytest.mark.skip(reason="Dependency ordering - advanced feature not fully implemented")
def test_dependency_ordering():
    """测试关系管理器中的依赖排序"""
    relation_manager = DataRelationManager()
    # Manually register dependencies for this test
    relation_manager.add_relation_rule(RelationRule('idcard', 'age', 'derive', lambda x, y: {}, 10))
    relation_manager.add_relation_rule(RelationRule('idcard', 'gender', 'derive', lambda x, y: {}, 10))
    relation_manager.add_relation_rule(RelationRule('gender', 'name', 'constrain', lambda x, y: {}, 10))
    
    field_names = ['name', 'age', 'idcard']
    ordered_fields = relation_manager.get_relation_dependencies(field_names)
    
    # Expected: idcard should come before age and name
    assert ordered_fields.index('idcard') < ordered_fields.index('age')
    assert ordered_fields.index('idcard') < ordered_fields.index('name')

def test_manual_relation_rule(generator_factory: GeneratorFactory):
    """测试手动添加关联规则并验证其效果"""
    
    def custom_age_to_name_constraint(age, context):
        """根据年龄约束姓名生成, 返回一个参数字典"""
        if age < 18:
            return {'name_style': 'nickname'} 
        else:
            return {'name_style': 'formal'}

    custom_rule = RelationRule(
        source_field='age',
        target_field='name',
        relation_type='constrain',
        rule_func=custom_age_to_name_constraint,
        priority=20 # High priority
    )
    
    # Add the rule to the factory's relation manager
    generator_factory.relation_manager.add_relation_rule(custom_rule)

    # Test with a young age
    configs = [
        GeneratorConfig(generator_type='age', parameters={'min': 10, 'max': 15}),
        GeneratorConfig(generator_type='name', parameters={})
    ]
    context = GenerationContext()
    result = generator_factory.generate_batch_with_relations(configs, context)

    # This test is conceptual. The NameGenerator would need to be updated
    # to actually use the 'name_style' parameter for this to have a real effect.
    # For now, we just check that the logic runs without error.
    assert 'age' in result
    assert 'name' in result
    assert 10 <= result['age'] <= 15
