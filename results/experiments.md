# Decision experiments: results

All runs are on 21 Nov 2026 against the five seeded PRs. ✅ means the verdict matches the label (`experiment/seeded_prs/labels.md`). Each cell shows the verdict, then the failed rubric rows, then the run link.

| PR (label) | default: Sonnet | A: same_model (Haiku) | B: with_spec (Sonnet + spec) |
|---|---|---|---|
| S1 #13 (clean → APPROVE) | ✅ APPROVE · none · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44924367862) | ✅ APPROVE · none · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44925038019) | ✅ APPROVE · none · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44925179708) (spec read) |
| S2 #14 (logic bug → CHANGES) | ✅ CHANGES · R1, R4 · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44924370850) | ✅ CHANGES · R4, R5 · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44925040982) | ✅ CHANGES · R1, R4 · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44925408399) (spec read). First trial [44925182739](https://github.com/keshavdubeyy/tinydb/actions/runs/44925182739) was **invalid**: its `cat … spec.md` was denied by the tool guard and it never retried with Read. That trial gave CHANGES · R1, R3, R4. |
| S3 #15 (weak tests → CHANGES) | ✅ CHANGES · R3 · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44924375113) | ✅ CHANGES · R3, R4 · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44925043823) | ✅ CHANGES · R3 · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44925185685) (spec read) |
| S4 #16 (risky change → CHANGES) | ✅ CHANGES · R5 · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44924379841) | ✅ CHANGES · R5 · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44925046839) | ✅ CHANGES · R5 · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44925190171) (spec read) |
| S5 #17 (clean → APPROVE) | ✅ APPROVE · none · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44924382880) | ✅ APPROVE · none · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44925050553) | ✅ APPROVE · none · [run](https://github.com/keshavdubeyy/tinydb/actions/runs/44925192698) (spec read) |
| **Correct verdicts** | **5/5** | **5/5** | **5/5** (valid trials) |
| **Cost (5 reviews)** | $0.133 | **$0.019** (about 7x cheaper) | $0.148 (valid trials) |

## Experiment A (ADR-006): does the reviewer need the stronger model?

**Result: no difference in verdicts on this set.** Haiku got all five right for about one seventh of the cost.

Differences in quality:
- **Row attribution was less precise.** On S2, Haiku filed the cache bug under R5 ("risky change") as well as R4. Sonnet filed it under R1/R4, which is where it belongs.
- **Haiku also went deeper once.** On S3 it raised an extra R4 point: an old table handle can still cache stale results after the table is re-created. This is a real, related problem, but arguably beyond the issue.

**Negative result for ADR-006's assumption.** On single, clear defects, the stronger model bought nothing measurable. Not tested: the harder case from the issue runs, where Sonnet found a second, unreported instance of the bug (`update_multiple` in issue #2).

## Experiment B (ADR-008): does seeing the spec make the reviewer agree with the implementer?

**Result: no measurable agreement bias.** In all valid trials, the spec-reading reviewer reached the same verdict as the baseline, including on S4, where the spec explicitly lists the risky fsync removal as a requirement. The reviewer still failed R5 and noted that the issue says nothing about it. It judged the spec against the issue, not the other way round.

**Negative result for ADR-008's main worry**, at this sample size. Hiding the spec is still cheap and harmless, so the rule stays. The evidence for it is now "precaution", not "measured effect".

**Side finding:** reading the spec is optional, so one of six trials never read it. This happened because the guard denied a `cat` and the agent did not fall back to the Read tool. A future version should put the spec into the prompt for this variant, so that the treatment is guaranteed.

## Threats to validity
- n = 5 per variant, one run each. Model outputs vary between runs, so one flip would change a 5/5 into a 4/5.
- The defects and specs were written by the same person who wrote the rubric.
- With the spec seen in only 5 valid trials, a small bias could go undetected.
