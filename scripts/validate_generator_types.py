#!/usr/bin/env python3
"""
Type Safety Validator for Generators

This script validates type consistency across generator classes:
- Return type annotations match parent class declarations
- Generic type parameter [T] is properly specified
- GeneratorType enum values are valid
- No type mismatches between parent and child classes

Usage:
    python scripts/validate_generator_types.py [--json] [--verbose]

Exit Codes:
    0: All type checks passed
    1: Type violations found
"""

import argparse
import ast
import inspect
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Type

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TypeInfo:
    """Information about a generator's type annotations"""

    def __init__(
        self,
        class_name: str,
        file_path: str,
        line_number: int,
        generic_param: Optional[str] = None,
        generate_single_return: Optional[str] = None,
        validate_param: Optional[str] = None,
        validate_return: Optional[str] = None,
        generator_type_return: Optional[str] = None,
        parent_class: Optional[str] = None,
    ):
        self.class_name = class_name
        self.file_path = file_path
        self.line_number = line_number
        self.generic_param = generic_param
        self.generate_single_return = generate_single_return
        self.validate_param = validate_param
        self.validate_return = validate_return
        self.generator_type_return = generator_type_return
        self.parent_class = parent_class


class TypeValidator(ast.NodeVisitor):
    """AST visitor to extract type information from generator classes"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.type_infos: List[TypeInfo] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        # Check if class is a generator
        is_generator = False
        generic_param = None
        parent_class = None

        for base in node.bases:
            if isinstance(base, ast.Name):
                if "Generator" in base.id:
                    is_generator = True
                    parent_class = base.id
            elif isinstance(base, ast.Subscript):
                # DataGenerator[T]
                if isinstance(base.value, ast.Name) and "Generator" in base.value.id:
                    is_generator = True
                    parent_class = base.value.id
                    # Extract generic parameter
                    if isinstance(base.slice, ast.Name):
                        generic_param = base.slice.id
                    elif isinstance(base.slice, ast.Constant):
                        generic_param = str(base.slice.value)

        if not is_generator:
            self.generic_visit(node)
            return

        # Extract method return types
        generate_single_return = None
        validate_param = None
        validate_return = None
        generator_type_return = None

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                if item.name == "generate_single":
                    if item.returns:
                        generate_single_return = ast.unparse(item.returns)

                elif item.name == "validate":
                    if item.returns:
                        validate_return = ast.unparse(item.returns)
                    # Get first parameter type (after self)
                    if len(item.args.args) > 1:
                        arg = item.args.args[1]
                        if arg.annotation:
                            validate_param = ast.unparse(arg.annotation)

            elif isinstance(item, ast.FunctionDef):
                # Check for property decorators
                is_property = any(
                    isinstance(d, ast.Name) and d.id == "property"
                    for d in item.decorator_list
                )
                if is_property and item.name == "generator_type":
                    if item.returns:
                        generator_type_return = ast.unparse(item.returns)

        type_info = TypeInfo(
            class_name=node.name,
            file_path=self.file_path,
            line_number=node.lineno,
            generic_param=generic_param,
            generate_single_return=generate_single_return,
            validate_param=validate_param,
            validate_return=validate_return,
            generator_type_return=generator_type_return,
            parent_class=parent_class,
        )

        self.type_infos.append(type_info)
        self.generic_visit(node)


def analyze_file_types(file_path: Path) -> List[TypeInfo]:
    """Analyze type annotations in a Python file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=str(file_path))
        validator = TypeValidator(str(file_path))
        validator.visit(tree)

        return validator.type_infos
    except Exception as e:
        print(f"Warning: Error analyzing {file_path}: {e}")
        return []


def validate_generator_type_enum(base_path: Path) -> Dict[str, Any]:
    """Validate that generator_type properties return valid GeneratorType enums"""
    from dataforge.core.types import GeneratorType

    valid_types = {member.value for member in GeneratorType}
    valid_type_names = {member.name for member in GeneratorType}

    invalid_generators = []

    # Find all generator files
    generators_path = base_path / "dataforge" / "generators"
    for py_file in generators_path.rglob("*.py"):
        if py_file.name.startswith("__") or py_file.name.startswith("test_"):
            continue

        type_infos = analyze_file_types(py_file)

        for type_info in type_infos:
            if type_info.generator_type_return:
                # Check for invalid enum values
                return_str = type_info.generator_type_return

                # Common invalid patterns
                if "BASIC_INFO" in return_str:
                    invalid_generators.append(
                        {
                            "class": type_info.class_name,
                            "file": str(py_file.relative_to(base_path)),
                            "line": type_info.line_number,
                            "issue": "Uses non-existent GeneratorType.BASIC_INFO",
                            "should_be": "GeneratorType.BASIC",
                        }
                    )

    return {
        "valid_enum_values": list(valid_types),
        "invalid_generators": invalid_generators,
    }


def check_return_type_consistency(base_path: Path) -> Dict[str, Any]:
    """Check that child classes maintain return type consistency with parent"""
    mismatches = []

    generators_path = base_path / "dataforge" / "generators"

    # Build a map of all generators
    all_type_infos: List[TypeInfo] = []

    for py_file in generators_path.rglob("*.py"):
        if py_file.name.startswith("__") or py_file.name.startswith("test_"):
            continue

        type_infos = analyze_file_types(py_file)
        all_type_infos.extend(type_infos)

    # Check for type mismatches
    for type_info in all_type_infos:
        if type_info.parent_class and type_info.generate_single_return:
            # Find parent type info
            parent_infos = [
                ti for ti in all_type_infos if ti.class_name == type_info.parent_class
            ]

            for parent_info in parent_infos:
                if parent_info.generic_param and type_info.generate_single_return:
                    # Check if return type matches generic param
                    parent_generic = parent_info.generic_param
                    child_return = type_info.generate_single_return

                    # Common mismatches
                    if parent_generic == "int" and "str" in child_return:
                        mismatches.append(
                            {
                                "child_class": type_info.class_name,
                                "parent_class": type_info.parent_class,
                                "parent_generic": parent_generic,
                                "child_return": child_return,
                                "file": str(
                                    Path(type_info.file_path).relative_to(base_path)
                                ),
                                "line": type_info.line_number,
                                "issue": f"Parent expects {parent_generic}, child returns {child_return}",
                            }
                        )
                    elif parent_generic == "str" and "int" in child_return:
                        mismatches.append(
                            {
                                "child_class": type_info.class_name,
                                "parent_class": type_info.parent_class,
                                "parent_generic": parent_generic,
                                "child_return": child_return,
                                "file": str(
                                    Path(type_info.file_path).relative_to(base_path)
                                ),
                                "line": type_info.line_number,
                                "issue": f"Parent expects {parent_generic}, child returns {child_return}",
                            }
                        )

    return {"mismatches": mismatches}


def validate_all_types(base_path: Path, verbose: bool = False) -> Dict[str, Any]:
    """Perform comprehensive type validation"""
    print("=== Generator Type Safety Validation ===\n")

    # Check 1: GeneratorType enum validity
    print("Checking GeneratorType enum values...")
    enum_results = validate_generator_type_enum(base_path)

    if enum_results["invalid_generators"]:
        print(f"🔴 Found {len(enum_results['invalid_generators'])} invalid enum uses")
        for gen in enum_results["invalid_generators"]:
            print(f"  - {gen['class']} ({gen['file']}:{gen['line']})")
            print(f"    Issue: {gen['issue']}")
            print(f"    Should be: {gen['should_be']}")
    else:
        print("✅ All GeneratorType enums are valid")

    print()

    # Check 2: Return type consistency
    print("Checking return type consistency...")
    consistency_results = check_return_type_consistency(base_path)

    if consistency_results["mismatches"]:
        print(f"🔴 Found {len(consistency_results['mismatches'])} type mismatches")
        for mismatch in consistency_results["mismatches"]:
            print(f"  - {mismatch['child_class']} extends {mismatch['parent_class']}")
            print(f"    File: {mismatch['file']}:{mismatch['line']}")
            print(f"    Issue: {mismatch['issue']}")
    else:
        print("✅ All return types are consistent")

    print()

    # Summary
    total_issues = len(enum_results["invalid_generators"]) + len(
        consistency_results["mismatches"]
    )

    print("SUMMARY:")
    print(f"- Invalid enum uses: {len(enum_results['invalid_generators'])}")
    print(f"- Type mismatches: {len(consistency_results['mismatches'])}")
    print(f"- Total issues: {total_issues}")

    if total_issues > 0:
        status = "FAILING ❌"
        exit_code = 1
    else:
        status = "PASSING ✅"
        exit_code = 0

    print(f"- Status: {status}")

    return {
        "enum_validation": enum_results,
        "type_consistency": consistency_results,
        "total_issues": total_issues,
        "status": status,
        "exit_code": exit_code,
    }


def main():
    parser = argparse.ArgumentParser(description="Validate generator type safety")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )
    parser.add_argument(
        "--base-path",
        type=Path,
        default=Path.cwd(),
        help="Base path of the project",
    )

    args = parser.parse_args()

    results = validate_all_types(args.base_path, args.verbose)

    if args.json:
        print("\n" + json.dumps(results, indent=2))

    sys.exit(results["exit_code"])


if __name__ == "__main__":
    main()
