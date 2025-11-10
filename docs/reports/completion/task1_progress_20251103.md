# Task 1 Progress: DataGenerator基类接口修复

**执行日期**: 2025-11-03
**状态**: 部分完成 (Partially Complete)

## ✅ 已完成的工作

### 1. 基类更新 (100%)
- ✅ 在 `core/types.py` 中更新 GeneratorType 枚举，添加 ADVANCED 类型
- ✅ 在 `core/generator.py` 中添加所有必需的抽象方法:
  - `generate_single(context) -> T` (抽象方法)
  - `validate(data: T) -> bool` (抽象方法)
  - `generator_type -> GeneratorType` (抽象属性)
  - `supported_parameters -> list[str]` (抽象属性)
- ✅ 保持向后兼容：`generate()` 方法作为 `generate_single()` 的包装器
- ✅ 更新 `generate_batch()` 调用 `generate_single()` 而非 `generate()`

### 2. 检查脚本创建 (100%)
- ✅ 创建 `scripts/check_generator_compliance.py` 脚本
- ✅ 脚本功能：
  - AST 解析检测缺失的方法和属性
  - 统计报告（总数、合规数、需修复数）
  - 详细列出每个生成器缺少的内容

### 3. 生成器修复工具创建 (100%)
- ✅ 创建 `scripts/generate_missing_methods.py` 模板生成工具
- ✅ 工具功能：
  - 根据生成器类型生成标准化代码模板
  - 自动生成 validate(), generator_type, supported_parameters 方法
  - 提供重命名和导入指导

### 4. 示例生成器修复 (1/113)
- ✅ 完整修复 `generators/basic/idcard.py` 中的 IDCardGenerator:
  - 添加 GeneratorType 导入
  - 重命名 `generate()` 为 `generate_single()`
  - 添加 `validate()` 方法（调用 self.validator.validate()）
  - 添加 `generator_type` 属性返回 GeneratorType.BASIC
  - 添加 `supported_parameters` 属性返回参数列表
  - 修复内部调用 `self.generate()` 为 `self.generate_single()`

## 📊 当前状态

### 合规性统计
- **总计生成器**: 113
- **已修复**: 1 (IDCardGenerator)
- **待修复**: 112
- **合规率**: 0.88% (1/113)

### 需修复的文件分布
```
advanced/: 12个文件, 22个生成器类
auth/: 4个文件, 4个生成器类
basic/: 11个文件, 21个生成器类
contact/: 5个文件, 11个生成器类
finance/: 8个文件, 8个生成器类
identifier/: 12个文件, 19个生成器类
network/: 7个文件, 13个生成器类
numeric/: 2个文件, 8个生成器类
text/: 4个文件, 7个生成器类
```

## 🎯 下一步行动计划

### 高优先级生成器（建议立即修复）
1. **basic/name.py** - ChineseNameGenerator (高频使用)
2. **basic/phone.py** - ChinesePhoneGenerator (高频使用)
3. **basic/bankcard.py** - ChineseBankCardGenerator (高频使用)
4. **basic/age.py** - ChineseAgeGenerator (高频使用)
5. **contact/email.py** - EmailGenerator (高频使用)
6. **contact/phone.py** - PhoneGenerator (高频使用)

### 批量修复策略
1. **按类别分组修复**:
   - 第1批: basic/ 下的11个文件 (21个生成器)
   - 第2批: identifier/ 下的12个文件 (19个生成器)
   - 第3批: contact/ 下的5个文件 (11个生成器)
   - 第4批: 其余类别

2. **使用模板工具**:
   ```bash
   # 生成模板代码
   python scripts/generate_missing_methods.py BASIC param1 param2 param3

   # 复制生成的代码到对应生成器
   # 手动调整参数列表
   ```

3. **验证修复**:
   ```bash
   # 每批修复后运行检查
   python scripts/check_generator_compliance.py
   ```

## 🔧 修复模板

### 标准修复模式（适用于有 validator 的生成器）
```python
# 1. 添加导入
from ...core.types import GeneratorType

# 2. 重命名方法
def generate_single(self, context: Optional[GenerationContext] = None) -> T:
    # 原 generate() 方法的代码
    pass

# 3. 添加 validate 方法
def validate(self, data: T) -> bool:
    """验证生成的数据"""
    return self.validator.validate(data)

# 4. 添加 generator_type 属性
@property
def generator_type(self) -> GeneratorType:
    """返回生成器类型"""
    return GeneratorType.BASIC  # 根据实际情况修改

# 5. 添加 supported_parameters 属性
@property
def supported_parameters(self) -> list[str]:
    """返回支持的参数列表"""
    return ['param1', 'param2', 'param3']  # 根据实际参数修改
```

### 无 Validator 的生成器修复模式
```python
def validate(self, data: T) -> bool:
    """验证生成的数据"""
    # 实现基本验证
    return data is not None and isinstance(data, expected_type)
```

## ⏱️ 时间估算

- **已用时间**: ~4小时（基类设计、脚本创建、示例修复）
- **剩余估算**:
  - 高优先级6个生成器: 3小时
  - 其余106个生成器: 20-30小时（考虑批量操作和学习曲线）

## 📝 建议

1. **分阶段执行**: 不必一次性修复全部113个生成器
2. **优先级导向**: 先修复高频使用的生成器（basic, contact, identifier）
3. **测试驱动**: 每修复一批生成器后运行测试确保不破坏功能
4. **CI集成**: 考虑将 compliance check 集成到 CI/CD pipeline

## ⚠️ 注意事项

1. **类型参数**: 某些生成器可能需要更新类型参数定义（如 int, str, dict）
2. **Validator 实例化**: 确保所有使用 validator 的地方都正确初始化
3. **导入路径**: 确保 GeneratorType 从 core.types 导入
4. **向后兼容**: 保持现有 API 不变，generate() 继续工作

## 🎓 参考资料

- 基类定义: `dataforge/core/generator.py`
- 修复示例: `dataforge/generators/basic/idcard.py`
- 检查脚本: `scripts/check_generator_compliance.py`
- 模板生成: `scripts/generate_missing_methods.py`
