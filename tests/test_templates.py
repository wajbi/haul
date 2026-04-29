"""Tests for haul/templates.py"""

import pytest
from pathlib import Path
from haul.templates import (
    load_templates,
    save_templates,
    create_template,
    get_template,
    delete_template,
    list_templates,
    add_file_to_template,
    remove_file_from_template,
)


@pytest.fixture
def templates_file(tmp_path):
    return tmp_path / "templates.json"


def test_load_templates_returns_empty_when_no_file(templates_file):
    result = load_templates(templates_file)
    assert result == {}


def test_load_templates_handles_corrupt_file(templates_file):
    templates_file.write_text("not json{{")
    result = load_templates(templates_file)
    assert result == {}


def test_save_and_load_templates(templates_file):
    data = {"base": {"files": [".bashrc"], "description": "Basic shell"}}
    save_templates(data, templates_file)
    result = load_templates(templates_file)
    assert result == data


def test_create_template_stores_data(templates_file):
    tmpl = create_template("vim", [".vimrc", ".vim/"], "Vim config", templates_file)
    assert tmpl["files"] == [".vimrc", ".vim/"]
    assert tmpl["description"] == "Vim config"
    loaded = load_templates(templates_file)
    assert "vim" in loaded


def test_create_template_no_files(templates_file):
    tmpl = create_template("empty", [], templates_file=templates_file)
    assert tmpl["files"] == []


def test_get_template_returns_none_for_missing(templates_file):
    result = get_template("nonexistent", templates_file)
    assert result is None


def test_get_template_returns_existing(templates_file):
    create_template("shell", [".bashrc"], templates_file=templates_file)
    tmpl = get_template("shell", templates_file)
    assert tmpl is not None
    assert ".bashrc" in tmpl["files"]


def test_delete_template_removes_entry(templates_file):
    create_template("to_delete", [], templates_file=templates_file)
    result = delete_template("to_delete", templates_file)
    assert result is True
    assert get_template("to_delete", templates_file) is None


def test_delete_template_returns_false_for_missing(templates_file):
    result = delete_template("ghost", templates_file)
    assert result is False


def test_add_file_to_template(templates_file):
    create_template("git", [".gitconfig"], templates_file=templates_file)
    add_file_to_template("git", ".gitignore_global", templates_file)
    tmpl = get_template("git", templates_file)
    assert ".gitignore_global" in tmpl["files"]


def test_add_file_no_duplicates(templates_file):
    create_template("git", [".gitconfig"], templates_file=templates_file)
    add_file_to_template("git", ".gitconfig", templates_file)
    tmpl = get_template("git", templates_file)
    assert tmpl["files"].count(".gitconfig") == 1


def test_remove_file_from_template(templates_file):
    create_template("shell", [".bashrc", ".zshrc"], templates_file=templates_file)
    remove_file_from_template("shell", ".zshrc", templates_file)
    tmpl = get_template("shell", templates_file)
    assert ".zshrc" not in tmpl["files"]
    assert ".bashrc" in tmpl["files"]


def test_list_templates_returns_all(templates_file):
    create_template("a", [], templates_file=templates_file)
    create_template("b", [], templates_file=templates_file)
    result = list_templates(templates_file)
    assert "a" in result
    assert "b" in result
