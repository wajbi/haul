"""Remote repository management for haul."""

import json
from pathlib import Path

DEFAULT_REMOTES = {}


def load_remotes(remotes_file: str) -> dict:
    path = Path(remotes_file)
    if not path.exists():
        return dict(DEFAULT_REMOTES)
    try:
        with open(path) as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return dict(DEFAULT_REMOTES)
        return data
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_REMOTES)


def save_remotes(remotes_file: str, remotes: dict) -> None:
    path = Path(remotes_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(remotes, f, indent=2)


def add_remote(remotes_file: str, name: str, url: str, branch: str = "main") -> dict:
    remotes = load_remotes(remotes_file)
    if name in remotes:
        raise ValueError(f"Remote '{name}' already exists")
    remotes[name] = {"url": url, "branch": branch}
    save_remotes(remotes_file, remotes)
    return remotes[name]


def remove_remote(remotes_file: str, name: str) -> bool:
    remotes = load_remotes(remotes_file)
    if name not in remotes:
        return False
    del remotes[name]
    save_remotes(remotes_file, remotes)
    return True


def get_remote(remotes_file: str, name: str) -> dict | None:
    remotes = load_remotes(remotes_file)
    return remotes.get(name)


def list_remotes(remotes_file: str) -> list[tuple[str, dict]]:
    remotes = load_remotes(remotes_file)
    return list(remotes.items())


def update_remote(remotes_file: str, name: str, url: str = None, branch: str = None) -> dict:
    remotes = load_remotes(remotes_file)
    if name not in remotes:
        raise KeyError(f"Remote '{name}' not found")
    if url is not None:
        remotes[name]["url"] = url
    if branch is not None:
        remotes[name]["branch"] = branch
    save_remotes(remotes_file, remotes)
    return remotes[name]
