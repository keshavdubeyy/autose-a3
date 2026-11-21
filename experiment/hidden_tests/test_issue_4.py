"""Hidden acceptance tests for issue 4: search(cond, limit=n) returns at most
n matching documents, in normal search order, without poisoning the cache.
"""
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage


def _db():
    db = TinyDB(storage=MemoryStorage)
    db.insert_multiple([{'level': 'error', 'i': i} for i in range(6)]
                       + [{'level': 'info', 'i': 99}])
    return db


def test_limit_returns_first_n_matches_in_order():
    db = _db()
    res = db.search(Query().level == 'error', limit=2)
    assert [d['i'] for d in res] == [0, 1]


def test_limit_larger_than_matches_returns_all_matches():
    db = _db()
    res = db.search(Query().level == 'error', limit=100)
    assert len(res) == 6


def test_limit_does_not_poison_cache_either_way():
    db = _db()
    Log = Query()
    assert len(db.search(Log.level == 'error')) == 6
    assert len(db.search(Log.level == 'error', limit=1)) == 1

    db2 = _db()
    assert len(db2.search(Log.level == 'error', limit=1)) == 1
    assert len(db2.search(Log.level == 'error')) == 6
