# Contributing to DataForge

We welcome contributions to DataForge! This guide will help you contribute effectively.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Generator Development](#generator-development)
- [Generator Registration](#generator-registration)
- [Testing Requirements](#testing-requirements)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

- **Be respectful** in all interactions
- **Provide constructive feedback** on code reviews
- **Ask questions** when requirements are unclear
- **Document your code** thoroughly
- **Write tests** for new functionality

---

## How to Contribute

### Types of Contributions

We welcome:
- **New generators** for additional data types
- **Bug fixes** and performance improvements
- **Documentation** enhancements
- **Test coverage** improvements
- **Feature requests** and ideas

### Getting Started

1. **Fork** the repository
2. **Create a feature branch** from `main`
3. **Make your changes** following our standards
4. **Test thoroughly** with pytest
5. **Submit a pull request** with clear description

---

## Development Setup

### Prerequisites

- Python 3.9+
- pip or uv package manager
- Git

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/dataforge.git
cd dataforge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Install with all extras (API, performance, etc.)
pip install -e ".[dev,api,performance]"
```

### Verify Installation

```bash
# Run tests
pytest tests/

# Run code quality checks
black dataforge/ && isort dataforge/ && ruff check dataforge/ && mypy dataforge/

# Test CLI
dataforge generate idcard --count 5
```

---

## Generator Development

### Generator Interface Requirements

All generators MUST implement the `DataGenerator[T]` interface:

```python
from dataforge.core.generator import DataGenerator, GenerationContext, GeneratorType
from typing import Optional

class MyDataGenerator(DataGenerator[str]):
    """My custom data generator"""

    def _setup(self) -> None:
        """Initialize generator-specific state from self.parameters"""
        self.my_param = self.parameters.get("my_param", "default")

    def generate_single(self, context: Optional[GenerationContext] = None) -> str:
        """Generate single data item (REQUIRED)"""
        # Your generation logic here
        return "generated_value"

    def validate(self, data: str) -> bool:
        """Validate generated data (REQUIRED)"""
        # Your validation logic here
        return isinstance(data, str) and len(data) > 0

    @property
    def generator_type(self) -> GeneratorType:
        """Return generator category (REQUIRED)"""
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        """Return list of supported parameter names (REQUIRED)"""
        return ["my_param"]
```

### Generator Categories

Place your generator in the appropriate directory:

- `basic/` - Basic data types (name, age, gender, etc.)
- `contact/` - Contact information (phone, email, address)
- `identifier/` - ID numbers (idcard, bankcard, passport, etc.)
- `auth/` - Authentication data (password, username, token)
- `network/` - Network data (IP, MAC, URL, etc.)
- `finance/` - Financial data (stock codes, transactions)
- `numeric/` - Numeric data (integers, decimals, ranges)
- `text/` - Text data (strings, Chinese text, multilingual)
- `advanced/` - Complex generators (JSON, XML, timestamps)

### Optional Methods

Override these for optimization or special behavior:

```python
def generate_batch(self, count: int, context: Optional[GenerationContext] = None) -> list[T]:
    """Override for batch generation optimization"""
    return [self.generate_single(context) for _ in range(count)]

def _get_related_value(self, context: GenerationContext, field: str) -> Any:
    """Extract related field values from context"""
    return context.get_generated_data(field)
```

---

## Generator Registration

**IMPORTANT**: All generators MUST be registered to be discoverable by users.

### Quick Start

Use the registration helper script:

```bash
# Scan for unregistered generators
python scripts/add_registrations.py --scan

# Get suggestions for a specific file
python scripts/add_registrations.py --suggest dataforge/generators/basic/my_generator.py

# Apply registration automatically
python scripts/add_registrations.py --apply dataforge/generators/basic/my_generator.py
```

### Manual Registration

If registering manually, use the **wrapper class pattern**:

```python
from dataforge.core.factory import register_generator

class MyDataGenerator(DataGenerator[str]):
    """Implementation class"""
    # ... implementation ...

# Register with wrapper class
@register_generator("my_data", ["my-data", "我的数据"])
class GenericMyDataGenerator(MyDataGenerator):
    """通用my_data生成器注册版本"""
    pass
```

### Registration Standards

Follow the **[REGISTRATION_STANDARDS.md](./REGISTRATION_STANDARDS.md)** document for detailed guidelines:

**Key Rules**:
- Primary name in `snake_case` without "Generator" suffix
- Add Chinese translations for user-facing data types
- Include 2-5 relevant aliases
- Use wrapper class pattern (`Generic<X>Generator`)
- Ensure unique primary names (no collisions)

**Example**:
```python
@register_generator("phone", ["telephone", "mobile", "手机号", "电话", "手机号码"])
class GenericPhoneNumberGenerator(PhoneNumberGenerator):
    """通用电话号码生成器注册版本"""
    pass
```

See [REGISTRATION_STANDARDS.md](./REGISTRATION_STANDARDS.md) for:
- Detailed naming conventions
- Category-specific guidelines
- Alias strategies
- Complete examples
- Common mistakes to avoid

---

## Testing Requirements

### Test Coverage

All new generators MUST include unit tests covering:

- ✅ **Valid data generation** (basic functionality)
- ✅ **Parameter validation** (invalid inputs rejected)
- ✅ **Edge cases** (min/max values, boundary conditions)
- ✅ **Data validation** (validate() method works correctly)
- ✅ **Batch generation** (generate_batch() if overridden)
- ✅ **Registration** (generator is discoverable by name/aliases)

### Test File Location

Place tests in `tests/generators/<category>/`:

```
tests/
└── generators/
    ├── basic/
    │   └── test_my_generator.py
    ├── contact/
    ├── identifier/
    └── ...
```

### Test Template

```python
import pytest
from dataforge.core.factory import default_factory

class TestMyDataGenerator:
    """Test suite for MyDataGenerator"""

    def test_generation_basic(self):
        """Test basic data generation"""
        generator = default_factory.create_generator("my_data")
        result = generator.generate_single()
        assert result is not None
        assert generator.validate(result)

    def test_generation_with_parameters(self):
        """Test generation with parameters"""
        generator = default_factory.create_generator(
            "my_data",
            my_param="custom_value"
        )
        result = generator.generate_single()
        assert "custom_value" in result

    def test_batch_generation(self):
        """Test batch generation"""
        generator = default_factory.create_generator("my_data")
        results = generator.generate_batch(100)
        assert len(results) == 100
        assert all(generator.validate(r) for r in results)

    def test_validation_invalid_data(self):
        """Test validation rejects invalid data"""
        generator = default_factory.create_generator("my_data")
        assert not generator.validate("")
        assert not generator.validate(None)

    def test_registration_by_name(self):
        """Test generator is registered by primary name"""
        generator = default_factory.create_generator("my_data")
        assert generator is not None

    def test_registration_by_alias(self):
        """Test generator is registered by aliases"""
        generator = default_factory.create_generator("my-data")  # alias
        assert generator is not None
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/generators/basic/test_my_generator.py

# Run with coverage
pytest tests/ --cov=dataforge --cov-report=html

# Run only unit tests
pytest tests/ -m unit

# Run specific test function
pytest tests/generators/basic/test_my_generator.py::TestMyDataGenerator::test_generation_basic
```

---

## Code Style

### Standards

DataForge enforces strict code quality standards:

- **PEP 8**: Python style guide (via Black formatter)
- **Type hints**: All functions, methods, variables
- **Docstrings**: PEP 257 format for all public APIs
- **Import sorting**: isort with Black profile
- **Linting**: ruff for code quality

### Formatting

```bash
# Format code (run before committing)
black dataforge/

# Sort imports
isort dataforge/

# Lint with ruff
ruff check dataforge/

# Type check with mypy
mypy dataforge/

# Run all checks
black dataforge/ && isort dataforge/ && ruff check dataforge/ && mypy dataforge/
```

### Naming Conventions

- **Variables/functions**: `snake_case` (e.g., `user_name`, `generate_data`)
- **Classes**: `CamelCase` (e.g., `DataGenerator`, `IDCardGenerator`)
- **Constants**: `ALL_CAPS` (e.g., `DEFAULT_BATCH_SIZE`)
- **Private members**: `_single_underscore` prefix
- **Registration names**: `snake_case` without "Generator" suffix

### Security

- **NEVER use `random` module** for security-sensitive data (use `secrets`)
- **NEVER hardcode** credentials, API keys, or sensitive data
- **NEVER log** generated ID cards, bank cards, or PII in production
- **ALWAYS validate** user inputs (CLI args, API requests, config files)
- **ALWAYS use** parameterized queries (prevent SQL injection)

```python
# ❌ WRONG - Insecure
import random
phone_digit = str(random.randint(0, 9))

# ✅ CORRECT - Secure
import secrets
phone_digit = str(secrets.randbelow(10))
```

---

## Pull Request Process

### Before Submitting

1. **Update tests** for your changes
2. **Run code quality checks** (`black`, `isort`, `ruff`, `mypy`)
3. **Run test suite** and ensure all tests pass
4. **Update documentation** if adding features
5. **Check git status** for unintended files

```bash
# Pre-submission checklist
black dataforge/ && isort dataforge/ && ruff check dataforge/
pytest tests/
git status
```

### Pull Request Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix/feature causing existing functionality to change)
- [ ] Documentation update

## Testing
- [ ] Added unit tests for new functionality
- [ ] All tests pass locally
- [ ] Code quality checks pass (black, isort, ruff, mypy)

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly hard-to-understand areas
- [ ] I have updated documentation where needed
- [ ] My changes generate no new warnings
- [ ] I have added tests proving my fix/feature works
- [ ] New and existing tests pass locally

## Related Issues
Closes #<issue_number>
```

### PR Review Process

1. **Automated CI checks** run (tests, linting, type checking)
2. **Code review** by maintainers
3. **Feedback addressed** (if changes requested)
4. **Approval** from at least one maintainer
5. **Merge** to main branch

### After Merge

- Your contribution will be included in the next release
- You'll be added to CONTRIBUTORS.md (if not already)
- Close any related issues

---

## Additional Resources

### Documentation

- [CLAUDE.md](./CLAUDE.md) - Project overview and development guidelines
- [REGISTRATION_STANDARDS.md](./REGISTRATION_STANDARDS.md) - Generator registration standards
- [README.md](./README.md) - Project README
- [ARCHITECTURE.md](./docs/ARCHITECTURE.md) - System architecture (if exists)

### Tools

- **Registration Helper**: `scripts/add_registrations.py`
- **Test Runner**: `pytest tests/`
- **Code Formatter**: `black dataforge/`
- **Import Sorter**: `isort dataforge/`
- **Linter**: `ruff check dataforge/`
- **Type Checker**: `mypy dataforge/`

### Getting Help

- **Issues**: Create an issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Pull Requests**: Submit PRs for code contributions

---

## Quick Reference

### Common Commands

```bash
# Development setup
pip install -e ".[dev]"

# Run tests
pytest tests/

# Code quality
black dataforge/ && isort dataforge/ && ruff check dataforge/ && mypy dataforge/

# Register generators
python scripts/add_registrations.py --scan
python scripts/add_registrations.py --apply <file>

# Test CLI
dataforge generate <name> --count 10

# Check registration
python -c "from dataforge.core.factory import default_factory; print(sorted(default_factory._generators.keys()))"
```

### File Structure

```
dataforge/
├── generators/
│   ├── basic/           # Your new generator here
│   ├── contact/
│   ├── identifier/
│   └── ...
├── core/
│   ├── generator.py     # Base class
│   └── factory.py       # Registration system
└── ...

tests/
└── generators/
    ├── basic/           # Your tests here
    └── ...

scripts/
└── add_registrations.py  # Registration helper
```

---

## Thank You!

Thank you for contributing to DataForge! Your contributions help make test data generation better for everyone.

If you have questions, don't hesitate to ask through GitHub Issues or Discussions.
