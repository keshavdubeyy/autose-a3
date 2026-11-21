"""Hidden acceptance tests for issue 1: stale search() results after dropping a table.

Kept outside the fork so the bot never sees them.
"""
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage


def test_search_on_held_table_is_empty_after_drop_table(tmp_path):
    db = TinyDB(tmp_path / 'db.json')
    users = db.table('users')
    users.insert({'name': 'alice'})
    User = Query()
    assert users.search(User.name == 'alice')  # warms the query cache

    db.drop_table('users')

    assert users.search(User.name == 'alice') == []


def test_count_on_held_table_is_zero_after_drop_table(tmp_path):
    db = TinyDB(tmp_path / 'db.json')
    users = db.table('users')
    users.insert({'name': 'alice'})
    User = Query()
    assert users.count(User.name == 'alice') == 1

    db.drop_table('users')

    assert users.count(User.name == 'alice') == 0


def test_search_on_held_table_is_empty_after_drop_tables():
    db = TinyDB(storage=MemoryStorage)
    users = db.table('users')
    users.insert({'name': 'alice'})
    User = Query()
    assert users.search(User.name == 'alice')

    db.drop_tables()

    assert users.search(User.name == 'alice') == []
