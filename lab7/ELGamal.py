from ec import ECPoint


class ElGamal:

    def __init__(self, p, a, b, p_x, p_y):
        self.p_point = ECPoint(p_x, p_y, a, b, p)
        self.a = a
        self.b = b
        self.p = p

    def gen_keys(self, k):
        q_point = k * self.p_point
        return q_point

    def encrypt(self, m, r, qa):
        s = m * self.p_point

        c1 = r * self.p_point

        c2 = r * qa
        c2 = c2 + s

        return c1, c2

    def decrypt(self, c1, c2, ka):
        c1_prime = ECPoint(c1.x, (-1 * c1.y) % self.p, self.a, self.b, self.p)
        s_prime = ka * c1_prime
        s_prime = c2 + s_prime
        return s_prime
