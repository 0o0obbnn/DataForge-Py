# 交易日历生成器使用指南（重构版）

## 📚 概述

交易日历生成器已经过重构，现在支持：
- ✅ 通过YAML配置文件管理节假日数据
- ✅ 懒加载 + 内存缓存机制
- ✅ API自动更新节假日数据
- ✅ 完全向后兼容
- ✅ 性能无损（与硬编码相当）

---

## 🚀 快速开始

### 方式1：使用新gen API（推荐）

```python
from dataforge import gen

# 生成单个交易日
trading_day = gen.trading_calendar()
print(trading_day)
# {'date': '2024-11-06', 'is_trading_day': True, 'day_type': 'TRADING', ...}

# 生成节假日
holiday = gen.trading_calendar(
    start_date='2024-10-01',
    end_date='2024-10-07',
    day_type='HOLIDAY'
)
print(holiday['holiday_name'])  # '国庆节'

# 批量生成
trading_days = gen.trading_calendar(count=10, day_type='TRADING')
```

### 方式2：使用旧API（完全兼容）

```python
from dataforge import default_factory, GeneratorConfig

config = GeneratorConfig(
    generator_type='trading_calendar',
    parameters={
        'start_date': '2024-09-15',
        'end_date': '2024-09-20',
        'day_type': 'HOLIDAY'
    }
)

generator = default_factory.create_generator(config)
result = generator.generate_single()
```

---

## ⚙️ 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `start_date` | str | "2024-01-01" | 开始日期 (YYYY-MM-DD) |
| `end_date` | str | "2024-12-31" | 结束日期 (YYYY-MM-DD) |
| `day_type` | str | "TRADING" | 日期类型 (TRADING/HOLIDAY/ALL) |
| `include_weekends` | bool | False | 是否包含周末 |
| `market` | str | "ALL" | 市场代码 (SH/SZ/ALL) |

---

## 📁 配置文件管理

### 配置文件位置

```
data_forge_py/
└── config/
    └── trading_calendar.yaml  # 节假日配置文件
```

### 配置文件结构

```yaml
version: "2025.1"
last_updated: "2025-12-23"

holidays:
  2024:
    - date: "2024-01-01"
      name: "元旦"
      type: "LEGAL"
    - date: "2024-02-09"
      name: "春节"
      type: "LEGAL"

adjusted_working_days:
  2024:
    - "2024-02-04"  # 春节前补班
    - "2024-02-18"  # 春节后补班
```

### 手动更新配置文件

直接编辑 `config/trading_calendar.yaml` 文件即可。

---

## 🌐 API自动更新

### 更新单个年份

```python
from dataforge.data.trading_calendar_updater import TradingCalendarUpdater

updater = TradingCalendarUpdater()

# 更新2026年数据
updater.update_year(2026)
```

### 批量更新多个年份

```python
# 批量更新2024-2026年数据
updater.update_multiple_years([2024, 2025, 2026])
```

### 命令行更新

```bash
# 更新2026年数据
python -m dataforge.data.trading_calendar_updater 2026

# 批量更新
python -m dataforge.data.trading_calendar_updater 2024 2025 2026

# 预览更新（不实际写入）
python -m dataforge.data.trading_calendar_updater 2026 --dry-run
```

---

## 🔧 高级用法

### 自定义配置文件路径

通过环境变量指定配置文件：

```bash
export DATAFORGE_TRADING_CALENDAR_CONFIG=/path/to/your/config.yaml
```

```python
import os
os.environ['DATAFORGE_TRADING_CALENDAR_CONFIG'] = '/path/to/your/config.yaml'

from dataforge import gen
trading_day = gen.trading_calendar()
```

### 强制重新加载配置

```python
from dataforge.data.trading_calendar_config import get_trading_calendar_config

config = get_trading_calendar_config()

# 强制重新加载配置文件
config.reload()
```

### 查看配置状态

```python
config = get_trading_calendar_config()

print(config)  # 查看配置概览
print(config.is_cached())  # 是否已缓存
print(config.get_all_years())  # 包含的年份
print(config.get_version())  # 配置版本
```

---

## 📊 性能优化

### 缓存机制

- **首次加载：** ~10ms（包含配置文件解析）
- **缓存后：** ~1.4ms（与硬编码相当）
- **批量生成：** ~1.3ms/个

### 缓存策略

1. **懒加载：** 首次使用时才加载配置文件
2. **内存缓存：** 加载后缓存在内存，后续访问秒级响应
3. **热更新：** 检测文件修改时间，自动重新加载
4. **降级机制：** 配置文件缺失时使用内置默认数据

---

## 🎯 使用示例

### 生成2024年所有国庆节假日

```python
from dataforge import gen

# 生成国庆节假日
holidays = gen.trading_calendar(
    start_date='2024-10-01',
    end_date='2024-10-07',
    day_type='HOLIDAY',
    count=10
)

for holiday in holidays:
    print(f"{holiday['date']} - {holiday['holiday_name']}")
```

### 查找下一个交易日

```python
from dataforge import gen
from datetime import datetime

# 从今天开始查找交易日
today = datetime.now().strftime('%Y-%m-%d')
next_month = datetime.now().replace(month=datetime.now().month+1).strftime('%Y-%m-%d')

trading_day = gen.trading_calendar(
    start_date=today,
    end_date=next_month,
    day_type='TRADING'
)

print(f"下一个交易日: {trading_day['date']}")
```

---

## ⚠️ 注意事项

1. **配置文件优先：** 优先使用配置文件，配置文件缺失时使用内置默认数据
2. **数据时效性：** 建议每年更新一次节假日数据
3. **向后兼容：** 旧代码无需修改，完全兼容
4. **性能无损：** 缓存后性能与硬编码相当

---

## 🆚 新旧方案对比

| 特性 | 旧方案（硬编码） | 新方案（配置文件） |
|------|-----------------|-------------------|
| **维护成本** | 每年改代码+发版 | 更新配置文件 |
| **灵活性** | 无法自定义 | 用户可自定义 |
| **数据时效** | 只支持到2025 | API自动更新 |
| **性能** | ~1.4ms | ~1.4ms（相同） |
| **代码行数** | 368行 | 258行（减少30%） |
| **向后兼容** | - | 100%兼容 |

---

## 📝 更新日志

### v2.0.0 (2025-12-23)

- ✅ 重构为配置文件方案
- ✅ 实现懒加载 + 内存缓存
- ✅ 支持API自动更新
- ✅ 代码量减少30%（368→258行）
- ✅ 完全向后兼容

---

## 🤝 贡献

欢迎提交PR更新节假日数据！

1. 编辑 `config/trading_calendar.yaml`
2. 提交PR
3. 审核通过后合并

---

**老王温馨提示：** 新方案性能无损，维护更简单，强烈推荐升级！
