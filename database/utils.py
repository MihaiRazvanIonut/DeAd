def base36encode(number):
    if not isinstance(number, int):
        raise TypeError('number must be an integer')
    is_negative = number < 0
    number = abs(number)

    alphabet, base36 = ['0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', '']

    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36
    if is_negative:
        base36 = '-' + base36

    return base36 or alphabet[0]
