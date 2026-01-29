# DataForge 上下文感知数据生成系统

## 概述

DataForge上下文感知数据生成系统是一个智能的数据生成框架，能够根据业务上下文、依赖关系和一致性要求生成高质量的结构化数据。系统采用工厂模式和上下文驱动设计，确保生成的数据既符合业务规则又保持一致性。

## 核心架构

### 1. 上下文管理 (GenerationContext)
- **功能**: 集中管理数据生成过程中的所有上下文信息
- **特性**:
  - 键值存储：存储任意业务上下文数据
  - 元数据追踪：记录数据来源、置信度、类型等信息
  - 依赖管理：定义字段间的依赖关系，自动生成正确顺序
  - 验证机制：确保数据完整性和一致性

### 2. 生成器工厂 (GeneratorFactory)
- **功能**: 统一创建和管理各类数据生成器
- **特性**:
  - 动态生成器创建：根据配置动态实例化生成器
  - 注册机制：支持自定义生成器注册
  - 生命周期管理：统一管理生成器实例

### 3. 增强生成器 (Enhanced Generators)
- **功能**: 提供上下文感知的数据生成能力
- **包含组件**:
  - EnhancedNameGenerator: 智能姓名生成
  - EnhancedAgeGenerator: 年龄生成（考虑上下文）
  - EnhancedIDCardGenerator: 身份证生成（与姓名年龄匹配）
  - EnhancedPhoneGenerator: 手机号生成
  - EnhancedEmailGenerator: 邮箱生成（基于姓名和公司）

### 4. 个人数据生成器 (PersonDataGenerator)
- **功能**: 综合生成完整的个人档案数据
- **特性**:
  - 一键生成：姓名、年龄、身份证、手机、邮箱
  - 上下文集成：自动使用现有上下文信息
  - 批量生成：支持批量数据生成
  - 生成顺序：按依赖关系自动排序

## 使用指南

### 基础使用

#### 1. 简单数据生成
```python
from dataforge.generators.basic.enhanced_generators import PersonDataGenerator

# 创建生成器
person_gen = PersonDataGenerator()

# 生成单条数据
person_data = person_gen.generate_person()
print(person_data['data'])  # 生成的数据
print(person_data['context'])  # 上下文信息
```

#### 2. 上下文感知生成
```python
from dataforge.core.context import GenerationContext
from dataforge.generators.basic.enhanced_generators import PersonDataGenerator

# 创建上下文
context = GenerationContext()
context.set('company', 'DataForge', {'type': 'organization'})
context.set('department', 'Engineering', {'type': 'department'})

# 使用上下文生成数据
person_gen = PersonDataGenerator(external_context=context)
person_data = person_gen.generate_person()

# 验证上下文集成
assert 'company' in person_data['context']['data']
```

#### 3. 批量生成
```python
# 批量生成5条记录
batch_data = person_gen.generate_batch(5)
for record in batch_data:
    print(record['data']['name'], record['data']['email'])
```

### 高级功能

#### 1. 依赖关系管理
```python
context = GenerationContext()

# 定义依赖关系：邮箱需要姓名和年龄
context.add_dependency('email', 'name')
context.add_dependency('email', 'age')

# 自动生成会按正确顺序执行
order = context.get_generation_order()
print(order)  # ['name', 'age', 'email', ...]
```

#### 2. 数据一致性验证
```python
context = GenerationContext()

# 设置已知信息
context.set('name', '张三', {'source': 'user_input', 'confidence': 0.95})
context.set('age', 28, {'source': 'user_input', 'confidence': 0.95})

# 生成器会使用已知信息，不会重新生成
person_gen = PersonDataGenerator(external_context=context)
person_data = person_gen.generate_person()

assert person_data['data']['name'] == '张三'
assert person_data['data']['age'] == 28
```

#### 3. 工厂模式集成
```python
from dataforge.core.factory import default_factory, GeneratorConfig

# 使用工厂创建生成器
config = GeneratorConfig(generator_type='name', parameters={})
name_gen = default_factory.create_generator(config)

# 在上下文中使用
data = name_gen.generate(context)
```

## 业务场景示例

### 1. 员工数据生成
```python
# 创建企业上下文
context = GenerationContext()
context.set('company', 'TechCorp')
context.set('department', 'Engineering')
context.set('office', 'Beijing')

# 生成员工数据
person_gen = PersonDataGenerator(external_context=context)
employees = person_gen.generate_batch(100)

# 所有员工都有统一的公司和部门信息
```

### 2. 客户档案生成
```python
# 创建客户上下文
context = GenerationContext()
context.set('customer_type', 'VIP')
context.set('region', 'Shanghai')
context.set('acquisition_channel', 'social_media')

# 生成VIP客户数据
vip_customers = person_gen.generate_batch(50)
```

### 3. 测试数据生成
```python
# 创建测试上下文
context = GenerationContext()
context.set('test_suite', 'integration_test')
context.set('data_version', 'v1.2')

# 生成测试数据
test_data = person_gen.generate_batch(1000)
```

## 数据质量保证

### 1. 一致性检查
- **字段一致性**: 确保相关字段数据匹配（如身份证与年龄）
- **格式一致性**: 确保数据格式符合规范
- **业务一致性**: 确保符合业务规则

### 2. 完整性验证
- **必填字段**: 确保所有必填字段都有值
- **依赖验证**: 确保依赖关系完整
- **上下文验证**: 确保上下文信息完整

### 3. 可追溯性
- **元数据记录**: 记录每个字段的来源和生成逻辑
- **版本追踪**: 记录数据生成版本和规则版本
- **审计日志**: 记录生成过程中的关键决策

## 扩展指南

### 1. 添加自定义生成器
```python
from dataforge.core.generator import DataGenerator

class CustomGenerator(DataGenerator):
    def generate_single(self, context):
        # 实现自定义生成逻辑
        value = self._generate_value()
        return value

# 注册到工厂
default_factory.register('custom', CustomGenerator)
```

### 2. 扩展上下文功能
```python
class BusinessContext(GenerationContext):
    def add_business_rule(self, rule_name, rule_config):
        # 添加业务规则
        pass

    def validate_business_rules(self):
        # 验证业务规则
        pass
```

### 3. 集成外部数据源
```python
class DatabaseContext(GenerationContext):
    def load_from_database(self, query):
        # 从数据库加载上下文
        pass

    def sync_with_api(self, api_endpoint):
        # 与API同步数据
        pass
```

## 性能优化

### 1. 批量处理优化
- **连接池**: 复用数据库连接
- **缓存机制**: 缓存常用数据
- **并行处理**: 支持并行数据生成

### 2. 内存管理
- **对象池**: 重用生成器实例
- **垃圾回收**: 及时清理无用对象
- **内存监控**: 监控内存使用情况

### 3. 配置优化
- **参数调优**: 根据业务需求调整参数
- **规则优化**: 优化生成规则和算法
- **缓存策略**: 制定合适的缓存策略

## 最佳实践

### 1. 上下文设计
- **分层设计**: 按业务域分层管理上下文
- **版本控制**: 对上下文进行版本管理
- **文档化**: 详细记录上下文结构和用途

### 2. 生成策略
- **渐进生成**: 按依赖关系逐步生成
- **回退机制**: 提供生成失败时的回退方案
- **验证检查**: 每个步骤后进行验证

### 3. 监控和调试
- **日志记录**: 详细记录生成过程
- **性能监控**: 监控生成性能指标
- **错误处理**: 完善的错误处理和恢复机制

## 故障排除

### 常见问题

#### 1. 上下文数据未生效
- **检查**: 确认使用了external_context参数
- **验证**: 检查上下文键名是否正确
- **调试**: 打印上下文内容进行确认

#### 2. 依赖关系错误
- **检查**: 确认依赖关系定义正确
- **验证**: 检查循环依赖
- **调试**: 打印生成顺序进行确认

#### 3. 数据不一致
- **检查**: 确认上下文数据优先级
- **验证**: 检查生成器实现
- **调试**: 对比上下文和生成结果

## 总结

DataForge上下文感知数据生成系统提供了：

1. **智能化**: 根据上下文智能调整生成策略
2. **一致性**: 确保数据间的一致性和完整性
3. **可扩展**: 支持自定义生成器和业务规则
4. **可追溯**: 完整的元数据和审计追踪
5. **高性能**: 优化的批量生成和缓存机制

通过合理使用本系统，可以大大提高测试数据、业务数据生成的质量和效率，同时确保数据符合实际业务需求。
