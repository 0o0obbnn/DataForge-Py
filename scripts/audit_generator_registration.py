#!/usr/bin/env python3
"""
Generator Registration Audit Script

This script audits all generator classes in the dataforge/generators/ directory
to verify they are properly registered with the @register_generator decorator.

Usage:
    python scripts/audit_generator_registration.py [--json] [--verbose]

Exit Codes:
    0: All generators properly registered
    1: Unregistered generators found (critical failures)
    2: Warnings found (duplicates, etc.)
"""

import argparse
import ast
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class GeneratorInfo:
    """Information about a generator class"""

    def __init__(
        self,
        name: str,
        file_path: str,
        line_number: int,
        has_decorator: bool = False,
        registered_name: Optional[str] = None,
        aliases: Optional[List[str]] = None,
        inherits_from: Optional[str] = None,
    ):
        self.name = name
        self.file_path = file_path
        self.line_number = line_number
        self.has_decorator = has_decorator
        self.registered_name = registered_name
        self.aliases = aliases or []
        self.inherits_from = inherits_from


class GeneratorVisitor(ast.NodeVisitor):
    """AST visitor to find generator classes and their decorators"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.generators: List[GeneratorInfo] = []
        self.current_decorators: List[ast.expr] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        # Check if class inherits from DataGenerator
        inherits_from_generator = False
        parent_name = None

        for base in node.bases:
            if isinstance(base, ast.Name):
                if "Generator" in base.id and base.id != "GeneratorConfig":
                    inherits_from_generator = True
                    parent_name = base.id
            elif isinstance(base, ast.Subscript):
                if isinstance(base.value, ast.Name):
                    if "Generator" in base.value.id:
                        inherits_from_generator = True
                        parent_name = base.value.id

        if not inherits_from_generator:
            self.generic_visit(node)
            return

        # Check for @register_generator decorator
        has_decorator = False
        registered_name = None
        aliases = []

        for decorator in node.decorator_list:
            decorator_name = None

            if isinstance(decorator, ast.Name):
                decorator_name = decorator.id
            elif isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Name):
                    decorator_name = decorator.func.id
                    # Extract decorator arguments
                    if decorator_name == "register_generator" and decorator.args:
                        # First argument is the name
                        if isinstance(decorator.args[0], ast.Constant):
                            registered_name = decorator.args[0].value
                        # Second argument may be aliases
                        if len(decorator.args) > 1:
                            if isinstance(decorator.args[1], ast.List):
                                aliases = [
                                    elt.value
                                    for elt in decorator.args[1].elts
                                    if isinstance(elt, ast.Constant)
                                ]

            if decorator_name == "register_generator":
                has_decorator = True

        gen_info = GeneratorInfo(
            name=node.name,
            file_path=self.file_path,
            line_number=node.lineno,
            has_decorator=has_decorator,
            registered_name=registered_name,
            aliases=aliases,
            inherits_from=parent_name,
        )

        self.generators.append(gen_info)
        self.generic_visit(node)


def find_generator_files(base_path: Path) -> List[Path]:
    """Find all Python files in the generators directory"""
    generators_path = base_path / "dataforge" / "generators"
    if not generators_path.exists():
        print(f"Error: Generators path not found: {generators_path}")
        sys.exit(1)

    python_files = []
    for file_path in generators_path.rglob("*.py"):
        # Skip __init__.py and test files
        if file_path.name == "__init__.py":
            continue
        if file_path.name.startswith("test_"):
            continue
        python_files.append(file_path)

    return sorted(python_files)


def analyze_generator_file(file_path: Path) -> List[GeneratorInfo]:
    """Analyze a single generator file for classes"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=str(file_path))
        visitor = GeneratorVisitor(str(file_path))
        visitor.visit(tree)

        return visitor.generators
    except SyntaxError as e:
        print(f"Warning: Syntax error in {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Warning: Error analyzing {file_path}: {e}")
        return []


def check_runtime_registration(base_path: Path) -> Set[str]:
    """Check actual runtime registration by importing the factory"""
    try:
        # Add project root to path
        sys.path.insert(0, str(base_path))

        from dataforge.core.factory import default_registry

        registered_names = set(default_registry.list_generators())

        # Also check aliases
        if hasattr(default_registry, "_aliases"):
            registered_names.update(default_registry._aliases.keys())

        return registered_names
    except Exception as e:
        print(f"Warning: Could not check runtime registration: {e}")
        return set()


def audit_generators(base_path: Path, verbose: bool = False) -> Dict[str, Any]:
    """Perform comprehensive audit of generator registration"""
    print("=== Generator Registration Audit ===\n")

    # Find all generator files
    generator_files = find_generator_files(base_path)
    if verbose:
        print(f"Found {len(generator_files)} generator files\n")

    # Analyze all files
    all_generators: List[GeneratorInfo] = []
    for file_path in generator_files:
        generators = analyze_generator_file(file_path)
        all_generators.extend(generators)

    # Check runtime registration
    runtime_registered = check_runtime_registration(base_path)

    # Categorize generators
    registered_generators: List[GeneratorInfo] = []
    unregistered_generators: List[GeneratorInfo] = []
    duplicate_registrations: Dict[str, List[GeneratorInfo]] = defaultdict(list)

    for gen in all_generators:
        if gen.has_decorator:
            registered_generators.append(gen)

            # Track duplicates by registered name
            if gen.registered_name:
                duplicate_registrations[gen.registered_name].append(gen)

            # Track duplicates by aliases
            for alias in gen.aliases:
                duplicate_registrations[alias].append(gen)
        else:
            unregistered_generators.append(gen)

    # Filter to only actual duplicates
    duplicate_registrations = {
        name: gens for name, gens in duplicate_registrations.items() if len(gens) > 1
    }

    # Print results
    total = len(all_generators)
    registered_count = len(registered_generators)
    unregistered_count = len(unregistered_generators)

    print(f"Total generator classes found: {total}")
    print(f"Registered: {registered_count}")
    print(f"Unregistered: {unregistered_count}")
    print(f"Runtime registered names: {len(runtime_registered)}\n")

    # Critical: Unregistered generators
    if unregistered_generators:
        print(f"🔴 UNREGISTERED GENERATORS ({len(unregistered_generators)}):")
        for i, gen in enumerate(unregistered_generators, 1):
            rel_path = Path(gen.file_path).relative_to(base_path)
            print(f"{i}. {gen.name} ({rel_path}:{gen.line_number})")
            if verbose and gen.inherits_from:
                print(f"   Inherits from: {gen.inherits_from}")
        print()

    # Warnings: Duplicate registrations
    if duplicate_registrations:
        print(f"⚠️  DUPLICATE REGISTRATIONS ({len(duplicate_registrations)}):")
        for name, gens in duplicate_registrations.items():
            print(f"- '{name}' registered by {len(gens)} generators:")
            for gen in gens:
                rel_path = Path(gen.file_path).relative_to(base_path)
                print(f"  - {gen.name} ({rel_path}:{gen.line_number})")
        print()

    # Success: Well-formed registrations
    if registered_generators and verbose:
        print(f"✅ WELL-FORMED REGISTRATIONS ({len(registered_generators)}):")
        for gen in registered_generators[:10]:  # Show first 10
            rel_path = Path(gen.file_path).relative_to(base_path)
            aliases_str = f" [aliases: {', '.join(gen.aliases)}]" if gen.aliases else ""
            print(f"- {gen.name} as '{gen.registered_name}'{aliases_str}")
        if len(registered_generators) > 10:
            print(f"  ... and {len(registered_generators) - 10} more")
        print()

    # Summary
    print("SUMMARY:")
    print(f"- Critical: {len(unregistered_generators)} unregistered generators")
    print(f"- Warnings: {len(duplicate_registrations)} duplicate registrations")

    # Determine status
    if unregistered_count > 0:
        status = "FAILING ❌"
        exit_code = 1
    elif duplicate_registrations:
        status = "WARNING ⚠️"
        exit_code = 2
    else:
        status = "PASSING ✅"
        exit_code = 0

    print(f"- Status: {status}")

    return {
        "total_generators": total,
        "registered": registered_count,
        "unregistered": unregistered_count,
        "runtime_registered": len(runtime_registered),
        "duplicates": len(duplicate_registrations),
        "status": status,
        "exit_code": exit_code,
        "unregistered_generators": [
            {
                "name": g.name,
                "file": str(Path(g.file_path).relative_to(base_path)),
                "line": g.line_number,
                "inherits_from": g.inherits_from,
            }
            for g in unregistered_generators
        ],
        "duplicate_registrations": {
            name: [
                {
                    "class": g.name,
                    "file": str(Path(g.file_path).relative_to(base_path)),
                    "line": g.line_number,
                }
                for g in gens
            ]
            for name, gens in duplicate_registrations.items()
        },
        "registered_generators": [
            {
                "name": g.name,
                "registered_as": g.registered_name,
                "aliases": g.aliases,
                "file": str(Path(g.file_path).relative_to(base_path)),
            }
            for g in registered_generators
        ],
    }


def main():
    parser = argparse.ArgumentParser(
        description="Audit generator registration status"
    )
    parser.add_argument(
        "--json", action="store_true", help="Output results as JSON"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )
    parser.add_argument(
        "--base-path",
        type=Path,
        default=Path.cwd(),
        help="Base path of the project (default: current directory)",
    )

    args = parser.parse_args()

    # Run audit
    results = audit_generators(args.base_path, args.verbose)

    # Output
    if args.json:
        print("\n" + json.dumps(results, indent=2))

    sys.exit(results["exit_code"])


if __name__ == "__main__":
    main()
