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

test_card = "6222021234567890"
checksum = calculate_luhn(test_card)
print(f"Card: {test_card}")
print(f"Luhn checksum: {checksum}")
print(f"Valid: {checksum == 0}")

# Try to find a valid checksum digit
for last_digit in range(10):
    test = test_card[:-1] + str(last_digit)
    if calculate_luhn(test) == 0:
        print(f"Valid card with last digit {last_digit}: {test}")
