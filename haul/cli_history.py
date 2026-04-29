"""CLI commands for sync history."""

import click
from haul.history import get_recent, clear_history, format_history_line


@click.group(name="history")
def history_cmd():
    """View and manage sync history."""
    pass


@history_cmd.command(name="show")
@click.option("--n", default=10, show_default=True, help="Number of entries to show.")
@click.option("--history-file", default=None, help="Path to history file.")
def history_show(n, history_file):
    """Show recent sync history."""
    kwargs = {}
    if history_file:
        kwargs["history_file"] = history_file

    entries = get_recent(n=n, **kwargs)
    if not entries:
        click.echo("No history found.")
        return

    for entry in reversed(entries):
        click.echo(format_history_line(entry))


@history_cmd.command(name="clear")
@click.option("--history-file", default=None, help="Path to history file.")
@click.confirmation_option(prompt="Clear all sync history?")
def history_clear(history_file):
    """Clear all sync history."""
    kwargs = {}
    if history_file:
        kwargs["history_file"] = history_file

    clear_history(**kwargs)
    click.echo("History cleared.")
