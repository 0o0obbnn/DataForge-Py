def calculate_luhn(card_number):
    """计算Luhn校验和"""
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

# Find a valid 16-digit ICBC card number
base = "622202123456789"
print(f"Testing base: {base}")
for last_digit in range(10):
    test = base + str(last_digit)
    checksum = calculate_luhn(test)
    print(f"  {test}: checksum={checksum}")
    if checksum == 0:
        print(f"✓ Valid 16-digit ICBC card: {test}")
        break
