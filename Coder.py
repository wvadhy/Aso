import random

class Coder():

    __key = None
    __inter = None
    _hashed = []

    @staticmethod
    def encode(password: str = None) -> int:
        Coder.__key = random.randint(10**10,10**50)
        Coder.__inter = [str(ord(_)) for _ in password]
        __converted = int(''.join(Coder.__inter))
        __final = __converted ^ Coder.__key
        return __final

    @staticmethod
    def decode(encrypted: int = None) -> str:
        __temp = encrypted ^ Coder.__key
        __ret = ''.join([chr(int(_)) for _ in Coder.__inter])
        Coder._hashed.append(__ret)
        return __ret

