"""Status reporting for haul — show sync state of tracked dotfiles."""

import os
from pathlib import Path
from typing import Optional

from haul.sync import files_differ, resolve_path
from haul.config import get


STATUS_SYNCED = "synced"
STATUS_MODIFIED = "modified"
STATUS_MISSING_SOURCE = "missing_source"
STATUS_MISSING_DEST = "missing_dest"
STATUS_UNTRACKED = "untracked"


def file_status(source: str, dest: str) -> str:
    """Return the sync status between a source and destination path."""
    src = Path(resolve_path(source))
    dst = Path(resolve_path(dest))

    if not src.exists():
        return STATUS_MISSING_SOURCE
    if not dst.exists():
        return STATUS_MISSING_DEST
    if files_differ(str(src), str(dst)):
        return STATUS_MODIFIED
    return STATUS_SYNCED


def status_all(files: Optional[list] = None) -> list[dict]:
    """Return status for all tracked file pairs.

    Each entry is a dict with keys: source, dest, status.
    """
    tracked = files or get("files") or []
    results = []

    for entry in tracked:
        if isinstance(entry, dict):
            source = entry.get("source", "")
            dest = entry.get("dest", "")
        elif isinstance(entry, (list, tuple)) and len(entry) == 2:
            source, dest = entry
        else:
            continue

        status = file_status(source, dest)
        results.append({"source": source, "dest": dest, "status": status})

    return results


STATUS_ICONS = {
    STATUS_SYNCED: "✓",
    STATUS_MODIFIED: "~",
    STATUS_MISSING_SOURCE: "!",
    STATUS_MISSING_DEST: "+",
    STATUS_UNTRACKED: "?",
}


def format_status_line(entry: dict) -> str:
    """Format a single status entry as a human-readable string."""
    icon = STATUS_ICONS.get(entry["status"], "?")
    return f"  [{icon}] {entry['source']} -> {entry['dest']}  ({entry['status']})"
