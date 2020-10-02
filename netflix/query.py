"""Query module"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from functools import cached_property
from os import environ
from pprint import pprint
from typing import Any
import json
import math
import re

from py.path import local
from tabulate import tabulate
import requests

from .private import KEY


__all__ = ["Query", "Page", "Search"]


class Query(ABC):
    DATADIR = "data"
    RATE_LIMIT_PADDING = 5

    url: str = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"
    dirpath: Any
    json: dict
    ptype: str = "undefined"

    def __init__(self):
        """Initializer"""
        self.dirpath = local(self.__class__.DATADIR).join(self.ptype)
        self.json = {}

    @cached_property
    @abstractmethod
    def filepath(self):
        """Return the LocalPath object for for this page"""

    @cached_property
    @abstractmethod
    def params(self) -> dict:
        """Query params"""

    def _get_lockfile(self):
        """Set empty lockfile to default of ~/.config/nfx/<api-name>, then return lockfile"""
        if not self.__dict__.get('lockfile'):
            home = environ.get("HOME")
            if not home: raise Exception("HOME not defined")
            m = re.search(r"https?://(.+)\.p\.rapidapi\.com", self.url)
            self.__dict__['lockfile'] = local(f"{home}/.config/nfx").join(m.groups()[0])
        return self.__dict__['lockfile']

    def _set_lockfile(self, value):
        """Set the lockfile property"""
        self.__dict__['lockfile'] = value
    lockfile = property(_get_lockfile, _set_lockfile)

    def rate_limit_refreshed(self, ts):
        """determine (guess) if the rate limit has rolleed over for the next day"""
        exp = datetime.fromtimestamp(int(ts)) + timedelta(days=1)
        return int(datetime.today().timestamp()) >= int(exp.timestamp())

    def is_locked(self):
        """Return True if the rate limit has been reached"""
        if not self.lockfile.isfile():
            return False

        ts, status = self.lockfile.read().split()
        if status == "pending":
            self.lockfile.remove()
            return False

        if self.rate_limit_refreshed(ts):
            self.lock(ts=ts, status="pending")
            return False

        return True

    def lock(self, ts=None, status="locked"):
        """Disallow further requests if the rate limit has been reached"""
        if self.lockfile.isfile():
            _, s = self.lockfile.read().split()
            if s == "pending":
                # if the rate-limit-remaining is still under the limit then
                # that means the logic in rate_limit_refreshed() must be wrong
                raise Exception(f"Rate limit refresh logic incorrect. See file {self.lockfile.basename}")
        if not ts:
            ts = datetime.today().timestamp()
        if not self.lockfile.dirpath().isdir():
            self.lockfile.dirpath().mkdir()
        self.lockfile.write(f"{int(ts)} {status}")

    def is_fresh(self):
        """Return True if file exists and was created less than a day ago"""
        if not self.filepath.isfile():
            return False

        yesterday = datetime.today() - timedelta(days=1)
        return self.filepath.mtime() > yesterday.timestamp()

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

    def download(self):
        """Download a page"""
        if self.is_locked():
            raise Exception("Unable to proceed--RateLimit reached")

        response = requests.get(
            self.url,
            params=self.params,
            headers={'x-rapidapi-key': KEY})

        print("Rate Limit Remaining:",
              response.headers['X-RateLimit-Requests-Remaining'],
              "\n"
        )

        if int(response.headers['X-RateLimit-Requests-Remaining']) <= self.RATE_LIMIT_PADDING:
            self.lock()

        if response.status_code != 200 or not response.text:
            raise(f"Failed to download page {page}: {response.status_code} {response.reason}")

        self.json = response.json()
        self.filepath.write(response.text)

    @property
    def compiled_url(self):
        """Return URL string including all params"""
        params = "&".join([f"{k}={v}" for k,v in self.params.items()])
        return f"{self.url}?{params}"


class Page(Query):
    """Paginating queries"""
    QUERIES = {
        'new': "new1",
        'expiring': "exp"
    }

    url: str = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi"
    num: int

    def __init__(self, ptype, num):
        """Initializer"""
        self.num = num
        self.ptype = ptype
        self.dirpath = local(self.__class__.DATADIR).join(self.ptype)
        self.json = {}

    @cached_property
    def qtype(self) -> str:
        """Return the query type for this """
        return self.__class__.QUERIES[self.ptype]

    @cached_property
    def filepath(self):
        """Return the LocalPath object for for this page"""
        return self.dirpath.join(f"{self.num}.json")

    @cached_property
    def params(self) -> dict:
        """Query params"""
        return {'q': f"get:{self.qtype}:US", 't': "ns", 'st': "adv", 'p': self.num}


class Search(Query):
    """Search class"""
    url: str = "https://unogsng.p.rapidapi.com/search"
    query: str

    def __init__(self, query):
        """Initializer"""
        self.query = query
        self.dirpath = local(self.__class__.DATADIR).join("search")
        self.json = {}

    @cached_property
    def params(self) -> dict:
        """Query params"""
        return {
            "type": "movie",
            'countrylist': 78,
            'audio': "english",
            'country_andorunique': "unique",
            'query': self.query,
        }

    @cached_property
    def filepath(self):
        """Return the LocalPath object for for this page"""
        return self.dirpath.join(f"{self.query.replace(' ', '_')}.json")

    def print(self):
        """Print the results"""
        fields = {
            'id': "nfid",
            'title': "title",
            'rating': "imdbrating",
            'year': "year",
            'runtime': "rt"
        }

        for i,m in enumerate(self.json['results']):
            self.json['results'][i]['rt'] = \
                self.seconds2str(self.json['results'][i]['runtime'])

        data = [
            [m[f] for f in fields.values()]
            for m in self.json['results']
        ]

        print(tabulate(data))

    def seconds2str(self, seconds: int) -> str:
        """Convert seconds int to string in format #h#m"""
        in_mins = seconds // 60
        hours = in_mins // 60
        mins = in_mins % 60
        return f"{hours}h{mins}m"
