"""Tag-based file grouping for haul dotfiles."""

import json
from pathlib import Path

DEFAULT_TAGS_FILE = Path.home() / ".haul" / "tags.json"


def load_tags(tags_file=None):
    """Load tags from disk. Returns dict mapping tag -> list of file paths."""
    path = Path(tags_file or DEFAULT_TAGS_FILE)
    if not path.exists():
        return {}
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_tags(tags, tags_file=None):
    """Save tags dict to disk."""
    path = Path(tags_file or DEFAULT_TAGS_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(tags, f, indent=2)


def add_tag(tag, file_path, tags_file=None):
    """Associate a file path with a tag. Creates tag if it doesn't exist."""
    tags = load_tags(tags_file)
    if tag not in tags:
        tags[tag] = []
    if file_path not in tags[tag]:
        tags[tag].append(file_path)
    save_tags(tags, tags_file)
    return tags


def remove_tag(tag, file_path, tags_file=None):
    """Remove a file path from a tag. Removes tag entirely if empty."""
    tags = load_tags(tags_file)
    if tag not in tags:
        return tags
    tags[tag] = [f for f in tags[tag] if f != file_path]
    if not tags[tag]:
        del tags[tag]
    save_tags(tags, tags_file)
    return tags


def get_files_for_tag(tag, tags_file=None):
    """Return list of file paths associated with a tag."""
    tags = load_tags(tags_file)
    return tags.get(tag, [])


def get_tags_for_file(file_path, tags_file=None):
    """Return all tags associated with a given file path."""
    tags = load_tags(tags_file)
    return [tag for tag, files in tags.items() if file_path in files]


def delete_tag(tag, tags_file=None):
    """Remove a tag and all its file associations."""
    tags = load_tags(tags_file)
    removed = tags.pop(tag, None)
    save_tags(tags, tags_file)
    return removed is not None
