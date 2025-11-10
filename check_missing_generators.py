#!/usr/bin/env python3
"""检查缺失的生成器"""

try:
    from dataforge.core.factory import default_registry
    
    expected = [
        'organization_code', 'drivers_license', 'logistics', 'landline', 'ipaddress', 
        'domain', 'port', 'url', 'device_id', 'session_token', 'timezone', 
        'geo_coordinates', 'http_header', 'chinese', 'multilingual', 
        'sms_verification_code', 'email_verification_token', 'future', 'datetime', 
        'timestamp', 'json', 'xml', 'yaml', 'sql_injection', 'xss_payload', 'user_behavior'
    ]
    
    missing = []
    for gen in expected:
        if not default_registry.is_registered(gen):
            missing.append(gen)
    
    print('Missing generators:', missing)
    print('Total missing:', len(missing))
    
    # 检查可用的生成器
    available = default_registry.list_generators()
    print('Available generators count:', len(available))
    
except Exception as e:
    print(f'Error: {e}')