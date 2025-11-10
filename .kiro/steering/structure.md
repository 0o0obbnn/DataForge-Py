---
inclusion: auto
---

# DataForge Project Structure

## Root Directory Organization

```
dataforge/                    # Main Python package
├── api/                     # FastAPI REST API
├── auth/                    # Authentication modules
├── cli/                     # Command-line interface
├── config/                  # Configuration management
├── core/                    # Core engine (factory, registry, generator base)
├── data/                    # Reference data (regions, banks, etc.)
├── db/                      # Database models and operations
├── generators/              # Data generators by category
│   ├── basic/              # Basic types (name, age, gender, address)
│   ├── contact/            # Contact info (email, phone)
│   ├── datetime/           # Date and time generators
│   ├── finance/            # Financial data (bank cards, stocks)
│   ├── identifier/         # ID types (ID card, USCC, LEI)
│   ├── network/            # Network data (IP, MAC, URL)
│   ├── numeric/            # Numeric generators
│   └── text/               # Text generators
├── output/                  # Output formatters (JSON, CSV, XML, SQL)
└── utils/                   # Utility functions

tests/                       # Test suite
├── unit/                    # Unit tests (mirrors dataforge/ structure)
│   ├── test_core/
│   ├── test_generators/
│   ├── test_output/
│   └── test_utils/
├── integration/             # Integration tests
│   ├── test_api/
│   └── test_cli/
├── api/                     # API-specific tests
├── performance/             # Performance benchmarks
├── security/                # Security tests
├── fixtures/                # Test fixtures and sample data
└── conftest.py             # pytest configuration

web-console/                 # Vue 3 frontend
├── src/
│   ├── api/                # API client
│   ├── components/         # Vue components
│   ├── router/             # Vue Router
│   ├── stores/             # Pinia stores
│   ├── types/              # TypeScript types
│   ├── utils/              # Utility functions
│   └── views/              # Page views
└── public/                 # Static assets

docs/                        # Documentation
├── api/                    # API documentation
├── architecture/           # Architecture decisions
├── development/            # Development guides
├── guides/                 # User guides
├── plans/                  # Project plans
└── reports/                # Audit and review reports

openspec/                    # OpenSpec specifications
├── specs/                  # Current capability specs
└── changes/                # Proposed changes and archives

scripts/                     # Utility scripts
├── development/            # Development helpers
├── maintenance/            # Maintenance scripts
└── archive/                # Archived scripts

examples/                    # Usage examples
└── config_samples/         # Sample configuration files
```

## Key Architectural Patterns

### Generator Pattern
All data generators inherit from `DataGenerator[T]` base class and implement:
- `generate_single()`: Generate one data item
- `generate_batch(count)`: Generate multiple items
- `validate(data)`: Validate generated data
- `generator_type`: Property defining generator category
- `supported_parameters`: List of configurable parameters

### Factory Pattern
- `GeneratorRegistry`: Registers and manages generator classes
- `GeneratorFactory`: Creates generator instances from configurations
- `default_factory` and `default_registry`: Global singletons

### Plugin Architecture
Generators are registered via:
1. Entry points in `pyproject.toml`
2. Decorator `@register_generator()`
3. Manual registration with `default_registry.register()`

### Configuration Management
- YAML-based configuration files
- CLI parameter overrides
- Pydantic models for validation
- `GeneratorConfig` for generator parameters

## File Naming Conventions

### Python Files
- **Modules**: `snake_case.py` (e.g., `id_card.py`, `bank_card.py`)
- **Tests**: `test_<module>.py` (e.g., `test_email.py`)
- **Classes**: `PascalCase` (e.g., `EmailGenerator`, `IDCardGenerator`)
- **Functions**: `snake_case` (e.g., `generate_single`, `validate_luhn`)

### Documentation
- **Plans**: `PLAN_NAME_YYYY-MM-DD.md`
- **Reports**: `REPORT_TYPE_YYYYMMDD.md`
- **Guides**: Descriptive names in English or Chinese

### Configuration
- **YAML**: `snake_case.yaml` or descriptive names
- **Environment**: `.env.example`, `.env.development`, `.env.production`

## Module Organization Rules

### Generator Placement
Place generators in the appropriate category directory:
- **basic/**: Fundamental data types (name, age, gender, address)
- **contact/**: Communication data (email, phone, social media)
- **datetime/**: Temporal data (timestamps, date ranges)
- **finance/**: Financial data (bank cards, stocks, funds)
- **identifier/**: ID numbers (ID card, USCC, organization codes)
- **network/**: Network-related (IP, MAC, URL, domain)
- **numeric/**: Numeric data (integers, floats, ranges)
- **text/**: Text generation (lorem ipsum, sentences)

### Test Organization
Mirror the source structure in tests:
- `tests/unit/test_generators/test_basic/test_name.py` tests `dataforge/generators/basic/name.py`
- Use pytest markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.api`

### Import Conventions
```python
# Absolute imports from package root
from dataforge.core.generator import DataGenerator
from dataforge.generators.basic.name import NameGenerator

# Relative imports within same package
from .base import BaseGenerator
from ..utils import validate_format
```

## Critical Directories

- **dataforge/core/**: Core engine - do not modify without careful consideration
- **dataforge/generators/**: Add new generators here following existing patterns
- **tests/**: Maintain 80%+ coverage, especially for core modules
- **docs/**: Keep documentation synchronized with code changes
- **.kiro/steering/**: AI assistant guidance - update when conventions change
