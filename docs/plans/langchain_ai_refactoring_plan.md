# LangChain + 本地 AI 模型重构计划

## 执行摘要

本计划旨在将 DataForge 项目重构为支持 LangChain 和本地 AI 模型的智能数据生成框架。通过集成 AI 能力，提升数据生成的智能性、真实性和多样性，同时保持向后兼容性和高性能。

## 完成日期

计划制定日期: 2025-12-22

## 项目背景

### 当前状态

- ✅ 配置化迁移已完成（5个生成器已配置化）
- ✅ 稳定的生成器架构（DataGenerator 抽象基类）
- ✅ 工厂模式和注册机制完善
- ✅ LangChain 依赖已安装（pyproject.toml）
- ✅ 本地模型支持依赖已准备（ollama, transformers）

### 重构目标

1. **智能数据生成**: 使用 AI 模型生成更真实、更符合上下文的数据
2. **本地模型支持**: 支持 Ollama、本地 transformers 模型，保护数据隐私
3. **LangChain 集成**: 利用 LangChain 的链式编排和提示管理能力
4. **向后兼容**: 保持现有 API 不变，AI 功能作为增强选项
5. **性能优化**: 缓存 AI 生成结果，支持批量优化

---

## 架构设计

### 1. AI 生成器架构

```
DataGenerator (现有基类)
    ↓
AIGenerator (新增 AI 基类)
    ↓
LangChainGenerator (LangChain 实现)
    ├── LocalModelGenerator (Ollama/Transformers)
    ├── CloudModelGenerator (OpenAI/Anthropic)
    └── HybridGenerator (本地+云端混合)
```

### 2. 核心组件

#### 2.1 AI 模型管理器 (`dataforge/ai/models.py`)

**职责**:
- 统一管理 AI 模型实例（本地和云端）
- 模型加载和初始化
- 连接池管理
- 模型切换和降级

**设计要点**:
```python
class AIModelManager:
    """AI 模型管理器"""
    
    def __init__(self):
        self.local_models: dict[str, Any] = {}
        self.cloud_models: dict[str, Any] = {}
        self.default_model: str = "local"
    
    def get_model(self, model_name: str, provider: str = "auto") -> Any:
        """获取模型实例，支持自动降级"""
        pass
    
    def load_local_model(self, model_name: str, model_path: str = None):
        """加载本地模型（Ollama 或 Transformers）"""
        pass
```

#### 2.2 LangChain 链构建器 (`dataforge/ai/chains.py`)

**职责**:
- 构建 LangChain 提示链
- 管理提示模板
- 处理生成结果解析和验证

**设计要点**:
```python
class DataGenerationChain:
    """数据生成链"""
    
    def __init__(self, llm: BaseLLM, prompt_template: str):
        self.llm = llm
        self.prompt = PromptTemplate.from_template(prompt_template)
        self.chain = LLMChain(llm=llm, prompt=self.prompt)
    
    def generate(self, context: dict) -> str:
        """执行链式生成"""
        pass
    
    def generate_batch(self, contexts: list[dict]) -> list[str]:
        """批量生成（优化）"""
        pass
```

#### 2.3 AI 生成器基类 (`dataforge/generators/ai/base.py`)

**职责**:
- 定义 AI 生成器的通用接口
- 实现缓存和批量优化
- 处理 AI 生成错误和降级

**设计要点**:
```python
class AIGenerator(DataGenerator[T]):
    """AI 驱动的生成器基类"""
    
    def __init__(self, config: GeneratorConfig):
        super().__init__(config)
        self.model_manager = AIModelManager()
        self.cache = GenerationCache()
        self.fallback_generator: Optional[DataGenerator[T]] = None
    
    def generate_single(self, context: Optional[GenerationContext] = None) -> T:
        """AI 生成，失败时降级到传统生成器"""
        # 1. 检查缓存
        # 2. 构建提示
        # 3. 调用 AI 模型
        # 4. 解析和验证结果
        # 5. 缓存结果
        # 6. 失败时降级
        pass
```

---

## 实施计划

### 阶段一：基础设施搭建（3-5天）

#### 任务 1.1: AI 模型管理器实现

**目标**: 创建统一的 AI 模型管理基础设施

**任务清单**:
- [ ] 创建 `dataforge/ai/` 目录结构
- [ ] 实现 `AIModelManager` 类
- [ ] 集成 Ollama 客户端
- [ ] 集成 Transformers（HuggingFace）
- [ ] 实现模型连接池
- [ ] 添加模型健康检查
- [ ] 编写单元测试

**验收标准**:
- ✅ 可以成功加载本地 Ollama 模型
- ✅ 可以成功加载 Transformers 模型
- ✅ 支持模型切换和降级
- ✅ 单元测试覆盖率 ≥ 80%

#### 任务 1.2: LangChain 集成层

**目标**: 集成 LangChain 核心功能

**任务清单**:
- [ ] 创建 LangChain 适配器
- [ ] 实现提示模板管理
- [ ] 实现链式编排
- [ ] 添加输出解析器（Pydantic）
- [ ] 实现批量生成优化
- [ ] 编写单元测试

**验收标准**:
- ✅ 可以构建和执行 LangChain 链
- ✅ 支持提示模板变量替换
- ✅ 支持批量生成（并行）
- ✅ 单元测试覆盖率 ≥ 80%

#### 任务 1.3: 缓存和性能优化

**目标**: 实现 AI 生成结果缓存机制

**任务清单**:
- [ ] 实现生成结果缓存（基于提示+参数）
- [ ] 实现缓存失效策略
- [ ] 添加缓存统计和监控
- [ ] 编写单元测试

**验收标准**:
- ✅ 相同提示+参数返回缓存结果
- ✅ 缓存命中率可监控
- ✅ 缓存大小可配置
- ✅ 单元测试覆盖率 ≥ 80%

---

### 阶段二：AI 生成器实现（5-7天）

#### 任务 2.1: AI 生成器基类

**目标**: 创建 AI 生成器的抽象基类

**任务清单**:
- [ ] 创建 `AIGenerator` 基类
- [ ] 实现提示构建逻辑
- [ ] 实现结果解析和验证
- [ ] 实现降级机制（AI 失败时使用传统生成器）
- [ ] 编写单元测试

**验收标准**:
- ✅ `AIGenerator` 继承 `DataGenerator`
- ✅ 支持提示模板自定义
- ✅ AI 失败时自动降级
- ✅ 单元测试覆盖率 ≥ 80%

#### 任务 2.2: 智能姓名生成器（试点）

**目标**: 实现第一个 AI 驱动的生成器作为试点

**任务清单**:
- [ ] 创建 `AINameGenerator`
- [ ] 设计姓名生成提示模板
- [ ] 实现上下文感知（性别、地区）
- [ ] 集成传统生成器作为降级
- [ ] 编写单元测试和集成测试

**验收标准**:
- ✅ 可以生成符合上下文的姓名
- ✅ AI 失败时降级到传统生成器
- ✅ 性能满足要求（< 500ms/次，缓存后 < 10ms）
- ✅ 单元测试覆盖率 ≥ 85%

#### 任务 2.3: 智能地址生成器

**目标**: 实现 AI 驱动的地址生成

**任务清单**:
- [ ] 创建 `AIAddressGenerator`
- [ ] 设计地址生成提示模板
- [ ] 实现地区上下文感知
- [ ] 集成传统生成器作为降级
- [ ] 编写单元测试

**验收标准**:
- ✅ 可以生成符合地区的真实地址
- ✅ 支持批量生成优化
- ✅ 单元测试覆盖率 ≥ 85%

#### 任务 2.4: 智能文本生成器

**目标**: 实现 AI 驱动的文本生成（文章、段落等）

**任务清单**:
- [ ] 创建 `AITextGenerator`
- [ ] 设计文本生成提示模板
- [ ] 实现主题和风格控制
- [ ] 集成传统生成器作为降级
- [ ] 编写单元测试

**验收标准**:
- ✅ 可以生成符合主题的文本
- ✅ 支持多种文本类型（段落、文章等）
- ✅ 单元测试覆盖率 ≥ 85%

---

### 阶段三：高级功能（3-5天）

#### 任务 3.1: 上下文增强

**目标**: 利用 AI 增强上下文感知能力

**任务清单**:
- [ ] 实现 AI 上下文分析
- [ ] 增强 `GenerationContext` 的 AI 字段
- [ ] 实现上下文一致性检查
- [ ] 编写单元测试

**验收标准**:
- ✅ AI 可以分析上下文并生成一致数据
- ✅ 上下文一致性检查通过
- ✅ 单元测试覆盖率 ≥ 80%

#### 任务 3.2: 批量优化

**目标**: 优化批量生成性能

**任务清单**:
- [ ] 实现批量提示构建
- [ ] 实现并行 AI 调用
- [ ] 实现结果批量解析
- [ ] 编写性能测试

**验收标准**:
- ✅ 批量生成性能提升 ≥ 50%
- ✅ 支持并发控制（避免过载）
- ✅ 性能测试通过

#### 任务 3.3: 配置和 CLI 集成

**目标**: 将 AI 功能集成到 CLI 和配置系统

**任务清单**:
- [ ] 添加 AI 相关 CLI 参数
- [ ] 更新配置文件格式（支持 AI 配置）
- [ ] 添加 AI 模型选择选项
- [ ] 更新文档

**验收标准**:
- ✅ CLI 支持 AI 模型选择
- ✅ 配置文件支持 AI 参数
- ✅ 文档完整更新

---

### 阶段四：测试和文档（2-3天）

#### 任务 4.1: 集成测试

**目标**: 确保 AI 功能与现有系统集成良好

**任务清单**:
- [ ] 编写集成测试套件
- [ ] 测试 AI 生成器与传统生成器共存
- [ ] 测试降级机制
- [ ] 性能基准测试

**验收标准**:
- ✅ 所有集成测试通过
- ✅ 性能满足要求
- ✅ 降级机制工作正常

#### 任务 4.2: 文档更新

**目标**: 更新项目文档，添加 AI 功能说明

**任务清单**:
- [ ] 更新 README（AI 功能说明）
- [ ] 创建 AI 使用指南
- [ ] 创建模型配置指南
- [ ] 更新 API 文档

**验收标准**:
- ✅ README 包含 AI 功能说明
- ✅ 使用指南完整
- ✅ API 文档更新

---

## 技术实现细节

### 1. 模型选择策略

**优先级顺序**:
1. **本地模型（Ollama）**: 默认选择，数据隐私保护
2. **本地模型（Transformers）**: Ollama 不可用时
3. **云端模型（OpenAI/Anthropic）**: 本地模型不可用或需要更高质量时

**降级机制**:
```python
def get_model_with_fallback(self, preferred: str) -> Any:
    """获取模型，支持自动降级"""
    try:
        return self.get_model(preferred)
    except ModelUnavailableError:
        # 降级到下一个可用模型
        for fallback in self.fallback_chain:
            try:
                return self.get_model(fallback)
            except ModelUnavailableError:
                continue
        # 所有模型都不可用，抛出异常
        raise AllModelsUnavailableError()
```

### 2. 提示模板设计

**模板结构**:
```yaml
# dataforge/ai/prompts/name_generation.yaml
name_generation:
  system: |
    你是一个专业的测试数据生成助手。
    根据给定的上下文信息，生成符合要求的测试数据。
  
  user: |
    请生成一个{count}个中文姓名，要求：
    - 性别: {gender}
    - 地区: {region}
    - 风格: {style}
    
    只返回姓名列表，每行一个，不要其他解释。
  
  output_format: "list"
  validation_rules:
    - "每个姓名应为2-4个字符"
    - "符合中文姓名规范"
```

### 3. 缓存策略

**缓存键生成**:
```python
def generate_cache_key(self, prompt: str, parameters: dict) -> str:
    """生成缓存键"""
    key_data = {
        "prompt": prompt,
        "parameters": sorted(parameters.items()),
        "model": self.model_name
    }
    return hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()
```

**缓存失效**:
- TTL: 24小时（可配置）
- 手动清除: 通过 API 或 CLI
- 模型切换时自动清除

### 4. 性能优化

**批量生成优化**:
```python
async def generate_batch_async(self, contexts: list[dict]) -> list[str]:
    """异步批量生成"""
    # 构建批量提示
    batch_prompt = self.build_batch_prompt(contexts)
    
    # 并行调用（限制并发数）
    semaphore = asyncio.Semaphore(max_concurrent=5)
    tasks = [self._generate_with_semaphore(semaphore, ctx) for ctx in contexts]
    results = await asyncio.gather(*tasks)
    
    return results
```

---

## 测试策略

### 单元测试

**覆盖范围**:
- AI 模型管理器
- LangChain 集成层
- AI 生成器基类
- 各个 AI 生成器实现
- 缓存机制
- 降级机制

**测试工具**:
- pytest
- pytest-asyncio（异步测试）
- pytest-mock（模拟 AI 模型）

### 集成测试

**测试场景**:
1. AI 生成器与传统生成器共存
2. 模型切换和降级
3. 批量生成性能
4. 缓存机制
5. CLI 集成

### 性能测试

**基准指标**:
- 单次生成延迟: < 500ms（本地模型），< 2s（云端模型）
- 缓存命中后延迟: < 10ms
- 批量生成吞吐量: ≥ 10 items/s（本地模型），≥ 5 items/s（云端模型）

---

## 风险评估和缓解措施

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| 本地模型性能不足 | 高 | 中 | 提供云端模型降级选项，优化提示模板 |
| AI 生成结果不符合格式 | 高 | 中 | 实现严格的输出解析和验证，失败时降级 |
| 模型加载时间过长 | 中 | 低 | 实现模型预加载和连接池 |
| 成本控制（云端模型） | 中 | 中 | 默认使用本地模型，云端模型需显式启用 |
| 向后兼容性问题 | 高 | 低 | AI 功能作为可选增强，传统生成器保持不变 |

---

## 成功标准

项目成功的标准：

1. ✅ AI 模型管理器正常工作，支持本地和云端模型
2. ✅ LangChain 集成完成，可以构建和执行生成链
3. ✅ 至少 3 个 AI 生成器实现并测试通过
4. ✅ 性能满足要求（单次 < 500ms，批量 ≥ 10 items/s）
5. ✅ 降级机制工作正常，AI 失败时自动使用传统生成器
6. ✅ 向后兼容性保持，现有 API 和功能不受影响
7. ✅ 文档完整，包含使用指南和配置说明
8. ✅ 测试覆盖率 ≥ 80%

---

## 时间表

| 阶段 | 任务 | 预计时间 | 开始日期 | 完成日期 |
|------|------|---------|---------|---------|
| 阶段一 | AI 模型管理器 | 2 天 | TBD | TBD |
| 阶段一 | LangChain 集成 | 2 天 | TBD | TBD |
| 阶段一 | 缓存机制 | 1 天 | TBD | TBD |
| 阶段二 | AI 生成器基类 | 2 天 | TBD | TBD |
| 阶段二 | 智能姓名生成器 | 2 天 | TBD | TBD |
| 阶段二 | 智能地址生成器 | 1.5 天 | TBD | TBD |
| 阶段二 | 智能文本生成器 | 1.5 天 | TBD | TBD |
| 阶段三 | 上下文增强 | 2 天 | TBD | TBD |
| 阶段三 | 批量优化 | 1.5 天 | TBD | TBD |
| 阶段三 | 配置集成 | 1.5 天 | TBD | TBD |
| 阶段四 | 集成测试 | 1.5 天 | TBD | TBD |
| 阶段四 | 文档更新 | 1 天 | TBD | TBD |

**总计**: 18-20 个工作日（约 4 周）

---

## 后续优化建议

重构完成后，可以考虑：

1. **更多 AI 生成器**: 扩展到更多数据类型
2. **Fine-tuning**: 针对特定场景微调模型
3. **向量数据库**: 使用 ChromaDB 存储和检索生成历史
4. **A/B 测试**: 对比 AI 生成和传统生成的质量
5. **成本优化**: 实现更智能的模型选择策略

---

**计划制定日期**: 2025-12-22  
**计划审核状态**: 待审核  
**计划执行状态**: 待开始
