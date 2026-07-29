# Output Schemas

Use these exact shapes. They exist so a reader can find the decision in five seconds and
so reports from different roles can be merged by the orchestrator without reformatting.

Rules that apply to all schemas:

- Fill every field. If a field does not apply, write `n/a` and why. Never delete a field.
- IDs are stable: `<ROLE>-<NNN>`, e.g. `SEC-004`, `ARCH-011`. Once assigned, never reused.
- `MUST-FIX` and `OPPORTUNITY` are never mixed in the same list.

---

## 1. `FINDING`

```
### [ID] Title in one line, stating the consequence
- Class: MUST-FIX | OPPORTUNITY
- Severity: S0 | S1 | S2 | S3
- Confidence: HIGH | MEDIUM | LOW
- Layer: architecture | domain | security | data | performance | ux | tests | delivery
- Owner role: architect | backend | frontend | database | security | qa | devops | product
- Evidence: path/to/file.ext:120-134  (or: command + relevant output)
- Impact: what breaks, for whom, under what conditions
- Trigger: the rule, defect or metric this violates
- Effort: XS | S | M | L | XL
- Risk of fixing: LOW | MEDIUM | HIGH
- Priority score: <number>  (see manual/06-matriz-de-priorizacao.md)
```

A finding without `Evidence` must be re-labelled `HYPOTHESIS` and moved to the open
questions list.

---

## 2. `CHANGE PROPOSAL`

Required before editing anything non-trivial.

```
## Proposal [ID]: <what changes>
Resolves: [FINDING-ID, ...]

### Problem as constraint
<one sentence, solution-free>

### Alternatives
| # | Approach | Cost | Risk | Reversibility | Return |
|---|----------|------|------|---------------|--------|
| A | ... | ... | ... | ... | ... |
| B | ... | ... | ... | ... | ... |
| C | Do nothing / accept risk | 0 | ... | full | ... |

### Decision
Chosen: <A|B|C>
Because: <the trade-off explicitly accepted>
Invalidated if: <the condition that would change this decision>

### Blast radius
Files: <n> | Modules: <list> | Public contracts touched: <none|list>
Migration required: <no|yes + plan>

### Verification plan
1. <exact command or test>
2. <regression scope>
3. <metric before → expected after, if performance>

### Rollback
<how to undo, and how long it takes>
```

---

## 3. `CHANGE REPORT`

After implementation and validation.

```
## Change [ID] — DONE | PARTIAL | REVERTED
Resolves: [FINDING-ID, ...]  |  Proposal: [PROPOSAL-ID]

Diff summary: <n files, +a/-b lines, modules touched>

### Verification performed
- <command> → <result>
- <test suite> → <pass/fail counts>
- <metric> → before X, after Y, method Z

### Definition of Done
<checklist from manual/08-definition-of-done.md, each item marked and justified if N/A>

### Residual risk
<what could still go wrong, and the monitoring that would catch it>

### Side effects observed
<none, or list>

### Follow-ups created
[BACKLOG-ID] <title> — <severity>
```

---

## 4. `AUDIT REPORT` (role 09 only)

```
# Audit — <module/PR> — <date>
Verdict: APPROVED | APPROVED WITH CONDITIONS | REJECTED

## Scores (0–10, each with a one-line justification)
| Dimension | Score | Justification |
|---|---|---|
| Architecture | | |
| Domain correctness | | |
| Security | | |
| Data | | |
| Performance | | |
| UX / Accessibility | | |
| Tests | | |
| Observability / Delivery | | |
| **Weighted total** | | |

## Regressions detected
[ID] <what regressed> — evidence — introduced by <change ID>

## Unmet Definition of Done items
## Conditions for approval  (if APPROVED WITH CONDITIONS)
## Residual risk accepted, and by whom
```

Scoring rules: a score of 10 requires meeting the Definition of Excellence, not merely the
absence of problems. Any `S0` or unfixed `S1` caps the weighted total at 4 and forces
`REJECTED`. Weights are defined in `manual/10-metricas-de-qualidade.md`.

---

## 5. `BLOCKED`

Use when a stop condition in `AGENTS.md §4` triggers.

```
## BLOCKED — <one line>
Stop condition: <which one>
What I established: <verified facts>
What I ruled out: <and how>
Options:
  A. <option> — cost, risk
  B. <option> — cost, risk
Recommendation: <A|B> because <reason>
Decision needed from: <human owner | other role>
```

---

## 6. `HANDOFF`

Between roles, via the orchestrator.

```
## Handoff → <target role>
Context: <the minimum they need, no history narration>
Evidence gathered: <paths, commands, outputs>
Question to answer: <one specific question>
Out of scope for them: <what not to touch>
Deadline gate: <which G-gate this blocks>
```

---

## 7. Final answer structure (any task)

```
<Outcome in 1–3 sentences: what happened / what you found>

<Supporting detail, ordered by importance>

MUST-FIX (blocks delivery)
1. ...

OPPORTUNITY (backlog)
1. ...

Not verified
- ...

Next step
<the single highest-value action>
```
