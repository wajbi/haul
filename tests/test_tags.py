"""Tests for haul/tags.py and basic CLI tag commands."""

import pytest
from click.testing import CliRunner
from haul.tags import (
    load_tags,
    save_tags,
    add_tag,
    remove_tag,
    get_files_for_tag,
    get_tags_for_file,
    delete_tag,
)
from haul.cli_tags import tags_cmd


@pytest.fixture
def tags_file(tmp_path):
    return tmp_path / "tags.json"


def test_load_tags_returns_empty_when_no_file(tags_file):
    result = load_tags(tags_file)
    assert result == {}


def test_load_tags_handles_corrupt_file(tags_file):
    tags_file.write_text("not json")
    result = load_tags(tags_file)
    assert result == {}


def test_save_and_load_tags(tags_file):
    data = {"shell": [".bashrc", ".zshrc"]}
    save_tags(data, tags_file)
    loaded = load_tags(tags_file)
    assert loaded == data


def test_add_tag_creates_tag(tags_file):
    add_tag("editor", ".vimrc", tags_file)
    tags = load_tags(tags_file)
    assert "editor" in tags
    assert ".vimrc" in tags["editor"]


def test_add_tag_no_duplicates(tags_file):
    add_tag("editor", ".vimrc", tags_file)
    add_tag("editor", ".vimrc", tags_file)
    tags = load_tags(tags_file)
    assert tags["editor"].count(".vimrc") == 1


def test_remove_tag_removes_file(tags_file):
    add_tag("shell", ".bashrc", tags_file)
    add_tag("shell", ".zshrc", tags_file)
    remove_tag("shell", ".bashrc", tags_file)
    files = get_files_for_tag("shell", tags_file)
    assert ".bashrc" not in files
    assert ".zshrc" in files


def test_remove_tag_deletes_empty_tag(tags_file):
    add_tag("solo", ".tmux.conf", tags_file)
    remove_tag("solo", ".tmux.conf", tags_file)
    tags = load_tags(tags_file)
    assert "solo" not in tags


def test_get_tags_for_file(tags_file):
    add_tag("shell", ".bashrc", tags_file)
    add_tag("linux", ".bashrc", tags_file)
    tags = get_tags_for_file(".bashrc", tags_file)
    assert "shell" in tags
    assert "linux" in tags


def test_delete_tag(tags_file):
    add_tag("temp", ".foo", tags_file)
    result = delete_tag("temp", tags_file)
    assert result is True
    assert load_tags(tags_file) == {}


def test_delete_tag_missing_returns_false(tags_file):
    result = delete_tag("nonexistent", tags_file)
    assert result is False


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_tags_list_empty(runner, tmp_path, monkeypatch):
    monkeypatch.setattr("haul.tags.DEFAULT_TAGS_FILE", tmp_path / "tags.json")
    result = runner.invoke(tags_cmd, ["list"])
    assert result.exit_code == 0
    assert "No tags" in result.output


def test_cli_tags_add_and_show(runner, tmp_path, monkeypatch):
    monkeypatch.setattr("haul.tags.DEFAULT_TAGS_FILE", tmp_path / "tags.json")
    runner.invoke(tags_cmd, ["add", "shell", ".bashrc"])
    result = runner.invoke(tags_cmd, ["show", "shell"])
    assert ".bashrc" in result.output
