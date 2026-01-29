# DataForge

DataForge是一款高效、灵活且高度可配置的测试数据生成工具，专注于为软件测试团队提供高质量、真实且多样化的测试数据，特别针对中国本土化数据生成进行了深度优化。

## 特性

- 💡 **简洁 API**: 类似 Faker 的链式调用，`gen.name()` 即可生成数据
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
- **港澳台证件** (`hk_mo_tw_id`): 支持港澳居民来往内地通行证、台湾居民来往大陆通行证、港澳台居民居住证
- **银行卡号** (`bankcard`): 支持Luhn算法校验，多种银行和卡组织
- **手机号** (`phone`): 支持三大运营商号段
- **姓名** (`name`): 中英文姓名生成
- **地址** (`address`): 基于行政区划的地址生成
- **企业名称** (`company_name`): 支持行业、公司类型配置（✅ 已配置化）
- **职业/职位** (`occupation`): 支持多行业、多级别配置（✅ 已配置化）
- **教育水平** (`education`): 支持中英文教育体系（✅ 已配置化）
- **车牌号** (`license_plate`): 支持燃油/新能源车牌（✅ 已配置化）

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

### 💡 简化 API（推荐新手使用）

DataForge 提供了类似 Faker 的简洁 API，让你快速上手：

```python
from dataforge import gen

# 🎯 生成单个数据
name = gen.name()                    # 姓名
phone = gen.phone()                  # 手机号
email = gen.email()                  # 邮箱
idcard = gen.idcard()                # 身份证
address = gen.address()              # 地址

# 📦 批量生成数据
names = gen.name(count=10)           # 生成10个姓名
phones = gen.phone(count=5)          # 生成5个手机号

# ⚙️ 带参数生成
phone = gen.phone(operator='MOBILE')                    # 中国移动号码
idcard = gen.idcard(region='北京', gender='MALE')      # 北京男性身份证
idcards = gen.idcard(region='上海', count=5)           # 批量生成上海身份证

# 🔍 发现和帮助
gen.list_generators()                # 查看所有可用生成器（94个）
gen.is_available('name')             # 检查生成器是否可用
print(gen)                           # 查看使用帮助
```

**完整示例：生成用户资料**

```python
from dataforge import gen

# 生成一个完整的用户资料
user = {
    'name': gen.name(),
    'gender': gen.gender(),
    'age': gen.age(),
    'phone': gen.phone(operator='MOBILE'),
    'email': gen.email(),
    'idcard': gen.idcard(region='北京'),
    'address': gen.address(),
    'company': gen.company_name()
}

print(user)
# 输出示例：
# {
#     'name': '张伟',
#     'gender': 'Male',
#     'age': 28,
#     'phone': '13812345678',
#     'email': 'zhangwei@example.com',
#     'idcard': '110101199501011234',
#     'address': '北京市朝阳区...',
#     'company': '北京科技有限公司'
# }
```

### 🔧 高级 API（适用于复杂场景）

对于更复杂的需求，可以使用配置化的 API：

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

## 配置化生成器

DataForge 支持通过配置文件管理生成器的数据源，无需修改代码即可更新数据。

### 已配置化的生成器

以下生成器已支持配置文件管理：

- **企业名称** (`company_name`): `resources/company_name_zh.yaml`
- **职业/职位** (`occupation`): `resources/occupation_zh.yaml`
- **教育水平** (`education`): `resources/education_zh.yaml`
- **车牌号** (`license_plate`): `resources/license_plate_zh.yaml`

### 修改配置

编辑对应的 YAML 配置文件即可更新数据，无需修改代码：

```yaml
# resources/occupation_zh.yaml
occupation:
  industries:
    IT:
      positions:
        SENIOR:
          - 技术总监
          - 架构师
          # 添加新的职位...
```

### 配置加载机制

- **自动缓存**：配置只加载一次，后续从内存读取
- **Fallback机制**：配置文件缺失时自动使用默认配置
- **多语言支持**：通过 `locale` 参数支持不同语言环境

详细说明请查看[配置化迁移完成报告](docs/configuration_migration_completion_report.md)。

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
