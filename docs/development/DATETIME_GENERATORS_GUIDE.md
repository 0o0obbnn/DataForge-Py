# DataForge 时间生成器完整指南

## 概述

DataForge提供了完整的时间相关数据生成解决方案，包括基础时间戳、增强时间戳、高级时间戳和日期时间范围生成器。

## 生成器类型

### 1. 基础时间戳生成器 (GenericTimestampGenerator)

**功能**: 生成基础Unix时间戳
**输出**: 字符串格式的时间戳

```python
from dataforge.generators.datetime import GenericTimestampGenerator

# 基础使用
gen = GenericTimestampGenerator()
timestamp = gen.generate()  # 例如: "1756547737"

# 验证
is_valid = gen.validate("1756547737")  # True
```

### 2. 增强时间戳生成器 (GenericEnhancedTimestampGenerator)

**功能**: 支持多种精度和格式
**特性**: 毫秒、微秒、纳秒级精度

```python
from dataforge.generators.datetime import GenericEnhancedTimestampGenerator

# 毫秒级精度
gen = GenericEnhancedTimestampGenerator({
    "precision": "milliseconds",
    "output_format": "INTEGER"
})
result = gen.generate()  # 例如: 1756547737159

# ISO格式
gen = GenericEnhancedTimestampGenerator({
    "precision": "seconds",
    "output_format": "ISO"
})
result = gen.generate()  # 例如: "2025-08-30T17:55:37"
```

### 3. 高级时间戳生成器 (GenericAdvancedTimestampGenerator)

**功能**: 最完整的时间戳生成功能
**特性**: 精度、格式、时区、范围、相对时间

#### 基本配置

```python
from dataforge.generators.datetime import GenericAdvancedTimestampGenerator

# 基础使用
gen = GenericAdvancedTimestampGenerator()
result = gen.generate()  # Unix时间戳
```

#### 精度控制

```python
# 支持四种精度
precisions = ["SECONDS", "MILLISECONDS", "MICROSECONDS", "NANOSECONDS"]

for precision in precisions:
    gen = GenericAdvancedTimestampGenerator({"precision": precision})
    result = gen.generate()
    print(f"{precision}: {result}")
```

#### 格式输出

```python
formats = ["UNIX", "ISO", "CUSTOM"]

for fmt in formats:
    gen = GenericAdvancedTimestampGenerator({
        "format": fmt,
        "custom_format": "%Y-%m-%d %H:%M:%S" if fmt == "CUSTOM" else None
    })
    result = gen.generate()
    print(f"{fmt}: {result}")
```

#### 时区处理

```python
# UTC时区
gen = GenericAdvancedTimestampGenerator({
    "timezone_aware": True,
    "timezone": "UTC",
    "format": "ISO"
})

# 本地时区
gen = GenericAdvancedTimestampGenerator({
    "timezone_aware": True,
    "timezone": "Asia/Shanghai",
    "format": "ISO"
})
```

#### 日期范围限制

```python
gen = GenericAdvancedTimestampGenerator({
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-12-31T23:59:59",
    "format": "ISO"
})
```

#### 相对时间

```python
gen = GenericAdvancedTimestampGenerator({
    "relative_to": "TODAY",  # NOW, TODAY, YESTERDAY, TOMORROW
    "offset_days": 7,
    "offset_hours": 12,
    "format": "ISO"
})
```

### 4. 日期时间范围生成器 (GenericAdvancedDateTimeRangeGenerator)

**功能**: 生成日期时间范围字符串

#### 基础范围

```python
from dataforge.generators.datetime import GenericAdvancedDateTimeRangeGenerator

# 7天范围
gen = GenericAdvancedDateTimeRangeGenerator({
    "duration_days": 7,
    "format": "RANGE"
})
result = gen.generate()  # "2025-08-30 17:55:37 至 2025-09-06 17:55:37"
```

#### 持续时间格式

```python
gen = GenericAdvancedDateTimeRangeGenerator({
    "duration_days": 2,
    "duration_hours": 12,
    "format": "DURATION"
})
result = gen.generate()  # "2025-08-30 17:55:37 (持续 2天 12小时)"
```

#### 自定义起始时间

```python
gen = GenericAdvancedDateTimeRangeGenerator({
    "start_datetime": "2024-06-15T08:00:00",
    "duration_hours": 3,
    "format": "ISO"
})
```

#### 多种输出格式

```python
formats = ["ISO", "SQL", "CN", "US", "RANGE", "DURATION"]

for fmt in formats:
    gen = GenericAdvancedDateTimeRangeGenerator({
        "duration_hours": 1,
        "format": fmt
    })
    result = gen.generate()
    print(f"{fmt}: {result}")
```

## 批量生成

所有生成器都支持批量生成：

```python
# 高级时间戳批量生成
gen = GenericAdvancedTimestampGenerator({
    "format": "ISO",
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-12-31T23:59:59"
})

# 生成10个时间戳
timestamps = gen.generate_batch(10)
for ts in timestamps:
    print(ts)

# 日期范围批量生成
range_gen = GenericAdvancedDateTimeRangeGenerator({
    "duration_days": 1,
    "format": "RANGE"
})

ranges = range_gen.generate_batch(5)
for range_str in ranges:
    print(range_str)
```

## 验证功能

所有生成器都提供验证方法：

```python
# 时间戳验证
gen = GenericAdvancedTimestampGenerator()

# 有效验证
assert gen.validate(1704067200) is True
assert gen.validate("1704067200") is True

# 无效验证
assert gen.validate("invalid") is False
assert gen.validate(-1) is False

# 日期范围验证
range_gen = GenericAdvancedDateTimeRangeGenerator()
assert range_gen.validate("2024-01-01 00:00:00 至 2024-01-02 00:00:00") is True
assert range_gen.validate("invalid range") is False
```

## 完整示例

```python
from dataforge.generators.datetime import (
    GenericAdvancedTimestampGenerator,
    GenericAdvancedDateTimeRangeGenerator
)

# 创建高级时间戳生成器
timestamp_gen = GenericAdvancedTimestampGenerator({
    "precision": "MILLISECONDS",
    "format": "ISO",
    "timezone_aware": True,
    "timezone": "UTC",
    "start_date": "2024-01-01T00:00:00Z",
    "end_date": "2024-12-31T23:59:59Z"
})

# 生成时间戳
timestamp = timestamp_gen.generate()
print(f"生成的ISO时间戳: {timestamp}")

# 创建日期范围生成器
range_gen = GenericAdvancedDateTimeRangeGenerator({
    "duration_days": 7,
    "format": "ISO",
    "include_timezone": True,
    "timezone": "UTC"
})

# 生成日期范围
range_str = range_gen.generate()
print(f"生成的日期范围: {range_str}")
```

## 测试验证

运行测试确保功能正常：

```bash
# 运行高级时间戳测试
python -m pytest dataforge/generators/datetime/test_advanced_timestamp.py -v

# 运行集成测试
python -m pytest test_integration_datetime.py -v

# 运行完整演示
python demo_complete_datetime.py
```
