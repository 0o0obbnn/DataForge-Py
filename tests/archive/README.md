# Test Archive

This directory contains archived test files that are no longer actively used but preserved for reference.

## Archive Policy

Files are archived when:
- They have been replaced by newer, better-structured tests
- They were experimental or temporary test scripts
- They are no longer compatible with current codebase

## Archived Files Status

### Obsolete Files (Can be deleted)
These files are simple test scripts that have been replaced by proper pytest tests:

1. **test_hello.py** - Simple "Hello World" script, no actual tests
2. **simple_test.py** - Basic import test, replaced by proper unit tests
3. **test_marital_simple.py** - Simple marital status test, replaced by `tests/unit/test_generators/test_basic/test_marital_status.py`
4. **run_test.py** - Old test runner, replaced by pytest
5. **run_unit_test.py** - Old test runner, replaced by pytest
6. **run_all_tests.py** - Old test runner, replaced by pytest
7. **diagnose_test.py** - Diagnostic script, no longer needed
8. **test_import.py** - Import test, replaced by proper tests
9. **test_import_unit.py** - Import test, replaced by proper tests

### Integration Test Archives (Replaced)
These integration tests have been superseded by current integration tests:

10. **integration_test.py** - Old integration test
11. **integration_test_updated.py** - Updated version, still old
12. **integration_test_final.py** - "Final" version, but replaced
13. **e2e_test.py** - Old E2E test
14. **e2e_test_fixed.py** - Fixed version, but replaced
15. **comprehensive_test.py** - Comprehensive test, replaced by organized test suite

### Generator Test Archives (Replaced)
These generator tests have been replaced by organized unit tests:

16. **test_basic_generators.py** - Replaced by tests in `tests/unit/test_generators/`
17. **test_new_generators.py** - Replaced by organized generator tests
18. **test_enhanced_coverage.py** - Coverage test, replaced by pytest-cov
19. **test_marital_full_integration.py** - Replaced by proper integration tests
20. **test_marital_status_simple.py** - Replaced by unit test
21. **test_phone_type_safe.py** - Replaced by `tests/unit/test_generators/test_contact/test_phone.py`

### API Test Archives (Replaced)
22. **test_api.py** - Replaced by `tests/integration/test_api/`
23. **test_api_direct.py** - Replaced by proper API tests

### Fix/Debug Archives (Temporary)
24. **test_fixes.py** - Temporary fix test
25. **test_type_fix.py** - Type fix test
26. **test_generator_interface.py** - Interface test, replaced by proper tests

## Cleanup Recommendation

**Action**: Delete all 26 files listed above
**Reason**: All functionality is now covered by the organized test suite in:
- `tests/unit/` - Unit tests
- `tests/integration/` - Integration tests
- `tests/performance/` - Performance tests

**Date**: 2025-11-07
**Reviewed by**: AI Assistant
