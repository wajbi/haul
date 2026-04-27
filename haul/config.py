"""Configuration management for haul."""

import os
import json
from pathlib import Path
from typing import Any

DEFAULT_CONFIG = {
    "dotfiles_dir": "~/.dotfiles",
    "backup_dir": "~/.dotfiles_backup",
    "auto_backup": True,
    "conflict_strategy": "ask",  # ask, keep_local, keep_remote
    "tracked_files": [],
}

CONFIG_PATH = Path(os.environ.get("HAUL_CONFIG", "~/.haulrc")).expanduser()


def load_config() -> dict[str, Any]:
    """Load config from disk, falling back to defaults."""
    if not CONFIG_PATH.exists():
        return DEFAULT_CONFIG.copy()

    with open(CONFIG_PATH, "r") as f:
        user_config = json.load(f)

    return {**DEFAULT_CONFIG, **user_config}


def save_config(config: dict[str, Any]) -> None:
    """Persist config to disk."""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Config saved to {CONFIG_PATH}")


def get(key: str) -> Any:
    """Get a single config value."""
    config = load_config()
    if key not in config:
        raise KeyError(f"Unknown config key: '{key}'")
    return config[key]


def set_value(key: str, value: Any) -> None:
    """Set a single config value and save."""
    config = load_config()
    if key not in DEFAULT_CONFIG:
        raise KeyError(f"Unknown config key: '{key}'")
    config[key] = value
    save_config(config)
