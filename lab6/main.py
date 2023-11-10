import gostcrypto
from lab5.GOST3411.GOST3411 import GOST3411

message = input("Enter your message:\n")

hash_result = GOST3411().hash(message, 256)

# SIGNING

private_key = bytearray.fromhex('7a929ade789bb9be10ed359dd39a72c11b60961f49397eee1d19ce9891ec3b28')

digest = bytearray.fromhex(hash_result)

sign_obj = gostcrypto.gostsignature.new(gostcrypto.gostsignature.MODE_256,
                                        gostcrypto.gostsignature.CURVES_R_1323565_1_024_2019[
                                            'id-tc26-gost-3410-2012-256-paramSetB'])

signature = sign_obj.sign(private_key, digest)
print(signature)

# VERIFY

public_key = bytearray.fromhex(
    'fd21c21ab0dc84c154f3d218e9040bee64fff48bdff814b232295b09d0df72e45026dec9ac4f07061a2a01d7a2307e0659239a82a95862df86041d1458e45049')

if sign_obj.verify(public_key, digest, signature):
    print('Signature is correct')
else:
    print('Signature is not correct')
