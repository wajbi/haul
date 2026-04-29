"""Conflict detection and resolution for haul."""

import os
import shutil
from datetime import datetime
from haul.sync import file_checksum, files_differ, resolve_path


def detect_conflict(source: str, dest: str) -> bool:
    """Return True if both files exist and have diverged."""
    src = resolve_path(source)
    dst = resolve_path(dest)
    if not os.path.exists(src) or not os.path.exists(dst):
        return False
    return files_differ(src, dst)


def backup_file(path: str, backup_dir: str = "~/.haul/backups") -> str:
    """Copy file to backup dir with a timestamp suffix. Returns backup path."""
    resolved = resolve_path(path)
    backup_root = resolve_path(backup_dir)
    os.makedirs(backup_root, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(resolved)
    backup_path = os.path.join(backup_root, f"{filename}.{timestamp}.bak")
    shutil.copy2(resolved, backup_path)
    return backup_path


def resolve_conflict(source: str, dest: str, strategy: str = "source") -> dict:
    """
    Resolve a conflict between source and dest.

    Strategies:
      - 'source': overwrite dest with source (default)
      - 'dest':   keep dest, overwrite source
      - 'backup': backup dest then overwrite with source

    Returns a dict with 'action' and optional 'backup' keys.
    """
    src = resolve_path(source)
    dst = resolve_path(dest)

    if strategy == "source":
        shutil.copy2(src, dst)
        return {"action": "overwrote_dest", "winner": "source"}

    elif strategy == "dest":
        shutil.copy2(dst, src)
        return {"action": "overwrote_source", "winner": "dest"}

    elif strategy == "backup":
        backup_path = backup_file(dest)
        shutil.copy2(src, dst)
        return {"action": "backup_and_overwrite", "winner": "source", "backup": backup_path}

    else:
        raise ValueError(f"Unknown conflict strategy: {strategy!r}")


def list_conflicts(file_pairs: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Given a list of (source, dest) pairs, return only those with conflicts."""
    return [(src, dst) for src, dst in file_pairs if detect_conflict(src, dst)]
