DataForge 项目整理分类清理计划（2025-11-07）

注意：本文件仅为“设计与制定计划”，不在本次提交中执行任何实际移动/删除/修改操作

一、总体目标
- 建立清晰、可扩展、可测试的目录结构与命名规范
- 清理重复/过时代码与文档，消除技术债务与类型/注册隐患
- 在不影响现有功能的前提下，分阶段推进，批次化实施与回滚可控

二、指导原则
- 安全优先：每一批次均通过 CI（lint、type-check、unit/integration）全绿后再进入下一批
- 渐进推进：先规范、后迁移、再收敛，杜绝大爆炸式重构
- 契约一致：所有生成器遵循 [dataforge/core/generator.py](dataforge/core/generator.py) 的公共契约
- 文档先行：每批次输出“变更记录、影响评估、回滚说明”

三、当前问题概览（来自已观测现象）
- 目录层次混乱：脚本、文档、报告、示例与源码耦合在根目录
- 生成器契约不一致：签名覆写不兼容、访问未知属性（_generate、validator）
- 重复/临时文件较多：多份报告与一次性脚本散落
- 前端与后端规范不一：如 tsconfig 与 Python 规范缺乏统一标准

四、目标目录结构（不立即执行，仅规划）
- 根目录（项目元信息）
  - README.md、LICENSE、pyproject.toml、requirements*.txt、.env.example
  - .github/（CI 工作流）
  - docs/（手册、规范、报告归档）
  - scripts/（维护与工具脚本）
  - openspec/（OpenSpec 与 AGENTS 文档）
  - web-console/（前端）
  - tests/（单元/集成/端到端）
  - dataforge/（Python 源码）
- dataforge/
  - core/（核心契约与基础设施：context、generator、types、validator 等）
  - generators/
    - basic/、advanced/、numeric/、text/、finance/、network/、identifier/、contact/
  - data/（静态数据与加载器）
  - output/（导出器）
  - api/、cli/（对外接口与命令行）
  - utils/（通用工具）

五、命名与规范统一（计划落地）
- Python
  - 导入顺序与分组：标准库、第三方、本地；强制 [ruff](pyproject.toml) 检查
  - 类型检查：mypy 或 Pylance 等价通过；不可在方法签名中泄露扩展类型（如 ExtendedGenerationContext）
  - 生成器覆写规则：generate/generate_single 签名必须与基类一致；仅调用 _generate_raw
  - 注册规范：统一使用 [dataforge/core/factory.py](dataforge/core/factory.py) 的 @register_generator 装饰器；aliases 仅为 list[str]
- 前端
  - 构建以 Vite 为准；tsc noEmit 模式类型检查；路径别名 @ 指向 src
  - 约定 src 结构：app、components、features、pages、stores、api、utils、assets
- 文档
  - 归档到 docs/ 下，按分类：architecture、guides、reports、standards、plans
  - 报告文件命名规范：CATEGORY_YYYY-MM-DD.md

六、批次化执行计划（仅设计，不执行）
批次 0：基线盘点与风控
- 输出清单：目录树、重复文件报告、脏点列表（未知属性访问、签名不一致、随意注册等）
- 建议脚本：
  - 列出树与大小：python -m pip install treelib；或使用现有 [list_files 工具占位]
  - 重复/相似检测：hash + 路径聚合
  - 类型/风格：ruff check、mypy、pytest -q
- 验收标准：报告产出并归档到 docs/reports/

批次 1：根目录与文档收敛
- 将一批历史报告与一次性文档归档至 docs/reports
- README 精简并指向详细文档
- 不移动源码与测试
- 验收：CI 全绿、文档链接有效

批次 2：核心契约一致性（core）
- 审核与修订 [dataforge/core/generator.py](dataforge/core/generator.py)、[dataforge/core/context.py](dataforge/core/context.py)、[dataforge/core/types.py](dataforge/core/types.py)
- 统一 DataGenerator[T] 契约，禁止子类签名漂移，移除接口违背点
- 验收：类型检查零错误；生成器基于契约最小实现通过

批次 3：生成器树整顿（generators/*）
- 清理重复/危险覆写：删除顶层 shadow、未知属性访问；仅保留 _setup/_generate_raw/validate/supported_parameters
- 统一注册方式为装饰器；别名统一为英文复数或多语言等价短名
- 对每类生成器建立 README 简述与样例
- 验收：模块内 pytest 覆盖率≥80%，Pylance 报错 0

批次 4：数据资产与加载器（data/）
- dataforge/data 归档与说明：数据来源、许可证、体量预估、加载 API
- 严禁大文件入仓；建议通过下载器或可复现脚本生成
- 验收：加载器用例通过；数据路径通过配置注入

批次 5：API 与 CLI
- 规范 [dataforge/api](dataforge/api) 与 [dataforge/cli](dataforge/cli) 的入口与依赖注入
- 对外契约稳定化与版本化（语义化版本说明）
- 验收：接口回归通过；命令行帮助与示例可运行

批次 6：测试体系归并
- tests/ 下划分 unit / integration / e2e，统一命名 test_*.py
- 引入 fixtures 与 property-based 测试（hypothesis 可选）
- 覆盖率阈值 85% 起步，逐步提升
- 验收：覆盖率达标、无脆弱测试

批次 7：脚本区与自动化
- scripts/ 中只保留可复用、无副作用脚本；加 usage 说明
- 将一性迁移脚本移动至 scripts/archive/ 以备审计
- 验收：脚本静态检查通过；必要时改为 console_scripts

批次 8：前端 web-console
- 规范 src 结构与配置；[web-console/tsconfig.json](web-console/tsconfig.json) 维持 noEmit: true
- API 代理与跨域策略文档化；与后端路径约定
- 验收：pnpm build / vite build 成功；eslint/tsc 通过

批次 9：CI/CD 与质量门禁
- GitHub Actions：ruff、mypy、pytest、frontend typecheck/build
- pre-commit：ruff、codespell、end-of-file-fixer、trailing-whitespace
- 覆盖率阈值门禁；变更体积与大文件拦截
- 验收：CI 全流程通过

批次 10：文档与知识沉淀
- 维护 openspec 与架构决策记录（ADR）
- 迁移说明（开发者指南、升级指南）
- 验收：开发者可依文档完成环境搭建与贡献

七、分类与迁移规则（样例）
- 文档类：移动至 docs/（reports、guides、standards、plans）
- 一次性脚本：移动至 scripts/archive/
- 生成器：仅在通过契约统一与测试通过后再做物理移动
- 数据文件：统一放置 dataforge/data/，大文件走外链或可复现脚本
- 命名规范：下划线 snake_case，避免重名与多义

八、风险与回滚策略
- 每批次建立可回退分支与“变更映射表”
- 保持提交粒度小与消息规范，便于 bisect
- 对关键目录移动采用软迁移（复制+弃用标记）再在下一批次清理

九、度量与验收指标
- 静态检查：ruff 0 违规、类型检查 0 错误
- 测试：覆盖率≥85%，关键路径 100%
- 文档：每批产出计划、记录、影响、回滚四类文档

十、实施节奏（建议）
- 每批 0.5–1.5 天，期间冻结非必要功能变更
- 高风险批次安排 code owner 审核

附录 A：首轮扫描任务（不执行，仅列出）
- 生成器签名/覆写一致性扫描：匹配 generate/generate_single 与基类差异
- 寻找对未知属性的访问（_generate、validator 等）
- register_generator 调用有效性与 aliases 类型校验
- TODO/DEBUG/临时标记聚合

附录 B：后续可引入的自动化
- 统一 import 排序与格式化（ruff、isort 风格）
- mypy 严格度逐批提升（warn-return-any、disallow-untyped-defs）
- 生成器模板与脚手架（cookiecutter）减少人为偏差

交付物
- 本计划文件：[PROJECT_REORGANIZATION_PLAN_2025-11-07.md](PROJECT_REORGANIZATION_PLAN_2025-11-07.md)
- 各批次计划与报告：docs/plans/ 与 docs/reports/ 下创建（执行时再提交）

参考文件（示例，便于后续执行对齐）
- [dataforge/core/generator.py](dataforge/core/generator.py)
- [dataforge/core/factory.py](dataforge/core/factory.py)
- [dataforge/generators/text/chinese.py](dataforge/generators/text/chinese.py)
- [web-console/tsconfig.json](web-console/tsconfig.json)
- [pyproject.toml](pyproject.toml)
