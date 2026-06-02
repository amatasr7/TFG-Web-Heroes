from __future__ import annotations

import hashlib
import hmac
import secrets

PBKDF2_ITERATIONS = 200_000
HASH_NAME = "sha256"
SALT_SIZE = 16


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(SALT_SIZE)
    derived_key = hashlib.pbkdf2_hmac(HASH_NAME, password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return f"{salt.hex()}${derived_key.hex()}"


def verify_password(password: str, stored_password: str) -> bool:
    try:
        salt_hex, hash_hex = stored_password.split("$", 1)
    except ValueError:
        return False

    salt = bytes.fromhex(salt_hex)
    expected_key = bytes.fromhex(hash_hex)
    derived_key = hashlib.pbkdf2_hmac(HASH_NAME, password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return hmac.compare_digest(derived_key, expected_key)
