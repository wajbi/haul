"""Tests for haul config module."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch

import haul.config as cfg


@pytest.fixture
def tmp_config(tmp_path, monkeypatch):
    config_file = tmp_path / ".haulrc"
    monkeypatch.setattr(cfg, "CONFIG_PATH", config_file)
    return config_file


def test_load_config_returns_defaults_when_no_file(tmp_config):
    result = cfg.load_config()
    assert result == cfg.DEFAULT_CONFIG


def test_save_and_load_config(tmp_config):
    custom = {**cfg.DEFAULT_CONFIG, "auto_backup": False}
    cfg.save_config(custom)
    loaded = cfg.load_config()
    assert loaded["auto_backup"] is False


def test_load_config_merges_with_defaults(tmp_config):
    # Write partial config
    tmp_config.write_text(json.dumps({"auto_backup": False}))
    loaded = cfg.load_config()
    assert loaded["auto_backup"] is False
    # Other defaults should still be present
    assert loaded["conflict_strategy"] == "ask"


def test_get_returns_value(tmp_config):
    assert cfg.get("conflict_strategy") == "ask"


def test_get_raises_on_unknown_key(tmp_config):
    with pytest.raises(KeyError, match="Unknown config key"):
        cfg.get("nonexistent_key")


def test_set_value_persists(tmp_config):
    cfg.set_value("auto_backup", False)
    assert cfg.get("auto_backup") is False


def test_set_value_raises_on_unknown_key(tmp_config):
    with pytest.raises(KeyError, match="Unknown config key"):
        cfg.set_value("made_up_key", "value")
