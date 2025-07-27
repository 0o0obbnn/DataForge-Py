# DataForge

DataForge是一款高效、灵活且高度可配置的测试数据生成工具，专注于为软件测试团队提供高质量、真实且多样化的测试数据，特别针对中国本土化数据生成进行了深度优化。

## 特性

- 🇨🇳 **中国本土化支持**: 身份证、银行卡、手机号、统一社会信用代码等
- 🔗 **数据关联性**: 支持字段间逻辑关联，确保数据一致性
- 🎯 **高度可配置**: 丰富的CLI参数和YAML配置文件支持
- 🚀 **高性能**: 快速生成大量数据
- 🔌 **可扩展**: 插件式架构，轻松添加自定义生成器
- 📊 **多格式输出**: JSON、CSV、XML、SQL、YAML等格式

## 快速开始

### 安装

```bash
pip install dataforge
```

### 基本用法

```bash
# 生成10个身份证号
dataforge generate idcard --count 10

# 生成银行卡号并输出为JSON
dataforge generate bankcard --count 5 --output.format json

# 生成关联数据（身份证和对应年龄）
dataforge generate idcard,age --count 10 --idcard.gender MALE --age.min 25 --age.max 45

# 使用配置文件
dataforge generate --config user_data.yaml
```

### 支持的数据类型

#### 基础信息类
- **身份证号** (`idcard`): 支持地区、性别、出生日期范围配置
- **银行卡号** (`bankcard`): 支持Luhn算法校验，多种银行和卡组织
- **手机号** (`phone`): 支持三大运营商号段
- **姓名** (`name`): 中英文姓名生成
- **地址** (`address`): 基于行政区划的地址生成

#### 标识类
- **UUID** (`uuid`): 多种UUID格式
- **业务单据号** (`document_id`): 自定义格式的业务编号

更多数据类型请查看[完整文档](https://dataforge.readthedocs.io/)。

### 配置文件示例

```yaml
# user_data.yaml
generators:
  - generator_type: idcard
    count: 100
    parameters:
      region: "北京"
      gender: "ANY"
      birth_date_range: ["1990-01-01", "2000-12-31"]
  
  - generator_type: phone
    count: 100
    parameters:
      operator: "ANY"
      valid: true

output:
  format: json
  file: "test_data.json"
  pretty: true
```

## Python API使用

```python
from dataforge import default_factory, GeneratorConfig

# 创建生成器配置
config = GeneratorConfig(
    generator_type='idcard',
    parameters={
        'region': '北京',
        'gender': 'MALE',
        'birth_date_range': ('1990-01-01', '2000-12-31')
    }
)

# 创建生成器并生成数据
generator = default_factory.create_generator(config)
data = generator.generate_batch(10)
print(data)
```

## 自定义生成器

```python
from dataforge import DataGenerator, register_generator, GeneratorType

@register_generator('custom_id', ['my_id'])
class CustomIDGenerator(DataGenerator[str]):
    def _setup(self):
        self.prefix = self.parameters.get('prefix', 'ID')
    
    def generate_single(self, context=None):
        import uuid
        return f"{self.prefix}_{uuid.uuid4().hex[:8].upper()}"
    
    def validate(self, data):
        return isinstance(data, str) and data.startswith(self.prefix)
    
    @property 
    def generator_type(self):
        return GeneratorType.IDENTIFIER
    
    @property
    def supported_parameters(self):
        return ['prefix']
```

## 命令行选项

### 全局选项
- `--version`: 显示版本信息
- `--verbose, -v`: 详细输出
- `--debug`: 调试模式

### 生成选项
- `--count, -n`: 生成数量
- `--config, -c`: 配置文件路径
- `--output.format`: 输出格式 (json/csv/xml/sql/yaml)
- `--output.file`: 输出文件路径
- `--output.pretty`: 美化输出

### 身份证选项
- `--idcard.region`: 地区代码或名称
- `--idcard.gender`: 性别 (MALE/FEMALE/ANY) 
- `--idcard.birth_date_range`: 出生日期范围
- `--idcard.valid`: 是否生成有效身份证

### 更多选项
查看完整选项列表：
```bash
dataforge generate --help
```

## 开发

### 环境设置
```bash
git clone https://github.com/dataforge/dataforge.git
cd dataforge
pip install -e ".[dev]"
```

### 运行测试
```bash
pytest tests/
```

### 代码格式化
```bash
black dataforge/
flake8 dataforge/
```

## 贡献

欢迎贡献代码！请查看[贡献指南](CONTRIBUTING.md)了解详情。

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

## 联系我们

- 文档: https://dataforge.readthedocs.io/
- 问题反馈: https://github.com/dataforge/dataforge/issues
- 邮箱: contact@dataforge.org