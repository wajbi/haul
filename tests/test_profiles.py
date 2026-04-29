"""Tests for haul/profiles.py"""

import pytest
from pathlib import Path
from haul.profiles import (
    create_profile,
    delete_profile,
    get_profile,
    list_profiles,
    load_profiles,
    save_profiles,
)


@pytest.fixture
def profiles_file(tmp_path):
    return str(tmp_path / "profiles.json")


def test_load_profiles_returns_empty_when_no_file(profiles_file):
    result = load_profiles(profiles_file)
    assert result == {}


def test_load_profiles_handles_corrupt_file(tmp_path):
    bad = tmp_path / "profiles.json"
    bad.write_text("not json!")
    assert load_profiles(str(bad)) == {}


def test_save_and_load_profiles(profiles_file):
    data = {"work": {"source_dir": "/src", "dest_dir": "/dst", "files": []}}
    save_profiles(data, profiles_file)
    loaded = load_profiles(profiles_file)
    assert loaded == data


def test_create_profile_stores_data(profiles_file):
    profile = create_profile("home", "/home/src", "/home/dst", [".bashrc"], profiles_file)
    assert profile["source_dir"] == "/home/src"
    assert profile["dest_dir"] == "/home/dst"
    assert profile["files"] == [".bashrc"]


def test_create_profile_overwrites_existing(profiles_file):
    create_profile("home", "/old/src", "/old/dst", [], profiles_file)
    create_profile("home", "/new/src", "/new/dst", [], profiles_file)
    profile = get_profile("home", profiles_file)
    assert profile["source_dir"] == "/new/src"


def test_get_profile_returns_none_for_missing(profiles_file):
    assert get_profile("nonexistent", profiles_file) is None


def test_delete_profile_removes_entry(profiles_file):
    create_profile("temp", "/s", "/d", [], profiles_file)
    removed = delete_profile("temp", profiles_file)
    assert removed is True
    assert get_profile("temp", profiles_file) is None


def test_delete_profile_returns_false_if_missing(profiles_file):
    assert delete_profile("ghost", profiles_file) is False


def test_list_profiles_returns_names(profiles_file):
    create_profile("alpha", "/s", "/d", [], profiles_file)
    create_profile("beta", "/s", "/d", [], profiles_file)
    names = list_profiles(profiles_file)
    assert set(names) == {"alpha", "beta"}


def test_list_profiles_empty_when_no_file(profiles_file):
    assert list_profiles(profiles_file) == []
