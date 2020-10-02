"""Page module"""

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
import requests

from .private import KEY

class Page:
    """Page class"""
    DATADIR = 'data'
    QUERIES = {
        'new': "new1",
        'expiring': "exp"
    }
    URL: str = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"

    num: int
    dirpath: Any
    json: dict
    ptype: str

    def __init__(self, ptype, num):
        """Initializer"""
        self.num = num
        self.ptype = ptype
        self.dirpath = local(self.__class__.DATADIR).join(ptype)
        self.json = {}

    @cached_property
    def filepath(self):
        """Return the LocalPath object for for this page"""
        return self.dirpath.join(f"{self.num}.json")

    def is_fresh(self):
        """Return True if file exists and was created less than a day ago"""
        if not self.filepath.isfile():
            return False

        yesterday = datetime.today() - timedelta(days=1)
        return self.filepath.mtime() > yesterday.timestamp()

    def is_last(self):
        """Return True if this is the last page"""
        if (PER_PAGE * self.num) >= MAX:
            return True

        pages = math.ceil(int(self.json['COUNT']) / PER_PAGE)
        return self.num >= pages

    def load(self):
        """Read the file and set self.json"""
        if self.json:
            return
        self.json = json.loads(self.filepath.read())

    def get(self):
        """Depending on freshness either download or load the page"""
        if self.is_fresh():
            self.load()
        else:
            self.download()

    def query(self) -> str:
        """Return the query type for this """
        return self.__class__.QUERIES[self.ptype]

    def download(self):
        """Download a page, return filepath"""
        response = requests.get(
            self.__class__.URL,
            params={'q': f"get:{self.query}:US", 't': "ns", 'st': "adv", 'p': self.num},
            headers={'x-rapidapi-key': KEY}
        )

        if response.status_code != 200 or not response.text:
            raise(f"Failed to download page {page}: {response.status_code} {response.reason}")

        self.json = response.json()
        self.filepath.write(response.text)
