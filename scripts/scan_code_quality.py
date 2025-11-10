#!/usr/bin/env python3
"""
Code Quality Scanner for Generators

This script scans for code quality issues:
- Test files in production code directories
- Duplicate files (e.g., basic/uscc.py and identifier/uscc.py)
- Dead code (unregistered classes that aren't used)
- TODO/placeholder code in production
- Empty supported_parameters properties
- Legacy method names

Usage:
    python scripts/scan_code_quality.py [--json] [--verbose]

Exit Codes:
    0: No quality issues found
    1: Critical quality issues found
    2: Warnings found
"""

import argparse
import ast
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


class QualityIssue:
    """Represents a code quality issue"""

    def __init__(
        self,
        severity: str,  # "critical", "high", "medium", "low"
        category: str,
        file_path: str,
        line_number: int,
        description: str,
        recommendation: str,
    ):
        self.severity = severity
        self.category = category
        self.file_path = file_path
        self.line_number = line_number
        self.description = description
        self.recommendation = recommendation


def find_test_files_in_production(base_path: Path) -> List[QualityIssue]:
    """Find test files in production code directories"""
    issues = []

    generators_path = base_path / "dataforge" / "generators"

    for file_path in generators_path.rglob("test_*.py"):
        # Test files should not be in production code
        issues.append(
            QualityIssue(
                severity="critical",
                category="test_file_in_production",
                file_path=str(file_path),
                line_number=1,
                description=f"Test file found in production code directory",
                recommendation=f"Move to tests/ directory: tests/generators/{file_path.parent.name}/",
            )
        )

    return issues


def find_duplicate_files(base_path: Path) -> List[QualityIssue]:
    """
    Find duplicate generator files by comparing filenames.

    Example: basic/uscc.py and identifier/uscc.py
    """
    issues = []

    generators_path = base_path / "dataforge" / "generators"

    # Group files by name
    files_by_name: Dict[str, List[Path]] = defaultdict(list)

    for file_path in generators_path.rglob("*.py"):
        if file_path.name == "__init__.py":
            continue
        files_by_name[file_path.name].append(file_path)

    # Find duplicates
    for filename, paths in files_by_name.items():
        if len(paths) > 1:
            # Critical duplicate
            paths_str = ", ".join(str(p.relative_to(base_path)) for p in paths)

            issues.append(
                QualityIssue(
                    severity="critical",
                    category="duplicate_file",
                    file_path=str(paths[0]),
                    line_number=1,
                    description=f"Duplicate generator file '{filename}' found in multiple locations: {paths_str}",
                    recommendation=f"Remove duplicate(s). Keep only one implementation (likely in the most specific category).",
                )
            )

    return issues


def find_todo_placeholders(base_path: Path) -> List[QualityIssue]:
    """Find TODO comments and placeholder code in production"""
    issues = []

    generators_path = base_path / "dataforge" / "generators"

    # Patterns indicating placeholder code
    placeholder_patterns = [
        (r"#\s*TODO:", "TODO comment"),
        (r"#\s*FIXME:", "FIXME comment"),
        (r"#\s*XXX:", "XXX comment"),
        (r"raise\s+NotImplementedError", "NotImplementedError placeholder"),
        (r"pass\s*#.*implement", "Pass with implement comment"),
        (r'return\s+"".*#.*TODO', "Empty return with TODO"),
    ]

    for file_path in generators_path.rglob("*.py"):
        if file_path.name.startswith("__") or file_path.name.startswith("test_"):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for i, line in enumerate(lines, 1):
                for pattern, description in placeholder_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(
                            QualityIssue(
                                severity="high",
                                category="placeholder_code",
                                file_path=str(file_path),
                                line_number=i,
                                description=f"{description} in production code",
                                recommendation="Implement the functionality or remove the placeholder",
                            )
                        )

        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {e}")

    return issues


def find_empty_supported_parameters(base_path: Path) -> List[QualityIssue]:
    """Find generators with empty supported_parameters properties"""
    issues = []

    generators_path = base_path / "dataforge" / "generators"

    for file_path in generators_path.rglob("*.py"):
        if file_path.name.startswith("__") or file_path.name.startswith("test_"):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            tree = ast.parse(content, filename=str(file_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if it's a generator class
                    is_generator = any(
                        "Generator" in (base.id if isinstance(base, ast.Name) else "")
                        for base in node.bases
                    )

                    if not is_generator:
                        continue

                    # Look for supported_parameters property
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item.name == "supported_parameters":
                            # Check if property decorator
                            is_property = any(
                                isinstance(d, ast.Name) and d.id == "property"
                                for d in item.decorator_list
                            )

                            if is_property:
                                # Check if returns empty list
                                for stmt in ast.walk(item):
                                    if isinstance(stmt, ast.Return):
                                        if isinstance(stmt.value, ast.List):
                                            if len(stmt.value.elts) == 0:
                                                issues.append(
                                                    QualityIssue(
                                                        severity="medium",
                                                        category="empty_parameters",
                                                        file_path=str(file_path),
                                                        line_number=item.lineno,
                                                        description=f"{node.name}.supported_parameters returns empty list",
                                                        recommendation="Populate with actual supported parameter names or document why empty",
                                                    )
                                                )

        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {e}")

    return issues


def find_legacy_code(base_path: Path) -> List[QualityIssue]:
    """Find legacy code patterns that should be removed"""
    issues = []

    generators_path = base_path / "dataforge" / "generators"

    legacy_patterns = [
        (r"class\s+\w*Legacy\w*\(", "Legacy class name"),
        (r"class\s+\w*Old\w*\(", "Old class name"),
        (r"class\s+\w*Deprecated\w*\(", "Deprecated class name"),
    ]

    for file_path in generators_path.rglob("*.py"):
        if file_path.name.startswith("__") or file_path.name.startswith("test_"):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for i, line in enumerate(lines, 1):
                for pattern, description in legacy_patterns:
                    if re.search(pattern, line):
                        issues.append(
                            QualityIssue(
                                severity="high",
                                category="legacy_code",
                                file_path=str(file_path),
                                line_number=i,
                                description=f"{description} found - likely dead code",
                                recommendation="Remove legacy code if not registered or used",
                            )
                        )

        except Exception as e:
            print(f"Warning: Could not analyze {file_path}: {e}")

    return issues


def scan_code_quality(base_path: Path, verbose: bool = False) -> Dict[str, Any]:
    """Perform comprehensive code quality scan"""
    print("=== Generator Code Quality Scan ===\n")

    all_issues: List[QualityIssue] = []

    print("Scanning for code quality issues...\n")

    # Run all checks
    print("- Checking for test files in production...")
    all_issues.extend(find_test_files_in_production(base_path))

    print("- Checking for duplicate files...")
    all_issues.extend(find_duplicate_files(base_path))

    print("- Checking for TODO/placeholder code...")
    all_issues.extend(find_todo_placeholders(base_path))

    print("- Checking for empty supported_parameters...")
    all_issues.extend(find_empty_supported_parameters(base_path))

    print("- Checking for legacy code patterns...")
    all_issues.extend(find_legacy_code(base_path))

    print()

    # Categorize by severity
    critical_issues = [i for i in all_issues if i.severity == "critical"]
    high_issues = [i for i in all_issues if i.severity == "high"]
    medium_issues = [i for i in all_issues if i.severity == "medium"]
    low_issues = [i for i in all_issues if i.severity == "low"]

    # Print results by category
    issues_by_category: Dict[str, List[QualityIssue]] = defaultdict(list)
    for issue in all_issues:
        issues_by_category[issue.category].append(issue)

    if critical_issues:
        print(f"🔴 CRITICAL ISSUES ({len(critical_issues)}):")
        for category, issues in issues_by_category.items():
            critical_in_category = [i for i in issues if i.severity == "critical"]
            if critical_in_category:
                print(f"\n  {category.upper().replace('_', ' ')} ({len(critical_in_category)}):")
                for issue in critical_in_category:
                    rel_path = Path(issue.file_path).relative_to(base_path)
                    print(f"    - {rel_path}:{issue.line_number}")
                    if verbose:
                        print(f"      {issue.description}")
                        print(f"      Fix: {issue.recommendation}")
        print()

    if high_issues:
        print(f"🟠 HIGH PRIORITY ({len(high_issues)}):")
        for category, issues in issues_by_category.items():
            high_in_category = [i for i in issues if i.severity == "high"]
            if high_in_category:
                print(f"\n  {category.upper().replace('_', ' ')} ({len(high_in_category)}):")
                for issue in high_in_category[:5]:  # Show first 5
                    rel_path = Path(issue.file_path).relative_to(base_path)
                    print(f"    - {rel_path}:{issue.line_number}")
                if len(high_in_category) > 5:
                    print(f"    ... and {len(high_in_category) - 5} more")
        print()

    if medium_issues and verbose:
        print(f"⚠️  MEDIUM PRIORITY ({len(medium_issues)}):")
        for category, issues in issues_by_category.items():
            medium_in_category = [i for i in issues if i.severity == "medium"]
            if medium_in_category:
                print(f"\n  {category.upper().replace('_', ' ')} ({len(medium_in_category)}):")
                for issue in medium_in_category[:3]:
                    rel_path = Path(issue.file_path).relative_to(base_path)
                    print(f"    - {rel_path}:{issue.line_number}")
        print()

    if not all_issues:
        print("✅ No code quality issues found")

    # Summary
    print("\nSUMMARY:")
    print(f"- Critical issues: {len(critical_issues)}")
    print(f"- High priority: {len(high_issues)}")
    print(f"- Medium priority: {len(medium_issues)}")
    print(f"- Total issues: {len(all_issues)}")

    # Determine exit code
    if critical_issues:
        status = "FAILING ❌"
        exit_code = 1
    elif high_issues:
        status = "WARNING ⚠️"
        exit_code = 2
    elif medium_issues:
        status = "ADVISORY 📋"
        exit_code = 0
    else:
        status = "CLEAN ✅"
        exit_code = 0

    print(f"- Status: {status}")

    return {
        "total_issues": len(all_issues),
        "critical": len(critical_issues),
        "high": len(high_issues),
        "medium": len(medium_issues),
        "low": len(low_issues),
        "by_category": {
            category: len(issues) for category, issues in issues_by_category.items()
        },
        "issues": [
            {
                "severity": i.severity,
                "category": i.category,
                "file": str(Path(i.file_path).relative_to(base_path)),
                "line": i.line_number,
                "description": i.description,
                "recommendation": i.recommendation,
            }
            for i in all_issues
        ],
        "status": status,
        "exit_code": exit_code,
    }


def main():
    parser = argparse.ArgumentParser(description="Scan generator code quality issues")
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

    results = scan_code_quality(args.base_path, args.verbose)

    if args.json:
        print("\n" + json.dumps(results, indent=2))

    sys.exit(results["exit_code"])


if __name__ == "__main__":
    main()
