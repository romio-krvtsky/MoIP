import random

from ELGamal import ElGamal


def text_to_int(text):
    return ord(text)


def check(decpypt):
    s_real = message * elgamal.p_point
    assert decpypt.y == s_real.y, decpypt.x


if __name__ == '__main__':
    a = 7
    b = 43308876546767276905765904595650931995942111794451039583252968842033849580414
    x = 2
    y = 4018974056539037503335449422937059775635739389905545080690979365213431566280
    p = 57896044618658097711785492504343953926634992332820282019728792003956564821041
    n = 57896044618658097711785492504343953927082934583725450622380973592137631069619
    ka = random.getrandbits(256)  # private

    elgamal = ElGamal(p, a, b, x, y)
    r = random.getrandbits(128)
    qa = elgamal.gen_keys(ka)  # public
    with open("input.txt", "r", encoding='utf-8') as f:
        text = f.read()

    for item in text:
        message = text_to_int(item)
        c1, c2 = elgamal.encrypt(message, r, qa)
        print(c1.x, c1.y)
        print(c2.y, c1.y)
        print()
        decpypt = elgamal.decrypt(c1, c2, ka)
        check(decpypt)

