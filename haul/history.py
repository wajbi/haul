"""Track sync history for dotfiles."""

import json
import os
from datetime import datetime
from pathlib import Path

DEFAULT_HISTORY_FILE = os.path.expanduser("~/.haul/history.json")
MAX_HISTORY_ENTRIES = 100


def load_history(history_file: str = DEFAULT_HISTORY_FILE) -> list:
    """Load sync history from disk."""
    path = Path(history_file)
    if not path.exists():
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_history(entries: list, history_file: str = DEFAULT_HISTORY_FILE) -> None:
    """Save sync history to disk."""
    path = Path(history_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    trimmed = entries[-MAX_HISTORY_ENTRIES:]
    with open(path, "w") as f:
        json.dump(trimmed, f, indent=2)


def record_sync(source: str, dest: str, action: str, history_file: str = DEFAULT_HISTORY_FILE) -> dict:
    """Record a sync event and persist it."""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "source": source,
        "dest": dest,
        "action": action,
    }
    entries = load_history(history_file)
    entries.append(entry)
    save_history(entries, history_file)
    return entry


def get_recent(n: int = 10, history_file: str = DEFAULT_HISTORY_FILE) -> list:
    """Return the n most recent history entries."""
    entries = load_history(history_file)
    return entries[-n:]


def clear_history(history_file: str = DEFAULT_HISTORY_FILE) -> None:
    """Clear all history entries."""
    save_history([], history_file)


def format_history_line(entry: dict) -> str:
    """Format a history entry for display."""
    ts = entry.get("timestamp", "unknown")[:19].replace("T", " ")
    action = entry.get("action", "?").upper().ljust(8)
    source = entry.get("source", "?")
    dest = entry.get("dest", "?")
    return f"[{ts}] {action} {source} -> {dest}"
