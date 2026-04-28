"""CLI entry point for haul."""

import click
from haul import config as cfg
from haul.sync import sync_all


@click.group()
def cli():
    """haul — sync your dotfiles across machines."""
    pass


# ---------- config commands ----------

@cli.group()
def config():
    """Manage haul configuration."""
    pass


@config.command("show")
def config_show():
    """Print the current config."""
    data = cfg.load_config()
    for key, value in data.items():
        click.echo(f"{key} = {value}")


@config.command("get")
@click.argument("key")
def config_get(key):
    """Get a config value by key."""
    value = cfg.get(key)
    if value is None:
        click.echo(f"Key '{key}' not found.", err=True)
        raise SystemExit(1)
    click.echo(value)


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """Set a config value."""
    cfg.set_value(key, value)
    click.echo(f"Set {key} = {value}")


# ---------- sync commands ----------

@cli.command()
@click.option("--dry-run", is_flag=True, help="Preview changes without writing files.")
def sync(dry_run):
    """Sync dotfiles into the repo directory."""
    data = cfg.load_config()
    repo_dir = data.get("repo_dir", "")
    dotfiles = data.get("dotfiles", [])

    if not repo_dir:
        click.echo("Error: 'repo_dir' is not configured. Run: haul config set repo_dir <path>", err=True)
        raise SystemExit(1)

    if not dotfiles:
        click.echo("No dotfiles configured. Add entries under 'dotfiles' in your config.")
        return

    if dry_run:
        click.echo("Dry run — no files will be written.\n")

    results = sync_all(dotfiles, repo_dir, dry_run=dry_run)
    for r in results:
        icon = {"copied": "✔", "skipped": "–", "dry_run": "~"}.get(r["status"], "✘")
        click.echo(f"  {icon}  {r['name']}  ({r['status']})")


if __name__ == "__main__":
    cli()
