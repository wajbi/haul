"""Tests for haul/conflicts.py"""

import os
import pytest
from haul.conflicts import detect_conflict, backup_file, resolve_conflict, list_conflicts


@pytest.fixture
def tmp_files(tmp_path):
    src = tmp_path / "source.txt"
    dst = tmp_path / "dest.txt"
    src.write_text("source content")
    dst.write_text("dest content")
    return str(src), str(dst)


@pytest.fixture
def identical_files(tmp_path):
    src = tmp_path / "source.txt"
    dst = tmp_path / "dest.txt"
    src.write_text("same content")
    dst.write_text("same content")
    return str(src), str(dst)


def test_detect_conflict_different_content(tmp_files):
    src, dst = tmp_files
    assert detect_conflict(src, dst) is True


def test_detect_conflict_same_content(identical_files):
    src, dst = identical_files
    assert detect_conflict(src, dst) is False


def test_detect_conflict_missing_source(tmp_files):
    _, dst = tmp_files
    assert detect_conflict("/nonexistent/path.txt", dst) is False


def test_detect_conflict_missing_dest(tmp_files):
    src, _ = tmp_files
    assert detect_conflict(src, "/nonexistent/path.txt") is False


def test_backup_file_creates_backup(tmp_files, tmp_path):
    src, dst = tmp_files
    backup_dir = str(tmp_path / "backups")
    backup_path = backup_file(dst, backup_dir=backup_dir)
    assert os.path.exists(backup_path)
    assert open(backup_path).read() == "dest content"


def test_resolve_conflict_strategy_source(tmp_files):
    src, dst = tmp_files
    result = resolve_conflict(src, dst, strategy="source")
    assert result["winner"] == "source"
    assert open(dst).read() == "source content"


def test_resolve_conflict_strategy_dest(tmp_files):
    src, dst = tmp_files
    result = resolve_conflict(src, dst, strategy="dest")
    assert result["winner"] == "dest"
    assert open(src).read() == "dest content"


def test_resolve_conflict_strategy_backup(tmp_files, tmp_path):
    src, dst = tmp_files
    backup_dir = str(tmp_path / "backups")
    # monkeypatch backup dir isn't needed — we test via direct call
    result = resolve_conflict.__wrapped__(src, dst, strategy="backup") if hasattr(resolve_conflict, "__wrapped__") else resolve_conflict(src, dst, strategy="backup")
    assert result["action"] == "backup_and_overwrite"
    assert open(dst).read() == "source content"


def test_resolve_conflict_invalid_strategy(tmp_files):
    src, dst = tmp_files
    with pytest.raises(ValueError, match="Unknown conflict strategy"):
        resolve_conflict(src, dst, strategy="magic")


def test_list_conflicts_returns_only_conflicting(tmp_files, identical_files):
    pairs = [tmp_files, identical_files]
    conflicts = list_conflicts(pairs)
    assert len(conflicts) == 1
    assert conflicts[0] == tmp_files
