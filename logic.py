from global_val import CYRILLIC, CYRILLIC_LEN

def get_weight(c: str) -> int:
    return CYRILLIC.index(c.lower())

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def cipher_vigenere(text: str, key: str) -> str:
    res = []
    for i, char in enumerate(text):
        modif = get_weight(key[i % len(key)])
        c_num = get_weight(char)
        res.append(CYRILLIC[(c_num + modif) % CYRILLIC_LEN])
    return "".join(res)

def cipher_decimation(text: str, step: int) -> str:
    length = len(text)
    res = [text[(i * step) % length] for i in range(length)]
    return "".join(res)

def decipher_vigenere(text: str, key: str) -> str:
    res = []
    for i, char in enumerate(text):
        modif = get_weight(key[i % len(key)])
        c_num = get_weight(char)
        res.append(CYRILLIC[(c_num - modif) % CYRILLIC_LEN])
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
    L = len(text)
    inv_step = mod_inverse(step, L)
    return "".join([text[(i * inv_step) % L] for i in range(L)])
