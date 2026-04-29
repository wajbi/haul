"""Tests for haul/cli_templates.py"""

import pytest
from click.testing import CliRunner
from haul.cli_templates import templates_cmd
from haul import templates as tmpl_module


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    tf = tmp_path / "templates.json"
    monkeypatch.setattr(tmpl_module, "DEFAULT_TEMPLATES_FILE", tf)
    return tf


def test_templates_list_empty(runner, isolated):
    result = runner.invoke(templates_cmd, ["list"])
    assert result.exit_code == 0
    assert "No templates" in result.output


def test_templates_create_and_list(runner, isolated):
    result = runner.invoke(templates_cmd, ["create", "shell", "-d", "Shell config", ".bashrc"])
    assert result.exit_code == 0
    assert "created" in result.output

    result = runner.invoke(templates_cmd, ["list"])
    assert "shell" in result.output
    assert "Shell config" in result.output


def test_templates_show(runner, isolated):
    runner.invoke(templates_cmd, ["create", "vim", ".vimrc", ".vim/"])
    result = runner.invoke(templates_cmd, ["show", "vim"])
    assert result.exit_code == 0
    assert ".vimrc" in result.output


def test_templates_show_missing(runner, isolated):
    result = runner.invoke(templates_cmd, ["show", "ghost"])
    assert "not found" in result.output


def test_templates_delete(runner, isolated):
    runner.invoke(templates_cmd, ["create", "tmp"])
    result = runner.invoke(templates_cmd, ["delete", "tmp"])
    assert result.exit_code == 0
    assert "deleted" in result.output

    result = runner.invoke(templates_cmd, ["list"])
    assert "tmp" not in result.output


def test_templates_add_and_remove_file(runner, isolated):
    runner.invoke(templates_cmd, ["create", "git", ".gitconfig"])
    runner.invoke(templates_cmd, ["add-file", "git", ".gitignore_global"])
    result = runner.invoke(templates_cmd, ["show", "git"])
    assert ".gitignore_global" in result.output

    runner.invoke(templates_cmd, ["remove-file", "git", ".gitignore_global"])
    result = runner.invoke(templates_cmd, ["show", "git"])
    assert ".gitignore_global" not in result.output
