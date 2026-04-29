"""Main CLI entry point for haul."""

import click
from haul.config import get, set_value, load_config
from haul.cli_status import status_cmd
from haul.cli_conflicts import conflicts_cmd
from haul.cli_history import history_cmd
from haul.cli_profiles import profiles_cmd


@click.group()
@click.version_option("0.1.0", prog_name="haul")
def cli():
    """haul — sync dotfiles across machines."""


@cli.group()
def config():
    """Manage haul configuration."""


@config.command("show")
def config_show():
    """Print the current configuration."""
    cfg = load_config()
    for key, value in cfg.items():
        click.echo(f"{key} = {value}")


@config.command("get")
@click.argument("key")
def config_get(key):
    """Get a configuration value."""
    value = get(key)
    if value is None:
        click.echo(f"Key '{key}' not found.", err=True)
        raise SystemExit(1)
    click.echo(value)


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """Set a configuration value."""
    set_value(key, value)
    click.echo(f"Set {key} = {value}")


cli.add_command(status_cmd, name="status")
cli.add_command(conflicts_cmd, name="conflicts")
cli.add_command(history_cmd, name="history")
cli.add_command(profiles_cmd, name="profiles")


if __name__ == "__main__":
    cli()
