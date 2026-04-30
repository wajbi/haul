"""Tests for haul/remotes.py."""

import json
import pytest
from pathlib import Path
from haul.remotes import (
    load_remotes,
    save_remotes,
    add_remote,
    remove_remote,
    get_remote,
    list_remotes,
    update_remote,
)


@pytest.fixture
def remotes_file(tmp_path):
    return str(tmp_path / "remotes.json")


def test_load_remotes_returns_empty_when_no_file(remotes_file):
    result = load_remotes(remotes_file)
    assert result == {}


def test_load_remotes_handles_corrupt_file(remotes_file):
    Path(remotes_file).parent.mkdir(parents=True, exist_ok=True)
    Path(remotes_file).write_text("not json")
    result = load_remotes(remotes_file)
    assert result == {}


def test_save_and_load_remotes(remotes_file):
    data = {"origin": {"url": "git@github.com:user/dots.git", "branch": "main"}}
    save_remotes(remotes_file, data)
    loaded = load_remotes(remotes_file)
    assert loaded == data


def test_add_remote_stores_data(remotes_file):
    info = add_remote(remotes_file, "origin", "git@github.com:user/dots.git")
    assert info["url"] == "git@github.com:user/dots.git"
    assert info["branch"] == "main"
    remotes = load_remotes(remotes_file)
    assert "origin" in remotes


def test_add_remote_custom_branch(remotes_file):
    info = add_remote(remotes_file, "backup", "https://example.com/repo.git", branch="dev")
    assert info["branch"] == "dev"


def test_add_remote_raises_on_duplicate(remotes_file):
    add_remote(remotes_file, "origin", "https://example.com/a.git")
    with pytest.raises(ValueError, match="already exists"):
        add_remote(remotes_file, "origin", "https://example.com/b.git")


def test_remove_remote_returns_true(remotes_file):
    add_remote(remotes_file, "origin", "https://example.com/repo.git")
    assert remove_remote(remotes_file, "origin") is True
    assert get_remote(remotes_file, "origin") is None


def test_remove_remote_returns_false_when_missing(remotes_file):
    assert remove_remote(remotes_file, "ghost") is False


def test_get_remote_returns_none_for_missing(remotes_file):
    assert get_remote(remotes_file, "nope") is None


def test_list_remotes_returns_all(remotes_file):
    add_remote(remotes_file, "origin", "https://example.com/a.git")
    add_remote(remotes_file, "backup", "https://example.com/b.git", branch="dev")
    items = list_remotes(remotes_file)
    names = [n for n, _ in items]
    assert "origin" in names
    assert "backup" in names


def test_update_remote_url(remotes_file):
    add_remote(remotes_file, "origin", "https://old.example.com/repo.git")
    info = update_remote(remotes_file, "origin", url="https://new.example.com/repo.git")
    assert info["url"] == "https://new.example.com/repo.git"
    assert info["branch"] == "main"


def test_update_remote_raises_when_missing(remotes_file):
    with pytest.raises(KeyError):
        update_remote(remotes_file, "ghost", url="https://example.com")
