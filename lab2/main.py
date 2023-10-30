from consts import *
from stb import STB


def main():
    data = read_data()
    print(f"Data: {data}")
    print("#"*100)
    key = int.from_bytes('erpwkwekrokpdasdasda'.encode(), 'big')
    synchro = 312312412412

    stb = STB(key)
    # encrypt
    encrypted_text = stb.encrypt(data, synchro)
    write_encrypted_data(encrypted_text)
    print("#"*100)
    # decrypt
    decrypted_text = stb.decrypt(encrypted_text, synchro)
    write_decrypted_data(decrypted_text)
    print("#"*100)

def read_data():
    file = open("data.txt", "r", encoding="utf8")
    data = file.read()
    file.close()
    return data


def write_encrypted_data(encrypted_text: bytes):
    file = open("encrypted.txt", "w+", encoding="utf8")
    file.write(str(encrypted_text))
    print(f"Encrypted: {encrypted_text}")
    file.close()


def write_decrypted_data(decrypted_text: str):
    file = open("decrypted.txt", "w+", encoding="utf8")
    file.write(decrypted_text)
    print(f"Decrypted: {decrypted_text}")
    file.close()


if __name__ == '__main__':
    main()
