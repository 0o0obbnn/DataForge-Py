# 基础信息生成器示例

本目录包含DataForge基础信息生成器的使用示例。

## 📁 文件列表

### company_demo.py - 企业信息生成示例 🏢

专门用于生成企业名称和统一社会信用代码的完整示例。

**功能演示：**
1. ✅ 基础企业信息生成
2. ✅ 带参数的企业名称生成（行业、类型、地区）
3. ✅ 带参数的统一社会信用代码生成
4. ✅ 完整企业档案生成
5. ✅ 数据验证
6. ✅ JSON格式导出
7. ✅ CSV格式导出
8. ✅ 批量生成（100家企业）
9. ✅ 特定行业企业生成
10. ✅ 真实场景应用（工商注册系统）

**运行方式：**
```bash
python examples/basic/company_demo.py
```

**生成器参数：**

#### 企业名称生成器 (company_name)
- `industry`: 行业类型 (IT, FINANCE, RETAIL, MANUFACTURING, EDUCATION)
- `type`: 企业类型 (CO_LTD, GROUP, INSTITUTE, TECH, TRADING)
- `prefix_region`: 是否添加地区前缀 (True/False)
- `language`: 语言 (chinese/english)

#### 统一社会信用代码生成器 (uscc)
- `type`: 组织类型
  - `enterprise` - 企业
  - `individual` - 个体工商户
  - `organization` - 社会组织
  - `government` - 政府机关

**示例输出：**
```
企业名称: 北京科技创新有限公司
统一社会信用代码: 91110000MA01234567
组织机构代码: 12345678-9
```

---

### contact_demo.py - 联系方式生成示例 📞

演示如何生成各种联系方式信息。

**运行方式：**
```bash
python examples/basic/contact_demo.py
```

---

### personal_info_demo.py - 个人信息生成示例 👤

演示如何生成个人基本信息。

**运行方式：**
```bash
python examples/basic/personal_info_demo.py
```

---

### profile_demo.py - 档案信息生成示例 📋

演示如何生成完整的个人档案信息。

**运行方式：**
```bash
python examples/basic/profile_demo.py
```

---

## 🚀 快速开始

### 1. 生成单个企业信息

```python
from dataforge import GeneratorConfig, default_factory

# 生成企业名称
company_name_config = GeneratorConfig("company_name", parameters={})
company_name_gen = default_factory.create_generator(company_name_config)
company_name = company_name_gen.generate()
print(f"企业名称: {company_name}")

# 生成统一社会信用代码
uscc_config = GeneratorConfig("uscc", parameters={"type": "enterprise"})
uscc_gen = default_factory.create_generator(uscc_config)
uscc = uscc_gen.generate()
print(f"统一社会信用代码: {uscc}")
```

### 2. 生成特定行业的企业

```python
# 生成IT行业企业
config = GeneratorConfig("company_name", parameters={
    "industry": "IT",
    "prefix_region": True
})
generator = default_factory.create_generator(config)
company_name = generator.generate()
print(f"IT企业: {company_name}")
```

### 3. 批量生成企业信息

```python
# 批量生成100家企业
company_name_gen = default_factory.create_generator(
    GeneratorConfig("company_name", parameters={})
)
uscc_gen = default_factory.create_generator(
    GeneratorConfig("uscc", parameters={"type": "enterprise"})
)

companies = []
for i in range(100):
    company = {
        "name": company_name_gen.generate(),
        "uscc": uscc_gen.generate()
    }
    companies.append(company)
```

## 📊 支持的企业类型

### 行业分类
- **IT** - 信息技术
- **FINANCE** - 金融服务
- **RETAIL** - 零售贸易
- **MANUFACTURING** - 制造业
- **EDUCATION** - 教育培训

### 企业类型
- **CO_LTD** - 有限公司
- **GROUP** - 集团公司
- **INSTITUTE** - 研究院所
- **TECH** - 科技公司
- **TRADING** - 贸易公司

### USCC组织类型
- **enterprise** - 企业
- **individual** - 个体工商户
- **organization** - 社会组织
- **government** - 政府机关

## 💡 使用技巧

1. **生成真实感的企业名称**：设置 `prefix_region: True` 添加地区前缀
2. **生成英文企业名称**：设置 `language: "english"`
3. **生成特定行业企业**：设置 `industry` 参数
4. **验证生成的数据**：使用 `generator.validate(data)` 方法

## 🔗 相关示例

- `../identifier/identifier_demo.py` - 更多标识符生成示例
- `../comprehensive_demo.py` - 所有生成器概览
- `../integration/integration_demo.py` - 集成应用示例

## 📝 注意事项

- 所有生成的企业名称和USCC都经过格式验证
- USCC遵循国家标准GB 32100-2015
- 企业名称符合工商注册规范
- 生成的数据仅用于测试和开发，不代表真实企业
