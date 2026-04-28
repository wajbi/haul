"""CLI command for displaying sync status."""

import click
from haul.status import status_all, format_status_line, STATUS_SYNCED, STATUS_MODIFIED


@click.command("status")
@click.option("--short", "-s", is_flag=True, help="Only show files that are out of sync.")
def status_cmd(short: bool) -> None:
    """Show the sync status of all tracked dotfiles."""
    results = status_all()

    if not results:
        click.echo("No files are being tracked. Add entries under 'files' in your config.")
        return

    out_of_sync = [r for r in results if r["status"] != STATUS_SYNCED]
    display = out_of_sync if short else results

    if not display:
        click.secho("All files are in sync.", fg="green")
        return

    if short and out_of_sync:
        click.secho(f"{len(out_of_sync)} file(s) out of sync:", fg="yellow")

    for entry in display:
        color = "green" if entry["status"] == STATUS_SYNCED else "yellow"
        if entry["status"] in ("missing_source", "missing_dest"):
            color = "red"
        click.secho(format_status_line(entry), fg=color)

    if not short:
        synced_count = sum(1 for r in results if r["status"] == STATUS_SYNCED)
        click.echo(f"\n{synced_count}/{len(results)} file(s) synced.")
