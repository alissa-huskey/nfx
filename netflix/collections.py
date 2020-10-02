from datetime import datetime, timedelta
from pprint import pprint
from typing import Any
from functools import cached_property
import json
import math
import re
import html

from py.path import local
from tabulate import tabulate

from .page import Page


__all__ = ["Collection", "Expiring", "NewReleases"]


class Collection:
    """."""
    DATADIR = 'data'
    EXPIRE_DAYS = 1
    PER_PAGE = 100
    MAX = 500

    dirpath: Any
    movies: list
    pages: list
    count: int
    ctype: str

    def __init__(self):
        """Initializer"""
        self.dirpath = local(self.__class__.DATADIR).join(self.ctype)
        self.pages = []
        self.movies = []
        self.count = 0

    @cached_property
    def output_fields(self) -> dict:
        """Returns dict of fields to print title -> field"""
        return {
            'id': "netflixid",
            'title': "title",
            'released': "released",
            'runtime': "runtime"
        }

    @cached_property
    def page_count(self) -> int:
        """Return the total number of pages"""
        return math.ceil(int(self.pages[0].json['COUNT']) / self.PER_PAGE)

    def load(self):
        """Load all files"""
        num = 0
        while True:
            num += 1
            page = Page(self.ctype, num)
            page.get()
            self.pages.append(page)
            self.movies += page.json['ITEMS']

            if self.is_last(page):
                break

    def purge(self):
        """Delete files older than EXPIRE_DAYS ago"""
        expire = datetime.today() - timedelta(days=self.EXPIRE_DAYS)

        for f in self.dirpath.listdir():
            if f.mtime() <= expire.timestamp():
                f.remove()

    @cached_property
    def filtered(self):
        """Filter to only movies"""
        return [m for m in self.movies if m['type'] == "movie"]

    @cached_property
    def formatted(self):
        """Return list of movies formatted for print"""
        return [
            [html.unescape(m[f]) for f in self.output_fields.values()]
            for m in self.filtered]

    def print(self):
        """Print the movies"""
        print(tabulate(
            self.formatted,
            headers=[ f.capitalize() for f in self.output_fields.keys()])
        )

    def is_last(self, page) -> bool:
        """Return True if page is the last page"""
        if (self.PER_PAGE * page.num) >= self.MAX:
            return True

        return page.num >= self.page_count


class Expiring(Collection):
    """Expiring releases collection"""
    ctype: str = "expiring"

    @cached_property
    def output_fields(self) -> dict:
        """Returns dict of fields to print title -> field"""
        fields = {'expiring': "unogsdate"}
        fields.update(super().output_fields)
        return fields


class NewReleases(Collection):
    """New releases collection"""
    ctype: str = "new"
