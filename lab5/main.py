from GOST3411.GOST3411 import GOST3411
from MD5.MD5 import MD5


def main():
    word = input("Enter any word:")

    md5_hash = MD5.hash(word)

    print("#" * 100)
    print("Hash of MD5:")
    print(md5_hash)
    print("#" * 100)
    print("Hash of GOST34.11 (256/528 bits):")

    print(GOST3411().hash(word, 256))
    print(GOST3411().hash(word, 512))
    print("#" * 100)


if __name__ == "__main__":
    main()
