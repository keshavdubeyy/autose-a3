---
id: 1
type: bug
title: "search() still returns records after I drop the table"
hidden_tests: hidden_tests/test_issue_1.py
github_issue: https://github.com/keshavdubeyy/tinydb/issues/1
---

**search() still returns records after I drop the table**

Hey, ran into something confusing. In my app I create the table once at startup and reuse it:

```python
db = TinyDB('app.json')
users = db.table('users')
```

There's an admin "reset" button that calls `db.drop_table('users')`. After that, `users.all()` is empty like I'd expect, but `users.search(...)` keeps giving me the old users. `users.count(...)` also still says 1. So the same table says it's empty and not empty at the same time 😅

Repro:

```python
from tinydb import TinyDB, Query
db = TinyDB('test.json')
users = db.table('users')
users.insert({'name': 'alice'})
User = Query()
print(users.search(User.name == 'alice'))   # [{'name': 'alice'}]

db.drop_table('users')
print(users.all())                          # []  <- fine
print(users.search(User.name == 'alice'))   # [{'name': 'alice'}]  <- ???
```

Same thing happens with `db.drop_tables()`. Restarting the app fixes it, so I guess something is being remembered somewhere. tinydb from master, Python 3.12.
