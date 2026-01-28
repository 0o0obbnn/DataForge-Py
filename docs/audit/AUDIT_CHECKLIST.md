# DataForge 审计改进检查清单

使用此清单跟踪改进进度。完成每项任务后，将`[ ]`改为`[x]`。

---

## Phase 1: 紧急清理 (Day 1-2)

### 代码库清理
- [x] 删除所有.bak文件 (`find dataforge -name "*.bak" -delete`)
- [x] 删除所有.bak2文件 (`find dataforge -name "*.bak2" -delete`)
- [x] 更新.gitignore添加`*.bak`和`*.bak2`
- [x] 验证无备份文件 (`find dataforge -name "*.bak*"` 返回空)
- [ ] 提交更改 (`git commit -m "chore: remove backup files"`)

### 代码格式化
- [x] 运行isort排序导入 (`isort dataforge/ tests/`)
- [x] 运行black格式化 (`black dataforge/ tests/`)
- [x] 运行ruff自动修复 (`ruff check --fix dataforge/ tests/`)
- [x] 手动修复剩余107个ruff问题（修复了195个问题）
- [x] 验证格式正确 (`ruff check dataforge/` 无错误)
- [x] 验证black通过 (`black --check dataforge/` 无错误)
- [ ] 提交更改 (`git commit -m "style: auto-fix formatting"`)

### Python版本修复
- [ ] 决定版本策略（升级到3.10+或移除新语法）
- [ ] 更新pyproject.toml中的`requires-python`
- [ ] 更新tool.black的`target-version`
- [ ] 更新tool.mypy的`python_version`
- [ ] 修复或移除3.10+语法（如`X | Y` union）
- [ ] 验证版本一致性
- [ ] 提交更改 (`git commit -m "fix: unify Python version requirements"`)

### 测试文件清理
- [ ] 移除`dataforge/generators/advanced/test_advanced_timestamp.py`
- [ ] 重命名`tests/integration/integration_test.py`为`test_integration.py`
- [ ] 重命名`tests/integration/validation_test.py`为`test_validation.py`
- [ ] 验证测试可被发现 (`pytest --collect-only`)
- [ ] 提交更改 (`git commit -m "test: fix test file structure"`)

---

## Phase 2: 类型安全 (Day 3-7)

### 安装类型存根
- [ ] 安装types-redis (`pip install types-redis`)
- [ ] 安装types-pytz (`pip install types-pytz`)
- [ ] 安装types-PyYAML (`pip install types-PyYAML`)
- [ ] 安装types-python-dateutil (`pip install types-python-dateutil`)
- [ ] 更新pyproject.toml添加类型存根依赖
- [ ] 提交更改 (`git commit -m "chore: add type stubs"`)

### 修复utils模块
- [ ] 修复`dataforge/utils/validation.py`类型注解
- [ ] 移除`dataforge/utils/validation.py`不可达代码
- [ ] 添加`dataforge/utils/validation.py`函数docstring
- [ ] 修复`dataforge/utils/helpers.py`类型注解
- [ ] 移除`dataforge/utils/helpers.py`不可达代码
- [ ] 验证mypy通过 (`mypy dataforge/utils/`)
- [ ] 提交更改 (`git commit -m "fix(types): add type annotations to utils"`)

### 修复output模块
- [ ] 修复`dataforge/output/sql.py`类型注解
- [ ] 修复`dataforge/output/sql.py`的Optional参数
- [ ] 修复`dataforge/output/csv.py`类型注解
- [ ] 修复`dataforge/output/json.py`类型注解
- [ ] 修复`dataforge/output/xml.py`类型注解和Optional
- [ ] 移除`dataforge/output/xml.py`不可达代码
- [ ] 修复`dataforge/output/formatter.py`类型注解
- [ ] 修复`dataforge/output/formatter.py`的DictWriter问题
- [ ] 验证mypy通过 (`mypy dataforge/output/`)
- [ ] 提交更改 (`git commit -m "fix(types): add type annotations to output"`)

### 修复core模块
- [ ] 修复`dataforge/core/redis_client.py`类型注解
- [ ] 移除`dataforge/core/redis_client.py`未使用的导入
- [ ] 修复`dataforge/core/cache.py`类型注解
- [ ] 修复`dataforge/core/cache.py`的类型推断问题
- [ ] 修复`dataforge/core/relations.py`类型注解
- [ ] 修复`dataforge/core/context.py`类型注解
- [ ] 修复`dataforge/core/logging_config.py`的Handler类型
- [ ] 修复`dataforge/core/factory.py`类型注解
- [ ] 移除`dataforge/core/factory.py`不可达代码
- [ ] 更新`dataforge/core/factory.py`使用内置type
- [ ] 验证mypy通过 (`mypy dataforge/core/`)
- [ ] 提交更改 (`git commit -m "fix(types): add type annotations to core"`)

### 修复generators模块
- [ ] 修复`dataforge/generators/advanced/datetime.py`类型注解
- [ ] 移除`dataforge/generators/advanced/datetime.py`不可达代码
- [ ] 修复`dataforge/generators/advanced/enhanced_timestamp.py`
- [ ] 移除不可达代码
- [ ] 修复其他generators模块的类型问题
- [ ] 验证mypy通过 (`mypy dataforge/generators/`)
- [ ] 提交更改 (`git commit -m "fix(types): add type annotations to generators"`)

### 配置mypy严格模式
- [ ] 更新pyproject.toml放宽全局mypy设置
- [ ] 为core模块启用严格模式
- [ ] 为output模块启用严格模式
- [ ] 为utils模块启用严格模式
- [ ] 验证配置正确 (`mypy dataforge/`)
- [ ] 提交更改 (`git commit -m "chore: configure mypy strict mode"`)

---

## Phase 3: 测试改进 (Day 8-12)

### 测试覆盖率基线
- [ ] 运行测试生成覆盖率 (`pytest --cov=dataforge --cov-report=html`)
- [ ] 查看HTML报告 (`htmlcov/index.html`)
- [ ] 记录当前覆盖率百分比: _____%
- [ ] 识别未覆盖的关键模块
- [ ] 创建覆盖率提升计划

### 核心模块测试
- [ ] 为`dataforge/core/generator.py`添加单元测试
- [ ] 为`dataforge/core/factory.py`添加单元测试
- [ ] 为`dataforge/core/exceptions.py`添加单元测试
- [ ] 为`dataforge/core/validator.py`添加单元测试
- [ ] 为`dataforge/core/cache.py`添加单元测试
- [ ] 验证core模块覆盖率>90%
- [ ] 提交更改 (`git commit -m "test: improve core module coverage"`)

### Output模块测试
- [ ] 为`dataforge/output/sql.py`添加测试
- [ ] 为`dataforge/output/csv.py`添加测试
- [ ] 为`dataforge/output/json.py`添加测试
- [ ] 为`dataforge/output/xml.py`添加测试
- [ ] 为`dataforge/output/formatter.py`添加测试
- [ ] 验证output模块覆盖率>90%
- [ ] 提交更改 (`git commit -m "test: improve output module coverage"`)

### Utils模块测试
- [ ] 为`dataforge/utils/validation.py`添加测试
- [ ] 为`dataforge/utils/helpers.py`添加测试
- [ ] 验证utils模块覆盖率>90%
- [ ] 提交更改 (`git commit -m "test: improve utils module coverage"`)

### 集成测试
- [ ] 审查现有集成测试
- [ ] 添加缺失的集成测试场景
- [ ] 验证所有生成器集成测试通过
- [ ] 提交更改 (`git commit -m "test: enhance integration tests"`)

### 最终验证
- [ ] 运行完整测试套件 (`pytest tests/`)
- [ ] 验证总体覆盖率>90%
- [ ] 生成覆盖率徽章
- [ ] 更新README添加覆盖率徽章

---

## Phase 4: 文档改进 (Day 13-15)

### Docstring审计
- [ ] 安装interrogate (`pip install interrogate`)
- [ ] 运行docstring检查 (`interrogate -v dataforge/`)
- [ ] 记录当前docstring覆盖率: _____%
- [ ] 识别缺失docstring的模块

### Core模块文档
- [ ] 为`dataforge/core/generator.py`添加docstring
- [ ] 为`dataforge/core/factory.py`添加docstring
- [ ] 为`dataforge/core/exceptions.py`添加docstring
- [ ] 为`dataforge/core/validator.py`添加docstring
- [ ] 验证core模块docstring覆盖率>90%
- [ ] 提交更改 (`git commit -m "docs: add docstrings to core module"`)

### Output模块文档
- [ ] 为output模块所有公共函数添加docstring
- [ ] 验证docstring格式符合Google style
- [ ] 添加使用示例
- [ ] 提交更改 (`git commit -m "docs: add docstrings to output module"`)

### Utils模块文档
- [ ] 为utils模块所有公共函数添加docstring
- [ ] 添加使用示例
- [ ] 提交更改 (`git commit -m "docs: add docstrings to utils module"`)

### Generators模块文档
- [ ] 为主要生成器添加docstring
- [ ] 添加参数说明和示例
- [ ] 提交更改 (`git commit -m "docs: add docstrings to generators"`)

### API文档生成
- [ ] 安装Sphinx (`pip install sphinx sphinx-rtd-theme`)
- [ ] 初始化Sphinx (`sphinx-quickstart`)
- [ ] 配置conf.py
- [ ] 生成API文档 (`sphinx-apidoc -o docs/source/ dataforge/`)
- [ ] 构建HTML文档 (`make html`)
- [ ] 验证文档可访问
- [ ] 提交更改 (`git commit -m "docs: generate API documentation"`)

### 用户文档
- [ ] 审查README.md完整性
- [ ] 添加更多使用示例
- [ ] 更新CONTRIBUTING.md
- [ ] 创建或更新CHANGELOG.md
- [ ] 提交更改 (`git commit -m "docs: improve user documentation"`)

---

## Phase 5: 安全与性能 (Day 16-18)

### 安全扫描
- [ ] 安装安全工具 (`pip install bandit pip-audit safety`)
- [ ] 运行bandit扫描 (`bandit -r dataforge/ -ll`)
- [ ] 记录发现的问题数量: _____
- [ ] 修复Critical级别安全问题
- [ ] 修复High级别安全问题
- [ ] 运行pip-audit (`pip-audit`)
- [ ] 更新有漏洞的依赖
- [ ] 运行safety检查 (`safety check`)
- [ ] 验证无安全问题
- [ ] 提交更改 (`git commit -m "security: fix security issues"`)

### 性能基准
- [ ] 创建性能基准测试文件
- [ ] 为核心生成器添加基准测试
- [ ] 运行基准测试 (`pytest tests/performance/ --benchmark-only`)
- [ ] 保存基准结果 (`--benchmark-save=baseline`)
- [ ] 记录关键性能指标
- [ ] 提交更改 (`git commit -m "perf: establish performance benchmarks"`)

### 性能优化
- [ ] 使用cProfile分析性能瓶颈
- [ ] 识别慢速函数
- [ ] 优化关键路径
- [ ] 验证性能提升
- [ ] 提交更改 (`git commit -m "perf: optimize critical paths"`)

### 异步支持
- [ ] 审查异步API使用
- [ ] 扩展异步生成器支持
- [ ] 添加异步批量生成
- [ ] 添加异步测试
- [ ] 提交更改 (`git commit -m "feat: enhance async support"`)

---

## 最终验证

### 代码质量
- [ ] Ruff检查通过 (`ruff check dataforge/` 无错误)
- [ ] Black检查通过 (`black --check dataforge/` 无错误)
- [ ] Isort检查通过 (`isort --check dataforge/` 无错误)

### 类型安全
- [ ] Mypy检查通过 (`mypy dataforge/` 无错误)
- [ ] 类型注解覆盖率>95%

### 测试
- [ ] 所有测试通过 (`pytest tests/`)
- [ ] 测试覆盖率>90%
- [ ] 无跳过的测试

### 安全
- [ ] Bandit扫描通过（无中高级别问题）
- [ ] Pip-audit通过（无已知漏洞）
- [ ] Safety检查通过

### 文档
- [ ] Docstring覆盖率>90%
- [ ] API文档生成成功
- [ ] README完整且最新

### 构建与发布
- [ ] 包构建成功 (`python -m build`)
- [ ] 本地安装成功 (`pip install -e .`)
- [ ] CLI命令可用 (`dataforge --version`)
- [ ] 所有入口点正常工作

---

## 持续改进

### CI/CD集成
- [ ] 添加GitHub Actions工作流
- [ ] 配置自动测试
- [ ] 配置自动类型检查
- [ ] 配置自动安全扫描
- [ ] 配置自动发布

### Pre-commit钩子
- [ ] 安装pre-commit (`pip install pre-commit`)
- [ ] 创建.pre-commit-config.yaml
- [ ] 配置black、ruff、mypy钩子
- [ ] 安装钩子 (`pre-commit install`)
- [ ] 测试钩子 (`pre-commit run --all-files`)

### 监控与维护
- [ ] 设置依赖更新提醒
- [ ] 设置安全漏洞监控
- [ ] 建立定期审计计划（每月/每季度）
- [ ] 创建维护文档

---

## 进度统计

**Phase 1**: [x] 14/15 完成 (93%)  
**Phase 2**: [ ] 0/30 完成  
**Phase 3**: [ ] 0/20 完成  
**Phase 4**: [ ] 0/25 完成  
**Phase 5**: [ ] 0/15 完成  
**最终验证**: [ ] 0/15 完成  
**持续改进**: [ ] 0/10 完成  

**总进度**: 0/130 (0%)

---

## 时间记录

| Phase | 开始日期 | 完成日期 | 实际用时 | 计划用时 |
|-------|---------|---------|---------|---------|
| Phase 1 | | | | 1-2天 |
| Phase 2 | | | | 3-5天 |
| Phase 3 | | | | 3-5天 |
| Phase 4 | | | | 2-3天 |
| Phase 5 | | | | 2-3天 |
| **总计** | | | | **11-18天** |

---

## 备注

使用此区域记录遇到的问题、解决方案和经验教训：

```
日期: 
问题: 
解决方案: 
经验: 

---

日期: 
问题: 
解决方案: 
经验: 
```

---

**检查清单版本**: 1.0  
**创建日期**: 2025-11-21  
**最后更新**: 2025-11-21
