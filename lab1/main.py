from gamma_decr import gamma_decrpt
from GOST import GOST


def main():
    # data = input("enter data:\n")
    try:
        gost = GOST()
        with open("input.txt", "r", encoding='utf-8') as data_file:
            data = data_file.read()
        print(f"Data:\n {data}")
        encrypted_data = gost.gamma_encrypt_text(data)
        print('#' * 80)
        print(f'ENCRYPTED DATA:\t{encrypted_data}')
        with open("encrypted_data.txt", "w", encoding='utf-8') as encrypted_file:
            encrypted_file.write(encrypted_data)
        print('#' * 80)
        decrypted_data = gamma_decrpt(encrypted_data)
        print(f'DECRYPTED DATA:\t{decrypted_data}')
        with open("decrypted_data.txt", "w", encoding='utf-8') as decrypted_file:
            decrypted_file.write(decrypted_data)
    except:
        print(Exception())
    finally:
        print("#" * 5 + '\nend.')


if __name__ == '__main__':
    main()
