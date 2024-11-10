def convert_to_decimal(num, base):
    num = list(num)[::-1]
    ans = 0
    base = int(base)
    for i in range(len(num)):
        if num[i] == 'A':
            ans += 10 * base**i
        elif num[i] == 'B':
            ans += 11 * base**i
        elif num[i] == 'C':
            ans += 12 * base**i
        elif num[i] == 'D':
            ans += 13 * base**i
        elif num[i] == 'E':
            ans += 14 * base**i
        elif num[i] == 'F':
            ans += 15 * base**i
        else:
            ans += int(num[i]) * base**i

    return ans


def convert_to_any_base(num, base):
    ans = ''
    num = int(num)
    base = int(base)
    while num > 0:
        if num % base == 10:
            ans += 'A'
        elif num % base == 11:
            ans += 'B'
        elif num % base == 12:
            ans += 'C'
        elif num % base == 13:
            ans += 'D'
        elif num % base == 14:
            ans += 'E'
        elif num % base == 15:
            ans += 'F'
        else:
            ans += str(num % base)
        num //= base
    return ans[::-1]


