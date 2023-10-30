import random
import numpy as np

H = np.array([[1, 0, 1, 0, 1, 0, 1],
              [0, 1, 1, 0, 0, 1, 1],
              [0, 0, 0, 1, 1, 1, 1]])

G = np.array([[1, 1, 0, 1],
              [1, 0, 1, 1],
              [1, 0, 0, 0],
              [0, 1, 1, 1],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, 1]])

R = np.array([[0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0],
              [0, 0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 0, 1]])


def random_binary_non_singular_matrix(n):
    while True:
        a = np.random.randint(0, 2, size=(n, n))

        if np.linalg.det(a) != 0:
            return a


S = random_binary_non_singular_matrix(4)
S_inv = np.linalg.inv(S).astype(int)


def generate_permutation_matrix(n):
    i = np.eye(n)
    p = np.random.permutation(i)
    return p.astype(int)


P = generate_permutation_matrix(7)
P_inv = np.linalg.inv(P).astype(int)

G_hat = np.transpose(np.mod((S.dot(np.transpose(G))).dot(P), 2))


def detect_error(err_enc_bits):
    err_idx_vec = np.mod(H.dot(err_enc_bits), 2)
    err_idx_vec = err_idx_vec[::-1]
    err_idx = int(''.join(str(bit) for bit in err_idx_vec), 2)
    return err_idx - 1


def hamming7_4_encode(p_str):
    p = np.array([int(x) for x in p_str])
    prod = np.mod(G_hat.dot(p), 2)
    return prod


def hamming7_4_decode(c):
    prod = np.mod(R.dot(c), 2)
    return prod


def flip_bit(bits, n):
    bits[n] = (bits[n] + 1) % 2


def add_error(enc_bits):
    error = [0] * 7
    idx = random.randint(0, 6)
    error[idx] = 1
    return np.mod(enc_bits + error, 2)


def split_binary_string(string, n):
    return [string[i:i + n] for i in range(0, len(string), n)]


def bits_to_str(bits):
    chunks = [bits[i:i + 8] for i in range(0, len(bits), 8)]

    chars = [chr(int(chunk, 2)) for chunk in chunks]

    text = ''.join(chars)

    return text
