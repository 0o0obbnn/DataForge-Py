# 硬编码数据审计报告

## 概述

本报告列出了 DataForge 项目中所有包含硬编码数据的生成器，这些数据适合迁移到配置文件中以提高可维护性和可扩展性。

## 审计日期

2025-12-22

## 发现的问题

### 1. 高优先级（大量硬编码数据，适合配置化）

#### 1.1 `education.py` - 教育水平生成器
**文件路径**: `dataforge/generators/basic/education.py`

**硬编码内容**:
- 中国教育体系数据（`china_system`）:
  - 学历级别：PRIMARY, JUNIOR, HIGH, UNIVERSITY, MASTER, PHD
  - 每个级别包含：name, degrees（学历名称列表）, schools（学校名称列表）
  - 学校列表包含：北京大学、清华大学、复旦大学等15所大学
- 国际教育体系数据（`international_system`）:
  - 学历级别：HIGH_SCHOOL, BACHELOR, MASTER, PHD, POSTDOC
  - 每个级别包含：name, degrees, schools
  - 学校列表包含：Harvard University, Stanford University, MIT等

**数据量**: 约 200+ 行硬编码数据

**建议**: 
- 创建 `resources/education_zh.yaml` 和 `resources/education_en.yaml`
- 将学校列表、学历级别、学历名称等迁移到配置文件

---

#### 1.2 `occupation.py` - 职业/职位生成器
**文件路径**: `dataforge/generators/basic/occupation.py`

**硬编码内容**:
- 行业分类（`industries`）:
  - IT, FINANCE, RETAIL, MANUFACTURING, EDUCATION, MEDICAL, MEDIA
  - 每个行业包含多个级别（SENIOR, MIDDLE, JUNIOR, INTERN）的职位列表
  - 每个级别包含 7-10 个职位名称
- 通用职位（`generic_positions`）:
  - 按级别分类的通用职位列表
- 部门分类（`departments`）:
  - 每个行业对应的部门列表
- 英文翻译映射（`_to_english` 方法中的 `translation_map`）:
  - 大量中文职位到英文的翻译映射

**数据量**: 约 500+ 行硬编码数据

**建议**:
- 创建 `resources/occupation_zh.yaml` 和 `resources/occupation_en.yaml`
- 将职位列表、行业分类、部门、翻译映射等迁移到配置文件

---

#### 1.3 `context_aware.py` - 上下文感知生成器
**文件路径**: `dataforge/generators/basic/context_aware.py`

**硬编码内容**:
- 姓名数据（`_first_names`）:
  - 男性名字列表：20个
  - 女性名字列表：20个
- 姓氏列表（`_last_names`）:
  - 20个常见姓氏

**数据量**: 约 60 行硬编码数据

**建议**:
- 注意：项目已有 `data/chinese/surnames.json` 和 `data/chinese/givennames.json`
- 建议统一使用数据文件，移除硬编码
- 或创建配置文件统一管理

---

#### 1.4 `license_plate.py` - 车牌号生成器
**文件路径**: `dataforge/generators/basic/license_plate.py`

**硬编码内容**:
- 省份简称映射（`provinces`）:
  - 34个省份的简称到全称的映射
  - 例如：{"京": "北京", "津": "天津", ...}

**数据量**: 约 40 行硬编码数据

**建议**:
- 创建 `resources/license_plate_zh.yaml`
- 将省份映射迁移到配置文件
- 注意：项目已有 `data/chinese/regions.json`，可考虑复用

---

### 2. 中优先级（中等量硬编码数据）

#### 2.1 `address.py` - 地址生成器
**文件路径**: `dataforge/generators/basic/address.py`

**硬编码内容**:
- 默认地区数据（`_get_default_regions_data`）:
  - 作为 fallback 的硬编码省份、城市、区县数据
  - 街道类型、建筑类型列表

**数据量**: 约 30 行硬编码数据

**状态**: 已使用数据加载器，但仍有硬编码 fallback

**建议**:
- 确保 `data/chinese/regions.json` 数据完整
- 移除或最小化硬编码 fallback

---

### 3. 低优先级（少量硬编码数据，可能是算法逻辑）

#### 3.1 `company_name.py` - 企业名称生成器
**文件路径**: `dataforge/generators/basic/company_name.py`

**状态**: ✅ **已配置化**（2025-12-22完成）

**完成内容**:
- 已创建 `resources/company_name_zh.yaml`
- 已创建 `resources/company_name_loader.py`
- 已修改生成器使用配置文件
- 所有测试通过

---

## 统计摘要

| 优先级 | 生成器数量 | 总硬编码行数（估算） |
|--------|-----------|---------------------|
| 高优先级 | 4 | ~800+ |
| 中优先级 | 1 | ~30 |
| 低优先级 | 1 | 0（已配置化） |
| **总计** | **6** | **~830+** |

## 配置化建议

### 推荐的配置文件结构

```
dataforge/resources/
├── company_name_zh.yaml          ✅ 已完成
├── company_name_en.yaml          ⏳ 待实现
├── education_zh.yaml              ⏳ 待实现
├── education_en.yaml              ⏳ 待实现
├── occupation_zh.yaml             ⏳ 待实现
├── occupation_en.yaml             ⏳ 待实现
├── license_plate_zh.yaml          ⏳ 待实现
└── names_zh.yaml                  ⏳ 待实现（统一管理姓名数据）
```

### 配置化优先级

1. **第一优先级**: `occupation.py` - 数据量最大，业务价值高
2. **第二优先级**: `education.py` - 数据量较大，经常需要更新学校列表
3. **第三优先级**: `license_plate.py` - 数据量中等，相对稳定
4. **第四优先级**: `context_aware.py` - 数据量小，但建议统一到现有数据文件

### 实施建议

1. **复用现有模式**: 参考 `company_name_loader.py` 的实现模式
2. **保持向后兼容**: 使用 fallback 机制，确保配置缺失时仍能工作
3. **统一数据源**: 对于已有 JSON 数据文件的（如姓名、地区），优先使用现有数据文件
4. **测试覆盖**: 每个配置化改造都要补充测试用例

## 性能影响评估

基于 `company_name.py` 的配置化经验：

- **配置加载**: 使用 `@lru_cache` 缓存，首次加载后零性能损失
- **生成性能**: 与硬编码版本基本一致（都是内存操作）
- **内存占用**: 可忽略（每个配置文件约 10-50KB）

## 下一步行动

1. ✅ 完成 `company_name.py` 配置化（已完成）
2. ⏳ 实施 `occupation.py` 配置化
3. ⏳ 实施 `education.py` 配置化
4. ⏳ 实施 `license_plate.py` 配置化
5. ⏳ 统一 `context_aware.py` 使用现有数据文件
6. ⏳ 优化 `address.py` 的 fallback 机制

## 注意事项

1. **数据一致性**: 确保配置文件中的数据与业务规则一致
2. **版本控制**: 配置文件应纳入版本控制，便于追踪变更
3. **文档维护**: 为每个配置文件添加注释说明数据来源和更新规则
4. **测试验证**: 配置化后必须运行完整测试套件确保功能正常

---

**报告生成时间**: 2025-12-22  
**审计人员**: AI Assistant  
**审核状态**: 待审核
