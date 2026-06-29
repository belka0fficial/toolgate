import base64
from cryptography.fernet import Fernet
from hashlib import sha256
from app.core.config import TOOLGATE_MASTER_KEY

def _build_fernet() -> Fernet:
    key = base64.urlsafe_b64encode(sha256(TOOLGATE_MASTER_KEY.encode()).digest())
    return Fernet(key)

def encrypt_value(value: str) -> str:
    return _build_fernet().encrypt(value.encode()).decode()

def decrypt_value(value: str) -> str:
    return _build_fernet().decrypt(value.encode()).decode()
