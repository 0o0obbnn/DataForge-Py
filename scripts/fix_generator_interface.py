#!/usr/bin/env python3
"""
Interface Compliance Fixer

Fixes legacy DataForge generators to comply with the DataGenerator[T] abstract interface.

Legacy Pattern (doesn't work):
    def generate(self, context=None) -> T:
        return value

Required Interface:
    def generate_single(self, context: Optional[GenerationContext] = None) -> T:
        return value

    @property
    def generator_type(self) -> GeneratorType:
        return GeneratorType.BASIC

    @property
    def supported_parameters(self) -> list[str]:
        return ["param1", "param2"]

    def validate(self, data: T) -> bool:
        return isinstance(data, expected_type)

Usage:
    python scripts/fix_generator_interface.py --scan          # Scan for non-compliant generators
    python scripts/fix_generator_interface.py --analyze FILE  # Analyze specific file
    python scripts/fix_generator_interface.py --fix FILE      # Fix specific file
    python scripts/fix_generator_interface.py --fix-all       # Fix all non-compliant generators
"""

import ast
import re
from pathlib import Path
from typing import Optional, List, Set, Dict
from dataclasses import dataclass


@dataclass
class InterfaceIssue:
    """Describes an interface compliance issue"""
    generator_class: str
    file_path: Path
    missing_generate_single: bool = False
    has_legacy_generate: bool = False
    missing_generator_type: bool = False
    missing_supported_parameters: bool = False
    missing_validate: bool = False
    uses_random_module: bool = False
    return_type: Optional[str] = None
    has_validator_class: bool = False
    parameter_names: List[str] = None

    def __post_init__(self):
        if self.parameter_names is None:
            self.parameter_names = []

    @property
    def is_compliant(self) -> bool:
        """Check if generator is fully compliant"""
        return not (
            self.missing_generate_single or
            self.missing_generator_type or
            self.missing_supported_parameters or
            self.missing_validate
        )

    @property
    def severity(self) -> str:
        """Get issue severity"""
        if self.missing_generate_single:
            return "CRITICAL"
        elif self.missing_generator_type or self.missing_validate:
            return "HIGH"
        elif self.missing_supported_parameters:
            return "MEDIUM"
        else:
            return "LOW"


class InterfaceAnalyzer:
    """Analyzes generator classes for interface compliance"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.generators_dir = project_root / "dataforge" / "generators"
        self.issues: List[InterfaceIssue] = []

    def scan_all_generators(self) -> List[InterfaceIssue]:
        """Scan all generator files for interface issues"""
        print("🔍 Scanning for interface compliance issues...")

        for py_file in self.generators_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            self._analyze_file(py_file)

        print(f"✅ Analyzed {len(self.issues)} generator classes")
        return self.issues

    def _analyze_file(self, file_path: Path) -> None:
        """Analyze a single Python file for interface issues"""
        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(file_path))

            # Check if uses random module
            uses_random = "import random" in content or "from random import" in content

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if it inherits from DataGenerator
                    if self._inherits_from_datagenerator(node):
                        issue = self._analyze_class(node, file_path, content, uses_random)
                        if issue and not issue.is_compliant:
                            self.issues.append(issue)

        except Exception as e:
            print(f"⚠️  Error analyzing {file_path}: {e}")

    def _inherits_from_datagenerator(self, node: ast.ClassDef) -> bool:
        """Check if class inherits from DataGenerator"""
        for base in node.bases:
            base_name = self._get_name(base)
            if "DataGenerator" in base_name or "ContextAwareGenerator" in base_name:
                return True
        return False

    def _get_name(self, node: ast.expr) -> str:
        """Extract name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Subscript):
            if isinstance(node.value, ast.Name):
                return node.value.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return ""

    def _analyze_class(self, node: ast.ClassDef, file_path: Path, content: str, uses_random: bool) -> Optional[InterfaceIssue]:
        """Analyze a class for interface compliance"""

        # Extract method names
        methods = {m.name for m in node.body if isinstance(m, ast.FunctionDef)}
        properties = {m.name for m in node.body
                     if isinstance(m, ast.FunctionDef) and
                     any(isinstance(d, ast.Name) and d.id == 'property' for d in m.decorator_list)}

        # Check for interface compliance
        has_generate_single = "generate_single" in methods
        has_legacy_generate = "generate" in methods and "generate_single" not in methods
        has_generator_type = "generator_type" in properties
        has_supported_parameters = "supported_parameters" in properties
        has_validate = "validate" in methods

        # Extract return type from generate or generate_single
        return_type = self._extract_return_type(node, content)

        # Check for validator class in same file
        has_validator_class = self._has_validator_class(content, node.name)

        # Extract parameter names from _setup or __init__
        parameter_names = self._extract_parameter_names(node, content)

        issue = InterfaceIssue(
            generator_class=node.name,
            file_path=file_path,
            missing_generate_single=not has_generate_single,
            has_legacy_generate=has_legacy_generate,
            missing_generator_type=not has_generator_type,
            missing_supported_parameters=not has_supported_parameters,
            missing_validate=not has_validate,
            uses_random_module=uses_random,
            return_type=return_type,
            has_validator_class=has_validator_class,
            parameter_names=parameter_names
        )

        return issue

    def _extract_return_type(self, node: ast.ClassDef, content: str) -> Optional[str]:
        """Extract return type from generate or generate_single method"""
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name in ["generate", "generate_single"]:
                if item.returns:
                    return ast.unparse(item.returns)

        # Try to extract from class definition DataGenerator[Type]
        for base in node.bases:
            if isinstance(base, ast.Subscript):
                base_name = self._get_name(base.value)
                if "DataGenerator" in base_name:
                    return ast.unparse(base.slice)

        return None

    def _has_validator_class(self, content: str, generator_class: str) -> bool:
        """Check if file contains a validator class for this generator"""
        validator_name = generator_class.replace("Generator", "Validator")
        return f"class {validator_name}" in content

    def _extract_parameter_names(self, node: ast.ClassDef, content: str) -> List[str]:
        """Extract parameter names from _setup or __init__ methods"""
        params = set()

        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name in ["_setup", "__init__"]:
                # Find all self.parameters.get() calls
                for child in ast.walk(item):
                    if isinstance(child, ast.Call):
                        # Check for self.parameters.get("param_name")
                        if (isinstance(child.func, ast.Attribute) and
                            child.func.attr == "get" and
                            len(child.args) > 0 and
                            isinstance(child.args[0], ast.Constant)):
                            param_name = child.args[0].value
                            params.add(param_name)

        return sorted(list(params))

    def print_summary(self) -> None:
        """Print compliance summary"""
        total = len(self.issues)
        critical = sum(1 for i in self.issues if i.severity == "CRITICAL")
        high = sum(1 for i in self.issues if i.severity == "HIGH")
        medium = sum(1 for i in self.issues if i.severity == "MEDIUM")

        print(f"\n📊 Interface Compliance Summary:")
        print(f"   Total non-compliant: {total}")
        print(f"   🔴 Critical: {critical} (missing generate_single)")
        print(f"   🟠 High: {high} (missing generator_type or validate)")
        print(f"   🟡 Medium: {medium} (missing supported_parameters)")

        # Group by category
        by_category: Dict[str, int] = {}
        for issue in self.issues:
            relative_path = issue.file_path.relative_to(self.generators_dir)
            category = relative_path.parts[0] if relative_path.parts else "unknown"
            by_category[category] = by_category.get(category, 0) + 1

        print("\n📁 By Category:")
        for category, count in sorted(by_category.items()):
            print(f"   {category}: {count} non-compliant")

        # Show which issues are most common
        missing_generate_single = sum(1 for i in self.issues if i.missing_generate_single)
        missing_generator_type = sum(1 for i in self.issues if i.missing_generator_type)
        missing_validate = sum(1 for i in self.issues if i.missing_validate)
        missing_supported_parameters = sum(1 for i in self.issues if i.missing_supported_parameters)
        uses_random = sum(1 for i in self.issues if i.uses_random_module)

        print("\n🔧 Issue Breakdown:")
        print(f"   Missing generate_single: {missing_generate_single}")
        print(f"   Missing generator_type: {missing_generator_type}")
        print(f"   Missing validate: {missing_validate}")
        print(f"   Missing supported_parameters: {missing_supported_parameters}")
        print(f"   Uses unsafe random module: {uses_random}")


class InterfaceFixer:
    """Fixes interface compliance issues in generator classes"""

    # Category to GeneratorType mapping
    CATEGORY_TO_TYPE = {
        "basic": "BASIC",
        "contact": "CONTACT",
        "identifier": "IDENTIFIER",
        "auth": "AUTH",
        "network": "NETWORK",
        "finance": "FINANCE",
        "numeric": "NUMERIC",
        "text": "TEXT",
        "advanced": "ADVANCED",
    }

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.generators_dir = project_root / "dataforge" / "generators"

    def fix_generator(self, issue: InterfaceIssue, dry_run: bool = False) -> str:
        """
        Fix interface compliance issues in a generator.

        Returns the modified file content.
        """
        content = issue.file_path.read_text(encoding="utf-8")

        # Parse the file
        tree = ast.parse(content, filename=str(issue.file_path))

        # Find the generator class
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == issue.generator_class:
                # Generate fixes
                fixes = self._generate_fixes(issue, node, content)

                # Apply fixes
                modified_content = self._apply_fixes(content, node, fixes, issue)

                if not dry_run:
                    issue.file_path.write_text(modified_content, encoding="utf-8")
                    print(f"✅ Fixed {issue.generator_class} in {issue.file_path.name}")
                else:
                    print(f"🔍 [DRY RUN] Would fix {issue.generator_class} in {issue.file_path.name}")

                return modified_content

        raise ValueError(f"Could not find class {issue.generator_class} in {issue.file_path}")

    def _generate_fixes(self, issue: InterfaceIssue, node: ast.ClassDef, content: str) -> Dict[str, str]:
        """Generate fix code for missing methods"""
        fixes = {}

        # Determine return type
        return_type = issue.return_type or "Any"

        # Fix 1: generate_single
        if issue.missing_generate_single:
            if issue.has_legacy_generate:
                # Wrap existing generate() method
                fixes["generate_single"] = self._generate_generate_single_wrapper(return_type)
            else:
                # Create new implementation
                fixes["generate_single"] = self._generate_generate_single_stub(return_type)

        # Fix 2: generator_type
        if issue.missing_generator_type:
            generator_type = self._infer_generator_type(issue.file_path)
            fixes["generator_type"] = self._generate_generator_type(generator_type)

        # Fix 3: supported_parameters
        if issue.missing_supported_parameters:
            fixes["supported_parameters"] = self._generate_supported_parameters(issue.parameter_names)

        # Fix 4: validate
        if issue.missing_validate:
            if issue.has_validator_class:
                fixes["validate"] = self._generate_validate_with_validator(return_type)
            else:
                fixes["validate"] = self._generate_validate_basic(return_type)

        return fixes

    def _generate_generate_single_wrapper(self, return_type: str) -> str:
        """Generate generate_single that wraps legacy generate()"""
        return f'''    def generate_single(self, context: Optional[GenerationContext] = None) -> {return_type}:
        """生成单个数据项"""
        return self.generate(context)'''

    def _generate_generate_single_stub(self, return_type: str) -> str:
        """Generate generate_single stub"""
        return f'''    def generate_single(self, context: Optional[GenerationContext] = None) -> {return_type}:
        """生成单个数据项 - TODO: Implement generation logic"""
        raise NotImplementedError("generate_single not implemented")'''

    def _generate_generator_type(self, generator_type: str) -> str:
        """Generate generator_type property"""
        return f'''    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型"""
        return GeneratorType.{generator_type}'''

    def _generate_supported_parameters(self, param_names: List[str]) -> str:
        """Generate supported_parameters property"""
        param_list = ", ".join(f'"{p}"' for p in param_names) if param_names else ""
        return f'''    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表"""
        return [{param_list}]'''

    def _generate_validate_with_validator(self, return_type: str) -> str:
        """Generate validate that uses existing validator"""
        return f'''    def validate(self, data: {return_type}) -> bool:
        """验证生成的数据"""
        if hasattr(self, 'validator') and hasattr(self.validator, 'validate'):
            return self.validator.validate(data)
        return True'''

    def _generate_validate_basic(self, return_type: str) -> str:
        """Generate basic validate based on return type"""
        # Simple type checking
        if return_type in ["str", "String"]:
            check = "isinstance(data, str) and len(data) > 0"
        elif return_type in ["int", "Integer"]:
            check = "isinstance(data, int)"
        elif return_type in ["float", "Float", "Decimal"]:
            check = "isinstance(data, (int, float))"
        elif return_type in ["bool", "Boolean"]:
            check = "isinstance(data, bool)"
        else:
            check = "data is not None"

        return f'''    def validate(self, data: {return_type}) -> bool:
        """验证生成的数据"""
        return {check}'''

    def _infer_generator_type(self, file_path: Path) -> str:
        """Infer GeneratorType from file path"""
        relative_path = file_path.relative_to(self.generators_dir)
        category = relative_path.parts[0] if relative_path.parts else "basic"
        return self.CATEGORY_TO_TYPE.get(category, "BASIC")

    def _apply_fixes(self, content: str, node: ast.ClassDef, fixes: Dict[str, str], issue: InterfaceIssue) -> str:
        """Apply generated fixes to file content"""
        lines = content.split("\n")

        # Find the end of the class (last non-empty line in class body)
        class_end_line = node.end_lineno - 1  # 0-indexed

        # Find last method in class
        last_method_line = class_end_line
        for item in reversed(node.body):
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                last_method_line = item.end_lineno - 1  # 0-indexed
                break

        # Insert fixes after the last method
        insert_line = last_method_line + 1

        # Add blank line before fixes
        fix_lines = [""]

        # Add each fix
        for method_name, fix_code in fixes.items():
            fix_lines.extend(fix_code.split("\n"))
            fix_lines.append("")  # Blank line between methods

        # Insert fixes
        lines = lines[:insert_line] + fix_lines + lines[insert_line:]

        # Fix imports if needed
        modified_content = "\n".join(lines)

        # Ensure required imports are present (smarter multi-line import handling)
        modified_content = self._ensure_imports(modified_content)

        # Fix random → secrets if needed
        if issue.uses_random_module:
            modified_content = self._fix_random_usage(modified_content)

        return modified_content

    def _ensure_imports(self, content: str) -> str:
        """Ensure required imports are present with proper multi-line handling"""
        lines = content.split("\n")

        # Check if imports are needed
        needs_generation_context = "Optional[GenerationContext]" in content or "context: GenerationContext" in content
        needs_generator_type = "GeneratorType." in content
        needs_optional = "Optional[" in content

        # Find import sections
        generator_import_idx = None
        types_import_idx = None
        typing_import_idx = None

        for i, line in enumerate(lines):
            if line.startswith("from ...core.generator import"):
                generator_import_idx = i
            elif line.startswith("from ...core.types import"):
                types_import_idx = i
            elif line.startswith("from typing import"):
                typing_import_idx = i

        # Handle GenerationContext import
        if needs_generation_context and generator_import_idx is not None:
            # Check if GenerationContext is already imported
            import_section = self._get_import_section(lines, generator_import_idx)
            if "GenerationContext" not in import_section:
                lines = self._add_to_multiline_import(lines, generator_import_idx, "GenerationContext")

        # Handle GeneratorType import
        if needs_generator_type:
            if types_import_idx is not None:
                import_section = self._get_import_section(lines, types_import_idx)
                if "GeneratorType" not in import_section:
                    lines = self._add_to_multiline_import(lines, types_import_idx, "GeneratorType")
            else:
                # Add new import before typing import or at beginning
                insert_idx = typing_import_idx if typing_import_idx else 0
                lines.insert(insert_idx, "from ...core.types import GeneratorType")

        # Handle Optional import
        if needs_optional and typing_import_idx is not None:
            import_section = self._get_import_section(lines, typing_import_idx)
            if "Optional" not in import_section:
                lines = self._add_to_multiline_import(lines, typing_import_idx, "Optional")

        return "\n".join(lines)

    def _get_import_section(self, lines: list[str], start_idx: int) -> str:
        """Get full multi-line import section starting at start_idx"""
        section = lines[start_idx]
        if "(" in section:
            # Multi-line import
            i = start_idx + 1
            while i < len(lines) and ")" not in lines[i - 1]:
                section += "\n" + lines[i]
                i += 1
        return section

    def _add_to_multiline_import(self, lines: list[str], start_idx: int, item_name: str) -> list[str]:
        """Add an item to a potentially multi-line import statement"""
        line = lines[start_idx]

        if "(" in line:
            # Multi-line import - add to the list
            # Find the closing parenthesis
            end_idx = start_idx
            while end_idx < len(lines) and ")" not in lines[end_idx]:
                end_idx += 1

            # Insert before the closing paren line
            if end_idx < len(lines):
                lines.insert(end_idx, f"    {item_name},")
        else:
            # Single-line import - convert to multi-line if needed
            if "," in line:
                # Already has multiple imports - just add comma and new import
                parts = line.split(" import ")
                if len(parts) == 2:
                    lines[start_idx] = parts[0] + " import (\n    " + parts[1] + ",\n    " + item_name + ",\n)"
            else:
                # Single import - add as second import
                parts = line.split(" import ")
                if len(parts) == 2:
                    lines[start_idx] = parts[0] + " import (\n    " + parts[1] + ",\n    " + item_name + ",\n)"

        return lines

    def _fix_random_usage(self, content: str) -> str:
        """Replace random module with secrets module (conservative approach)"""
        # Check if there are random.randint calls that need manual conversion
        has_randint = "random.randint(" in content
        has_randrange = "random.randrange(" in content
        has_normalvariate = "random.normalvariate(" in content or "random.gauss(" in content

        needs_manual_random = has_randint or has_randrange or has_normalvariate

        if not needs_manual_random:
            # Safe to fully replace random with secrets
            content = content.replace("import random\n", "import secrets\n")
            content = content.replace("from random import", "from secrets import")
        else:
            # Keep random import but add secrets, with warning
            if "import secrets" not in content:
                content = content.replace("import random\n", "import random  # TODO: Convert to secrets\nimport secrets\n")

            # Add warning comment
            lines = content.split("\n")
            last_import_idx = 0
            for i, line in enumerate(lines):
                if line.startswith("import ") or line.startswith("from "):
                    last_import_idx = i

            warning = "\n# WARNING: This file uses random.randint/randrange/normalvariate that needs manual review\n# Conversion patterns:\n#   random.randint(a, b) → secrets.randbelow(b - a + 1) + a\n#   random.randrange(n) → secrets.randbelow(n)\n#   For statistical distributions, consider if CSPRNG is necessary\n"
            lines.insert(last_import_idx + 1, warning)
            content = "\n".join(lines)

        # Replace SAFE random calls with secrets equivalents
        replacements = {
            "random.choice(": "secrets.choice(",
            "random.random()": "(secrets.randbelow(1000000) / 1000000)",  # Float 0-1
        }

        for old, new in replacements.items():
            content = content.replace(old, new)

        return content


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Interface Compliance Fixer")
    parser.add_argument("--scan", action="store_true", help="Scan for non-compliant generators")
    parser.add_argument("--analyze", type=str, metavar="FILE", help="Analyze specific file")
    parser.add_argument("--fix", type=str, metavar="FILE", help="Fix specific file")
    parser.add_argument("--fix-all", action="store_true", help="Fix all non-compliant generators")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be fixed without modifying files")
    parser.add_argument("--category", type=str, help="Fix only generators in specific category (e.g., 'basic', 'identifier')")

    args = parser.parse_args()

    # Determine project root
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent

    analyzer = InterfaceAnalyzer(project_root)
    fixer = InterfaceFixer(project_root)

    if args.scan:
        # Scan all generators
        analyzer.scan_all_generators()
        analyzer.print_summary()

        # List non-compliant generators
        if analyzer.issues:
            print(f"\n❌ Non-Compliant Generators ({len(analyzer.issues)}):")
            for issue in sorted(analyzer.issues, key=lambda i: (i.severity, str(i.file_path))):
                rel_path = issue.file_path.relative_to(project_root)
                print(f"\n   {rel_path}: {issue.generator_class}")
                print(f"   Severity: {issue.severity}")
                if issue.missing_generate_single:
                    print(f"      ❌ Missing generate_single()")
                if issue.has_legacy_generate:
                    print(f"      ⚠️  Has legacy generate() method")
                if issue.missing_generator_type:
                    print(f"      ❌ Missing generator_type property")
                if issue.missing_validate:
                    print(f"      ❌ Missing validate() method")
                if issue.missing_supported_parameters:
                    print(f"      ⚠️  Missing supported_parameters property")
                if issue.uses_random_module:
                    print(f"      ⚠️  Uses insecure random module")

    elif args.analyze:
        # Analyze specific file
        file_path = Path(args.analyze).resolve()
        analyzer._analyze_file(file_path)

        if analyzer.issues:
            for issue in analyzer.issues:
                print(f"\n📝 {issue.generator_class}:")
                print(f"   Status: {'✅ Compliant' if issue.is_compliant else '❌ Non-Compliant'}")
                print(f"   Severity: {issue.severity}")
                print(f"   Return type: {issue.return_type}")
                print(f"   Parameters: {', '.join(issue.parameter_names) if issue.parameter_names else 'None detected'}")
                print(f"   Has validator: {'Yes' if issue.has_validator_class else 'No'}")

                if not issue.is_compliant:
                    print(f"\n   Issues:")
                    if issue.missing_generate_single:
                        print(f"      - Missing generate_single()")
                    if issue.missing_generator_type:
                        print(f"      - Missing generator_type")
                    if issue.missing_validate:
                        print(f"      - Missing validate()")
                    if issue.missing_supported_parameters:
                        print(f"      - Missing supported_parameters")
        else:
            print("✅ All generators in file are compliant")

    elif args.fix:
        # Fix specific file
        file_path = Path(args.fix).resolve()
        analyzer._analyze_file(file_path)

        if analyzer.issues:
            for issue in analyzer.issues:
                try:
                    fixer.fix_generator(issue, dry_run=args.dry_run)
                except Exception as e:
                    print(f"❌ Error fixing {issue.generator_class}: {e}")
        else:
            print("✅ File already compliant")

    elif args.fix_all:
        # Fix all non-compliant generators
        analyzer.scan_all_generators()

        # Filter by category if specified
        issues_to_fix = analyzer.issues
        if args.category:
            issues_to_fix = [
                i for i in analyzer.issues
                if str(i.file_path.relative_to(analyzer.generators_dir)).startswith(args.category)
            ]
            print(f"\n🔧 Fixing {len(issues_to_fix)} generators in category '{args.category}'...")
        else:
            print(f"\n🔧 Fixing {len(issues_to_fix)} non-compliant generators...")

        success_count = 0
        error_count = 0

        for issue in issues_to_fix:
            try:
                fixer.fix_generator(issue, dry_run=args.dry_run)
                success_count += 1
            except Exception as e:
                print(f"❌ Error fixing {issue.generator_class}: {e}")
                error_count += 1

        print(f"\n📊 Results:")
        print(f"   ✅ Successfully fixed: {success_count}")
        if error_count > 0:
            print(f"   ❌ Errors: {error_count}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
