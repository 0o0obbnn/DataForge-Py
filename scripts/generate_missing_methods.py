#!/usr/bin/env python3
"""生成缺失方法的模板代码

使用方法:
python scripts/generate_missing_methods.py <generator_type> <param1> <param2> ...

示例:
python scripts/generate_missing_methods.py BASIC region gender valid
"""

import sys

TEMPLATE_VALIDATE = '''    def validate(self, data: {data_type}) -> bool:
        """验证生成的数据

        Args:
            data: 待验证的数据

        Returns:
            bool: 数据是否有效
        """
        if hasattr(self, 'validator'):
            return self.validator.validate(data)
        # 基本验证
        return data is not None'''

TEMPLATE_GENERATOR_TYPE = '''    @property
    def generator_type(self) -> GeneratorType:
        """返回生成器类型

        Returns:
            GeneratorType: 生成器类型
        """
        return GeneratorType.{gen_type}'''

TEMPLATE_SUPPORTED_PARAMETERS = '''    @property
    def supported_parameters(self) -> list[str]:
        """返回支持的参数列表

        Returns:
            list[str]: 支持的参数名称列表
        """
        return {params}'''

RENAME_GENERATE_INSTRUCTION = '''
# 重命名方法:
# 1. 将 def generate(self, context: Optional[GenerationContext] = None)
#    改为 def generate_single(self, context: Optional[GenerationContext] = None)
# 2. 如果其他地方调用了 self.generate()，改为 self.generate_single()
'''

IMPORT_INSTRUCTION = '''
# 添加导入:
from ...core.types import GeneratorType
'''

def main():
    if len(sys.argv) < 2:
        print("用法: python generate_missing_methods.py <generator_type> [param1] [param2] ...")
        print("\n可用的生成器类型:")
        print("  BASIC, IDENTIFIER, CONTACT, FINANCE, NETWORK, NUMERIC, TEXT, AUTH, ADVANCED")
        print("\n示例:")
        print("  python generate_missing_methods.py BASIC region birth_date_range gender valid")
        return 1

    gen_type = sys.argv[1].upper()
    params = sys.argv[2:] if len(sys.argv) > 2 else []

    print("=" * 80)
    print(f"生成器修复代码模板 - {gen_type} 类型")
    print("=" * 80)

    print(IMPORT_INSTRUCTION)
    print(RENAME_GENERATE_INSTRUCTION)

    print("\n# 添加以下方法到生成器类中:\n")

    # Validate方法
    print(TEMPLATE_VALIDATE.format(data_type="T"))
    print()

    # generator_type属性
    print(TEMPLATE_GENERATOR_TYPE.format(gen_type=gen_type))
    print()

    # supported_parameters属性
    params_str = str(params) if params else "[]"
    print(TEMPLATE_SUPPORTED_PARAMETERS.format(params=params_str))
    print()

    print("=" * 80)
    print("完成！复制上述代码到你的生成器类中")
    print("=" * 80)

if __name__ == '__main__':
    sys.exit(main())
