def luhn_checksum(number):
    """计算Luhn校验和"""
    def digits_of(n):
        return [int(d) for d in str(n)]

    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]

    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))

    return checksum % 10

def generate_valid_card(prefix):
    """生成有效的卡号"""
    # 生成15位基础号码
    base = prefix + "123456789"
    
    # 计算校验位
    for check_digit in range(10):
        card = base + str(check_digit)
        if luhn_checksum(card) == 0:
            return card
    return None

# 生成有效卡号
valid_card = generate_valid_card("622202")
print(f"Valid card: {valid_card}")
print(f"Luhn check: {luhn_checksum(valid_card)}")
