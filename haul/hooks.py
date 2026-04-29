"""Pre/post sync hooks — run shell commands before or after syncing."""

import subprocess
import json
from pathlib import Path

DEFAULT_HOOKS_FILE = Path.home() / ".haul" / "hooks.json"

DEFAULT_HOOKS = {
    "pre_sync": [],
    "post_sync": []
}


def load_hooks(hooks_file=None):
    path = Path(hooks_file) if hooks_file else DEFAULT_HOOKS_FILE
    if not path.exists():
        return dict(DEFAULT_HOOKS)
    try:
        with open(path) as f:
            data = json.load(f)
        hooks = dict(DEFAULT_HOOKS)
        hooks.update({k: v for k, v in data.items() if k in DEFAULT_HOOKS})
        return hooks
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_HOOKS)


def save_hooks(hooks, hooks_file=None):
    path = Path(hooks_file) if hooks_file else DEFAULT_HOOKS_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(hooks, f, indent=2)


def add_hook(event, command, hooks_file=None):
    if event not in DEFAULT_HOOKS:
        raise ValueError(f"Unknown hook event: {event}. Use 'pre_sync' or 'post_sync'.")
    hooks = load_hooks(hooks_file)
    if command not in hooks[event]:
        hooks[event].append(command)
        save_hooks(hooks, hooks_file)
    return hooks


def remove_hook(event, command, hooks_file=None):
    if event not in DEFAULT_HOOKS:
        raise ValueError(f"Unknown hook event: {event}.")
    hooks = load_hooks(hooks_file)
    if command in hooks[event]:
        hooks[event].remove(command)
        save_hooks(hooks, hooks_file)
    return hooks


def run_hooks(event, hooks_file=None, dry_run=False):
    hooks = load_hooks(hooks_file)
    commands = hooks.get(event, [])
    results = []
    for cmd in commands:
        if dry_run:
            results.append({"command": cmd, "returncode": None, "skipped": True})
            continue
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        results.append({
            "command": cmd,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        })
    return results
