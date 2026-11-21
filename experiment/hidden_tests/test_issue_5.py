"""Hidden acceptance tests for issue 5 (vague): update operations should not
crash on documents that are missing the field.

These encode the most reasonable reading of the issue: a missing numeric
field counts as 0, and deleting a missing field is a no-op. If the bot picks a
different (but defensible) interpretation, that is recorded in results, not
silently counted as a pass.
"""
from tinydb import TinyDB
from tinydb.operations import add, delete, increment
from tinydb.storages import MemoryStorage


def _db():
    db = TinyDB(storage=MemoryStorage)
    db.insert_multiple([{'name': 'a', 'visits': 5, 'nick': 'x'},
                        {'name': 'b'}])
    return db


def test_increment_with_missing_field_does_not_crash_and_counts_from_zero():
    db = _db()
    db.update(increment('visits'))
    assert [d['visits'] for d in db.all()] == [6, 1]


def test_add_with_missing_field_counts_from_zero():
    db = _db()
    db.update(add('visits', 10))
    assert [d['visits'] for d in db.all()] == [15, 10]


def test_delete_with_missing_field_is_a_noop_for_that_record():
    db = _db()
    db.update(delete('nick'))
    assert all('nick' not in d for d in db.all())
    assert [d['name'] for d in db.all()] == ['a', 'b']
