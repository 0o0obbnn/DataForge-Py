# DataForge - Python测试数据生成框架

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

DataForge是一个强大的Python测试数据生成框架，专门为中文环境设计，支持生成各种类型的测试数据。

## 🚀 主要特性

### 支持的数据类型
- **个人信息**: 中文姓名、身份证号码、手机号码、座机号码
- **企业信息**: 公司名称、统一社会信用代码
- **联系方式**: 电子邮箱、传真号码、客服电话
- **地址信息**: 中国大陆地址、邮政编码
- **金融数据**: 银行卡号、股票代码、基金代码
- **网络数据**: IP地址、MAC地址、URL、域名
- **时间数据**: 日期时间、时间戳、交易日历
- **其他数据**: 密码、UUID、验证码等

### 核心优势
- 🎯 **专为中文设计**: 支持中文姓名、地址、公司名称等本土化数据
- 🔧 **高度可配置**: 灵活的参数配置，满足不同场景需求
- 🚀 **高性能**: 支持批量生成和并发处理
- 📊 **数据关联**: 智能的数据关联生成，保证数据一致性
- 🎲 **多种格式**: 支持JSON、CSV、SQL、XML等多种输出格式
- ✅ **数据验证**: 内置数据验证功能，确保生成数据的有效性

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/0o0obbnn/dataforge-py.git
cd dataforge-py

# 安装依赖
pip install -r requirements.txt

# 安装项目
pip install -e .
```

## 🎯 快速开始

### 使用集成生成器类

```python
from chinese_data_generator import ChineseDataGenerator

# 创建生成器实例
generator = ChineseDataGenerator()

# 生成个人信息
print("姓名:", generator.generate_name())
print("身份证:", generator.generate_idcard())
print("手机号:", generator.generate_phone())
print("座机号:", generator.generate_landline())

# 生成企业信息
print("公司名称:", generator.generate_company_name())
print("统一社会信用代码:", generator.generate_uscc())

# 生成完整个人档案
person_profile = generator.generate_person_profile(
    gender='male',
    region='北京',
    area_code='010'
)
print(person_profile)
# 输出: {'姓名': '张伟', '身份证号码': '110101198605151234', '手机号码': '13812345678', '座机号码': '010-12345678'}
```

## 📚 支持的生成器类型

| 生成器类型 | 别名 | 描述 | 示例 |
|------------|------|------|------|
| `name` | `姓名` | 中文姓名 | 张三, 李四 |
| `idcard` | `身份证` | 18位身份证号 | 110101199001011234 |
| `phone` | `手机` | 11位手机号 | 13812345678 |
| `landline` | `座机`, `固话` | 座机号码 | 010-12345678 |
| `company_name` | `公司名称` | 公司名 | 北京科技有限公司 |
| `uscc` | `统一社会信用代码` | 18位信用代码 | 91110000123456789X |

## 🧪 运行测试

```bash
# 运行演示脚本
python chinese_data_generator.py
```

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。

## 📞 联系方式

- GitHub Issues: [提交问题](https://github.com/0o0obbnn/dataforge-py/issues)

---

**DataForge** - 让测试数据生成变得简单高效！ 🚀