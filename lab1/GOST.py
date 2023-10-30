class GOST:

    BLOCK_SIZE: int = 64
    SUBBLOCK_SIZE: int = 32
    ENCODING: str = 'utf-8'
    MAIN_256_BIT_KEY: str = '_SUPER_SECRET_RELIABLE_GOST_KEY_'
    ITERATIONS_COUNT: int = 32
    SUBKEY_COUNT: int = 8

    TABLE: list = [
        [0xF, 0xC, 0x2, 0xA, 0x6, 0x4, 0x5, 0x0,
         0x7, 0x9, 0xE, 0xD, 0x1, 0xB, 0x8, 0x3],
        [0xB, 0x6, 0x3, 0x4, 0xC, 0xF, 0xE, 0x2,
         0x7, 0xD, 0x8, 0x0, 0x5, 0xA, 0x9, 0x1],
        [0x1, 0xC, 0xB, 0x0, 0xF, 0xE, 0x6, 0x5,
         0xA, 0xD, 0x4, 0x8, 0x9, 0x3, 0x7, 0x2],
        [0x1, 0x5, 0xE, 0xC, 0xA, 0x7, 0x0, 0xD,
         0x6, 0x2, 0xB, 0x4, 0x9, 0x3, 0xF, 0x8],
        [0x0, 0xC, 0x8, 0x9, 0xD, 0x2, 0xA, 0xB,
         0x7, 0x3, 0x6, 0x5, 0x4, 0xE, 0xF, 0x1],
        [0x8, 0x0, 0xF, 0x3, 0x2, 0x5, 0xE, 0xB,
         0x1, 0xA, 0x4, 0x7, 0xC, 0x9, 0xD, 0x6],
        [0x3, 0x0, 0x6, 0xF, 0x1, 0xE, 0x9, 0x2,
         0xD, 0x8, 0xC, 0x4, 0xB, 0xA, 0x5, 0x7],
        [0x1, 0xA, 0x6, 0x8, 0xF, 0xB, 0x0, 0x4,
         0xC, 0x3, 0x5, 0x9, 0x7, 0xD, 0x2, 0xE]
    ]

    class GostBlock:
        def __init__(self, block_64: str):
            half_block_size: int = int(GOST.BLOCK_SIZE / 2)
            self.block_64 = int(block_64, 2)
            self.left_subblock = int(block_64[:half_block_size], 2)
            self.right_subblock = int(block_64[half_block_size:], 2)

        def get_block64(self):
            return self.block_64

        def get_left(self):
            return self.left_subblock

        def get_right(self):
            return self.right_subblock

        def set_subblocks(self, left, right):
            self.left = left
            self.right = right

        def get_binary_block_data(self):
            right = self.__get_binary_subblock_data__(self.get_right())
            left = self.__get_binary_subblock_data__(self.get_left())

            return right + left

        def get_text_block_data(self):
            right = self.__convert_subblock_to_text__(self.get_right())
            left = self.__convert_subblock_to_text__(self.get_left())

            return right + left

        def __get_binary_subblock_data__(self, subblock: int):
            return bin(subblock)[2:].zfill(GOST.SUBBLOCK_SIZE)

        def __convert_subblock_to_text__(self, subblock: int):
            try:
                return bytes.fromhex(hex(subblock)[2:]).decode(GOST.ENCODING)
            except:
                return ''

    def encrypt_text(self, data_str: str):
        binary_data = bin(self.__convert_string_to_integer__(data_str))[2:]
        return self.encrypt_binary_data(binary_data)

    def encrypt_integer_data(self, integer_data: int):
        binary_data = bin(integer_data)[2:]
        return self.encrypt_binary_data(binary_data)

    def encrypt_binary_data(self, binary_data: str):
        self.data = binary_data
        self.__init_data_length__()
        self.__init_subkeys__()
        encrypted_data = ''
        for i in range(0, self.length, self.BLOCK_SIZE):
            self.__init_subblocks__(i)

            for round_iteration in range(self.ITERATIONS_COUNT - self.SUBKEY_COUNT):
                self.__crypt_round__(round_iteration % self.SUBKEY_COUNT)

            for round_iteration in range(self.SUBKEY_COUNT):
                self.__crypt_round__(self.SUBKEY_COUNT - 1 - round_iteration)

            encrypted_data += self.block.get_binary_block_data()

        return encrypted_data

    def decrypt(self, encrypted_data: int):
        self.data = encrypted_data
        self.__init_data_length__()
        self.__init_subkeys__()
        decrypted_data = ''
        for i in range(0, self.length, self.BLOCK_SIZE):
            self.__init_subblocks__(i)

            for round_iteration in range(self.SUBKEY_COUNT):
                self.__crypt_round__(round_iteration)

            for round_iteration in range(self.ITERATIONS_COUNT - self.SUBKEY_COUNT):
                self.__crypt_round__(self.SUBKEY_COUNT -
                                     1 - round_iteration % self.SUBKEY_COUNT)

            decrypted_data += self.block.get_text_block_data()

        return self.data

    def __init_data_length__(self):
        self.length = self.__get_data_length__(self.data)
        self.data = self.data.zfill(self.length)

    def __get_data_length__(self, data):
        length = len(data)
        if length % self.BLOCK_SIZE != 0:
            length += (self.BLOCK_SIZE - (length % self.BLOCK_SIZE))

        return length

    def __crypt_round__(self, key_index):
        subkey = self.subkeys[key_index]
        res = (self.block.get_left() + subkey) % (1 << 32)

        res = self.__substitution_table__(res, key_index)
        res = self.__cyclic_left_shift__(res, 11, 32)
        res = res
        self.block.get_right()

        self.block.set_subblocks(res, self.block.get_left())

    def __substitution_table__(self, block_32: int, key_index: int):
        binary_block = bin(block_32)[2:].zfill(self.SUBBLOCK_SIZE)
        blocks = []
        for i in range(8):
            value = binary_block[i * 4:(i + 1) * 4]
            new_value = self.TABLE[key_index][int(value, 2)]
            blocks.append(bin(new_value)[2:].zfill(4))

        substituted_block = ''.join(blocks)

        return int(substituted_block, 2)

    def __cyclic_left_shift__(self, binary_number, shift_amount, length):
        shifted_number = (binary_number << shift_amount) | (
                binary_number >> (length - shift_amount))
        shifted_number &= (2 ** length - 1)

        return shifted_number

    def __init_subblocks__(self, block_index: int):
        left_index = block_index
        right_index = block_index + self.BLOCK_SIZE

        block: str = self.data[left_index:right_index]

        self.block = self.GostBlock(block)

    def __init_subkeys__(self):
        self.subkeys = [None] * self.SUBKEY_COUNT
        for i in range(self.SUBKEY_COUNT):
            self.subkeys[i] = int(
                self.MAIN_256_BIT_KEY[i * 4:(i + 1) * 4].encode(self.ENCODING).hex(), 16)

    def __convert_string_to_integer__(self, string: str):
        return int(string.encode(self.ENCODING).hex(), 16)

    def gamma_encrypt_text(self, data_str: str):
        length = len(data_str)
        if length % 8 != 0:
            length += (8 - (length % 8))
        self.offset = length - len(data_str)
        data_str = data_str.ljust(length, '.')
        binary_data = bin(self.__convert_string_to_integer__(data_str))[2:]
        return self.gamma_encrypt_binary_data(binary_data)

    def gamma_encrypt_binary_data(self, binary_data: str):
        synchromessage = 0x7777150820037777
        data = binary_data
        length = self.__get_data_length__(data)
        data.zfill(length)
        prev_gamma = synchromessage
        encrypted_data = ''
        block = int(data[0:self.BLOCK_SIZE], 2)
        gamma = prev_gamma
        prev_gamma = int(self.encrypt_integer_data(gamma), 2)
        encrypted_block = gamma ^ block
        encrypted_data += bin(encrypted_block)[2:]

        for i in range(self.BLOCK_SIZE, length, self.BLOCK_SIZE):
            block = int(data[i:(i + self.BLOCK_SIZE)], 2)
            gamma = prev_gamma
            prev_gamma = int(self.encrypt_integer_data(gamma), 2)
            encrypted_block = gamma ^ block
            encrypted_data += bin(encrypted_block)[2:]

        return encrypted_data

    def gamma_decrypt(self, encrypted_data: str):
        decrypted_data = self.gamma_encrypt_binary_data(encrypted_data)
        decrypted_text_data = bytes.fromhex(hex(int(decrypted_data, 2))[2:]).decode(self.ENCODING)
        size = len(decrypted_text_data)
        result = decrypted_text_data[:size - self.offset]
        return result
