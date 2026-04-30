"""Tests for haul/encryption.py"""

import json
import pytest
from pathlib import Path
from haul.encryption import (
    load_encryption_config,
    save_encryption_config,
    mark_encrypted,
    unmark_encrypted,
    is_marked_encrypted,
    encrypt_content,
    decrypt_content,
    list_encrypted_files,
)


@pytest.fixture
def enc_config(tmp_path):
    return str(tmp_path / "encryption.json")


def test_load_encryption_config_returns_defaults_when_no_file(enc_config):
    config = load_encryption_config(enc_config)
    assert config == {"encrypted_files": []}


def test_load_encryption_config_handles_corrupt_file(enc_config):
    Path(enc_config).parent.mkdir(parents=True, exist_ok=True)
    Path(enc_config).write_text("not valid json")
    config = load_encryption_config(enc_config)
    assert config == {"encrypted_files": []}


def test_save_and_load_encryption_config(enc_config):
    data = {"encrypted_files": ["/home/user/.bashrc"]}
    save_encryption_config(data, enc_config)
    loaded = load_encryption_config(enc_config)
    assert loaded == data


def test_mark_encrypted_adds_file(enc_config):
    result = mark_encrypted("/home/user/.ssh/config", enc_config)
    assert result is True
    assert is_marked_encrypted("/home/user/.ssh/config", enc_config)


def test_mark_encrypted_returns_false_if_already_marked(enc_config):
    mark_encrypted("/home/user/.netrc", enc_config)
    result = mark_encrypted("/home/user/.netrc", enc_config)
    assert result is False


def test_unmark_encrypted_removes_file(enc_config):
    mark_encrypted("/home/user/.aws/credentials", enc_config)
    result = unmark_encrypted("/home/user/.aws/credentials", enc_config)
    assert result is True
    assert not is_marked_encrypted("/home/user/.aws/credentials", enc_config)


def test_unmark_encrypted_returns_false_if_not_marked(enc_config):
    result = unmark_encrypted("/home/user/.bashrc", enc_config)
    assert result is False


def test_list_encrypted_files(enc_config):
    mark_encrypted("/home/user/.netrc", enc_config)
    mark_encrypted("/home/user/.ssh/config", enc_config)
    files = list_encrypted_files(enc_config)
    assert "/home/user/.netrc" in files
    assert "/home/user/.ssh/config" in files


def test_encrypt_decrypt_roundtrip():
    original = b"supersecret dotfile content"
    passphrase = "mypassword"
    encrypted = encrypt_content(original, passphrase)
    assert encrypted != original
    decrypted = decrypt_content(encrypted, passphrase)
    assert decrypted == original


def test_encrypt_different_passphrases_produce_different_output():
    content = b"some content"
    enc1 = encrypt_content(content, "pass1")
    enc2 = encrypt_content(content, "pass2")
    assert enc1 != enc2


def test_decrypt_wrong_passphrase_gives_wrong_result():
    original = b"secret"
    encrypted = encrypt_content(original, "correct")
    decrypted = decrypt_content(encrypted, "wrong")
    assert decrypted != original
