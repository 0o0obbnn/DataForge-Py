#!/usr/bin/env python3
"""检查生成器别名映射"""

try:
    from dataforge.core.factory import default_registry
    
    # 缺失的生成器及其可能的别名
    missing_with_aliases = {
        'organization_code': ['chinese_organization_code', 'org_code'],
        'drivers_license': ['generic_driver_license', 'driver_license', '驾驶证'],
        'logistics': ['generic_tracking_number', 'tracking_number', '物流单号', 'generic_waybill', 'waybill', '运单'],
        'landline': None,  # 可能确实缺失
        'ipaddress': None,  # 可能确实缺失
        'domain': None,  # 可能确实缺失
        'port': None,  # 可能确实缺失
        'url': None,  # 可能确实缺失
        'device_id': None,  # 可能确实缺失
        'session_token': ['session_id', 'session', 'auth_token', 'token'],
        'timezone': None,  # 可能确实缺失
        'geo_coordinates': None,  # 可能确实缺失
        'http_header': None,  # 可能确实缺失
        'chinese': ['chinese_text'],
        'multilingual': ['multilingual_text'],
        'sms_verification_code': ['sms_verification', 'sms_code'],
        'email_verification_token': ['email_verification', 'email_code'],
        'future': ['future_code', '期货合约', 'future', '期货'],
        'datetime': ['datetime_range', '日期时间范围', '时间范围'],
        'timestamp': ['advanced_timestamp', '高级时间戳', '时间戳'],
        'json': None,  # 可能确实缺失
        'xml': None,  # 可能确实缺失
        'yaml': None,  # 可能确实缺失
        'sql_injection': ['sql', 'sqli', 'sql_payload'],
        'xss_payload': ['xss', 'xss_script', 'xss_payload'],
        'user_behavior': ['user_behavior', '行为数据', '用户行为', 'analytics', 'analytics', '分析数据', '用户分析', '行为分析']
    }
    
    available = default_registry.list_generators()
    
    print("=== 生成器别名映射分析 ===")
    for missing, aliases in missing_with_aliases.items():
        if aliases:
            found_aliases = [alias for alias in aliases if alias in available]
            if found_aliases:
                print(f"✓ {missing} -> 可用别名: {found_aliases}")
            else:
                print(f"✗ {missing} -> 别名也不可用: {aliases}")
        else:
            print(f"? {missing} -> 无别名映射")
    
    print(f"\n总可用生成器数: {len(available)}")
    
except Exception as e:
    print(f'Error: {e}')