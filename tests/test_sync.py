"""Tests for haul/sync.py"""

import os
import pytest
from haul.sync import file_checksum, files_differ, sync_file, sync_all


@pytest.fixture
def tmp_files(tmp_path):
    src = tmp_path / "src" / ".bashrc"
    dst = tmp_path / "repo" / ".bashrc"
    src.parent.mkdir(parents=True)
    dst.parent.mkdir(parents=True)
    src.write_text("export PATH=$PATH:/usr/local/bin\n")
    return str(src), str(dst)


def test_file_checksum_returns_string(tmp_files):
    src, _ = tmp_files
    result = file_checksum(src)
    assert isinstance(result, str) and len(result) == 32


def test_file_checksum_returns_none_for_missing():
    assert file_checksum("/nonexistent/path/.bashrc") is None


def test_files_differ_same_content(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("hello")
    b.write_text("hello")
    assert not files_differ(str(a), str(b))


def test_files_differ_different_content(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("hello")
    b.write_text("world")
    assert files_differ(str(a), str(b))


def test_sync_file_copies(tmp_files):
    src, dst = tmp_files
    status = sync_file(src, dst)
    assert status == "copied"
    assert open(dst).read() == open(src).read()


def test_sync_file_skips_identical(tmp_files):
    src, dst = tmp_files
    sync_file(src, dst)
    status = sync_file(src, dst)
    assert status == "skipped"


def test_sync_file_dry_run(tmp_files):
    src, dst = tmp_files
    status = sync_file(src, dst, dry_run=True)
    assert status == "dry_run"
    assert not os.path.exists(dst)


def test_sync_file_raises_for_missing_src(tmp_path):
    with pytest.raises(FileNotFoundError):
        sync_file("/no/such/file", str(tmp_path / "dst"))


def test_sync_all(tmp_path):
    src_dir = tmp_path / "home"
    repo_dir = tmp_path / "repo"
    src_dir.mkdir()
    (src_dir / ".vimrc").write_text("set number\n")
    dotfiles = [{"name": ".vimrc", "src": str(src_dir / ".vimrc")}]
    results = sync_all(dotfiles, str(repo_dir))
    assert len(results) == 1
    assert results[0]["status"] == "copied"
    assert (repo_dir / ".vimrc").exists()
