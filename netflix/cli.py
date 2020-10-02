"""Netflix CLI module"""

from pprint import pprint

import click

from .collections import Expiring, NewReleases
from .page import Page

def execute(collection):
    """."""
    collection.purge()
    collection.load()
    collection.print()

@click.group(name="netflix")
def cli():
    """Netflix CLI"""

@cli.command()
def new():
    """List new releases"""
    execute(NewReleases())

@cli.command()
def expiring():
    """List expiring releases"""
    execute(Expiring())


if __name__ == "__main__":
    cli()
