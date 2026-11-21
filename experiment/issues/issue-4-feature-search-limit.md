---
id: 4
type: feature
title: "Option to limit how many results search() returns"
hidden_tests: hidden_tests/test_issue_4.py
github_issue: https://github.com/keshavdubeyy/tinydb/issues/4
---

**Option to limit how many results search() returns**

I have a table with ~20k log entries and I usually only want the first few that match, e.g. to show "latest 5 errors" on a dashboard. Right now I do:

```python
results = logs.search(Log.level == 'error')[:5]
```

which works, but it's a bit clunky and I'd rather say what I want directly. Something like:

```python
logs.search(Log.level == 'error', limit=5)
```

that gives back at most 5 matching records, in the same order search() normally returns them. Without `limit` it should work exactly like today.
