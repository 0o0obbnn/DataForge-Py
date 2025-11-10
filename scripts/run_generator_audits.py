#!/usr/bin/env python3
"""
DataForge Generator Audit Suite - Master Runner

This script runs all audit checks in sequence and generates a summary report.

Usage:
    python scripts/run_generator_audits.py [--json] [--verbose] [--output-dir DIR]

Exit Codes:
    0: All checks passed
    1: Critical failures found
    2: Warnings found
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class AuditResult:
    """Result from a single audit check"""

    def __init__(
        self,
        name: str,
        passed: bool,
        exit_code: int,
        details: Dict[str, Any],
        error: str = "",
    ):
        self.name = name
        self.passed = passed
        self.exit_code = exit_code
        self.details = details
        self.error = error


def run_audit_script(
    script_path: Path, json_output: bool = True, verbose: bool = False
) -> AuditResult:
    """
    Run a single audit script and capture results.

    Args:
        script_path: Path to the audit script
        json_output: Whether to capture JSON output
        verbose: Whether to enable verbose mode

    Returns:
        AuditResult with script execution results
    """
    name = script_path.stem.replace("_", " ").title()

    cmd = [sys.executable, str(script_path)]

    if json_output:
        cmd.append("--json")
    if verbose:
        cmd.append("--verbose")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )

        # Try to parse JSON output
        details = {}
        if json_output:
            try:
                # Find JSON in output (after regular output)
                lines = result.stdout.split("\n")
                json_start = -1
                for i, line in enumerate(lines):
                    if line.strip().startswith("{"):
                        json_start = i
                        break

                if json_start >= 0:
                    json_str = "\n".join(lines[json_start:])
                    details = json.loads(json_str)
            except json.JSONDecodeError as e:
                details = {"error": f"Failed to parse JSON: {e}"}

        passed = result.returncode == 0
        return AuditResult(
            name=name,
            passed=passed,
            exit_code=result.returncode,
            details=details,
            error=result.stderr if result.returncode != 0 else "",
        )

    except subprocess.TimeoutExpired:
        return AuditResult(
            name=name,
            passed=False,
            exit_code=1,
            details={},
            error="Script timed out after 5 minutes",
        )
    except Exception as e:
        return AuditResult(
            name=name,
            passed=False,
            exit_code=1,
            details={},
            error=str(e),
        )


def run_pytest_tests(
    test_path: Path, verbose: bool = False
) -> AuditResult:
    """
    Run pytest tests and capture results.

    Args:
        test_path: Path to the test file
        verbose: Whether to enable verbose mode

    Returns:
        AuditResult with test execution results
    """
    name = test_path.stem.replace("_", " ").replace("test ", "").title()

    cmd = ["pytest", str(test_path), "-v" if verbose else "-q", "--tb=short"]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )

        # Parse pytest output for pass/fail counts
        details = {"output": result.stdout}

        # Extract test counts
        if "passed" in result.stdout:
            import re

            match = re.search(r"(\d+) passed", result.stdout)
            if match:
                details["passed"] = int(match.group(1))

            match = re.search(r"(\d+) failed", result.stdout)
            if match:
                details["failed"] = int(match.group(1))

        passed = result.returncode == 0
        return AuditResult(
            name=name,
            passed=passed,
            exit_code=result.returncode,
            details=details,
            error=result.stderr if result.returncode != 0 else "",
        )

    except subprocess.TimeoutExpired:
        return AuditResult(
            name=name,
            passed=False,
            exit_code=1,
            details={},
            error="Tests timed out after 5 minutes",
        )
    except Exception as e:
        return AuditResult(
            name=name,
            passed=False,
            exit_code=1,
            details={},
            error=str(e),
        )


def generate_report(
    results: List[AuditResult], output_dir: Path, json_output: bool = False
) -> None:
    """
    Generate comprehensive audit report.

    Args:
        results: List of audit results
        output_dir: Directory to save reports
        json_output: Whether to also output JSON report
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = output_dir / f"audit_report_{timestamp}.txt"

    # Count results
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)

    # Count issues by severity
    critical_count = 0
    high_count = 0
    warning_count = 0

    for result in results:
        if result.details:
            critical_count += result.details.get("critical", 0)
            high_count += result.details.get("high", 0)
            warning_count += result.details.get("warnings", 0) + result.details.get(
                "medium", 0
            )

    # Generate text report
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("DataForge Generator Audit Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")

        f.write("SUMMARY\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total checks: {total}\n")
        f.write(f"Passed: {passed} ✅\n")
        f.write(f"Failed: {failed} ❌\n\n")

        f.write(f"Critical issues: {critical_count}\n")
        f.write(f"High priority: {high_count}\n")
        f.write(f"Warnings: {warning_count}\n\n")

        # Overall status
        if failed > 0 or critical_count > 0:
            status = "FAILING ❌"
        elif high_count > 0:
            status = "WARNING ⚠️"
        elif warning_count > 0:
            status = "ADVISORY 📋"
        else:
            status = "PASSING ✅"

        f.write(f"Overall Status: {status}\n\n")

        f.write("=" * 60 + "\n\n")

        # Detailed results
        f.write("DETAILED RESULTS\n")
        f.write("-" * 60 + "\n\n")

        for i, result in enumerate(results, 1):
            status_icon = "✅" if result.passed else "❌"
            f.write(f"[{i}/{total}] {result.name} {status_icon}\n")
            f.write(f"Exit Code: {result.exit_code}\n")

            if result.details:
                # Write key metrics
                for key in [
                    "total_generators",
                    "registered",
                    "unregistered",
                    "critical",
                    "high",
                    "medium",
                    "total_issues",
                ]:
                    if key in result.details:
                        f.write(f"  {key}: {result.details[key]}\n")

            if result.error:
                f.write(f"Error: {result.error}\n")

            f.write("\n")

        f.write("=" * 60 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 60 + "\n")

    print(f"\nDetailed report saved to: {report_file}")

    # Generate JSON report if requested
    if json_output:
        json_file = output_dir / f"audit_report_{timestamp}.json"

        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_checks": total,
                "passed": passed,
                "failed": failed,
                "critical_issues": critical_count,
                "high_issues": high_count,
                "warnings": warning_count,
                "status": status,
            },
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "exit_code": r.exit_code,
                    "details": r.details,
                    "error": r.error,
                }
                for r in results
            ],
        }

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)

        print(f"JSON report saved to: {json_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Run comprehensive generator audit suite"
    )
    parser.add_argument(
        "--json", action="store_true", help="Generate JSON reports"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("audit_results"),
        help="Directory to save reports (default: audit_results/)",
    )
    parser.add_argument(
        "--scripts-only",
        action="store_true",
        help="Run only audit scripts, skip pytest tests",
    )
    parser.add_argument(
        "--tests-only",
        action="store_true",
        help="Run only pytest tests, skip audit scripts",
    )

    args = parser.parse_args()

    base_path = Path(__file__).parent.parent
    scripts_path = base_path / "scripts"
    tests_path = base_path / "tests"

    print("=" * 60)
    print("DataForge Generator Audit Suite")
    print("=" * 60)
    print()

    results: List[AuditResult] = []

    # Audit scripts to run
    audit_scripts = [
        scripts_path / "audit_generator_registration.py",
        scripts_path / "validate_generator_types.py",
        scripts_path / "audit_security_issues.py",
        scripts_path / "scan_code_quality.py",
    ]

    # Test files to run
    test_files = [
        tests_path / "test_generator_interface_compliance.py",
        tests_path / "test_all_generators_comprehensive.py",
    ]

    total_checks = 0
    if not args.tests_only:
        total_checks += len(audit_scripts)
    if not args.scripts_only:
        total_checks += len(test_files)

    current = 0

    # Run audit scripts
    if not args.tests_only:
        print(f"Running {len(audit_scripts)} audit scripts...\n")

        for script in audit_scripts:
            current += 1
            print(f"[{current}/{total_checks}] Running {script.stem}...", end=" ")

            if not script.exists():
                print(f"❌ NOT FOUND")
                results.append(
                    AuditResult(
                        name=script.stem,
                        passed=False,
                        exit_code=1,
                        details={},
                        error="Script file not found",
                    )
                )
                continue

            result = run_audit_script(script, args.json, args.verbose)
            results.append(result)

            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(status)

            if not result.passed and result.details:
                # Print quick summary
                if "critical" in result.details:
                    print(f"  Critical: {result.details['critical']}")
                if "high" in result.details:
                    print(f"  High: {result.details['high']}")

        print()

    # Run pytest tests
    if not args.scripts_only:
        print(f"Running {len(test_files)} test suites...\n")

        for test_file in test_files:
            current += 1
            print(f"[{current}/{total_checks}] Running {test_file.stem}...", end=" ")

            if not test_file.exists():
                print(f"❌ NOT FOUND")
                results.append(
                    AuditResult(
                        name=test_file.stem,
                        passed=False,
                        exit_code=1,
                        details={},
                        error="Test file not found",
                    )
                )
                continue

            result = run_pytest_tests(test_file, args.verbose)
            results.append(result)

            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(status)

            if not result.passed and result.details:
                if "failed" in result.details:
                    print(f"  Failed tests: {result.details['failed']}")

        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed_count = sum(1 for r in results if r.passed)
    failed_count = sum(1 for r in results if not r.passed)

    # Count issues
    critical_total = sum(r.details.get("critical", 0) for r in results if r.details)
    high_total = sum(r.details.get("high", 0) for r in results if r.details)
    warning_total = sum(
        r.details.get("warnings", 0) + r.details.get("medium", 0)
        for r in results
        if r.details
    )

    print(f"Checks Passed: {passed_count}/{len(results)}")
    print(f"Checks Failed: {failed_count}/{len(results)}")
    print()
    print(f"Critical Issues: {critical_total}")
    print(f"High Issues: {high_total}")
    print(f"Warnings: {warning_total}")
    print()

    # Determine overall status
    if failed_count > 0 or critical_total > 0:
        overall_status = "FAILING ❌"
        exit_code = 1
    elif high_total > 0:
        overall_status = "WARNING ⚠️"
        exit_code = 2
    elif warning_total > 0:
        overall_status = "ADVISORY 📋"
        exit_code = 0
    else:
        overall_status = "PASSING ✅"
        exit_code = 0

    print(f"Overall Status: {overall_status}")
    print()

    # Next steps
    if exit_code != 0:
        print("Next Steps:")
        print("1. Review detailed reports in audit_results/")
        print("2. Fix critical issues first")
        print("3. Re-run audits to track progress")
        print()
        print("Run with --verbose for detailed output")

    # Generate report
    generate_report(results, args.output_dir, args.json)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
