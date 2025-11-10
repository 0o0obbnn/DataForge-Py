# DataForge Generator Registration Standards

**Version**: 1.0
**Date**: 2025-11-06
**Status**: Official Standard

This document defines the authoritative standards for registering DataForge generators.

---

## Table of Contents

1. [Overview](#overview)
2. [Naming Conventions](#naming-conventions)
3. [Alias Strategies](#alias-strategies)
4. [Registration Patterns](#registration-patterns)
5. [Category-Specific Guidelines](#category-specific-guidelines)
6. [Examples](#examples)
7. [Tools](#tools)

---

## Overview

### Why Registration Matters

Generator registration makes generators discoverable through:
- CLI: `dataforge generate <name>`
- API: `POST /generate/<name>`
- Factory: `default_factory.create_generator(name)`

**Unregistered generators are invisible** to users and cannot be used.

### Registration Mechanism

Generators are registered using the `@register_generator` decorator:

```python
from dataforge.core.factory import register_generator

@register_generator("name", ["alias1", "alias2"])
class MyDataGenerator(DataGenerator[str]):
    pass
```

**Components**:
- **Primary name**: The canonical name for this generator (required)
- **Aliases**: Alternative names users can use (optional but recommended)

---

## Naming Conventions

### 1. Primary Name Format

**Rule**: Use `snake_case` without "Generator" suffix

✅ **Correct**:
```python
@register_generator("idcard")          # Not "id_card_generator"
@register_generator("phone")           # Not "PhoneGenerator"
@register_generator("email")           # Not "e_mail"
@register_generator("license_plate")   # Multi-word uses underscores
```

❌ **Incorrect**:
```python
@register_generator("IDCardGenerator")  # CamelCase
@register_generator("idcard_generator") # Includes "Generator"
@register_generator("idCard")           # camelCase
@register_generator("id-card")          # kebab-case (use as alias instead)
```

### 2. Name Derivation Process

Start with the class name and apply transformations:

1. **Remove suffixes**: `Generator`, `Gen`, `Creator`, `Builder`
   - `IDCardGenerator` → `IDCard`

2. **Convert to snake_case**:
   - `IDCard` → `id_card`

3. **Remove category prefix** (if obvious from category):
   - `basic/BasicNameGenerator` → `name` (not `basic_name`)
   - `auth/AuthTokenGenerator` → `token` (not `auth_token`)
   - Exception: Keep if needed for disambiguation

4. **Simplify common patterns**:
   - `id_card` → `idcard` (single concept)
   - `license_plate` → `license_plate` (keep distinct words)

### 3. Uniqueness Requirement

**Each primary name must be unique** across the entire system.

If a name collision occurs:
- Add category prefix: `network_url` vs `contact_url`
- Add distinguishing feature: `integer` vs `random_integer`
- Use more specific name: `mobile_phone` vs `landline_phone`

---

## Alias Strategies

### 1. Alias Principles

Aliases should maximize **discoverability** without sacrificing **clarity**.

**Priority order**:
1. Chinese translations (for Chinese users)
2. Common abbreviations/acronyms
3. Alternative spellings/formats
4. Category prefixes
5. Hyphenated versions

### 2. Chinese Aliases

**Rule**: Add Chinese translations for all user-facing data types

```python
@register_generator("idcard", ["身份证", "身份证号"])
@register_generator("bankcard", ["银行卡", "银行卡号"])
@register_generator("phone", ["手机号", "电话", "手机号码"])
@register_generator("email", ["邮箱", "电子邮件"])
@register_generator("name", ["姓名", "名字"])
@register_generator("address", ["地址"])
@register_generator("gender", ["性别"])
@register_generator("age", ["年龄"])
@register_generator("company", ["公司", "公司名"])
```

**Guidelines**:
- Use the most common Chinese term
- Add variations if widely used (e.g., "邮箱" and "电子邮件")
- Ensure aliases are natural for Chinese speakers

### 3. Abbreviations and Acronyms

**Rule**: Add well-known abbreviations

```python
@register_generator("uscc", ["统一社会信用代码", "信用代码"])  # USCC = Unified Social Credit Code
@register_generator("uuid")                                    # UUID is the standard
@register_generator("lei")                                     # LEI = Legal Entity Identifier
@register_generator("http_header", ["http-header"])           # Not abbreviated (not well-known)
```

**When to abbreviate**:
- ✅ Industry-standard acronyms (UUID, LEI, USCC)
- ✅ Very long names (3+ words) → first letters
- ❌ Domain-specific jargon (avoid unless universal)

### 4. Alternative Formats

**Rule**: Provide hyphenated versions for multi-word names

```python
@register_generator("license_plate", ["车牌号", "license-plate"])
@register_generator("bank_card", ["银行卡", "bank-card"])
@register_generator("email_verification", ["email-verification"])
```

This accommodates users who type `dataforge generate license-plate` instead of `license_plate`.

### 5. Category Prefixes

**Rule**: Add category-prefixed aliases when needed for disambiguation

```python
# contact/phone.py
@register_generator("phone", ["telephone", "mobile", "手机号", "contact_phone"])

# network/url_generator.py
@register_generator("url", ["network_url"])  # Disambiguate from contact URL

# basic/age.py
@register_generator("age", ["年龄"])  # No prefix needed (no collision)
```

**When to add category prefixes**:
- Multiple generators with similar names in different categories
- User might be confused about which one they're getting
- As a secondary alias (not primary name)

### 6. Synonyms and Variants

**Rule**: Include common synonyms that users might search for

```python
@register_generator("phone", ["telephone", "mobile", "手机号", "电话", "手机号码"])
@register_generator("email", ["e-mail", "电子邮件", "邮箱"])
@register_generator("password", ["密码", "pwd"])  # pwd is common in tech
@register_generator("username", ["用户名", "user"])
```

### 7. Alias Count Guidelines

**Recommendation**: 2-5 aliases per generator

- **Minimum**: Chinese translation (if applicable)
- **Typical**: Chinese + hyphenated + 1-2 synonyms
- **Maximum**: Avoid excessive aliases (>7) that create confusion

---

## Registration Patterns

### Pattern 1: Wrapper Class (Recommended)

**Use when**: You don't want to modify the original generator class

```python
class EmailGenerator(DataGenerator[str]):
    """Email generator implementation"""
    def generate_single(self, context=None) -> str:
        # implementation
        pass

# Register via wrapper class
@register_generator("email", ["e-mail", "电子邮件", "邮箱"])
class GenericEmailGenerator(EmailGenerator):
    """通用电子邮件生成器注册版本"""
    pass
```

**Advantages**:
- Original class untouched (easier testing, cleaner separation)
- Clear separation of registration from implementation
- Multiple registrations possible (e.g., legacy names)

**Example in codebase**: `contact/email.py`, `contact/phone.py`

### Pattern 2: Direct Decoration

**Use when**: Generator is specifically designed for one registration

```python
@register_generator("idcard", ["身份证", "身份证号"])
class IDCardGenerator(DataGenerator[str]):
    """中国身份证号码生成器"""
    def generate_single(self, context=None) -> str:
        # implementation
        pass
```

**Advantages**:
- Simpler, fewer classes
- Clear that this class IS the registered generator

**Use for**: New generators designed for single purpose

### Pattern 3: Legacy Support

**Use when**: Maintaining backward compatibility with old names

```python
class PhoneGenerator(DataGenerator[str]):
    """Phone number generator"""
    pass

# New registration (preferred name)
@register_generator("phone", ["telephone", "mobile", "手机号", "电话"])
class GenericPhoneGenerator(PhoneGenerator):
    pass

# Legacy registration (deprecated)
@register_generator("phone_legacy")
class LegacyPhoneGenerator(PhoneGenerator):
    """Deprecated: Use 'phone' instead"""
    pass
```

---

## Category-Specific Guidelines

### basic/ - Basic Data Types

**Naming**: Remove "basic" prefix (implied by category)

```python
# basic/name.py
@register_generator("name", ["姓名", "名字"])

# basic/age.py
@register_generator("age", ["年龄"])

# basic/gender.py
@register_generator("gender", ["性别"])
```

**Aliases**: Prioritize Chinese translations

### contact/ - Contact Information

**Naming**: Simple contact type names

```python
# contact/email.py
@register_generator("email", ["e-mail", "电子邮件", "邮箱"])

# contact/phone.py
@register_generator("phone", ["telephone", "mobile", "手机号", "电话", "手机号码"])

# contact/landline.py
@register_generator("landline", ["固定电话"])
```

**Aliases**: Communication method synonyms

### identifier/ - Identification Numbers

**Naming**: Use abbreviated form if standard (LEI, USCC, UUID)

```python
# identifier/id.py
@register_generator("idcard", ["身份证", "身份证号"])

# identifier/bankcard.py
@register_generator("bankcard", ["银行卡", "银行卡号"])

# identifier/uscc.py
@register_generator("uscc", ["统一社会信用代码", "信用代码"])

# identifier/lei.py
@register_generator("lei")  # Legal Entity Identifier is standard
```

**Aliases**: Chinese terms, spelled-out versions

### auth/ - Authentication

**Naming**: Auth context can be implicit or explicit

```python
# auth/password.py
@register_generator("password", ["密码"])

# auth/username.py
@register_generator("username", ["用户名", "user"])

# auth/auth_token.py
@register_generator("token", ["auth_token"])  # "token" is clear in context

# auth/session_id.py
@register_generator("session_id", ["session-id"])
```

### network/ - Network Data

**Naming**: Standard network terminology

```python
# network/network.py
@register_generator("ip_address", ["ip-address", "ip"])
@register_generator("mac_address", ["mac-address", "mac"])

# network/url_generator.py
@register_generator("url", ["网址", "network_url"])
```

**Aliases**: Technical abbreviations (IP, MAC, URL)

### finance/ - Financial Data

**Naming**: Financial terminology

```python
# finance/stock.py
@register_generator("stock_code", ["股票代码"])

# finance/bond.py
@register_generator("bond_code", ["债券代码"])
```

### numeric/ - Numeric Data

**Naming**: Mathematical/numeric concepts

```python
# numeric/number.py
@register_generator("integer", ["整数"])
@register_generator("decimal", ["小数"])
@register_generator("percentage", ["百分比"])
```

### text/ - Text Data

**Naming**: Text type or characteristic

```python
# text/string.py
@register_generator("string", ["字符串"])

# text/chinese.py
@register_generator("chinese_text", ["中文文本", "chinese-text"])
```

### advanced/ - Complex Generators

**Naming**: Descriptive of advanced functionality

```python
# advanced/datetime.py
@register_generator("timestamp", ["时间戳"])
@register_generator("cron_expression", ["cron-expression", "cron"])

# advanced/json_generator.py
@register_generator("json", ["json_object"])
```

**Note**: May include "advanced_" prefix in aliases for disambiguation

---

## Examples

### Example 1: Basic Generator

```python
# File: dataforge/generators/basic/age.py

from dataforge.core.generator import DataGenerator, GenerationContext, GeneratorType
from dataforge.core.factory import register_generator

class AgeGenerator(DataGenerator[int]):
    """年龄生成器"""

    def generate_single(self, context: Optional[GenerationContext] = None) -> int:
        min_age = self.parameters.get("min", 18)
        max_age = self.parameters.get("max", 65)
        return secrets.randbelow(max_age - min_age + 1) + min_age

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC

@register_generator("age", ["年龄"])
class GenericAgeGenerator(AgeGenerator):
    """通用年龄生成器注册版本"""
    pass
```

### Example 2: Identifier Generator

```python
# File: dataforge/generators/identifier/bankcard.py

from dataforge.core.generator import DataGenerator
from dataforge.core.factory import register_generator

class BankCardGenerator(DataGenerator[str]):
    """银行卡号生成器"""

    def generate_single(self, context=None) -> str:
        # Implementation with Luhn algorithm
        pass

@register_generator("bankcard", ["银行卡", "银行卡号", "bank-card"])
class GenericBankCardGenerator(BankCardGenerator):
    """通用银行卡号生成器注册版本"""
    pass
```

### Example 3: Complex Generator with Disambiguation

```python
# File: dataforge/generators/contact/phone.py

from dataforge.core.generator import DataGenerator
from dataforge.core.factory import register_generator

class PhoneNumberGenerator(DataGenerator[str]):
    """电话号码生成器 - 支持手机、固话、400热线"""

    def generate_single(self, context=None) -> str:
        # Implementation
        pass

# Primary registration with comprehensive aliases
@register_generator("phone", ["telephone", "mobile", "手机号", "电话", "手机号码"])
class GenericPhoneNumberGenerator(PhoneNumberGenerator):
    """通用电话号码生成器注册版本"""
    pass
```

### Example 4: Multiple Generators in One File

```python
# File: dataforge/generators/advanced/datetime.py

from dataforge.core.generator import DataGenerator
from dataforge.core.factory import register_generator

class DateGenerator(DataGenerator[str]):
    """日期生成器"""
    pass

class TimeGenerator(DataGenerator[str]):
    """时间生成器"""
    pass

class TimestampGenerator(DataGenerator[int]):
    """时间戳生成器"""
    pass

# Register each separately
@register_generator("date", ["日期"])
class GenericDateGenerator(DateGenerator):
    pass

@register_generator("time", ["时间"])
class GenericTimeGenerator(TimeGenerator):
    pass

@register_generator("timestamp", ["时间戳"])
class GenericTimestampGenerator(TimestampGenerator):
    pass
```

---

## Tools

### Registration Helper Script

Use `scripts/add_registrations.py` to automate registration:

```bash
# Scan for unregistered generators
python scripts/add_registrations.py --scan

# Suggest registration for a specific file
python scripts/add_registrations.py --suggest dataforge/generators/basic/age.py

# Apply registration to a file (generates wrapper class)
python scripts/add_registrations.py --apply dataforge/generators/basic/age.py

# Apply with custom name and aliases
python scripts/add_registrations.py --apply dataforge/generators/basic/age.py \
    --name age --aliases "年龄,age_gen"
```

**The script automatically**:
- Discovers generator classes using AST parsing
- Suggests appropriate names based on class names and categories
- Generates Chinese aliases for common data types
- Creates wrapper classes with `@register_generator` decorators

### Manual Registration Checklist

When registering manually:

- [ ] Primary name is `snake_case` without "Generator" suffix
- [ ] Primary name is unique (no collisions)
- [ ] Chinese translation added (if user-facing data type)
- [ ] Hyphenated alias added (for multi-word names)
- [ ] Common synonyms included (1-2 max)
- [ ] Category prefix added if disambiguation needed
- [ ] Wrapper class uses `Generic<X>Generator` naming pattern
- [ ] Docstring includes "通用<X>生成器注册版本"
- [ ] Tested via CLI: `dataforge generate <name> --count 5`
- [ ] Tested via factory: `default_factory.create_generator(name)`

---

## Validation

### Registration Validation

To verify registration worked:

```python
from dataforge.core.factory import default_factory

# Check if name is registered
if "age" in default_factory._generators:
    print("✅ Registered")
else:
    print("❌ Not registered")

# List all registered names
print(f"Total registered: {len(default_factory._generators)}")
for name in sorted(default_factory._generators.keys()):
    print(f"  - {name}")
```

### CLI Testing

Test each registration via CLI:

```bash
# Test primary name
dataforge generate age --count 5

# Test aliases
dataforge generate 年龄 --count 5

# Test with parameters
dataforge generate age --count 10 --age.min 25 --age.max 45
```

---

## Common Mistakes

### ❌ Mistake 1: Including "Generator" in Name

```python
# WRONG
@register_generator("age_generator")

# CORRECT
@register_generator("age")
```

### ❌ Mistake 2: Using CamelCase

```python
# WRONG
@register_generator("BankCard")

# CORRECT
@register_generator("bankcard")
```

### ❌ Mistake 3: Forgetting Chinese Aliases

```python
# WRONG (for user-facing data)
@register_generator("idcard")

# CORRECT
@register_generator("idcard", ["身份证", "身份证号"])
```

### ❌ Mistake 4: Too Many Aliases

```python
# WRONG (overwhelming)
@register_generator("phone", [
    "telephone", "mobile", "cell", "cellphone",
    "tel", "phone_number", "手机号", "电话",
    "手机号码", "移动电话", "联系电话"
])

# CORRECT (focused)
@register_generator("phone", ["telephone", "mobile", "手机号", "电话", "手机号码"])
```

### ❌ Mistake 5: Modifying Original Class

```python
# WRONG (couples registration to implementation)
@register_generator("age")
class AgeGenerator(DataGenerator[int]):
    pass

# CORRECT (separation via wrapper)
class AgeGenerator(DataGenerator[int]):
    pass

@register_generator("age", ["年龄"])
class GenericAgeGenerator(AgeGenerator):
    pass
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-06 | Initial standards document created |

---

## References

- Generator Interface: `dataforge/core/generator.py`
- Factory System: `dataforge/core/factory.py`
- Registration Helper: `scripts/add_registrations.py`
- CLAUDE.md: Project development guidelines
