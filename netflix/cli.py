"""Netflix CLI module"""

from pprint import pprint

import click

from .collections import Expiring, NewReleases
from .query import Search

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


@cli.command()
@click.argument('query', nargs=-1)
def search(query):
    """Search by title"""
    search = Search(" ".join(query))
    search.load()
    search.print()


if __name__ == "__main__":
    cli()
