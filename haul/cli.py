"""Main CLI entry point for haul."""

import click
from haul.config import load_config, save_config, get, set_value
from haul.cli_status import status_cmd
from haul.cli_conflicts import conflicts_cmd
from haul.cli_history import history_cmd
from haul.cli_profiles import profiles_cmd
from haul.cli_tags import tags_cmd
from haul.cli_templates import templates_cmd
from haul.cli_remotes import remotes_cmd

CONFIG_FILE = ".haul/config.json"


@click.group()
def cli():
    """haul — sync dotfiles across machines."""
    pass


@cli.group()
def config():
    """Manage haul configuration."""
    pass


@config.command("show")
def config_show():
    """Show current configuration."""
    cfg = load_config(CONFIG_FILE)
    for key, value in cfg.items():
        click.echo(f"{key} = {value}")


@config.command("get")
@click.argument("key")
def config_get(key):
    """Get a configuration value."""
    cfg = load_config(CONFIG_FILE)
    value = get(cfg, key)
    if value is None:
        click.echo(f"Key '{key}' not found.", err=True)
        raise SystemExit(1)
    click.echo(value)


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """Set a configuration value."""
    cfg = load_config(CONFIG_FILE)
    set_value(cfg, key, value)
    save_config(CONFIG_FILE, cfg)
    click.echo(f"Set {key} = {value}")


cli.add_command(status_cmd, "status")
cli.add_command(conflicts_cmd, "conflicts")
cli.add_command(history_cmd, "history")
cli.add_command(profiles_cmd, "profiles")
cli.add_command(tags_cmd, "tags")
cli.add_command(templates_cmd, "templates")
cli.add_command(remotes_cmd, "remotes")
