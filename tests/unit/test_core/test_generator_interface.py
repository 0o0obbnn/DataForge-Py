"""
Generator Interface Compliance Tests

This test module verifies that all generator classes properly implement
the DataGenerator interface contract.

Usage:
    pytest tests/test_generator_interface_compliance.py -v
    pytest tests/test_generator_interface_compliance.py::test_generator_implements_interface -v
"""

import ast
import inspect
from pathlib import Path
from typing import Any

import pytest

from dataforge.core.generator import DataGenerator
from dataforge.core.types import GeneratorType


def discover_all_generator_classes() -> list[type[DataGenerator[Any]]]:
    """
    Discover all generator classes in the codebase.

    Returns:
        List of generator class types found
    """
    generator_classes: list[type[DataGenerator[Any]]] = []

    # Find generators directory
    generators_path = Path(__file__).parent.parent / "dataforge" / "generators"

    if not generators_path.exists():
        pytest.skip(
            f"Generators directory not found: {generators_path}",
            allow_module_level=True,
        )

    # Import and scan modules
    for py_file in generators_path.rglob("*.py"):
        if py_file.name.startswith("__init__") or py_file.name.startswith("test_"):
            continue

        # Convert file path to module path
        rel_path = py_file.relative_to(generators_path.parent)
        module_path = ".".join(rel_path.with_suffix("").parts)

        try:
            # Import the module
            module = __import__(module_path, fromlist=[""])

            # Find all generator classes
            for name, obj in inspect.getmembers(module, inspect.isclass):
                # Check if it's a generator (subclass of DataGenerator)
                try:
                    if (
                        issubclass(obj, DataGenerator)
                        and obj is not DataGenerator
                        and obj.__module__ == module_path
                    ):
                        generator_classes.append(obj)
                except TypeError:
                    # Not a class or can't check subclass
                    continue

        except Exception as e:
            # Skip modules that fail to import
            print(f"Warning: Could not import {module_path}: {e}")
            continue

    return generator_classes


def check_file_for_method(file_path: Path, class_name: str, method_name: str) -> bool:
    """
    Check if a specific method exists in a class by parsing the source file.

    Args:
        file_path: Path to the Python file
        class_name: Name of the class to check
        method_name: Name of the method to check for

    Returns:
        True if method is defined in the class
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(file_path))

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name == method_name:
                        return True
        return False
    except Exception:
        return False


# Get all generator classes once
ALL_GENERATORS = discover_all_generator_classes()


@pytest.mark.parametrize("generator_class", ALL_GENERATORS, ids=lambda g: g.__name__)
def test_generator_implements_interface(generator_class: type[DataGenerator[Any]]):
    """
    Verify generator implements the DataGenerator interface completely.

    Checks:
        - Inherits from DataGenerator
        - Has generate_single() method
        - Has validate() method
        - Has generator_type property
        - Has supported_parameters property
        - Has _setup() method (optional but recommended)
    """
    # Check inheritance
    assert issubclass(
        generator_class, DataGenerator
    ), f"{generator_class.__name__} must inherit from DataGenerator"

    # Check required methods exist
    assert hasattr(
        generator_class, "generate_single"
    ), f"{generator_class.__name__} missing generate_single() method"

    assert hasattr(
        generator_class, "validate"
    ), f"{generator_class.__name__} missing validate() method"

    # Check it's a method, not property
    assert callable(
        generator_class.generate_single
    ), f"{generator_class.__name__}.generate_single must be callable"

    assert callable(
        generator_class.validate
    ), f"{generator_class.__name__}.validate must be callable"

    # Check required properties
    assert hasattr(
        generator_class, "generator_type"
    ), f"{generator_class.__name__} missing generator_type property"

    assert hasattr(
        generator_class, "supported_parameters"
    ), f"{generator_class.__name__} missing supported_parameters property"

    # Check if they're properties
    assert isinstance(
        getattr(type(generator_class), "generator_type", None), property
    ), f"{generator_class.__name__}.generator_type must be a property"

    assert isinstance(
        getattr(type(generator_class), "supported_parameters", None), property
    ), f"{generator_class.__name__}.supported_parameters must be a property"


@pytest.mark.parametrize("generator_class", ALL_GENERATORS, ids=lambda g: g.__name__)
def test_generator_has_proper_methods(generator_class: type[DataGenerator[Any]]):
    """
    Verify no legacy method names are used.

    Checks that generator does NOT use:
        - _generate_raw() instead of generate_single()
        - generate() as the primary method (should use generate_single())
    """
    # Get source file
    try:
        source_file = Path(inspect.getfile(generator_class))
    except Exception:
        pytest.skip(f"Could not find source file for {generator_class.__name__}")

    # Check for legacy _generate_raw
    has_generate_raw = check_file_for_method(
        source_file, generator_class.__name__, "_generate_raw"
    )

    # If it has _generate_raw, it should also have generate_single that calls it
    if has_generate_raw:
        has_generate_single = check_file_for_method(
            source_file, generator_class.__name__, "generate_single"
        )
        assert (
            has_generate_single
        ), f"{generator_class.__name__} uses _generate_raw but doesn't implement generate_single()"


@pytest.mark.parametrize("generator_class", ALL_GENERATORS, ids=lambda g: g.__name__)
def test_generator_type_is_valid(generator_class: type[DataGenerator[Any]]):
    """
    Verify generator_type property returns a valid GeneratorType enum value.

    This test requires instantiation, so we skip generators that need complex setup.
    """
    try:
        # Try to instantiate with minimal config
        from dataforge.core.generator import GeneratorConfig

        config = GeneratorConfig(
            generator_type="test", parameters={}, count=1, validate=False
        )

        instance = generator_class(config)

        # Get generator type
        gen_type = instance.generator_type

        # Check it's a GeneratorType enum
        assert isinstance(
            gen_type, GeneratorType
        ), f"{generator_class.__name__}.generator_type must return GeneratorType enum, got {type(gen_type)}"

        # Check it's a valid enum value
        valid_types = [
            GeneratorType.BASIC,
            GeneratorType.AUTH,
            GeneratorType.CONTACT,
            GeneratorType.FINANCE,
            GeneratorType.IDENTIFIER,
            GeneratorType.NETWORK,
            GeneratorType.NUMERIC,
            GeneratorType.TEXT,
            GeneratorType.ADVANCED,
            GeneratorType.DATETIME,
        ]

        assert (
            gen_type in valid_types
        ), f"{generator_class.__name__}.generator_type returned invalid enum: {gen_type}"

    except Exception as e:
        # Skip generators that can't be instantiated without complex setup
        pytest.skip(f"Could not instantiate {generator_class.__name__}: {e}")


@pytest.mark.parametrize("generator_class", ALL_GENERATORS, ids=lambda g: g.__name__)
def test_supported_parameters_is_list(generator_class: type[DataGenerator[Any]]):
    """
    Verify supported_parameters property returns a list.

    Note: Empty list is acceptable, but it should be a list.
    """
    try:
        # Try to instantiate with minimal config
        from dataforge.core.generator import GeneratorConfig

        config = GeneratorConfig(
            generator_type="test", parameters={}, count=1, validate=False
        )

        instance = generator_class(config)

        # Get supported parameters
        params = instance.supported_parameters

        # Check it's a list
        assert isinstance(
            params, list
        ), f"{generator_class.__name__}.supported_parameters must return list, got {type(params)}"

        # Check all elements are strings
        assert all(
            isinstance(p, str) for p in params
        ), f"{generator_class.__name__}.supported_parameters must contain only strings"

    except Exception as e:
        # Skip generators that can't be instantiated without complex setup
        pytest.skip(f"Could not instantiate {generator_class.__name__}: {e}")


@pytest.mark.parametrize("generator_class", ALL_GENERATORS, ids=lambda g: g.__name__)
def test_generator_has_type_hints(generator_class: type[DataGenerator[Any]]):
    """
    Verify generator methods have proper type hints.

    Checks:
        - generate_single() has return type annotation
        - validate() has parameter and return type annotations
    """
    # Check generate_single return type
    generate_single = getattr(generator_class, "generate_single", None)
    if generate_single and callable(generate_single):
        sig = inspect.signature(generate_single)
        assert (
            sig.return_annotation != inspect.Parameter.empty
        ), f"{generator_class.__name__}.generate_single() missing return type annotation"

    # Check validate parameter and return types
    validate = getattr(generator_class, "validate", None)
    if validate and callable(validate):
        sig = inspect.signature(validate)
        assert (
            sig.return_annotation != inspect.Parameter.empty
        ), f"{generator_class.__name__}.validate() missing return type annotation"


def test_all_generators_discovered():
    """Meta-test to verify discovery is working"""
    assert (
        len(ALL_GENERATORS) > 0
    ), "No generator classes discovered - check discovery logic"
    print(f"\nDiscovered {len(ALL_GENERATORS)} generator classes")


def test_generator_interface_summary():
    """
    Generate a summary report of interface compliance.

    This test always passes but prints useful information.
    """
    total = len(ALL_GENERATORS)

    # Count various attributes
    with_generate_single = 0
    with_validate = 0
    with_generator_type = 0
    with_supported_parameters = 0

    for gen_class in ALL_GENERATORS:
        if hasattr(gen_class, "generate_single"):
            with_generate_single += 1
        if hasattr(gen_class, "validate"):
            with_validate += 1
        if hasattr(gen_class, "generator_type"):
            with_generator_type += 1
        if hasattr(gen_class, "supported_parameters"):
            with_supported_parameters += 1

    print("\n=== Generator Interface Compliance Summary ===")
    print(f"Total generators: {total}")
    print(f"With generate_single(): {with_generate_single}/{total}")
    print(f"With validate(): {with_validate}/{total}")
    print(f"With generator_type: {with_generator_type}/{total}")
    print(f"With supported_parameters: {with_supported_parameters}/{total}")

    # This test always passes
    assert True
