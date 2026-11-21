---
id: 3
type: feature
title: "Let count() work without a query"
hidden_tests: hidden_tests/test_issue_3.py
github_issue: https://github.com/keshavdubeyy/tinydb/issues/3
---

**Let count() work without a query**

Small thing, but I keep tripping over it. When I want the total number of records, I naturally type:

```python
db.count()
```

and get `TypeError: Table.count() missing 1 required positional argument: 'cond'`.

I know `len(db)` works, but `count()` is right there and it feels like it should just return the total when you don't pass a query. Could `count()` with no argument return the number of all documents?
