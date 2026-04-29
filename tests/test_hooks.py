"""Tests for haul/hooks.py"""

import pytest
import json
from pathlib import Path
from haul.hooks import (
    load_hooks, save_hooks, add_hook, remove_hook, run_hooks
)


@pytest.fixture
def hooks_file(tmp_path):
    return tmp_path / "hooks.json"


def test_load_hooks_returns_defaults_when_no_file(hooks_file):
    hooks = load_hooks(hooks_file)
    assert hooks == {"pre_sync": [], "post_sync": []}


def test_load_hooks_handles_corrupt_file(hooks_file):
    hooks_file.write_text("not valid json")
    hooks = load_hooks(hooks_file)
    assert hooks == {"pre_sync": [], "post_sync": []}


def test_save_and_load_hooks(hooks_file):
    data = {"pre_sync": ["echo before"], "post_sync": ["echo after"]}
    save_hooks(data, hooks_file)
    loaded = load_hooks(hooks_file)
    assert loaded["pre_sync"] == ["echo before"]
    assert loaded["post_sync"] == ["echo after"]


def test_add_hook_pre_sync(hooks_file):
    hooks = add_hook("pre_sync", "echo hello", hooks_file)
    assert "echo hello" in hooks["pre_sync"]


def test_add_hook_post_sync(hooks_file):
    hooks = add_hook("post_sync", "echo done", hooks_file)
    assert "echo done" in hooks["post_sync"]


def test_add_hook_no_duplicates(hooks_file):
    add_hook("pre_sync", "echo once", hooks_file)
    hooks = add_hook("pre_sync", "echo once", hooks_file)
    assert hooks["pre_sync"].count("echo once") == 1


def test_add_hook_unknown_event_raises(hooks_file):
    with pytest.raises(ValueError, match="Unknown hook event"):
        add_hook("on_magic", "echo nope", hooks_file)


def test_remove_hook(hooks_file):
    add_hook("post_sync", "echo remove_me", hooks_file)
    hooks = remove_hook("post_sync", "echo remove_me", hooks_file)
    assert "echo remove_me" not in hooks["post_sync"]


def test_remove_hook_not_present_is_noop(hooks_file):
    hooks = remove_hook("pre_sync", "echo ghost", hooks_file)
    assert "echo ghost" not in hooks["pre_sync"]


def test_run_hooks_dry_run(hooks_file):
    add_hook("pre_sync", "echo hi", hooks_file)
    results = run_hooks("pre_sync", hooks_file, dry_run=True)
    assert len(results) == 1
    assert results[0]["skipped"] is True
    assert results[0]["returncode"] is None


def test_run_hooks_executes_command(hooks_file):
    add_hook("post_sync", "echo haul", hooks_file)
    results = run_hooks("post_sync", hooks_file)
    assert results[0]["returncode"] == 0
    assert results[0]["stdout"] == "haul"


def test_run_hooks_empty_returns_empty_list(hooks_file):
    results = run_hooks("pre_sync", hooks_file)
    assert results == []
