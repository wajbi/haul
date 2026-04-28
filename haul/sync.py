"""Core sync logic for haul — handles copying dotfiles to/from a repo."""

import os
import shutil
import hashlib
from pathlib import Path
from typing import Optional


def file_checksum(path: str) -> Optional[str]:
    """Return MD5 checksum of a file, or None if it doesn't exist."""
    try:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except FileNotFoundError:
        return None


def files_differ(src: str, dst: str) -> bool:
    """Return True if two files have different contents."""
    return file_checksum(src) != file_checksum(dst)


def resolve_path(path: str) -> str:
    """Expand ~ and env vars in a path string."""
    return str(Path(path).expanduser().resolve())


def sync_file(src: str, dst: str, dry_run: bool = False) -> str:
    """
    Copy src to dst.
    Returns a status string: 'copied', 'skipped', or 'dry_run'.
    """
    src = resolve_path(src)
    dst = resolve_path(dst)

    if not os.path.exists(src):
        raise FileNotFoundError(f"Source file not found: {src}")

    if os.path.exists(dst) and not files_differ(src, dst):
        return "skipped"

    if dry_run:
        return "dry_run"

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    return "copied"


def sync_all(dotfiles: list[dict], repo_dir: str, dry_run: bool = False) -> list[dict]:
    """
    Sync a list of dotfile entries from their source paths into the repo.

    Each entry: {"name": str, "src": str}
    Returns a list of result dicts with name, status, src, dst.
    """
    results = []
    for entry in dotfiles:
        name = entry["name"]
        src = entry["src"]
        dst = os.path.join(repo_dir, name)
        try:
            status = sync_file(src, dst, dry_run=dry_run)
        except FileNotFoundError as e:
            status = f"error: {e}"
        results.append({"name": name, "src": src, "dst": dst, "status": status})
    return results
