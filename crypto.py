import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from argon2.low_level import hash_secret_raw, Type

def derive_key(password: str, salt: bytes):
    return hash_secret_raw(
        password.encode(),
        salt,
        time_cost=2,
        memory_cost=102400,
        parallelism=8,
        hash_len=32,
        type=Type.I
    )

def encrypt_data(key, data: bytes):
    aes = AESGCM(key)
    nonce = os.urandom(12)
    encrypted = aes.encrypt(nonce, data, None)
    return nonce + encrypted

def decrypt_data(key, encrypted_data: bytes):
    aes = AESGCM(key)
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]
    return aes.decrypt(nonce, ciphertext, None)