"""CLI commands for profile management."""

import click
from haul.profiles import (
    create_profile,
    delete_profile,
    get_profile,
    list_profiles,
)


@click.group("profiles")
def profiles_cmd():
    """Manage named sync profiles."""


@profiles_cmd.command("list")
def profiles_list():
    """List all saved profiles."""
    names = list_profiles()
    if not names:
        click.echo("No profiles found.")
        return
    for name in names:
        click.echo(f"  {name}")


@profiles_cmd.command("create")
@click.argument("name")
@click.option("--source", required=True, help="Source directory for this profile.")
@click.option("--dest", required=True, help="Destination directory for this profile.")
@click.option("--files", multiple=True, help="Specific files to include (repeatable).")
def profiles_create(name, source, dest, files):
    """Create a new profile."""
    create_profile(name, source, dest, list(files))
    click.echo(f"Profile '{name}' created.")


@profiles_cmd.command("show")
@click.argument("name")
def profiles_show(name):
    """Show details of a profile."""
    profile = get_profile(name)
    if profile is None:
        click.echo(f"Profile '{name}' not found.", err=True)
        raise SystemExit(1)
    click.echo(f"Name:   {name}")
    click.echo(f"Source: {profile['source_dir']}")
    click.echo(f"Dest:   {profile['dest_dir']}")
    files = profile.get("files", [])
    click.echo(f"Files:  {', '.join(files) if files else '(all)'}")


@profiles_cmd.command("delete")
@click.argument("name")
@click.confirmation_option(prompt="Are you sure you want to delete this profile?")
def profiles_delete(name):
    """Delete a profile."""
    removed = delete_profile(name)
    if removed:
        click.echo(f"Profile '{name}' deleted.")
    else:
        click.echo(f"Profile '{name}' not found.", err=True)
        raise SystemExit(1)
