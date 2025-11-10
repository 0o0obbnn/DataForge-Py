# DataForge 项目整理分类清理计划

**文档日期**: 2025-01-07  
**文档类型**: 项目重组计划（仅设计，不执行）  
**目标**: 建立清晰的项目结构，消除技术债务，提升可维护性

---

## 一、项目现状分析

### 1.1 目录结构问题

**根目录混乱**（100+ 文件）:
- 大量临时测试文件（test_*.py, e2e_test*.py, integration_test*.py）
- 重复的导出文件（test_export_*.csv/json/sql/xml，40+ 个）
- 重复的模板文件（template_template_*.json，28+ 个）
- 多份报告文档散落根目录（*_REPORT.md, *审查报告*.md，20+ 个）
- 临时脚本与正式代码混杂

**AI 配置目录过多**（8 个）:
- `.amazonq/`, `.augment/`, `.claude/`, `.cursor/`, `.genkit/`, `.lingma/`, `.serena/`, `.trae/`
- 规则文件重复定义（python-expert, pycoder, pythoncoder）

**缓存目录未忽略**:
- `.mypy_cache/`, `.ruff_cache/` 应在 .gitignore 中

**文档分散**:
- `docs/` 下有文档
- `claudedocs/` 单独存在
- 根目录大量 markdown 文档

### 1.2 代码质量问题

**生成器契约不一致**:
- 部分生成器未正确实现 `generate_single(context: GenerationContext)`
- 存在访问未定义属性（`_generate_raw`, `validator`）
- 方法签名与基类不匹配

**测试结构混乱**:
- `tests/` 下有结构化目录
- 根目录有大量独立测试文件
- `scripts/backup_tests_*/` 存在备份测试

**重复代码**:
- 多个 `fix_*.py` 脚本功能重叠
- 审计脚本分散在 scripts/ 和根目录

---

## 二、目标目录结构

```
data_forge_py/
├── .github/                    # CI/CD 配置
│   ├── workflows/
│   └── copilot-instructions.md
├── .vscode/                    # 统一 IDE 配置（可选）
├── docs/                       # 所有文档
│   ├── architecture/          # 架构设计
│   ├── guides/                # 使用指南
│   ├── reports/               # 历史报告归档
│   ├── plans/                 # 计划文档
│   └── api/                   # API 文档
├── scripts/                    # 维护脚本
│   ├── maintenance/           # 日常维护
│   ├── migration/             # 迁移脚本
│   └── archive/               # 历史脚本归档
├── openspec/                   # OpenSpec 规范
│   ├── specs/
│   └── changes/
├── dataforge/                  # 源代码
│   ├── core/                  # 核心模块
│   ├── generators/            # 生成器
│   ├── api/                   # API 接口
│   ├── cli/                   # 命令行
│   ├── config/                # 配置
│   ├── data/                  # 数据资源
│   ├── output/                # 输出格式化
│   └── utils/                 # 工具函数
├── tests/                      # 测试代码
│   ├── unit/                  # 单元测试
│   ├── integration/           # 集成测试
│   ├── e2e/                   # 端到端测试
│   ├── performance/           # 性能测试
│   └── fixtures/              # 测试数据
├── web-console/                # 前端控制台
├── examples/                   # 示例代码
├── .ai-rules/                  # AI 助手规则（统一）
├── .gitignore
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
└── requirements-dev.txt
```

---

## 三、分批整理计划

### 批次 0: 基线建立（准备阶段）

**目标**: 建立清理基线，确保可回滚

**任务**:
1. 创建完整的文件清单
2. 识别重复文件（hash 对比）
3. 标记临时文件与正式文件
4. 备份当前状态到分支

**输出**:
- `docs/reports/baseline_inventory_2025-01-07.md`
- `docs/reports/duplicate_files_2025-01-07.md`

---

### 批次 1: 根目录清理

**目标**: 清理根目录，保留核心配置文件

**移动规则**:

| 当前位置 | 目标位置 | 数量 |
|---------|---------|------|
| `*_REPORT.md`, `*审查*.md` | `docs/reports/` | 20+ |
| `*_PLAN*.md`, `*计划*.md` | `docs/plans/` | 5+ |
| `test_*.py` (根目录) | `tests/archive/` 或删除 | 15+ |
| `e2e_test*.py`, `integration_test*.py` | `tests/archive/` | 5+ |
| `test_export_*.csv/json/sql/xml` | 删除（临时文件） | 40+ |
| `template_template_*.json` | 删除（临时文件） | 28+ |
| `fix_*.py`, `check_*.py` | `scripts/archive/` | 10+ |
| `comprehensive_test.py`, `demo.py` | `examples/` 或删除 | 5+ |

**保留文件**:
- README.md, LICENSE, CONTRIBUTING.md
- pyproject.toml, requirements*.txt
- .gitignore, .env.example
- start_api.py（移至 scripts/）

**验收标准**:
- 根目录文件数 < 15
- CI 全绿
- 文档链接有效

---

### 批次 2: AI 配置整合

**目标**: 统一 AI 助手配置，减少冗余

**整合方案**:
```
.ai-rules/
├── python-expert.md      # 合并 pycoder.md, python-pro.md, pythoncoder.md
├── api-designer.md
├── java-architect.md
└── project-rules.md
```

**删除目录**:
- `.amazonq/`, `.augment/`, `.cursor/`, `.lingma/`, `.serena/`, `.trae/`
- 保留 `.github/` 和 `.claude/`（如需要）

**验收标准**:
- AI 配置目录 ≤ 2 个
- 规则文件无重复内容

---

### 批次 3: 文档归档

**目标**: 统一文档管理，建立清晰分类

**归档规则**:

```
docs/
├── architecture/
│   ├── DataForge项目架构设计.md
│   ├── ARCHITECTURE_ASSESSMENT_2025-11-05.md
│   └── DEEP_DIVE_CRITICAL_ISSUES_2025-11-05.md
├── guides/
│   ├── CONTEXT_SYSTEM_GUIDE.md
│   ├── DATETIME_GENERATORS_GUIDE.md
│   ├── PERFORMANCE_OPTIMIZATION.md
│   └── 启动前后端项目并进行联调.md
├── reports/
│   ├── 2025-11/
│   │   ├── 项目后端审查报告_20251101.md
│   │   ├── AUDIT_RESULTS_SUMMARY_2025-11-05.md
│   │   └── ...
│   └── completion/
│       ├── WEEK1_DAY1_COMPLETION_REPORT.md
│       └── ...
├── plans/
│   ├── MASTER_REPAIR_ROADMAP_2025-11-05.md
│   ├── 修复方案与执行计划_20251103.md
│   └── PROJECT_REORGANIZATION_PLAN_2025-01-07.md
└── api/
    └── (API 文档)
```

**删除**:
- `claudedocs/`（合并到 docs/reports/）

**验收标准**:
- 所有文档在 docs/ 下
- 按类型和日期分类
- README 更新文档索引

---

### 批次 4: 测试结构规范

**目标**: 建立清晰的测试层次结构

**重组方案**:

```
tests/
├── unit/                      # 单元测试
│   ├── test_core/
│   ├── test_generators/
│   └── test_utils/
├── integration/               # 集成测试
│   ├── test_api/
│   ├── test_cli/
│   └── test_export_system.py
├── e2e/                       # 端到端测试
│   └── test_complete_workflow.py
├── performance/               # 性能测试
│   ├── test_cache_performance.py
│   └── test_streaming_performance.py
├── fixtures/                  # 测试数据
│   ├── test_api_request.json
│   └── sample_configs/
├── conftest.py
└── README.md
```

**清理**:
- 删除 `tests/generators/` 下的非测试文件（basic_old_script.py）
- 删除 `tests/data/` 下的临时导出文件
- 移除根目录的独立测试文件

**验收标准**:
- pytest 发现所有测试
- 测试覆盖率 > 80%
- 无重复测试

---

### 批次 5: 脚本整理

**目标**: 规范维护脚本，归档历史脚本

**分类方案**:

```
scripts/
├── maintenance/               # 日常维护
│   ├── audit_generator_registration.py
│   ├── check_generator_compliance.py
│   └── scan_code_quality.py
├── migration/                 # 数据迁移
│   └── (迁移脚本)
├── development/               # 开发辅助
│   ├── start_api.py
│   └── debug_*.py
└── archive/                   # 历史归档
    ├── fix_*.py
    ├── comprehensive_test_fix.py
    └── backup_tests_20250915_220050/
```

**删除**:
- `scripts/playwright-report/`（临时报告）
- `scripts/package*.json`（非 Python 项目）
- 重复的 fix 脚本

**验收标准**:
- 每个脚本有 docstring 说明用途
- 归档脚本不影响主流程

---

### 批次 6: 生成器代码规范

**目标**: 统一生成器接口，消除类型错误

**修复清单**:
1. 所有生成器实现 `generate_single(context: Optional[GenerationContext])`
2. 移除对未定义属性的访问（`_generate_raw`, `validator`）
3. 统一使用 `self.parameters` 而非 `self.config.parameters`
4. 验证方法签名与基类一致

**验收标准**:
- Pylance 类型错误 = 0
- mypy 检查通过
- 所有生成器测试通过

---

### 批次 7: 缓存与临时文件

**目标**: 清理缓存，更新 .gitignore

**清理**:
- 删除 `.mypy_cache/`, `.ruff_cache/`
- 删除 `htmlcov/`（覆盖率报告）
- 删除 `dataforge.egg-info/`（重新生成）

**更新 .gitignore**:
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
.mypy_cache/
.ruff_cache/
.pytest_cache/

# Coverage
htmlcov/
.coverage
coverage.xml

# Build
dist/
build/
*.egg-info/

# Temp
*.tmp
*.log
test_export_*
template_template_*

# IDE
.vscode/
.idea/

# Env
.env
.env.local
```

---

### 批次 8: 前端整理

**目标**: 规范前端项目结构

**检查项**:
- `web-console/` 结构符合 Vue 3 最佳实践
- tsconfig.json 配置正确
- 依赖版本一致

**验收标准**:
- `pnpm build` 成功
- ESLint 无错误
- TypeScript 编译通过

---

### 批次 9: CI/CD 配置

**目标**: 建立质量门禁

**GitHub Actions**:
```yaml
name: CI
on: [push, pull_request]
jobs:
  lint:
    - ruff check
    - mypy dataforge/
  test:
    - pytest --cov=dataforge --cov-report=xml
  build:
    - python -m build
```

**Pre-commit hooks**:
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
```

---

### 批次 10: 文档更新

**目标**: 更新所有文档，确保准确性

**更新清单**:
- README.md（项目介绍、快速开始）
- CONTRIBUTING.md（贡献指南）
- docs/guides/（使用指南）
- API 文档（自动生成）

**验收标准**:
- 文档链接无死链
- 示例代码可运行
- 安装步骤准确

---

## 四、风险控制

### 4.1 回滚策略

**每批次操作前**:
1. 创建 Git 分支：`reorganize-batch-N`
2. 记录变更映射表
3. 提交前运行完整测试

**回滚方法**:
```bash
git checkout main
git branch -D reorganize-batch-N
```

### 4.2 验证检查点

**每批次完成后**:
- [ ] CI 全绿
- [ ] 测试覆盖率未降低
- [ ] 文档链接有效
- [ ] 功能无回归

---

## 五、执行时间表

| 批次 | 任务 | 预计时间 | 风险等级 |
|-----|------|---------|---------|
| 0 | 基线建立 | 0.5 天 | 低 |
| 1 | 根目录清理 | 1 天 | 中 |
| 2 | AI 配置整合 | 0.5 天 | 低 |
| 3 | 文档归档 | 1 天 | 低 |
| 4 | 测试结构规范 | 1.5 天 | 中 |
| 5 | 脚本整理 | 0.5 天 | 低 |
| 6 | 生成器代码规范 | 2 天 | 高 |
| 7 | 缓存清理 | 0.5 天 | 低 |
| 8 | 前端整理 | 1 天 | 中 |
| 9 | CI/CD 配置 | 1 天 | 中 |
| 10 | 文档更新 | 1 天 | 低 |

**总计**: 约 11 天

---

## 六、度量指标

### 6.1 清理前

- 根目录文件数: 100+
- 临时文件数: 80+
- AI 配置目录: 8
- 文档分散度: 高
- 类型错误数: 50+

### 6.2 清理后目标

- 根目录文件数: < 15
- 临时文件数: 0
- AI 配置目录: ≤ 2
- 文档分散度: 低（统一在 docs/）
- 类型错误数: 0

---

## 七、附录

### A. 重复文件清单

**导出文件**（40+ 个）:
- test_export_YYYYMMDD_HHMMSS.{csv,json,sql,xml}

**模板文件**（28+ 个）:
- template_template_YYYYMMDD_HHMMSS.json
- template_template_company_YYYYMMDD_HHMMSS.json

**报告文件**（20+ 个）:
- *_REPORT.md
- *审查报告*.md
- WEEK*_DAY*_*.md

### B. 脚本功能重复

**修复脚本**:
- fix_generator_interface.py
- fix_generator_interfaces.py
- fix_validated_generator.py
- batch_fix_all_generators.py
- quick_fix_priority_generators.py

**测试修复**:
- comprehensive_test_fix.py
- simple_test_fix.py
- test_import_fixer.py

### C. 参考文档

- [Python 项目结构最佳实践](https://docs.python-guide.org/writing/structure/)
- [测试组织规范](https://docs.pytest.org/en/stable/goodpractices.html)
- [Git 工作流](https://www.atlassian.com/git/tutorials/comparing-workflows)

---

**文档状态**: 计划阶段，待审批  
**下一步**: 获得团队确认后，开始批次 0 执行
