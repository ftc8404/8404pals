import os
import hashlib

while True:
    password = input()
    salt = os.urandom(32)
    hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode('utf-8'), salt, 100000, dklen=64)
    print("hash: 0x" + hash.hex())
    print("salt: 0x" + salt.hex())
    print()
