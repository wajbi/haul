"""Tests for haul/status.py"""

import pytest
from pathlib import Path
from haul.status import (
    file_status,
    status_all,
    format_status_line,
    STATUS_SYNCED,
    STATUS_MODIFIED,
    STATUS_MISSING_SOURCE,
    STATUS_MISSING_DEST,
)


@pytest.fixture
def tmp_files(tmp_path):
    src = tmp_path / "source.txt"
    dst = tmp_path / "dest.txt"
    src.write_text("hello world")
    dst.write_text("hello world")
    return str(src), str(dst)


def test_file_status_synced(tmp_files):
    src, dst = tmp_files
    assert file_status(src, dst) == STATUS_SYNCED


def test_file_status_modified(tmp_files):
    src, dst = tmp_files
    Path(dst).write_text("different content")
    assert file_status(src, dst) == STATUS_MODIFIED


def test_file_status_missing_source(tmp_files):
    src, dst = tmp_files
    Path(src).unlink()
    assert file_status(src, dst) == STATUS_MISSING_SOURCE


def test_file_status_missing_dest(tmp_files):
    src, dst = tmp_files
    Path(dst).unlink()
    assert file_status(src, dst) == STATUS_MISSING_DEST


def test_status_all_returns_list(tmp_files):
    src, dst = tmp_files
    files = [{"source": src, "dest": dst}]
    results = status_all(files)
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["status"] == STATUS_SYNCED


def test_status_all_tuple_entries(tmp_files):
    src, dst = tmp_files
    results = status_all([(src, dst)])
    assert results[0]["source"] == src
    assert results[0]["dest"] == dst


def test_status_all_empty():
    assert status_all([]) == []


def test_format_status_line_synced(tmp_files):
    src, dst = tmp_files
    entry = {"source": src, "dest": dst, "status": STATUS_SYNCED}
    line = format_status_line(entry)
    assert "✓" in line
    assert STATUS_SYNCED in line


def test_format_status_line_modified(tmp_files):
    src, dst = tmp_files
    entry = {"source": src, "dest": dst, "status": STATUS_MODIFIED}
    line = format_status_line(entry)
    assert "~" in line
