"""CLI commands for managing file tags in haul."""

import click
from haul.tags import (
    load_tags,
    add_tag,
    remove_tag,
    get_files_for_tag,
    get_tags_for_file,
    delete_tag,
)


@click.group("tags")
def tags_cmd():
    """Manage tags for grouping dotfiles."""
    pass


@tags_cmd.command("list")
def tags_list():
    """List all tags and their associated files."""
    tags = load_tags()
    if not tags:
        click.echo("No tags defined.")
        return
    for tag, files in sorted(tags.items()):
        click.echo(f"[{tag}]")
        for f in files:
            click.echo(f"  {f}")


@tags_cmd.command("add")
@click.argument("tag")
@click.argument("file_path")
def tags_add(tag, file_path):
    """Add a file to a tag."""
    add_tag(tag, file_path)
    click.echo(f"Tagged '{file_path}' as '{tag}'.")


@tags_cmd.command("remove")
@click.argument("tag")
@click.argument("file_path")
def tags_remove(tag, file_path):
    """Remove a file from a tag."""
    remove_tag(tag, file_path)
    click.echo(f"Removed '{file_path}' from tag '{tag}'.")


@tags_cmd.command("show")
@click.argument("tag")
def tags_show(tag):
    """Show all files associated with a tag."""
    files = get_files_for_tag(tag)
    if not files:
        click.echo(f"No files tagged as '{tag}'.")
        return
    for f in files:
        click.echo(f)


@tags_cmd.command("file")
@click.argument("file_path")
def tags_file(file_path):
    """Show all tags for a given file."""
    tags = get_tags_for_file(file_path)
    if not tags:
        click.echo(f"No tags found for '{file_path}'.")
        return
    for tag in tags:
        click.echo(tag)


@tags_cmd.command("delete")
@click.argument("tag")
def tags_delete(tag):
    """Delete a tag entirely."""
    if delete_tag(tag):
        click.echo(f"Deleted tag '{tag}'.")
    else:
        click.echo(f"Tag '{tag}' not found.", err=True)
