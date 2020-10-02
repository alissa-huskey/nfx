from os import makedirs
from pprint import pprint as pp
from datetime import datetime, timedelta
import re

from py.path import local

from netflix.query import Query


DIR = local(__file__).dirpath().join("fixtures", "lockfiles")


def mkfixture(name, contents, force=False):
    """Create fixture file"""
    if not DIR.isdir(): makedirs(DIR)
    f = DIR.join(name)
    if not f.isfile() or force: f.write(contents)
    return f


def test_is_locked_when_no_lockfile():
    """query.is_locked() should return False if lockfile does not exist"""
    q = Query()
    assert not q.is_locked()


def test_is_locked_when_rate_limit_refreshed():
    """query.is_locked() should return True if lockfile exists and contains timestamp > beginning of today"""
    d = datetime.today() - timedelta(days=1, hours=1)
    f = mkfixture("rate_limit_refreshed", f"{int(d.timestamp())} locked", True)
    q = Query()
    q.lockfile = f
    assert not q.is_locked()


def test_is_locked_when_status_pending():
    """query.is_locked() should return False if lockfile exists and contains status of pending"""
    f = mkfixture("status_pending", "_ pending")
    q = Query()
    q.lockfile = f
    assert not q.is_locked()


def test_is_locked_when_rate_limit_not_refreshed():
    """query.is_locked() should return True if lockfile exists and contains timestamp < beginning of today"""
    f = mkfixture("rate_limit_not_refreshed", f"{int(datetime.today().timestamp())} locked", True)
    q = Query()
    q.lockfile = f
    assert q.is_locked()


def test_lock():
    """self.lock() should write a timestamp and status locked"""
    f = DIR.join("lock")
    if f.isfile(): f.remove()
    q = Query()
    q.lockfile = f
    q.lock()

    assert f.isfile()
    assert re.fullmatch(r"^[0-9]+ locked", f.read())


def test_lock_with_args():
    """self.lock() should write a timestamp and status locked"""
    d = datetime.today() - timedelta(hours=1)
    f = mkfixture("lock_with_args", f"{int(d.timestamp())} locked", True)
    q = Query()
    q.lockfile = f
    q.lock(d.timestamp(), "pending")

    assert f.isfile()
    assert f"{int(d.timestamp())} pending" == f.read()


def test_rate_limit_refreshed_refreshed():
    """self.rate_limit_refreshed(ts) should return True if ts < beginning of day"""
    d = datetime.today() - timedelta(days=1, hours=1)
    q = Query()
    assert q.rate_limit_refreshed(d.timestamp())

def test_rate_limit_refreshed_not_refreshed():
    """self.rate_limit_refreshed(ts) should return False if ts > beginning of day"""
    q = Query()
    assert not q.rate_limit_refreshed(datetime.today().timestamp())
