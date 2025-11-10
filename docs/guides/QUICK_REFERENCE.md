# Quick Reference: Generator Verification Suite

Quick commands for running verification checks on DataForge generators.

## 🚀 Quick Commands

### Run Everything
```bash
# Full audit suite (recommended before commits)
python scripts/run_generator_audits.py

# With detailed output
python scripts/run_generator_audits.py --verbose

# Generate JSON reports
python scripts/run_generator_audits.py --json --output-dir my_reports/
```

### Individual Checks

```bash
# Check if all generators are registered
python scripts/audit_generator_registration.py

# Validate type safety
python scripts/validate_generator_types.py

# Security audit
python scripts/audit_security_issues.py

# Code quality scan
python scripts/scan_code_quality.py
```

### Run Tests

```bash
# Interface compliance tests
pytest tests/test_generator_interface_compliance.py -v

# Comprehensive functional tests
pytest tests/test_all_generators_comprehensive.py -v

# Run specific test
pytest tests/test_generator_interface_compliance.py::test_generator_implements_interface -v

# Skip slow tests
pytest tests/test_all_generators_comprehensive.py -m "not slow"
```

## 📊 Current Status (as of 2025-11-05)

```
Total generator classes: 192
Registered: 72 (37.5%)
Unregistered: 120 (62.5%)

Issues Found:
├── Critical: 131
│   ├── Unregistered generators: 120
│   └── Test files in production: 2
│   └── Duplicate files: 9
├── High Priority: 22
│   ├── TODO placeholders: 20
│   └── Legacy code: 2
└── Medium: 68
    └── Empty supported_parameters: 68

Overall Status: FAILING ❌
```

## 🎯 Priority Actions

1. **CRITICAL (Do First)**
   ```bash
   # Find unregistered generators
   python scripts/audit_generator_registration.py > unregistered.txt

   # Add @register_generator decorators to top 10
   # Then re-run to verify
   python scripts/audit_generator_registration.py
   ```

2. **CRITICAL (Clean Up)**
   ```bash
   # Find test files in production
   python scripts/scan_code_quality.py | grep "TEST_FILE"

   # Move files:
   # dataforge/generators/basic/test_marital_status.py → tests/generators/basic/
   # dataforge/generators/advanced/test_advanced_timestamp.py → tests/generators/advanced/
   ```

3. **HIGH PRIORITY**
   ```bash
   # Find TODO placeholders
   python scripts/scan_code_quality.py --verbose | grep "TODO"

   # Remove placeholders or implement functionality
   ```

## 📈 Tracking Progress

### Before Each Work Session
```bash
# Baseline check
python scripts/run_generator_audits.py > baseline.txt
```

### After Making Changes
```bash
# Verify improvements
python scripts/run_generator_audits.py > after_fix.txt

# Compare
diff baseline.txt after_fix.txt
```

### Track Metrics Over Time
```bash
# Save timestamped reports
python scripts/run_generator_audits.py --json --output-dir audit_history/

# View trends
ls -lh audit_history/
```

## 🔍 Common Workflows

### Adding a New Generator

```bash
# 1. Create generator file
# 2. Add @register_generator decorator
# 3. Verify registration
python scripts/audit_generator_registration.py | grep "MyNewGenerator"

# 4. Check interface compliance
pytest tests/test_generator_interface_compliance.py -k "MyNewGenerator"

# 5. Test functionality
pytest tests/test_all_generators_comprehensive.py -k "mynew"
```

### Fixing Registration Issues

```bash
# 1. Find unregistered
python scripts/audit_generator_registration.py | grep "UNREGISTERED" -A 200 > to_fix.txt

# 2. For each generator, add decorator:
@register_generator("generator_name", ["alias1", "alias2"])
class MyGenerator(DataGenerator[str]):
    ...

# 3. Verify
python scripts/audit_generator_registration.py
```

### Fixing Type Issues

```bash
# 1. Find type problems
python scripts/validate_generator_types.py > type_issues.txt

# 2. Fix enum values
# Replace: GeneratorType.BASIC_INFO
# With: GeneratorType.BASIC

# 3. Fix return types
# Ensure child matches parent generic type

# 4. Verify
python scripts/validate_generator_types.py
```

## 🛠️ Troubleshooting

### "Module not found" errors
```bash
# Ensure project is installed
pip install -e ".[dev]"

# Verify installation
python -c "import dataforge; print(dataforge.__file__)"
```

### "pytest not found"
```bash
# Install test dependencies
pip install pytest pytest-cov

# Or full dev dependencies
pip install -e ".[dev]"
```

### Scripts hang or timeout
```bash
# Run with timeout
timeout 300 python scripts/run_generator_audits.py

# Or skip problematic checks
python scripts/run_generator_audits.py --scripts-only
```

## 📝 Exit Codes

All scripts follow standard exit codes:

- `0`: Success - all checks passed ✅
- `1`: Failure - critical issues found ❌
- `2`: Warning - non-critical issues ⚠️

```bash
# Check exit code
python scripts/audit_generator_registration.py
echo $?  # Linux/Mac
echo %ERRORLEVEL%  # Windows
```

## 🔄 CI/CD Integration

### Pre-commit Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash
python scripts/run_generator_audits.py
if [ $? -ne 0 ]; then
    echo "Generator audits failed. Fix issues before committing."
    exit 1
fi
```

### GitHub Actions
```yaml
# .github/workflows/audits.yml
name: Generator Audits
on: [push, pull_request]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -e ".[dev]"
      - run: python scripts/run_generator_audits.py --json
      - uses: actions/upload-artifact@v3
        with:
          name: audit-reports
          path: audit_results/
```

## 📚 Documentation

- **Full Documentation**: `scripts/README.md`
- **Implementation Summary**: `VERIFICATION_SUITE_SUMMARY.md`
- **Code Review Report**: `generator_code_review_2025-11-05.md`

## 🎓 Best Practices

1. **Run audits frequently** - before every commit
2. **Fix critical issues first** - registration, interface violations
3. **Track progress** - save reports over time
4. **Use verbose mode** - when investigating issues
5. **Review JSON output** - for detailed metrics

## 💡 Tips

- Use `--json` flag for machine-readable output
- Use `--verbose` for debugging
- Save reports to track progress: `--output-dir history/`
- Run specific tests: `-k "pattern"`
- Skip slow tests: `-m "not slow"`

## 🚨 Known Issues

As of 2025-11-05:
- 120 generators need `@register_generator` decorator
- 2 test files in production code directories
- 9 duplicate generator files
- 20 TODO/placeholder implementations
- 68 empty `supported_parameters` properties

## 📞 Getting Help

```bash
# Script help
python scripts/run_generator_audits.py --help

# Pytest help
pytest --help

# View documentation
cat scripts/README.md
```

---

**Quick Start**: `python scripts/run_generator_audits.py`

**Status Check**: `python scripts/audit_generator_registration.py`

**Full Documentation**: `scripts/README.md`
