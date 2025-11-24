# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

DataForge is a high-efficiency, flexible, and highly configurable test data generation tool focused on providing high-quality, realistic, and diverse test data for software testing teams, with deep optimization for Chinese localized data generation.

## Build and Development Commands

### Environment Setup
```bash
# Install in development mode
pip install -e ".[dev]"

# Install with all optional dependencies
pip install -e ".[dev,api,performance]"
```

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test files
pytest test_basic_generators.py
pytest test_finance_generators.py

# Run single test functions
python test_basic_generators.py  # Direct execution
python demo_complete_generators.py  # Demo script

# Run comprehensive tests
python test_basic_generators_comprehensive.py
python test_auth_generators_comprehensive.py
```

### Code Quality
```bash
# Format code
black dataforge/
isort dataforge/

# Lint code
ruff check dataforge/
flake8 dataforge/

# Type checking
mypy dataforge/

# Run coverage
pytest --cov=dataforge tests/
```

### Package Building
```bash
# Build package
python -m build

# Install locally
pip install -e .
```

### API Server
```bash
# Start development API server
python start_api.py

# Or using the demo script
python demo_api.py
```

## Architecture Overview

### Core Architecture
DataForge follows a plugin-based architecture with these key components:

1. **Factory Pattern**: `dataforge.core.factory` - Central registry and factory for all generators
2. **Generator Base Classes**: `dataforge.core.generator` - Abstract base classes for different generator types
3. **Context System**: `dataforge.core.context` - Manages generation context and data relationships
4. **Relation Management**: `dataforge.core.relations` - Handles dependencies between generated fields

### Generator Organization
```
dataforge/generators/
├── basic/          # Basic personal information (name, age, etc.)
├── auth/           # Authentication data (tokens, verification codes)
├── contact/        # Contact information (phone, email)
├── datetime/       # Date/time related data (timestamps, trading calendars)
├── finance/        # Financial data (bank cards, account numbers)
├── identifier/     # ID numbers (passport, driver's license, visa)
├── network/        # Network data (IP addresses, URLs)
├── security/       # Security testing data
├── structured/     # Complex structured data (JSON, media files)
```

### Key Design Patterns
- **Factory Registration**: All generators register themselves using the `@register_generator` decorator
- **Configuration-Driven**: Each generator uses `GeneratorConfig` for parameterization
- **Context-Aware**: Generators can use `GenerationContext` for related data generation
- **Validation Pipeline**: Built-in validation for generated data integrity

### Data Generation Flow
1. Configuration parsing from CLI/config files
2. Generator instantiation via factory
3. Context setup with dependencies
4. Ordered generation based on field relationships
5. Validation and output formatting

## Chinese Localization Features

### Core Chinese Data Types
- **身份证号 (ID Cards)**: 18-digit Chinese ID numbers with regional and date validation
- **银行卡号 (Bank Cards)**: Chinese bank card numbers with Luhn algorithm validation
- **手机号 (Phone Numbers)**: Chinese mobile numbers for major carriers (移动/联通/电信)
- **统一社会信用代码 (USCC)**: Unified Social Credit Code for organizations
- **中文姓名 (Names)**: Realistic Chinese names with proper surname/given name combinations

### Business Data Types
- **护照号 (Passport Numbers)**: Chinese passport formats including diplomatic passports
- **驾驶证号 (Driver's License)**: 18-digit driver's license numbers by province
- **签证号 (Visa Numbers)**: Various visa formats (US, Schengen, etc.)
- **物流单号 (Logistics Tracking)**: Major Chinese courier service formats (顺丰, 京东, etc.)

## Context-Aware Data Generation

### Relationship Management
DataForge includes an advanced context system for generating related data:

```python
# Example: Generate person with consistent data
context = GenerationContext()
person_gen = PersonDataGenerator(external_context=context)
person_data = person_gen.generate_person()

# Automatically ensures ID card matches age, email matches name, etc.
```

### Field Dependencies
The system automatically handles dependencies:
- Age ↔ ID Card birth date consistency
- Name → Email generation
- Province → Phone number area codes
- Company context → Employee data

## Common Development Workflows

### Adding New Generators
1. Create generator class inheriting from `DataGenerator`
2. Implement required abstract methods
3. Add `@register_generator` decorator
4. Create comprehensive tests
5. Update relevant `__init__.py` files

### Testing New Features
1. Write unit tests in `test_[feature].py`
2. Create integration tests for context-aware features
3. Add demo scripts showing usage examples
4. Run comprehensive test suite

### Performance Testing
Use the performance test patterns found in existing test files:
```python
# Batch generation performance
results = generator.generate_batch(1000)
# Validate generation speed and memory usage
```

## Configuration

### CLI Configuration
DataForge provides extensive CLI options for each generator type:
```bash
# Basic usage
dataforge generate idcard --count 10

# With specific parameters
dataforge generate idcard --idcard-region 北京 --idcard-gender MALE --count 5

# Using config file
dataforge generate --config config.yaml
```

### YAML Configuration
```yaml
generators:
  - generator_type: idcard
    count: 100
    parameters:
      region: "北京"
      gender: "ANY"
      birth_date_range: ["1990-01-01", "2000-12-31"]

output:
  format: json
  pretty: true
```

## Important Implementation Notes

### Generator Registration
All generators must be registered in their respective `__init__.py` files for automatic discovery. The registration system uses the factory pattern with decorator-based registration.

### Context Propagation
When working with related data generation, always use the `GenerationContext` to ensure data consistency across related fields.

### Chinese Data Validation
Chinese-specific generators include extensive validation for regional codes, check digits, and format compliance. Always test with various regional parameters.

### Performance Considerations
- Generators support both single and batch generation
- Use caching for expensive data loading operations
- Consider memory usage when generating large datasets
- The preloader system optimizes startup performance

### Error Handling
The system includes comprehensive error handling for:
- Invalid configuration parameters
- Data validation failures
- Dependency resolution issues
- Resource loading problems

## Testing Strategy

### Test File Patterns
- `test_[module]_comprehensive.py` - Full feature testing
- `test_[module].py` - Basic functionality
- `demo_[feature].py` - Usage demonstrations
- Integration tests in main directory

### Validation Testing
All generators include validation methods that should be tested for:
- Format compliance
- Business rule adherence
- Edge case handling
- Performance under load

## Development Status

The project has completed development of P1-P3 priority features as documented in `PROJECT_COMPLETION_SUMMARY.md`. All core generators are implemented and tested, with extensive Chinese localization support and context-aware data generation capabilities.
