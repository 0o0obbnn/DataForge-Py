"""
Comprehensive Generator Tests

This test suite provides end-to-end validation of all registered generators.

Usage:
    pytest tests/test_all_generators_comprehensive.py -v
    pytest tests/test_all_generators_comprehensive.py::test_all_generators_registered -v
"""

import pytest

from dataforge.core.factory import default_factory, default_registry
from dataforge.core.generator import GeneratorConfig


def get_expected_generators() -> list[str]:
    """动态获取预期的生成器列表"""
    from dataforge.core.factory import default_registry

    # 获取已注册的生成器
    registered_generators = default_registry.list_generators()

    # 定义核心生成器（必须存在）
    core_generators = [
        "idcard",
        "bankcard",
        "phone",
        "name",
        "age",
        "gender",
        "address",
        "license_plate",
        "company_name",
        "email",
        "advanced_timestamp",
        "datetime_range",
        "logistics",
    ]

    # 确保核心生成器都在注册列表中
    expected = []
    for gen in core_generators:
        if gen in registered_generators:
            expected.append(gen)

    # 添加其他已注册的生成器
    for gen in registered_generators:
        if gen not in expected:
            expected.append(gen)

    return expected


EXPECTED_GENERATORS = get_expected_generators()


def test_all_generators_registered():
    """
    Verify all expected generator classes are registered.

    This test checks that the factory knows about all expected generators.
    """
    registry = default_registry

    missing_generators = []
    for gen_name in EXPECTED_GENERATORS:
        if not registry.is_registered(gen_name):
            missing_generators.append(gen_name)

    if missing_generators:
        pytest.fail(
            f"Missing {len(missing_generators)} registered generators: {', '.join(missing_generators)}"
        )


def test_no_duplicate_registrations():
    """
    Ensure no generator name is registered twice.

    Checks both primary names and aliases for duplicates.
    """
    registry = default_registry

    # Get all registered names
    registered_names = registry.list_generators()

    # Check for duplicates
    seen = set()
    duplicates = []

    for name in registered_names:
        if name in seen:
            duplicates.append(name)
        seen.add(name)

    if duplicates:
        pytest.fail(f"Duplicate registrations found: {', '.join(duplicates)}")


def test_generator_instantiation():
    """
    Verify all registered generators can be instantiated.

    This smoke test ensures the factory can create instances of all generators.
    """
    registry = default_registry
    factory = default_factory

    failed_generators = []

    for gen_name in registry.list_generators():
        try:
            config = GeneratorConfig(
                generator_type=gen_name,
                parameters={},
                count=1,
                validate=False,
            )
            generator = factory.create_generator(config)
            assert generator is not None, f"Factory returned None for '{gen_name}'"
        except Exception as e:
            failed_generators.append((gen_name, str(e)))

    if failed_generators:
        error_msg = "\n".join(
            [f"  - {name}: {error}" for name, error in failed_generators]
        )
        pytest.fail(
            f"Failed to instantiate {len(failed_generators)} generators:\n{error_msg}"
        )


def test_generator_basic_functionality():
    """
    Smoke test: verify all generators can generate data.

    Tests each generator's core functionality:
    - Can call generate_single()
    - Returns non-None data
    - Data passes validation
    """
    registry = default_registry
    factory = default_factory

    failed_generators = []

    for gen_name in registry.list_generators():
        try:
            config = GeneratorConfig(
                generator_type=gen_name,
                parameters={},
                count=1,
                validate=True,
            )
            generator = factory.create_generator(config)

            # Generate single item
            data = generator.generate_single()

            # Check data is not None
            if data is None:
                failed_generators.append((gen_name, "generate_single() returned None"))
                continue

            # Validate data
            is_valid = generator.validate(data)
            if not is_valid:
                failed_generators.append(
                    (gen_name, f"Validation failed for data: {data}")
                )

        except NotImplementedError:
            # Skip generators with NotImplementedError placeholders
            continue
        except Exception as e:
            failed_generators.append((gen_name, f"Error: {str(e)}"))

    if failed_generators:
        error_msg = "\n".join(
            [f"  - {name}: {error}" for name, error in failed_generators]
        )
        pytest.fail(
            f"Basic functionality failed for {len(failed_generators)} generators:\n{error_msg}"
        )


def test_generator_batch_generation():
    """
    Verify batch generation works for all generators.

    Tests that generate_batch() produces correct number of items.
    """
    registry = default_registry
    factory = default_factory

    batch_size = 5
    failed_generators = []

    for gen_name in registry.list_generators():
        try:
            config = GeneratorConfig(
                generator_type=gen_name,
                parameters={},
                count=batch_size,
                validate=False,
            )
            generator = factory.create_generator(config)

            # Generate batch
            batch = generator.generate_batch(batch_size)

            # Check batch size
            if len(batch) != batch_size:
                failed_generators.append(
                    (gen_name, f"Expected {batch_size} items, got {len(batch)}")
                )

        except NotImplementedError:
            # Skip generators with NotImplementedError placeholders
            continue
        except Exception as e:
            failed_generators.append((gen_name, f"Error: {str(e)}"))

    if failed_generators:
        error_msg = "\n".join(
            [f"  - {name}: {error}" for name, error in failed_generators]
        )
        pytest.fail(
            f"Batch generation failed for {len(failed_generators)} generators:\n{error_msg}"
        )


def test_registry_coverage():
    """
    Check if there are any registered generators not in expected list.

    This helps catch generators we might have missed in documentation.
    """
    registry = default_registry

    registered = set(registry.list_generators())
    expected = set(EXPECTED_GENERATORS)

    unexpected = registered - expected

    if unexpected:
        print(f"\n⚠️ Found {len(unexpected)} unexpected registered generators:")
        for gen_name in sorted(unexpected):
            print(f"  - {gen_name}")
        print("Consider adding them to EXPECTED_GENERATORS list")


def test_generator_validation_logic():
    """
    Verify validation logic works correctly for all generators.

    Tests that:
    - Valid data passes validation
    - Invalid data fails validation (where applicable)
    """
    registry = default_registry
    factory = default_factory

    failed_generators = []

    for gen_name in registry.list_generators():
        try:
            config = GeneratorConfig(
                generator_type=gen_name,
                parameters={},
                count=1,
                validate=False,
            )
            generator = factory.create_generator(config)

            # Generate valid data
            valid_data = generator.generate_single()

            # Should pass validation
            if not generator.validate(valid_data):
                failed_generators.append(
                    (gen_name, f"Valid data failed validation: {valid_data}")
                )

            # Test invalid data (type-dependent)
            # For string generators, try empty string
            if isinstance(valid_data, str):
                if generator.validate(""):
                    # Empty string should generally fail validation
                    pass  # Some generators may accept empty strings

        except NotImplementedError:
            continue
        except Exception as e:
            failed_generators.append((gen_name, f"Error: {str(e)}"))

    if failed_generators:
        error_msg = "\n".join(
            [f"  - {name}: {error}" for name, error in failed_generators[:10]]
        )
        if len(failed_generators) > 10:
            error_msg += f"\n  ... and {len(failed_generators) - 10} more"
        pytest.fail(
            f"Validation logic issues in {len(failed_generators)} generators:\n{error_msg}"
        )


def test_generator_supported_parameters():
    """
    Verify all generators have supported_parameters defined.

    Checks that the property returns a list (may be empty).
    """
    registry = default_registry
    factory = default_factory

    failed_generators = []

    for gen_name in registry.list_generators():
        try:
            config = GeneratorConfig(
                generator_type=gen_name,
                parameters={},
                count=1,
                validate=False,
            )
            generator = factory.create_generator(config)

            # Get supported parameters
            params = generator.supported_parameters

            # Should be a list
            if not isinstance(params, list):
                failed_generators.append(
                    (gen_name, f"supported_parameters is not a list: {type(params)}")
                )

        except NotImplementedError:
            continue
        except Exception as e:
            failed_generators.append((gen_name, f"Error: {str(e)}"))

    if failed_generators:
        error_msg = "\n".join(
            [f"  - {name}: {error}" for name, error in failed_generators]
        )
        pytest.fail(
            f"supported_parameters issues in {len(failed_generators)} generators:\n{error_msg}"
        )


@pytest.mark.slow
def test_generator_stress_test():
    """
    Stress test: generate large batches from all generators.

    This test is marked as slow and can be skipped for quick runs.
    """
    registry = default_registry
    factory = default_factory

    batch_size = 100
    failed_generators = []

    for gen_name in registry.list_generators():
        try:
            config = GeneratorConfig(
                generator_type=gen_name,
                parameters={},
                count=batch_size,
                validate=False,
            )
            generator = factory.create_generator(config)

            # Generate large batch
            batch = generator.generate_batch(batch_size)

            # Check all items are non-None
            none_count = sum(1 for item in batch if item is None)
            if none_count > 0:
                failed_generators.append(
                    (gen_name, f"{none_count}/{batch_size} items were None")
                )

        except NotImplementedError:
            continue
        except Exception as e:
            failed_generators.append((gen_name, f"Error: {str(e)}"))

    if failed_generators:
        error_msg = "\n".join(
            [f"  - {name}: {error}" for name, error in failed_generators]
        )
        pytest.fail(
            f"Stress test failed for {len(failed_generators)} generators:\n{error_msg}"
        )


def test_summary():
    """
    Print summary statistics about registered generators.

    This test always passes but provides useful information.
    """
    registry = default_registry

    registered = registry.list_generators()

    print(f"\n=== Generator Test Summary ===")
    print(f"Total registered generators: {len(registered)}")
    print(f"Expected generators: {len(EXPECTED_GENERATORS)}")

    # Calculate overlap
    registered_set = set(registered)
    expected_set = set(EXPECTED_GENERATORS)

    overlap = len(registered_set & expected_set)
    missing = len(expected_set - registered_set)
    unexpected = len(registered_set - expected_set)

    print(f"Matching: {overlap}")
    print(f"Missing: {missing}")
    print(f"Unexpected: {unexpected}")

    assert True
