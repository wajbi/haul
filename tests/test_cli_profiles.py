"""CLI-level tests for profile commands."""

import json
import pytest
from click.testing import CliRunner
from haul.cli_profiles import profiles_cmd


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    """Point profiles storage at a temp file."""
    profiles_path = str(tmp_path / "profiles.json")
    monkeypatch.setattr("haul.profiles.DEFAULT_PROFILES_FILE", profiles_path)
    monkeypatch.setattr("haul.cli_profiles.list_profiles", lambda: __import__("haul.profiles", fromlist=["list_profiles"]).list_profiles(profiles_path))
    return profiles_path


def test_profiles_list_empty(runner, tmp_path, monkeypatch):
    pf = str(tmp_path / "p.json")
    monkeypatch.setattr("haul.profiles.DEFAULT_PROFILES_FILE", pf)
    result = runner.invoke(profiles_cmd, ["list"])
    assert result.exit_code == 0
    assert "No profiles found" in result.output


def test_profiles_create_and_list(runner, tmp_path, monkeypatch):
    pf = str(tmp_path / "p.json")
    monkeypatch.setattr("haul.profiles.DEFAULT_PROFILES_FILE", pf)
    result = runner.invoke(profiles_cmd, ["create", "work", "--source", "/s", "--dest", "/d"])
    assert result.exit_code == 0
    assert "created" in result.output
    data = json.loads(open(pf).read())
    assert "work" in data


def test_profiles_show(runner, tmp_path, monkeypatch):
    pf = str(tmp_path / "p.json")
    monkeypatch.setattr("haul.profiles.DEFAULT_PROFILES_FILE", pf)
    runner.invoke(profiles_cmd, ["create", "home", "--source", "/src", "--dest", "/dst", "--files", ".vimrc"])
    result = runner.invoke(profiles_cmd, ["show", "home"])
    assert result.exit_code == 0
    assert "/src" in result.output
    assert ".vimrc" in result.output


def test_profiles_show_missing(runner, tmp_path, monkeypatch):
    pf = str(tmp_path / "p.json")
    monkeypatch.setattr("haul.profiles.DEFAULT_PROFILES_FILE", pf)
    result = runner.invoke(profiles_cmd, ["show", "ghost"])
    assert result.exit_code != 0


def test_profiles_delete(runner, tmp_path, monkeypatch):
    pf = str(tmp_path / "p.json")
    monkeypatch.setattr("haul.profiles.DEFAULT_PROFILES_FILE", pf)
    runner.invoke(profiles_cmd, ["create", "tmp", "--source", "/s", "--dest", "/d"])
    result = runner.invoke(profiles_cmd, ["delete", "tmp"], input="y\n")
    assert result.exit_code == 0
    assert "deleted" in result.output
