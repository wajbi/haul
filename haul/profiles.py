"""Profile management for haul — switch between named sync configurations."""

import json
import os
from pathlib import Path

DEFAULT_PROFILES_FILE = os.path.expanduser("~/.haul/profiles.json")


def load_profiles(profiles_file=DEFAULT_PROFILES_FILE):
    """Load all profiles from disk. Returns dict of profile_name -> config."""
    path = Path(profiles_file)
    if not path.exists():
        return {}
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_profiles(profiles, profiles_file=DEFAULT_PROFILES_FILE):
    """Persist profiles dict to disk."""
    path = Path(profiles_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(profiles, f, indent=2)


def create_profile(name, source_dir, dest_dir, files=None, profiles_file=DEFAULT_PROFILES_FILE):
    """Create or overwrite a named profile."""
    profiles = load_profiles(profiles_file)
    profiles[name] = {
        "source_dir": str(source_dir),
        "dest_dir": str(dest_dir),
        "files": files or [],
    }
    save_profiles(profiles, profiles_file)
    return profiles[name]


def get_profile(name, profiles_file=DEFAULT_PROFILES_FILE):
    """Fetch a single profile by name, or None if it doesn't exist."""
    return load_profiles(profiles_file).get(name)


def delete_profile(name, profiles_file=DEFAULT_PROFILES_FILE):
    """Remove a profile. Returns True if it existed, False otherwise."""
    profiles = load_profiles(profiles_file)
    if name not in profiles:
        return False
    del profiles[name]
    save_profiles(profiles, profiles_file)
    return True


def list_profiles(profiles_file=DEFAULT_PROFILES_FILE):
    """Return a list of profile names."""
    return list(load_profiles(profiles_file).keys())
