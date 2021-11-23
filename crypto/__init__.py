from cryptography.fernet import Fernet
import os

key_path = f'{os.curdir}{os.sep}crypto{os.sep}key'

# Load existing key if exists, otherwise create a new one.
try:
    with open(key_path, 'rb') as f:
        key = f.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open(key_path, 'wb+') as f:
        f.write(key)

fernet = Fernet(key)


def encrypt(data: bytes) -> bytes:
    """Encrypts data using Fernet."""
    return fernet.encrypt(data)
