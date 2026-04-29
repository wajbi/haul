"""Template management for haul — save and apply file sets as named templates."""

import json
from pathlib import Path

DEFAULT_TEMPLATES_FILE = Path.home() / ".haul" / "templates.json"


def load_templates(templates_file=None):
    path = Path(templates_file or DEFAULT_TEMPLATES_FILE)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def save_templates(templates, templates_file=None):
    path = Path(templates_file or DEFAULT_TEMPLATES_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(templates, indent=2))


def create_template(name, files, description="", templates_file=None):
    templates = load_templates(templates_file)
    templates[name] = {
        "files": list(files),
        "description": description,
    }
    save_templates(templates, templates_file)
    return templates[name]


def get_template(name, templates_file=None):
    templates = load_templates(templates_file)
    return templates.get(name)


def delete_template(name, templates_file=None):
    templates = load_templates(templates_file)
    if name not in templates:
        return False
    del templates[name]
    save_templates(templates, templates_file)
    return True


def list_templates(templates_file=None):
    return load_templates(templates_file)


def add_file_to_template(name, filepath, templates_file=None):
    templates = load_templates(templates_file)
    if name not in templates:
        return False
    if filepath not in templates[name]["files"]:
        templates[name]["files"].append(filepath)
    save_templates(templates, templates_file)
    return True


def remove_file_from_template(name, filepath, templates_file=None):
    templates = load_templates(templates_file)
    if name not in templates:
        return False
    templates[name]["files"] = [
        f for f in templates[name]["files"] if f != filepath
    ]
    save_templates(templates, templates_file)
    return True
