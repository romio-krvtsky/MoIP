def rot_hi(u):
    if u < 1 << 31:
        return (2 * u) % (1 << 32)
    else:
        return (2 * u + 1) % (1 << 32)


def rot_hi_r(u, r):
    result = u
    for i in range(r):
        result = rot_hi(result)
    return result


def sum_modul(u, v):
    return (u + v) % (1 << 32)


def sub_modul(u, v):
    return (u - v) % (1 << 32)


def split_message(message):
    chunks = []
    while message:
        chunk = message & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        chunks.append(chunk)
        message >>= 128
    return chunks


def join_chunks(chunks):
    answer = 0
    for chunk in chunks:
        answer <<= 128
        answer += chunk
    return answer
