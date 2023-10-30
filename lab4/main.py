import numpy as np
from mceliece import split_binary_string, hamming7_4_decode, add_error, hamming7_4_encode, detect_error, \
    bits_to_str, flip_bit, P_inv, S_inv


def read_text(file_name):
    result = []
    with open(file_name, "r", encoding="utf-8") as file:
        result.append(file.read())

    with open(file_name, "rb") as file:
        result.append(file.read())

    return result


def write_text(file_name, text):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(text[0])


def encode(text):
    binary_str = ''.join(format(x, '08b') for x in text)
    split_bits_list = split_binary_string(binary_str, 4)
    enc_msg = []
    for split_bits in split_bits_list:
        encode_bits = hamming7_4_encode(split_bits)
        error_bits = add_error(encode_bits)

        str_encode = ''.join(str(x) for x in error_bits)
        enc_msg.append(str_encode)

    encoded = ''.join(enc_msg)
    with open("encrypt.txt", "w", encoding="utf-8") as f:
        f.write(encoded)

    return enc_msg


def decode(encode_msg):
    decode_msg = []
    for encode_bits in encode_msg:
        encode_bits = np.array([int(x) for x in encode_bits])
        c_hat = np.mod(encode_bits.dot(P_inv), 2)
        error_idx = detect_error(c_hat)
        flip_bit(c_hat, error_idx)
        m_hat = hamming7_4_decode(c_hat)
        m_out = np.mod(m_hat.dot(S_inv), 2)

        str_dec = ''.join(str(x) for x in m_out)
        decode_msg.append(str_dec)

    decode_msg_str = ''.join(decode_msg)

    return decode_msg_str


if __name__ == '__main__':
    text = read_text("input.txt")
    print(f"DATA:\n{text}")
    print('#' * 150)

    result = [text[0]]

    encode_msg = encode(text[1])
    
    print(f"ENCRYPTED DATA:\n{encode_msg}")
    print('#' * 150)
    decode_msg = decode(encode_msg)

    txt = bits_to_str(decode_msg)
    result.append(txt)

    print(f"DECRYPTED DATA:\n{result} ")
    write_text("decoded.txt", result)
