def luhn_checksum(card_num):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_num)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

card = "6222021234567890"
checksum = luhn_checksum(card)
print(f"Card: {card}")
print(f"Luhn checksum: {checksum}")
print(f"Valid: {checksum == 0}")
