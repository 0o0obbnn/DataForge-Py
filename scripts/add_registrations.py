#!/usr/bin/env python3
"""
Registration Helper Script

Discovers unregistered generators and suggests registration names.
Uses AST parsing to analyze generator classes and suggest appropriate names.

Usage:
    python scripts/add_registrations.py --scan          # Scan for unregistered generators
    python scripts/add_registrations.py --suggest FILE  # Suggest names for specific file
    python scripts/add_registrations.py --apply FILE    # Apply registration to file
"""

import ast
import re
import secrets
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class GeneratorInfo:
    """Information about a discovered generator class"""
    class_name: str
    file_path: Path
    base_class: str
    is_registered: bool
    existing_registration: Optional[str] = None
    suggested_name: Optional[str] = None
    suggested_aliases: Optional[list[str]] = None
    docstring: Optional[str] = None
    generator_type: Optional[str] = None


class GeneratorDiscovery:
    """AST-based generator discovery and analysis"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.generators_dir = project_root / "dataforge" / "generators"
        self.discovered_generators: list[GeneratorInfo] = []

    def scan_all_generators(self) -> list[GeneratorInfo]:
        """Scan all generator files and discover classes"""
        print("🔍 Scanning for generator classes...")

        # Recursively find all .py files in generators/
        for py_file in self.generators_dir.rglob("*.py"):
            if py_file.name == "__init__.py":
                continue

            self._analyze_file(py_file)

        print(f"✅ Found {len(self.discovered_generators)} generator classes")
        return self.discovered_generators

    def _analyze_file(self, file_path: Path) -> None:
        """Analyze a single Python file for generator classes"""
        try:
            content = file_path.read_text(encoding="utf-8")
            tree = ast.parse(content, filename=str(file_path))

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    info = self._analyze_class(node, file_path, content)
                    if info:
                        self.discovered_generators.append(info)

        except Exception as e:
            print(f"⚠️  Error analyzing {file_path}: {e}")

    def _analyze_class(self, node: ast.ClassDef, file_path: Path, content: str) -> Optional[GeneratorInfo]:
        """Analyze a class definition to determine if it's a generator"""
        # Check if it inherits from DataGenerator
        base_classes = [self._get_base_name(base) for base in node.bases]

        if not any(base in ["DataGenerator", "GenericEmailGenerator", "GenericPhoneNumberGenerator",
                            "PhoneNumberGenerator", "EmailGenerator"] for base in base_classes):
            return None

        # Extract docstring
        docstring = ast.get_docstring(node)

        # Check if class is decorated with @register_generator
        is_registered = False
        existing_registration = None

        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call):
                if isinstance(decorator.func, ast.Name) and decorator.func.id == "register_generator":
                    is_registered = True
                    if decorator.args:
                        # First arg is the registration name
                        if isinstance(decorator.args[0], ast.Constant):
                            existing_registration = decorator.args[0].value

        # Determine generator type from file path
        relative_path = file_path.relative_to(self.generators_dir)
        category = relative_path.parts[0] if relative_path.parts else "unknown"

        return GeneratorInfo(
            class_name=node.name,
            file_path=file_path,
            base_class=base_classes[0] if base_classes else "Unknown",
            is_registered=is_registered,
            existing_registration=existing_registration,
            docstring=docstring,
            generator_type=category
        )

    def _get_base_name(self, base: ast.expr) -> str:
        """Extract base class name from AST node"""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Subscript):
            if isinstance(base.value, ast.Name):
                return base.value.id
        elif isinstance(base, ast.Attribute):
            return base.attr
        return "Unknown"

    def filter_unregistered(self) -> list[GeneratorInfo]:
        """Get only unregistered generators"""
        return [g for g in self.discovered_generators if not g.is_registered]

    def print_summary(self) -> None:
        """Print discovery summary"""
        total = len(self.discovered_generators)
        registered = sum(1 for g in self.discovered_generators if g.is_registered)
        unregistered = total - registered

        print(f"\n📊 Generator Discovery Summary:")
        print(f"   Total generators: {total}")
        print(f"   ✅ Registered: {registered}")
        print(f"   ❌ Unregistered: {unregistered}")

        # Group by category
        by_category = {}
        for gen in self.discovered_generators:
            cat = gen.generator_type
            if cat not in by_category:
                by_category[cat] = {"total": 0, "registered": 0}
            by_category[cat]["total"] += 1
            if gen.is_registered:
                by_category[cat]["registered"] += 1

        print("\n📁 By Category:")
        for category, stats in sorted(by_category.items()):
            unreg = stats["total"] - stats["registered"]
            print(f"   {category}: {stats['total']} total, {unreg} unregistered")


class NameSuggester:
    """Suggests registration names and aliases for generators"""

    # Common words to remove from class names
    SUFFIX_REMOVALS = ["Generator", "Gen", "Creator", "Builder"]

    # Category-specific naming patterns
    CATEGORY_PATTERNS = {
        "basic": ["basic_", ""],
        "contact": ["contact_", ""],
        "identifier": ["id_", ""],
        "auth": ["auth_", ""],
        "network": ["net_", "network_"],
        "finance": ["fin_", "finance_"],
        "numeric": ["num_", ""],
        "text": ["text_", ""],
        "advanced": ["adv_", "advanced_"],
    }

    # Chinese aliases for common generators
    CHINESE_ALIASES = {
        "idcard": ["身份证", "身份证号"],
        "bankcard": ["银行卡", "银行卡号"],
        "phone": ["手机号", "电话", "手机号码"],
        "email": ["邮箱", "电子邮件"],
        "name": ["姓名", "名字"],
        "address": ["地址"],
        "age": ["年龄"],
        "gender": ["性别"],
        "company": ["公司", "公司名"],
        "uscc": ["统一社会信用代码", "信用代码"],
        "password": ["密码"],
        "username": ["用户名"],
        "license_plate": ["车牌号"],
        "passport": ["护照"],
        "organization_code": ["组织机构代码"],
    }

    def suggest_name(self, generator: GeneratorInfo) -> tuple[str, list[str]]:
        """
        Suggest a registration name and aliases for a generator.

        Returns:
            (suggested_name, suggested_aliases)
        """
        # Start with class name
        class_name = generator.class_name

        # Remove common suffixes
        base_name = class_name
        for suffix in self.SUFFIX_REMOVALS:
            if base_name.endswith(suffix):
                base_name = base_name[:-len(suffix)]

        # Convert CamelCase to snake_case
        snake_name = self._camel_to_snake(base_name)

        # Remove category prefix if present
        category = generator.generator_type
        if category in self.CATEGORY_PATTERNS:
            for prefix in self.CATEGORY_PATTERNS[category]:
                if snake_name.startswith(prefix):
                    snake_name = snake_name[len(prefix):]

        # Generate aliases
        aliases = self._generate_aliases(snake_name, generator)

        return snake_name, aliases

    def _camel_to_snake(self, name: str) -> str:
        """Convert CamelCase to snake_case"""
        # Insert underscore before uppercase letters
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        # Insert underscore before uppercase letters preceded by lowercase
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        return s2.lower()

    def _generate_aliases(self, base_name: str, generator: GeneratorInfo) -> list[str]:
        """Generate alias list for a generator"""
        aliases = []

        # Add Chinese aliases if available
        if base_name in self.CHINESE_ALIASES:
            aliases.extend(self.CHINESE_ALIASES[base_name])

        # Add common variations
        # Hyphenated version
        if "_" in base_name:
            aliases.append(base_name.replace("_", "-"))

        # Abbreviated version (for long names)
        words = base_name.split("_")
        if len(words) > 2:
            abbrev = "".join(word[0] for word in words)
            aliases.append(abbrev)

        # Category prefix version
        category = generator.generator_type
        if category and category != "basic":
            aliases.append(f"{category}_{base_name}")

        # Remove duplicates while preserving order
        seen = {base_name}  # Don't include base name in aliases
        unique_aliases = []
        for alias in aliases:
            if alias not in seen:
                seen.add(alias)
                unique_aliases.append(alias)

        return unique_aliases


class CodeGenerator:
    """Generates @register_generator decorator code"""

    def generate_decorator(self, name: str, aliases: list[str]) -> str:
        """Generate the @register_generator decorator string"""
        if aliases:
            # Format aliases list
            alias_str = ", ".join(f'"{alias}"' for alias in aliases)
            return f'@register_generator("{name}", [{alias_str}])'
        else:
            return f'@register_generator("{name}")'

    def apply_registration(self, generator: GeneratorInfo, name: str, aliases: list[str]) -> str:
        """
        Apply registration decorator to a generator class in its file.

        Returns the modified file content.
        """
        content = generator.file_path.read_text(encoding="utf-8")

        # Check if already registered
        if generator.is_registered:
            raise ValueError(f"{generator.class_name} is already registered as '{generator.existing_registration}'")

        # Parse the file
        tree = ast.parse(content, filename=str(generator.file_path))

        # Find the class definition
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == generator.class_name:
                # Insert decorator before class
                decorator_code = self.generate_decorator(name, aliases)

                # Get line number of class definition
                class_line = node.lineno - 1  # 0-indexed

                lines = content.split("\n")

                # Find the actual start (accounting for existing decorators)
                insert_line = class_line

                # Insert decorator
                lines.insert(insert_line, decorator_code)

                return "\n".join(lines)

        raise ValueError(f"Could not find class {generator.class_name} in {generator.file_path}")

    def generate_wrapper_class(self, base_class: str, name: str, aliases: list[str]) -> str:
        """
        Generate a registered wrapper class (alternative approach).

        Returns code to append to file.
        """
        decorator = self.generate_decorator(name, aliases)
        class_name = f"Generic{base_class.replace('Generator', '')}Generator"

        code = f"""

{decorator}
class {class_name}({base_class}):
    \"\"\"通用{name}生成器注册版本\"\"\"

    pass
"""
        return code


def main():
    """Main entry point for the script"""
    import argparse

    parser = argparse.ArgumentParser(description="Generator Registration Helper")
    parser.add_argument("--scan", action="store_true", help="Scan for all generators")
    parser.add_argument("--suggest", type=str, metavar="FILE", help="Suggest registration for specific file")
    parser.add_argument("--apply", type=str, metavar="FILE", help="Apply registration to file")
    parser.add_argument("--name", type=str, help="Override suggested name")
    parser.add_argument("--aliases", type=str, help="Override aliases (comma-separated)")

    args = parser.parse_args()

    # Determine project root
    script_path = Path(__file__).resolve()
    project_root = script_path.parent.parent

    discovery = GeneratorDiscovery(project_root)
    suggester = NameSuggester()
    codegen = CodeGenerator()

    if args.scan:
        # Scan all generators
        discovery.scan_all_generators()
        discovery.print_summary()

        # List unregistered generators
        unregistered = discovery.filter_unregistered()
        if unregistered:
            print(f"\n❌ Unregistered Generators ({len(unregistered)}):")
            for gen in sorted(unregistered, key=lambda g: g.file_path):
                rel_path = gen.file_path.relative_to(project_root)
                print(f"   {rel_path}: {gen.class_name}")

                # Suggest names
                suggested_name, suggested_aliases = suggester.suggest_name(gen)
                print(f"      → Suggested: {suggested_name}")
                if suggested_aliases:
                    print(f"      → Aliases: {', '.join(suggested_aliases)}")
                print()

    elif args.suggest:
        # Suggest for specific file
        file_path = Path(args.suggest).resolve()
        discovery.scan_all_generators()

        # Find generators in this file
        matching = [g for g in discovery.discovered_generators if g.file_path == file_path]

        if not matching:
            print(f"❌ No generators found in {file_path}")
            return

        for gen in matching:
            print(f"\n📝 {gen.class_name} ({gen.generator_type})")
            print(f"   File: {gen.file_path.relative_to(project_root)}")
            print(f"   Status: {'✅ Registered' if gen.is_registered else '❌ Unregistered'}")

            if gen.is_registered:
                print(f"   Current: {gen.existing_registration}")
            else:
                suggested_name, suggested_aliases = suggester.suggest_name(gen)
                print(f"   Suggested name: {suggested_name}")
                print(f"   Suggested aliases: {', '.join(suggested_aliases)}")

                decorator = codegen.generate_decorator(suggested_name, suggested_aliases)
                print(f"\n   Decorator code:\n   {decorator}")

    elif args.apply:
        # Apply registration to file
        file_path = Path(args.apply).resolve()
        discovery.scan_all_generators()

        # Find generators in this file
        matching = [g for g in discovery.discovered_generators if g.file_path == file_path]

        if not matching:
            print(f"❌ No generators found in {file_path}")
            return

        for gen in matching:
            if gen.is_registered:
                print(f"⚠️  {gen.class_name} is already registered as '{gen.existing_registration}'")
                continue

            # Get name and aliases
            if args.name:
                name = args.name
            else:
                name, _ = suggester.suggest_name(gen)

            if args.aliases:
                aliases = [a.strip() for a in args.aliases.split(",")]
            else:
                _, aliases = suggester.suggest_name(gen)

            print(f"\n📝 Applying registration to {gen.class_name}:")
            print(f"   Name: {name}")
            print(f"   Aliases: {', '.join(aliases)}")

            try:
                # Generate wrapper class approach (safer than modifying existing class)
                wrapper_code = codegen.generate_wrapper_class(gen.class_name, name, aliases)

                # Append to file
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(wrapper_code)

                print(f"   ✅ Successfully registered {gen.class_name} as '{name}'")

            except Exception as e:
                print(f"   ❌ Error: {e}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
