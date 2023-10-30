from consts import *
from utils import *


class STB:
    subkeys = []

    def __init__(self, key):
        self.init_8_subkeys(key)

        self.clock_keys = []
        for _ in range(8):
            self.clock_keys.extend(self.subkeys)

    def init_8_subkeys(self, key: int):
        count = self.get_key_chunks_counts(key)
        self.generate_subkeys_from_key(key, count)
        self.extend_subkeys_if_needed(count)

    def generate_subkeys_from_key(self, key: int, count: int):
        for i in range(count):
            self.subkeys.append(key & 0xFFFF)
            key >>= 32

    def extend_subkeys_if_needed(self, count: int):
        if count == 4:
            self.subkeys.extend(self.subkeys)
        elif count == 6:
            self.subkeys.extend([
                self.subkeys[0] ^ self.subkeys[1] ^ self.subkeys[2],
                self.subkeys[3] ^ self.subkeys[4] ^ self.subkeys[5]
            ])

    @staticmethod
    def get_key_chunks_counts(key: int):
        key_length = len(bin(key)[2:])
        key_length &= (1 << 256) - 1
        if 256 >= key_length > 192:
            return 8
        elif 192 >= key_length > 128:
            return 6
        elif key_length <= 128:
            return 4

    def G(self, r, word):
        mask = (1 << 8) - 1
        final = 0
        for i in range(4):
            part = word & mask
            word >>= 8
            r = part & 0x0F
            l = (part & 0xF0) >> 4
            result = H[l][r]
            result <<= 8 * i
            final += result

        return rot_hi_r(final, r)

    def encrypt_block(self, block):
        if self.get_key_chunks_counts(block) != 4:
            raise ValueError()

        # block (128 bit) = a | b | c | d
        d = block & 0xFFFFFFFF
        block >>= 32

        c = block & 0xFFFFFFFF
        block >>= 32

        b = block & 0xFFFFFFFF
        block >>= 32

        a = block
        ##################################

        for i in range(1, 9):
            b = b ^ self.G(5, sum_modul(a, self.clock_keys[7 * i - 7]))
            c = c ^ self.G(21, sum_modul(d, self.clock_keys[7 * i - 6]))
            a = sub_modul(a, self.G(13, sum_modul(b, self.clock_keys[7 * i - 5])))
            e = self.G(21, sum_modul(sum_modul(b, c), self.clock_keys[7 * i - 4])) ^ (i % (2 ** 32))
            b = sum_modul(b, e)
            c = sub_modul(c, e)
            d = sum_modul(d, self.G(13, sum_modul(c, self.clock_keys[7 * i - 3])))
            b = b ^ self.G(21, sum_modul(a, self.clock_keys[7 * i - 2]))
            c = c ^ self.G(5, sum_modul(d, self.clock_keys[7 * i - 1]))
            a, b = b, a
            c, d = d, c
            b, c = c, b

        return (b << 96) + (d << 64) + (a << 32) + c

    def decrypt_block(self, X):
        if self.get_key_chunks_counts(X) != 4:
            raise ValueError()
        d = X & 0xFFFFFFFF
        X >>= 32
        c = X & 0xFFFFFFFF
        X >>= 32
        b = X & 0xFFFFFFFF
        X >>= 32
        a = X

        for i in range(8, 0, -1):
            b = b ^ self.G(5, sum_modul(a, self.clock_keys[7 * i - 1]))
            c = c ^ self.G(21, sum_modul(d, self.clock_keys[7 * i - 2]))
            a = sub_modul(a, self.G(13, sum_modul(b, self.clock_keys[7 * i - 3])))
            e = self.G(21, sum_modul(sum_modul(b, c), self.clock_keys[7 * i - 4])) ^ (i % (2 ** 32))
            b = sum_modul(b, e)
            c = sub_modul(c, e)
            d = sum_modul(d, self.G(13, sum_modul(c, self.clock_keys[7 * i - 5])))
            b = b ^ self.G(21, sum_modul(a, self.clock_keys[7 * i - 6]))
            c = c ^ self.G(5, sum_modul(d, self.clock_keys[7 * i - 7]))
            a, b = b, a
            c, d = d, c
            a, d = d, a

        return (c << 96) + (a << 64) + (d << 32) + b

    def encrypt_block_coupled(self, chunks, synchro: int):
        results = []

        for chunk in chunks:
            encrypted_chunk = self.encrypt_block(chunk ^ synchro)
            results.append(encrypted_chunk)
            synchro = encrypted_chunk

        return results

    def decrypt_block_coupled(self, chunks, synchro: int):
        results = []

        for chunk in chunks:
            decrypted_chunk = self.decrypt_block(chunk) ^ synchro
            results.append(decrypted_chunk)
            synchro = chunk

        return results

    def encrypt(self, message: str, synchro: int):
        plain_msg = int.from_bytes(message.encode(), 'big')
        chunks = split_message(plain_msg)
        results = self.encrypt_block_coupled(chunks, synchro)
        answer = join_chunks(results)

        return answer.to_bytes((answer.bit_length() + 7) // 8, 'big')

    def decrypt(self, message: bytes, synchro: int):
        plain_msg = int.from_bytes(message, 'big')
        chunks = reversed(split_message(plain_msg))
        results = self.decrypt_block_coupled(chunks, synchro)
        answer = join_chunks(reversed(results))

        return answer.to_bytes((answer.bit_length() + 7) // 8, 'big').decode()
