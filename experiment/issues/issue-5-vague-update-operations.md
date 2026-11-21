---
id: 5
type: vague
title: "update operations are really fragile"
hidden_tests: hidden_tests/test_issue_5.py
github_issue: https://github.com/keshavdubeyy/tinydb/issues/5
---

**update operations are really fragile**

The built-in update helpers keep breaking on my data. I added a "visits" counter to my app a few months ago, so older records just don't have it. Now `db.update(increment('visits'))` crashes with a KeyError and I have to write my own lambdas everywhere.

`delete()` is similar: if some records don't have the field, it blows up.

Could these be made more robust / forgiving? I feel like I shouldn't have to check every record by hand before using them.
