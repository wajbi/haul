"""CLI commands for conflict resolution."""

import click
from haul.conflicts import detect_conflict, resolve_conflict, list_conflicts
from haul.config import load_config


@click.group("conflicts")
def conflicts_cmd():
    """Detect and resolve file conflicts."""
    pass


@conflicts_cmd.command("check")
@click.argument("source")
@click.argument("dest")
def conflicts_check(source, dest):
    """Check if SOURCE and DEST are in conflict."""
    if detect_conflict(source, dest):
        click.echo(click.style(f"CONFLICT: {source} <-> {dest}", fg="red"))
    else:
        click.echo(click.style(f"OK: no conflict detected", fg="green"))


@conflicts_cmd.command("resolve")
@click.argument("source")
@click.argument("dest")
@click.option(
    "--strategy",
    type=click.Choice(["source", "dest", "backup"]),
    default="source",
    show_default=True,
    help="Resolution strategy.",
)
def conflicts_resolve(source, dest, strategy):
    """Resolve a conflict between SOURCE and DEST."""
    if not detect_conflict(source, dest):
        click.echo("No conflict detected — nothing to resolve.")
        return

    result = resolve_conflict(source, dest, strategy=strategy)
    click.echo(click.style(f"Resolved via '{strategy}': {result['action']}", fg="yellow"))
    if "backup" in result:
        click.echo(f"  Backup saved to: {result['backup']}")
