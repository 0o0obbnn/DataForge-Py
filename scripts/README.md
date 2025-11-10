# DataForge 测试脚本

本目录包含用于运行和管理DataForge项目测试的实用脚本。

## 📋 脚本列表

### 1. run_tests.py - 统一测试运行脚本

运行项目的各种测试。

#### 基本用法

```bash
# 运行所有测试
python scripts/run_tests.py

# 只运行单元测试
python scripts/run_tests.py --unit

# 只运行集成测试
python scripts/run_tests.py --integration

# 只运行性能测试
python scripts/run_tests.py --performance

# 只运行安全测试
python scripts/run_tests.py --security

# 只运行端到端测试
python scripts/run_tests.py --e2e

# 只运行压力测试
python scripts/run_tests.py --stress
```

#### 高级选项

```bash
# 运行测试并生成覆盖率报告
python scripts/run_tests.py --coverage

# 详细输出
python scripts/run_tests.py --verbose

# 遇到第一个失败就停止
python scripts/run_tests.py --failfast

# 按标记运行测试
python scripts/run_tests.py --markers unit

# 按关键字运行测试
python scripts/run_tests.py --keyword "test_name"
```

### 2. check_coverage.py - 覆盖率检查脚本

检查测试覆盖率并验证是否达到最低要求。

#### 基本用法

```bash
# 检查覆盖率（默认最低80%）
python scripts/check_coverage.py

# 设置自定义最低覆盖率阈值
python scripts/check_coverage.py --min 85

# 生成详细HTML报告
python scripts/check_coverage.py --report

# 只分析现有报告，不运行测试
python scripts/check_coverage.py --skip-tests
```

#### 输出示例

```
📊 总体覆盖率:
  行覆盖率: 85.23%
  分支覆盖率: 78.45%
  覆盖行数: 3421/4012

✅ 覆盖率达标 (>= 80%)

📦 模块覆盖率:
  ✅ dataforge.core: 92.34%
  ✅ dataforge.generators: 87.56%
  ⚠️ dataforge.utils: 75.23%
```

### 3. test_report.py - 测试报告生成脚本

生成各种格式的测试报告。

#### 基本用法

```bash
# 生成文本格式报告（默认）
python scripts/test_report.py

# 生成HTML格式报告
python scripts/test_report.py --format html

# 生成JSON格式报告
python scripts/test_report.py --format json

# 保存报告到文件
python scripts/test_report.py --format html --output report.html
```

#### 报告格式

**文本格式**:
```
============================================================
  DataForge 测试报告
============================================================

📊 测试统计:
  总测试数: 796
  收集时间: 2025-11-08T15:30:00

🧪 测试结果:
  ✅ 通过: 790
  ❌ 失败: 0
  ⏭️  跳过: 6
  ⚠️  错误: 0

✅ 所有测试通过！
```

**HTML格式**: 生成美观的HTML报告，包含图表和统计信息

**JSON格式**: 机器可读的JSON格式，便于集成到其他工具

## 🔧 CI/CD集成

项目包含GitHub Actions工作流配置：

### test.yml - 持续测试

在每次push和pull request时自动运行：
- 多Python版本测试（3.9-3.13）
- 多操作系统测试（Ubuntu, Windows, macOS）
- 代码质量检查（ruff, black, mypy）
- 覆盖率检查

### release.yml - 发布流程

在创建版本标签时自动运行：
- 运行完整测试套件
- 构建分发包
- 发布到PyPI
- 创建GitHub Release

## 📊 覆盖率报告

覆盖率报告会生成在以下位置：

- **HTML报告**: `htmlcov/index.html`
- **XML报告**: `coverage.xml`
- **终端输出**: 运行测试时直接显示

## 🎯 最佳实践

### 开发时

```bash
# 快速运行单元测试
python scripts/run_tests.py --unit -v

# 运行特定测试
python scripts/run_tests.py -k "test_name_generator"

# 检查覆盖率
python scripts/check_coverage.py
```

### 提交前

```bash
# 运行所有测试
python scripts/run_tests.py

# 检查覆盖率
python scripts/check_coverage.py --min 80

# 生成报告
python scripts/test_report.py --format html --output test_report.html
```

### CI/CD

GitHub Actions会自动运行所有测试，无需手动操作。

## 🐛 故障排除

### 问题：测试运行失败

```bash
# 详细输出查看错误
python scripts/run_tests.py --verbose

# 遇到第一个失败就停止，便于调试
python scripts/run_tests.py --failfast
```

### 问题：覆盖率报告不存在

```bash
# 先运行测试生成覆盖率
python scripts/run_tests.py --coverage

# 然后检查覆盖率
python scripts/check_coverage.py --skip-tests
```

### 问题：某些测试很慢

```bash
# 跳过性能测试和压力测试
python scripts/run_tests.py --unit --integration
```

## 📚 更多信息

- 测试组织计划: `docs/plans/test_organization_plan_2025-11-07.md`
- 测试报告: `docs/reports/`
- pytest文档: https://docs.pytest.org/

## 🤝 贡献

如果你想改进这些脚本：

1. 修改脚本文件
2. 测试你的更改
3. 更新此README
4. 提交Pull Request

---

**最后更新**: 2025-11-08
