---
id: 2
type: bug
title: "Failed update() leaves half the records changed (MemoryStorage)"
hidden_tests: hidden_tests/test_issue_2.py
github_issue: https://github.com/keshavdubeyy/tinydb/issues/2
---

**Failed update() leaves half the records changed (MemoryStorage)**

I use `MemoryStorage` in my unit tests and found something weird. If an `update()` blows up on one record, the records before it are already changed. So the error is raised, but the data is now half-updated.

```python
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from tinydb.operations import add

db = TinyDB(storage=MemoryStorage)
db.insert_multiple([{'score': 1}, {'score': 2}, {'score': 'oops'}])

try:
    db.update(add('score', 10))
except TypeError:
    pass

print(db.all())
# [{'score': 11}, {'score': 12}, {'score': 'oops'}]   <- first two got changed!
```

With the normal JSON file storage, the same code leaves everything untouched, which is what I'd expect: either the whole update happens or none of it. My tests pass on MemoryStorage and then behave differently in prod, which took me a while to figure out.
