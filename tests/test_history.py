"""Tests for haul/history.py."""

import json
import pytest
from pathlib import Path
from haul.history import (
    load_history,
    save_history,
    record_sync,
    get_recent,
    clear_history,
    format_history_line,
    MAX_HISTORY_ENTRIES,
)


@pytest.fixture
def history_file(tmp_path):
    return str(tmp_path / "history.json")


def test_load_history_returns_empty_when_no_file(history_file):
    result = load_history(history_file)
    assert result == []


def test_save_and_load_history(history_file):
    entries = [{"timestamp": "2024-01-01T00:00:00", "source": "a", "dest": "b", "action": "copy"}]
    save_history(entries, history_file)
    loaded = load_history(history_file)
    assert loaded == entries


def test_load_history_handles_corrupt_file(history_file):
    Path(history_file).parent.mkdir(parents=True, exist_ok=True)
    Path(history_file).write_text("not json")
    result = load_history(history_file)
    assert result == []


def test_record_sync_adds_entry(history_file):
    entry = record_sync("src/.bashrc", "~/.bashrc", "copy", history_file)
    assert entry["source"] == "src/.bashrc"
    assert entry["dest"] == "~/.bashrc"
    assert entry["action"] == "copy"
    assert "timestamp" in entry

    entries = load_history(history_file)
    assert len(entries) == 1


def test_record_sync_accumulates_entries(history_file):
    record_sync("a", "b", "copy", history_file)
    record_sync("c", "d", "skip", history_file)
    entries = load_history(history_file)
    assert len(entries) == 2


def test_save_history_trims_to_max(history_file):
    entries = [{"timestamp": "t", "source": str(i), "dest": "d", "action": "copy"} for i in range(MAX_HISTORY_ENTRIES + 20)]
    save_history(entries, history_file)
    loaded = load_history(history_file)
    assert len(loaded) == MAX_HISTORY_ENTRIES


def test_get_recent_returns_last_n(history_file):
    for i in range(15):
        record_sync(str(i), "dest", "copy", history_file)
    recent = get_recent(n=5, history_file=history_file)
    assert len(recent) == 5
    assert recent[-1]["source"] == "14"


def test_clear_history(history_file):
    record_sync("a", "b", "copy", history_file)
    clear_history(history_file)
    assert load_history(history_file) == []


def test_format_history_line():
    entry = {
        "timestamp": "2024-06-15T12:34:56",
        "source": "~/.dotfiles/.bashrc",
        "dest": "~/.bashrc",
        "action": "copy",
    }
    line = format_history_line(entry)
    assert "2024-06-15 12:34:56" in line
    assert "COPY" in line
    assert "~/.dotfiles/.bashrc" in line
    assert "~/.bashrc" in line
