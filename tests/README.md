# DataForge 测试指南

**最后更新**: 2025-01-07

---

## 目录结构

```
tests/
├── unit/                      # 单元测试
│   ├── test_core/            # 核心模块测试
│   ├── test_generators/      # 生成器单元测试
│   │   ├── test_basic/
│   │   ├── test_contact/
│   │   ├── test_datetime/
│   │   ├── test_network/
│   │   ├── test_identifier/
│   │   ├── test_finance/
│   │   ├── test_text/
│   │   └── test_numeric/
│   ├── test_output/          # 输出格式化测试
│   └── test_utils/           # 工具函数测试
├── integration/              # 集成测试
│   ├── test_api/            # API 集成测试
│   └── test_cli/            # CLI 集成测试
├── e2e/                      # 端到端测试
├── performance/              # 性能测试
├── fixtures/                 # 测试固定数据
├── archive/                  # 历史测试归档
└── conftest.py              # pytest 配置
```

---

## 运行测试

### 运行所有测试
```bash
pytest tests/
```

### 运行单元测试
```bash
pytest tests/unit/
```

### 运行特定模块测试
```bash
# 测试核心模块
pytest tests/unit/test_core/

# 测试生成器
pytest tests/unit/test_generators/test_basic/

# 测试 API
pytest tests/integration/test_api/
```

### 运行带标记的测试
```bash
# 只运行单元测试
pytest tests/ -m unit

# 只运行集成测试
pytest tests/ -m integration

# 只运行 API 测试
pytest tests/ -m api
```

### 生成覆盖率报告
```bash
# 终端报告
pytest --cov=dataforge --cov-report=term-missing

# HTML 报告
pytest --cov=dataforge --cov-report=html

# 查看报告
start htmlcov/index.html
```

### 详细输出
```bash
# 显示详细信息
pytest tests/ -v

# 显示打印输出
pytest tests/ -s

# 显示失败的详细信息
pytest tests/ -vv
```

---

## 编写测试

### 测试命名规范

**文件命名**:
- 格式: `test_<module_name>.py`
- 示例: `test_email.py`, `test_bankcard.py`

**测试函数命名**:
- 格式: `test_<feature>_<scenario>`
- 示例:
  ```python
  def test_email_generation_with_custom_domain():
      pass

  def test_bankcard_luhn_validation():
      pass
  ```

**测试类命名** (可选):
- 格式: `Test<ModuleName>`
- 示例:
  ```python
  class TestEmailGenerator:
      def test_generate_single(self):
          pass
  ```

### 使用 Fixtures

```python
import pytest
from dataforge.core.generator import GeneratorConfig

@pytest.mark.unit
def test_email_generation(generator_factory):
    """测试邮箱生成"""
    config = GeneratorConfig(
        generator_type="email",
        parameters={"domain_type": "REAL"}
    )
    generator = generator_factory.create_generator(config)
    email = generator.generate_single()

    assert email
    assert "@" in email
    assert generator.validate(email)
```

### 添加测试标记

```python
import pytest

@pytest.mark.unit
def test_unit_feature():
    """单元测试"""
    pass

@pytest.mark.integration
def test_integration_feature():
    """集成测试"""
    pass

@pytest.mark.slow
def test_slow_operation():
    """慢速测试"""
    pass
```

### 测试模板

```python
import pytest
from dataforge.core.generator import GeneratorConfig

@pytest.mark.unit
class TestModuleGenerator:
    """模块生成器测试"""

    def test_generate_single(self, generator_factory):
        """测试生成单个数据"""
        config = GeneratorConfig(
            generator_type="module_name",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        result = generator.generate_single()

        assert result is not None
        assert generator.validate(result)

    def test_generate_batch(self, generator_factory):
        """测试批量生成"""
        config = GeneratorConfig(
            generator_type="module_name",
            parameters={}
        )
        generator = generator_factory.create_generator(config)
        results = generator.generate_batch(10)

        assert len(results) == 10
        for result in results:
            assert generator.validate(result)

    def test_with_parameters(self, generator_factory):
        """测试带参数生成"""
        config = GeneratorConfig(
            generator_type="module_name",
            parameters={"param": "value"}
        )
        generator = generator_factory.create_generator(config)
        result = generator.generate_single()

        # 验证参数效果
        assert result is not None
```

---

## 可用 Fixtures

### 核心 Fixtures

- `generator_factory`: 生成器工厂实例
- `empty_registry`: 空的生成器注册表
- `populated_registry`: 预填充的生成器注册表
- `project_root`: 项目根目录路径
- `test_data_dir`: 测试数据目录路径
- `test_fixtures_dir`: 测试固定数据目录路径

### 使用示例

```python
def test_with_fixtures(generator_factory, test_data_dir):
    """使用多个 fixtures"""
    # 使用工厂创建生成器
    config = GeneratorConfig(generator_type="test", parameters={})
    generator = generator_factory.create_generator(config)

    # 使用测试数据目录
    data_file = test_data_dir / "sample.json"
    # ...
```

---

## 测试覆盖率目标

| 模块 | 目标覆盖率 |
|-----|-----------|
| 核心模块 (core/) | 100% |
| 生成器 (generators/) | 90% |
| 输出模块 (output/) | 90% |
| 工具函数 (utils/) | 85% |
| **总体** | **80%** |

---

## 常见问题

### Q: 如何跳过某个测试？
```python
@pytest.mark.skip(reason="暂时跳过")
def test_feature():
    pass
```

### Q: 如何标记预期失败的测试？
```python
@pytest.mark.xfail(reason="已知问题")
def test_known_issue():
    pass
```

### Q: 如何参数化测试？
```python
@pytest.mark.parametrize("input,expected", [
    ("test@example.com", True),
    ("invalid-email", False),
])
def test_email_validation(input, expected):
    assert validate_email(input) == expected
```

### Q: 如何测试异常？
```python
def test_exception():
    with pytest.raises(ValueError):
        raise ValueError("test error")
```

---

## 持续集成

测试在以下情况自动运行:
- 每次 push 到主分支
- 每次创建 Pull Request
- 每天定时运行

CI 要求:
- 所有测试必须通过
- 覆盖率不低于 80%
- 无 linting 错误

---

## 贡献指南

1. 为新功能编写测试
2. 确保所有测试通过
3. 保持测试覆盖率
4. 遵循命名规范
5. 添加适当的测试标记

---

## 相关文档

- [测试重组计划](../docs/plans/TEST_REORGANIZATION_PLAN_2025-01-07.md)
- [项目贡献指南](../CONTRIBUTING.md)
- [代码规范](../docs/guides/REGISTRATION_STANDARDS.md)

---

**维护者**: DataForge Team
**问题反馈**: https://github.com/dataforge/dataforge/issues
