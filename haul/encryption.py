"""Simple encryption support for sensitive dotfiles."""

import os
import json
import base64
import hashlib
from pathlib import Path

ENCRYPTION_CONFIG_FILE = os.path.expanduser("~/.haul/encryption.json")


def _derive_key(passphrase: str) -> bytes:
    """Derive a 32-byte key from a passphrase using SHA-256."""
    return hashlib.sha256(passphrase.encode()).digest()


def load_encryption_config(config_path: str = ENCRYPTION_CONFIG_FILE) -> dict:
    """Load the list of files marked for encryption."""
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"encrypted_files": []}
    except (json.JSONDecodeError, ValueError):
        return {"encrypted_files": []}


def save_encryption_config(data: dict, config_path: str = ENCRYPTION_CONFIG_FILE) -> None:
    """Save the encryption config to disk."""
    Path(config_path).parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(data, f, indent=2)


def mark_encrypted(filepath: str, config_path: str = ENCRYPTION_CONFIG_FILE) -> bool:
    """Mark a file as requiring encryption. Returns False if already marked."""
    config = load_encryption_config(config_path)
    if filepath in config["encrypted_files"]:
        return False
    config["encrypted_files"].append(filepath)
    save_encryption_config(config, config_path)
    return True


def unmark_encrypted(filepath: str, config_path: str = ENCRYPTION_CONFIG_FILE) -> bool:
    """Remove encryption mark from a file. Returns False if not marked."""
    config = load_encryption_config(config_path)
    if filepath not in config["encrypted_files"]:
        return False
    config["encrypted_files"].remove(filepath)
    save_encryption_config(config, config_path)
    return True


def is_marked_encrypted(filepath: str, config_path: str = ENCRYPTION_CONFIG_FILE) -> bool:
    """Check if a file is marked for encryption."""
    config = load_encryption_config(config_path)
    return filepath in config["encrypted_files"]


def encrypt_content(content: bytes, passphrase: str) -> bytes:
    """XOR-encrypt content with a derived key and return base64-encoded result."""
    key = _derive_key(passphrase)
    encrypted = bytes(b ^ key[i % len(key)] for i, b in enumerate(content))
    return base64.b64encode(encrypted)


def decrypt_content(encoded: bytes, passphrase: str) -> bytes:
    """Decode base64 and XOR-decrypt content with a derived key."""
    key = _derive_key(passphrase)
    encrypted = base64.b64decode(encoded)
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(encrypted))


def list_encrypted_files(config_path: str = ENCRYPTION_CONFIG_FILE) -> list:
    """Return list of files marked for encryption."""
    return load_encryption_config(config_path)["encrypted_files"]
