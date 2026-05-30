import json, os
from crypto import derive_key, encrypt_data, decrypt_data

VAULT_FILE = "vault.json"

def create_vault(master_password):
    salt = os.urandom(16)
    key = derive_key(master_password, salt)
    empty_data = encrypt_data(key, b"{}")

    with open(VAULT_FILE, "wb") as f:
        f.write(salt + empty_data)

def load_vault(master_password):
    with open(VAULT_FILE, "rb") as f:
        data = f.read()

    salt = data[:16]
    encrypted = data[16:]
    key = derive_key(master_password, salt)

    decrypted = decrypt_data(key, encrypted)
    return json.loads(decrypted), key, salt

def save_vault(vault_data, key, salt):
    encrypted = encrypt_data(key, json.dumps(vault_data).encode())
    with open(VAULT_FILE, "wb") as f:
        f.write(salt + encrypted)