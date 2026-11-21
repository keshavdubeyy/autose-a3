"""Hidden acceptance tests for issue 2: a failed update() must not partially
modify documents when using MemoryStorage (all-or-nothing, like JSONStorage).
"""
import pytest

from tinydb import TinyDB, Query
from tinydb.operations import add
from tinydb.storages import MemoryStorage


def _db():
    db = TinyDB(storage=MemoryStorage)
    db.insert_multiple([{'score': 1}, {'score': 2}, {'score': 'oops'}])
    return db


def test_failed_operation_update_leaves_all_documents_unchanged():
    db = _db()
    with pytest.raises(TypeError):
        db.update(add('score', 10))
    assert [d['score'] for d in db.all()] == [1, 2, 'oops']


def test_failed_callable_update_leaves_all_documents_unchanged():
    db = TinyDB(storage=MemoryStorage)
    db.insert_multiple([{'s': 1}, {'s': 2}, {'s': 3}])

    def boom(doc):
        if doc['s'] == 2:
            raise RuntimeError('bad record')
        doc['s'] = 99

    with pytest.raises(RuntimeError):
        db.update(boom)
    assert [d['s'] for d in db.all()] == [1, 2, 3]


def test_failed_conditional_update_leaves_all_documents_unchanged():
    db = _db()
    with pytest.raises(TypeError):
        db.update(add('score', 10), Query().score.exists())
    assert [d['score'] for d in db.all()] == [1, 2, 'oops']


def test_successful_update_still_applies():
    # Guard: the fix must not break normal updates.
    db = TinyDB(storage=MemoryStorage)
    db.insert_multiple([{'score': 1}, {'score': 2}])
    db.update(add('score', 10))
    assert [d['score'] for d in db.all()] == [11, 12]
