"""Hidden acceptance tests for issue 3: count() without a query returns the
total number of documents.
"""
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage


def test_count_without_query_returns_total():
    db = TinyDB(storage=MemoryStorage)
    db.insert_multiple([{'a': 1}, {'a': 2}, {'b': 3}])
    assert db.count() == 3


def test_count_without_query_on_empty_named_table_is_zero():
    db = TinyDB(storage=MemoryStorage)
    assert db.table('empty').count() == 0


def test_count_with_query_still_works():
    # Guard: existing behaviour must be unchanged.
    db = TinyDB(storage=MemoryStorage)
    db.insert_multiple([{'a': 1}, {'a': 2}, {'b': 3}])
    assert db.count(Query().a.exists()) == 2
