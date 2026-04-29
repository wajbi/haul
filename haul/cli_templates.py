"""CLI commands for template management."""

import click
from haul.templates import (
    list_templates,
    create_template,
    get_template,
    delete_template,
    add_file_to_template,
    remove_file_from_template,
)


@click.group("templates")
def templates_cmd():
    """Manage file templates."""


@templates_cmd.command("list")
def templates_list():
    """List all saved templates."""
    templates = list_templates()
    if not templates:
        click.echo("No templates saved.")
        return
    for name, data in templates.items():
        desc = f" — {data['description']}" if data.get("description") else ""
        click.echo(f"  {name}{desc} ({len(data['files'])} files)")


@templates_cmd.command("create")
@click.argument("name")
@click.option("--description", "-d", default="", help="Template description")
@click.argument("files", nargs=-1)
def templates_create(name, description, files):
    """Create a new template with optional files."""
    create_template(name, list(files), description)
    click.echo(f"Template '{name}' created.")


@templates_cmd.command("show")
@click.argument("name")
def templates_show(name):
    """Show files in a template."""
    tmpl = get_template(name)
    if tmpl is None:
        click.echo(f"Template '{name}' not found.", err=True)
        return
    desc = tmpl.get("description", "")
    if desc:
        click.echo(f"Description: {desc}")
    if not tmpl["files"]:
        click.echo("  (no files)")
    for f in tmpl["files"]:
        click.echo(f"  {f}")


@templates_cmd.command("delete")
@click.argument("name")
def templates_delete(name):
    """Delete a template."""
    if delete_template(name):
        click.echo(f"Template '{name}' deleted.")
    else:
        click.echo(f"Template '{name}' not found.", err=True)


@templates_cmd.command("add-file")
@click.argument("name")
@click.argument("filepath")
def templates_add_file(name, filepath):
    """Add a file to an existing template."""
    if add_file_to_template(name, filepath):
        click.echo(f"Added '{filepath}' to template '{name}'.")
    else:
        click.echo(f"Template '{name}' not found.", err=True)


@templates_cmd.command("remove-file")
@click.argument("name")
@click.argument("filepath")
def templates_remove_file(name, filepath):
    """Remove a file from a template."""
    if remove_file_from_template(name, filepath):
        click.echo(f"Removed '{filepath}' from template '{name}'.")
    else:
        click.echo(f"Template '{name}' not found.", err=True)
