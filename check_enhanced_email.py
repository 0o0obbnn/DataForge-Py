#!/usr/bin/env python3
"""测试enhanced_email是否注册"""

import sys
import os
sys.path.insert(0, '.')
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'

from dataforge.core.factory import default_registry

generators = default_registry.list_generators()
print(f"enhanced_email在注册列表中: {'enhanced_email' in generators}")
print(f"所有包含enhanced的生成器: {[g for g in generators if 'enhanced' in g]}")