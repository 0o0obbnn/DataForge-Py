---
inclusion: auto
---

# DataForge Technical Stack

## Backend (Python)

### Core Technologies
- **Python**: 3.9+ (supports 3.9, 3.10, 3.11, 3.12)
- **Build System**: setuptools with pyproject.toml
- **Package Manager**: pip with requirements.txt

### Key Dependencies
- **CLI**: Click 8.1.0+
- **Validation**: Pydantic 2.0.0+
- **Configuration**: PyYAML 6.0.0+
- **Data Processing**: pandas 2.0.0+
- **Fake Data**: Faker 15.0.0+
- **Date Handling**: python-dateutil 2.8.0+

### API Stack (Optional)
- **Framework**: FastAPI 0.100.0+
- **Server**: Uvicorn with standard extras
- **Auth**: python-jose with cryptography, passlib with bcrypt
- **Cache**: Redis 7.0.1+

### Development Tools
- **Testing**: pytest 7.0.0+, pytest-cov, pytest-mock
- **Formatting**: black 23.0.0+, isort 5.12.0+
- **Linting**: ruff 0.1.0+
- **Type Checking**: mypy 1.5.0+

## Frontend (Web Console)

### Core Technologies
- **Framework**: Vue 3 with Composition API
- **Language**: TypeScript
- **Build Tool**: Vite
- **State Management**: Pinia
- **HTTP Client**: Axios
- **UI Framework**: Ant Design Vue

## Common Commands

### Backend Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run tests with coverage
pytest --cov=dataforge --cov-report=term-missing

# Run specific test categories
pytest tests/ -m unit          # Unit tests only
pytest tests/ -m integration   # Integration tests only
pytest tests/ -m api           # API tests only

# Code formatting
black dataforge/
isort dataforge/

# Linting
ruff check dataforge/

# Type checking
mypy dataforge/

# Run CLI
dataforge generate idcard --count 10
dataforge generate --config config.yaml

# Start API server (development)
uvicorn dataforge.api.main:app --reload
```

### Frontend Development

```bash
# Navigate to web console
cd web-console/

# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Linting
npm run lint
```

### Testing Strategy

- **Unit Tests**: 80%+ coverage target for core business logic
- **Integration Tests**: Module interaction and API endpoints
- **Performance Tests**: Load testing with Locust or JMeter
- **Security Tests**: Input validation and dependency audits
- **Test Framework**: pytest with fixtures and markers
- **Test Organization**: Organized by module type (unit/, integration/, api/, performance/, security/)

### Code Quality Standards

- **Line Length**: 88 characters (Black default)
- **Type Hints**: Required for all public functions
- **Docstrings**: Required for all public classes and functions
- **Import Order**: isort with Black profile
- **Naming**: snake_case for Python, kebab-case for files

### Performance Optimization

- **Data Preloading**: Async preload of reference data at startup
- **Caching**: In-memory caching for frequently accessed data
- **Batch Generation**: Optimized for large-scale data generation
