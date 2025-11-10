#!/usr/bin/env python3
"""
Security Audit Script for Generators

This script audits security concerns in generator implementations:
- Auth generators using weak RNG (random vs secrets)
- Security payload generators missing safety warnings
- Hardcoded secrets or tokens
- Insecure defaults in auth-related generators

Usage:
    python scripts/audit_security_issues.py [--json] [--verbose]

Exit Codes:
    0: No security issues found
    1: Critical security issues found
    2: Warnings found
"""

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


class SecurityIssue:
    """Represents a security issue found in code"""

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


def check_rng_security(file_path: Path) -> List[SecurityIssue]:
    """
    Check if auth generators use secure random number generation.

    Critical: Auth generators must use secrets module, not random module.
    """
    issues = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split("\n")

        # Check if this is an auth generator
        is_auth_generator = (
            "generators/auth/" in str(file_path)
            or "password" in file_path.name.lower()
            or "token" in file_path.name.lower()
        )

        if not is_auth_generator:
            return issues

        # Check imports
        has_random_import = False
        has_secrets_import = False
        random_import_line = 0
        secrets_import_line = 0

        for i, line in enumerate(lines, 1):
            if re.search(r"^import random\b", line.strip()) or re.search(
                r"^from random import", line.strip()
            ):
                has_random_import = True
                random_import_line = i

            if re.search(r"^import secrets\b", line.strip()) or re.search(
                r"^from secrets import", line.strip()
            ):
                has_secrets_import = True
                secrets_import_line = i

        # Critical: Auth generator using random instead of secrets
        if has_random_import and not has_secrets_import:
            issues.append(
                SecurityIssue(
                    severity="critical",
                    category="weak_rng",
                    file_path=str(file_path),
                    line_number=random_import_line,
                    description=f"Auth generator uses weak 'random' module instead of cryptographically secure 'secrets' module",
                    recommendation="Replace 'import random' with 'import secrets' and use secrets.choice(), secrets.randbelow(), etc.",
                )
            )

        # Medium: Uses random even with secrets (might be using wrong one)
        if has_random_import and has_secrets_import:
            # Check if random is actually used
            for i, line in enumerate(lines, 1):
                if re.search(r"\brandom\.(choice|randint|shuffle)\b", line):
                    issues.append(
                        SecurityIssue(
                            severity="medium",
                            category="weak_rng",
                            file_path=str(file_path),
                            line_number=i,
                            description="Auth generator imports secrets but still uses random module functions",
                            recommendation="Use secrets module functions instead: secrets.choice(), secrets.randbelow()",
                        )
                    )
                    break

    except Exception as e:
        print(f"Warning: Could not analyze {file_path}: {e}")

    return issues


def check_payload_generator_warnings(file_path: Path) -> List[SecurityIssue]:
    """
    Check if security payload generators have appropriate safety warnings.

    Generators that create malicious payloads for testing should warn users.
    """
    issues = []

    # Payload generator files
    payload_indicators = [
        "sql_injection",
        "xss_payload",
        "xss",
        "injection",
        "exploit",
    ]

    if not any(indicator in file_path.name.lower() for indicator in payload_indicators):
        return issues

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for warning indicators
        warning_indicators = [
            "WARNING",
            "CAUTION",
            "DANGER",
            "DO NOT USE IN PRODUCTION",
            "TESTING ONLY",
            "security testing",
            "educational purposes",
        ]

        has_warning = any(
            indicator.lower() in content.lower() for indicator in warning_indicators
        )

        if not has_warning:
            issues.append(
                SecurityIssue(
                    severity="high",
                    category="missing_safety_warning",
                    file_path=str(file_path),
                    line_number=1,
                    description="Security payload generator missing safety warnings",
                    recommendation='Add prominent warning in docstring: "WARNING: This generator creates malicious payloads for security testing only. DO NOT use in production."',
                )
            )

    except Exception as e:
        print(f"Warning: Could not analyze {file_path}: {e}")

    return issues


def check_hardcoded_secrets(file_path: Path) -> List[SecurityIssue]:
    """
    Check for hardcoded secrets, tokens, or passwords in code.
    """
    issues = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Patterns that might indicate hardcoded secrets
        secret_patterns = [
            (r'password\s*=\s*["\'](?!.*(example|test|demo|xxx|password|123))[\w\d]+["\']', "hardcoded password"),
            (r'api_key\s*=\s*["\'][^"\']{20,}["\']', "hardcoded API key"),
            (r'secret\s*=\s*["\'][^"\']{20,}["\']', "hardcoded secret"),
            (r'token\s*=\s*["\'][^"\']{20,}["\']', "hardcoded token"),
            (r'Bearer\s+[A-Za-z0-9\-._~+/]+=*', "hardcoded bearer token"),
        ]

        for i, line in enumerate(lines, 1):
            for pattern, description in secret_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Skip if it's a comment or example
                    if line.strip().startswith("#") or "example" in line.lower():
                        continue

                    issues.append(
                        SecurityIssue(
                            severity="critical",
                            category="hardcoded_secret",
                            file_path=str(file_path),
                            line_number=i,
                            description=f"Possible {description} detected",
                            recommendation="Remove hardcoded secrets. Use environment variables or configuration files.",
                        )
                    )

    except Exception as e:
        print(f"Warning: Could not analyze {file_path}: {e}")

    return issues


def audit_security(base_path: Path, verbose: bool = False) -> Dict[str, Any]:
    """Perform comprehensive security audit"""
    print("=== Generator Security Audit ===\n")

    all_issues: List[SecurityIssue] = []

    # Find all generator files
    generators_path = base_path / "dataforge" / "generators"

    if not generators_path.exists():
        print(f"Error: Generators path not found: {generators_path}")
        return {
            "total_issues": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "status": "ERROR",
            "exit_code": 1,
        }

    generator_files = list(generators_path.rglob("*.py"))
    generator_files = [
        f for f in generator_files if not f.name.startswith("__") and not f.name.startswith("test_")
    ]

    print(f"Scanning {len(generator_files)} generator files...\n")

    # Run all checks
    for file_path in generator_files:
        all_issues.extend(check_rng_security(file_path))
        all_issues.extend(check_payload_generator_warnings(file_path))
        all_issues.extend(check_hardcoded_secrets(file_path))

    # Categorize by severity
    critical_issues = [i for i in all_issues if i.severity == "critical"]
    high_issues = [i for i in all_issues if i.severity == "high"]
    medium_issues = [i for i in all_issues if i.severity == "medium"]
    low_issues = [i for i in all_issues if i.severity == "low"]

    # Print results
    if critical_issues:
        print(f"🔴 CRITICAL SECURITY ISSUES ({len(critical_issues)}):")
        for issue in critical_issues:
            rel_path = Path(issue.file_path).relative_to(base_path)
            print(f"\n- {issue.category.upper()}: {issue.description}")
            print(f"  File: {rel_path}:{issue.line_number}")
            print(f"  Fix: {issue.recommendation}")
        print()

    if high_issues:
        print(f"🟠 HIGH PRIORITY ISSUES ({len(high_issues)}):")
        for issue in high_issues:
            rel_path = Path(issue.file_path).relative_to(base_path)
            print(f"\n- {issue.category.upper()}: {issue.description}")
            print(f"  File: {rel_path}:{issue.line_number}")
            print(f"  Fix: {issue.recommendation}")
        print()

    if medium_issues and verbose:
        print(f"⚠️  MEDIUM PRIORITY ISSUES ({len(medium_issues)}):")
        for issue in medium_issues:
            rel_path = Path(issue.file_path).relative_to(base_path)
            print(f"\n- {issue.category.upper()}: {issue.description}")
            print(f"  File: {rel_path}:{issue.line_number}")
        print()

    if not all_issues:
        print("✅ No security issues found")

    # Summary
    print("\nSUMMARY:")
    print(f"- Critical issues: {len(critical_issues)}")
    print(f"- High priority: {len(high_issues)}")
    print(f"- Medium priority: {len(medium_issues)}")
    print(f"- Total issues: {len(all_issues)}")

    # Determine exit code
    if critical_issues:
        status = "CRITICAL ❌"
        exit_code = 1
    elif high_issues:
        status = "WARNING ⚠️"
        exit_code = 2
    elif medium_issues:
        status = "ADVISORY 📋"
        exit_code = 0
    else:
        status = "SECURE ✅"
        exit_code = 0

    print(f"- Status: {status}")

    return {
        "total_issues": len(all_issues),
        "critical": len(critical_issues),
        "high": len(high_issues),
        "medium": len(medium_issues),
        "low": len(low_issues),
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
    parser = argparse.ArgumentParser(description="Audit generator security issues")
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

    results = audit_security(args.base_path, args.verbose)

    if args.json:
        print("\n" + json.dumps(results, indent=2))

    sys.exit(results["exit_code"])


if __name__ == "__main__":
    main()
