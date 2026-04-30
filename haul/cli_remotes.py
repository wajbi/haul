"""CLI commands for managing remotes."""

import click
from haul.remotes import add_remote, remove_remote, get_remote, list_remotes, update_remote

REMOTES_FILE = ".haul/remotes.json"


@click.group("remotes")
def remotes_cmd():
    """Manage remote repositories."""
    pass


@remotes_cmd.command("list")
def remotes_list():
    """List all configured remotes."""
    items = list_remotes(REMOTES_FILE)
    if not items:
        click.echo("No remotes configured.")
        return
    for name, info in items:
        click.echo(f"{name}  {info['url']}  (branch: {info['branch']})")


@remotes_cmd.command("add")
@click.argument("name")
@click.argument("url")
@click.option("--branch", default="main", show_default=True, help="Branch to track.")
def remotes_add(name, url, branch):
    """Add a new remote."""
    try:
        add_remote(REMOTES_FILE, name, url, branch)
        click.echo(f"Remote '{name}' added ({url} @ {branch}).")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@remotes_cmd.command("remove")
@click.argument("name")
def remotes_remove(name):
    """Remove a remote."""
    if remove_remote(REMOTES_FILE, name):
        click.echo(f"Remote '{name}' removed.")
    else:
        click.echo(f"Remote '{name}' not found.", err=True)
        raise SystemExit(1)


@remotes_cmd.command("show")
@click.argument("name")
def remotes_show(name):
    """Show details for a remote."""
    info = get_remote(REMOTES_FILE, name)
    if info is None:
        click.echo(f"Remote '{name}' not found.", err=True)
        raise SystemExit(1)
    click.echo(f"name:   {name}")
    click.echo(f"url:    {info['url']}")
    click.echo(f"branch: {info['branch']}")


@remotes_cmd.command("update")
@click.argument("name")
@click.option("--url", default=None, help="New URL.")
@click.option("--branch", default=None, help="New branch.")
def remotes_update(name, url, branch):
    """Update an existing remote's URL or branch."""
    try:
        info = update_remote(REMOTES_FILE, name, url=url, branch=branch)
        click.echo(f"Remote '{name}' updated: {info['url']} @ {info['branch']}.")
    except KeyError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
