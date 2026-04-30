"""Tests for haul/cli_remotes.py."""

import pytest
from click.testing import CliRunner
from haul.cli_remotes import remotes_cmd
import haul.cli_remotes as cli_remotes_module


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    monkeypatch.setattr(cli_remotes_module, "REMOTES_FILE", str(tmp_path / "remotes.json"))


def test_remotes_list_empty(runner, isolated):
    result = runner.invoke(remotes_cmd, ["list"])
    assert result.exit_code == 0
    assert "No remotes" in result.output


def test_remotes_add_and_list(runner, isolated):
    result = runner.invoke(remotes_cmd, ["add", "origin", "git@github.com:user/dots.git"])
    assert result.exit_code == 0
    assert "origin" in result.output

    result = runner.invoke(remotes_cmd, ["list"])
    assert "origin" in result.output
    assert "git@github.com:user/dots.git" in result.output


def test_remotes_add_duplicate_fails(runner, isolated):
    runner.invoke(remotes_cmd, ["add", "origin", "https://example.com/a.git"])
    result = runner.invoke(remotes_cmd, ["add", "origin", "https://example.com/b.git"])
    assert result.exit_code != 0
    assert "Error" in result.output


def test_remotes_show(runner, isolated):
    runner.invoke(remotes_cmd, ["add", "origin", "https://example.com/repo.git", "--branch", "trunk"])
    result = runner.invoke(remotes_cmd, ["show", "origin"])
    assert result.exit_code == 0
    assert "trunk" in result.output
    assert "https://example.com/repo.git" in result.output


def test_remotes_show_missing(runner, isolated):
    result = runner.invoke(remotes_cmd, ["show", "ghost"])
    assert result.exit_code != 0


def test_remotes_remove(runner, isolated):
    runner.invoke(remotes_cmd, ["add", "origin", "https://example.com/repo.git"])
    result = runner.invoke(remotes_cmd, ["remove", "origin"])
    assert result.exit_code == 0
    assert "removed" in result.output


def test_remotes_update(runner, isolated):
    runner.invoke(remotes_cmd, ["add", "origin", "https://old.example.com/repo.git"])
    result = runner.invoke(remotes_cmd, ["update", "origin", "--url", "https://new.example.com/repo.git"])
    assert result.exit_code == 0
    assert "new.example.com" in result.output
