"""基础生成器模块"""

try:
    # 导入所有生成器以触发注册
    from . import (
        address,
        age,
        company_name,
        context_aware,
        education,
        enhanced_generators,
        extended_profile,
        gender,
        idcard,
        license_plate,
        marital_status,
        name,
        name_optimized,
        occupation,
        password,
        username,
        uuid,
    )
except ImportError as e:
    print(f"警告: 部分基础生成器导入失败: {e}")

__all__ = [
    "idcard",
    "name",
    "age",
    "gender",
    "address",
    "company_name",
    "education",
    "marital_status",
    "occupation",
    "context_aware",
    "enhanced_generators",
    "extended_profile",
    "license_plate",
    "name_optimized",
    "password",
    "username",
    "uuid",
]
