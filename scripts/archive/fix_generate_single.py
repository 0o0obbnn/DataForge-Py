"""
Fix generate_single() NotImplementedError in all generators

This script replaces:
    raise NotImplementedError("generate_single not implemented")

With:
    return self._generate_raw(context)
"""

import os
import re

# Files to fix (from grep results)
files_to_fix = [
    "dataforge/generators/text/string.py",
    "dataforge/generators/numeric/number.py",
    "dataforge/generators/text/special_chars.py",
    "dataforge/generators/finance/future.py",
    "dataforge/generators/finance/stock.py",
    "dataforge/generators/finance/bond.py",
    "dataforge/generators/finance/crypto.py",
    "dataforge/generators/finance/fund.py",
    "dataforge/generators/finance/advanced.py",
    "dataforge/generators/finance/bank_account.py",
    "dataforge/generators/contact/communication.py",
    "dataforge/generators/contact/email.py",
    "dataforge/generators/advanced/trading_calendar.py",
    "dataforge/generators/advanced/user_behavior.py",
    "dataforge/generators/advanced/advanced_timestamp.py",
    "dataforge/generators/basic/company_name.py",
    "dataforge/generators/basic/gender.py",
    "dataforge/generators/basic/license_plate.py",
    "dataforge/generators/basic/name_optimized.py",
]

def fix_file(filepath):
    """Fix generate_single() implementation in a file"""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Pattern to match the NotImplementedError line
    pattern = r'raise NotImplementedError\("generate_single not implemented"\)'
    replacement = r'return self._generate_raw(context)'

    # Replace all occurrences
    content = re.sub(pattern, replacement, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count = len(re.findall(pattern, original_content))
        print(f"✅ Fixed {count} occurrence(s) in {filepath}")
        return True
    else:
        print(f"⏭️  No changes needed in {filepath}")
        return False

def main():
    """Fix all files"""
    print("Fixing generate_single() NotImplementedError in generators...\n")

    fixed_count = 0
    skipped_count = 0

    for filepath in files_to_fix:
        if fix_file(filepath):
            fixed_count += 1
        else:
            skipped_count += 1

    print(f"\n📊 Summary:")
    print(f"   Fixed: {fixed_count} files")
    print(f"   Skipped: {skipped_count} files")
    print(f"   Total: {len(files_to_fix)} files")

    print("\n✅ All fixes applied!")
    print("\nNext: Run pytest to verify fixes")

if __name__ == "__main__":
    main()
