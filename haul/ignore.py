"""Ignore patterns for haul — skip files that match configured patterns."""

import fnmatch
import os
from typing import List

from haul.config import get

# Default patterns to always ignore
DEFAULT_IGNORE_PATTERNS = [
    ".git",
    ".git/*",
    "*.swp",
    "*.swo",
    "*~",
    ".DS_Store",
    "Thumbs.db",
    "*.pyc",
    "__pycache__",
    "__pycache__/*",
]


def load_ignore_patterns(config: dict = None) -> List[str]:
    """Load ignore patterns from config, merged with defaults.

    Args:
        config: Optional config dict. If None, loads from default config.

    Returns:
        List of glob-style ignore patterns.
    """
    user_patterns = get("ignore_patterns", config) or []
    # Merge defaults with user patterns, avoiding duplicates
    all_patterns = list(DEFAULT_IGNORE_PATTERNS)
    for pattern in user_patterns:
        if pattern not in all_patterns:
            all_patterns.append(pattern)
    return all_patterns


def is_ignored(path: str, patterns: List[str] = None) -> bool:
    """Check if a file path matches any ignore pattern.

    Matches against both the full path and just the filename/basename.

    Args:
        path: File path to check (can be relative or absolute).
        patterns: List of glob patterns. If None, loads from config.

    Returns:
        True if the path should be ignored, False otherwise.
    """
    if patterns is None:
        patterns = load_ignore_patterns()

    basename = os.path.basename(path)
    # Normalize path separators
    normalized = path.replace("\\", "/")

    for pattern in patterns:
        # Match against full path
        if fnmatch.fnmatch(normalized, pattern):
            return True
        # Match against just the filename
        if fnmatch.fnmatch(basename, pattern):
            return True
        # Match against each path component
        parts = normalized.split("/")
        for part in parts:
            if fnmatch.fnmatch(part, pattern):
                return True

    return False


def filter_files(paths: List[str], patterns: List[str] = None) -> List[str]:
    """Filter a list of file paths, removing any that match ignore patterns.

    Args:
        paths: List of file paths to filter.
        patterns: List of glob patterns. If None, loads from config.

    Returns:
        Filtered list of paths with ignored files removed.
    """
    if patterns is None:
        patterns = load_ignore_patterns()

    return [p for p in paths if not is_ignored(p, patterns)]


def add_ignore_pattern(pattern: str, config: dict) -> dict:
    """Add a new ignore pattern to the config.

    Args:
        pattern: Glob pattern to add.
        config: Current config dict.

    Returns:
        Updated config dict.
    """
    existing = config.get("ignore_patterns", [])
    if pattern not in existing:
        config["ignore_patterns"] = existing + [pattern]
    return config


def remove_ignore_pattern(pattern: str, config: dict) -> dict:
    """Remove an ignore pattern from the config.

    Args:
        pattern: Glob pattern to remove.
        config: Current config dict.

    Returns:
        Updated config dict. No error if pattern wasn't present.
    """
    existing = config.get("ignore_patterns", [])
    config["ignore_patterns"] = [p for p in existing if p != pattern]
    return config
