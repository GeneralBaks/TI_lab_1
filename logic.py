from global_val import CYRILLIC, CYRILLIC_LEN, ENGLISH, ENGLISH_LEN

def get_weight_cyrillic(c: str) -> int:
    return CYRILLIC.index(c.lower())

def get_weight_english(c: str) -> int:
    return ENGLISH.index(c.lower())

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def cipher_vigenere(text: str, key: str) -> str:
    res = []
    key_i = 0

    for char in text:
        if char.lower() not in CYRILLIC:
            res.append(char)
            continue

        is_upper = char.isupper()

        modif = get_weight_cyrillic(key[key_i % len(key)])
        c_num = get_weight_cyrillic(char)
        new_char = CYRILLIC[(c_num + modif) % CYRILLIC_LEN]

        if is_upper:
            new_char = new_char.upper()

        res.append(new_char)
        key_i += 1

    return "".join(res)

def decipher_vigenere(text: str, key: str) -> str:
    res = []
    key_i = 0

    for char in text:
        if char.lower() not in CYRILLIC:
            res.append(char)
            continue

        is_upper = char.isupper()

        modif = get_weight_cyrillic(key[key_i % len(key)])
        c_num = get_weight_cyrillic(char)
        new_char = CYRILLIC[(c_num - modif + CYRILLIC_LEN) % CYRILLIC_LEN]

        if is_upper:
            new_char = new_char.upper()

        res.append(new_char)
        key_i += 1

    return "".join(res)


def cipher_decimation(text: str, step: int) -> str:
    res = []

    for char in text:
        if char.lower() not in ENGLISH:
            res.append(char)
            continue

        is_upper = char.isupper()

        i = get_weight_english(char)
        encrypted_pos = (i * step) % ENGLISH_LEN
        new_char = ENGLISH[encrypted_pos]

        if is_upper:
            new_char = new_char.upper()

        res.append(new_char)

    return "".join(res)


def mod_inverse(k: int, n: int) -> int:
    m0 = n
    y = 0
    x = 1

    if n == 1:
        return 0

    while k > 1:
        q = k // n
        t = n
        n = k % n
        k = t
        t = y
        y = x - q * y
        x = t

    if x < 0:
        x = x + m0

    return x

def decipher_decimation(text: str, step: int) -> str:
    inv_step = mod_inverse(step, ENGLISH_LEN)
    res = []

    for char in text:
        if char.lower() not in ENGLISH:
            res.append(char)
            continue

        is_upper = char.isupper()

        i = get_weight_english(char)
        decrypted_pos = (i * inv_step) % ENGLISH_LEN
        new_char = ENGLISH[decrypted_pos]

        if is_upper:
            new_char = new_char.upper()

        res.append(new_char)

    return "".join(res)

