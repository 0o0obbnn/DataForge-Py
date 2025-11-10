"""
测试上下文感知生成器
"""

import json

from dataforge.core.context import GenerationContext
from dataforge.generators.basic.enhanced_generators import PersonDataGenerator


def test_basic_context():
    """测试基础上下文功能"""
    print("=== 测试基础上下文功能 ===")

    context = GenerationContext()

    # 存储数据
    context.set("name", "张三", {"gender": "male", "age": 25})
    context.set("age", 25, {"group": "young_adult"})

    # 获取数据
    name = context.get("name")
    age = context.get("age")

    print(f"姓名: {name}")
    print(f"年龄: {age}")
    print(f"上下文快照: {json.dumps(context.snapshot(), indent=2, ensure_ascii=False)}")

    assert name == "张三"
    assert age == 25
    print("✓ 基础上下文测试通过\n")


def test_dependency_management():
    """测试依赖管理"""
    print("=== 测试依赖管理 ===")

    context = GenerationContext()

    # 添加依赖关系
    context.add_dependency("email", "name")  # 邮箱依赖姓名
    context.add_dependency("id_card", "name")  # 身份证依赖姓名
    context.add_dependency("id_card", "age")  # 身份证依赖年龄

    # 检查依赖
    deps = context.get_dependencies("email")
    print(f"邮箱的依赖: {deps}")

    order = context.get_generation_order()
    print(f"生成顺序: {order}")

    assert "name" in deps
    print("✓ 依赖管理测试通过\n")


def test_person_data_generator():
    """测试个人数据综合生成器"""
    print("=== 测试个人数据综合生成器 ===")

    generator = PersonDataGenerator()

    # 生成单个个人数据
    person_data = generator.generate_person()

    print("生成的个人数据:")
    print(json.dumps(person_data, indent=2, ensure_ascii=False))

    # 验证数据结构
    assert "data" in person_data
    assert "context" in person_data
    assert "generation_order" in person_data

    # 验证字段
    data = person_data["data"]
    required_fields = ["name", "age", "id_card", "phone", "email"]
    for field in required_fields:
        assert field in data, f"缺少字段: {field}"

    print("✓ 个人数据生成器测试通过\n")


def test_batch_generation():
    """测试批量生成"""
    print("=== 测试批量生成 ===")

    generator = PersonDataGenerator()

    # 批量生成3个人
    batch_data = generator.generate_batch(3)

    print(f"批量生成 {len(batch_data)} 个人")

    for i, person in enumerate(batch_data):
        print(f"第 {i + 1} 个人:")
        print(f"  姓名: {person['data']['name']}")
        print(f"  年龄: {person['data']['age']}")
        print(f"  身份证: {person['data']['id_card']}")
        print(f"  生成顺序: {person['generation_order']}")

    assert len(batch_data) == 3
    assert all("data" in person for person in batch_data)
    print("✓ 批量生成测试通过\n")


def test_context_consistency():
    """测试上下文一致性"""
    print("=== 测试上下文一致性 ===")

    generator = PersonDataGenerator()

    # 生成数据
    result = generator.generate_person()

    # 验证身份证年龄与上下文年龄的一致性
    id_card = result["data"]["id_card"]
    birth_year = int(id_card[6:10])
    current_year = 2024  # 假设当前年份
    calculated_age = current_year - birth_year

    context_age = result["data"]["age"]

    print(f"上下文年龄: {context_age}")
    print(f"身份证计算年龄: {calculated_age}")
    print(f"差异: {abs(calculated_age - context_age)}")

    # 年龄差异在合理范围内（±3岁，考虑生日月份差异）
    assert abs(calculated_age - context_age) <= 3
    print("✓ 上下文一致性测试通过\n")


if __name__ == "__main__":
    try:
        test_basic_context()
        test_dependency_management()
        test_person_data_generator()
        test_batch_generation()
        test_context_consistency()

        print("🎉 所有测试通过！")

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback

        traceback.print_exc()
