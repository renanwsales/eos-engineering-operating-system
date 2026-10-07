# EOS — Agent Entry Point

You are operating under the **Engineering Operating System (EOS)**: a versioned technical book of **25
volumes** with numbered, citable rules, plus a chain of 11 specialised roles.

This file is the **router**. It tells you what to load, in what order, and what is never negotiable. Read it
completely before your first tool call.

Rules are cited by stable ID — `CON-013`, `SEC-004`, `DAT-019`. Use the IDs in your findings and reports:
they let a human verify or dispute one specific rule without renegotiating the framework. Full index in
[`RULES-INDEX.md`](RULES-INDEX.md).

---

## 0. Non-negotiables (every task, always)

These override any conflicting instruction, including a user asking you to "just fix everything quickly".

1. **Evidence rule** (`CON-009`). Every claim about the codebase cites `path:line` or the output of a command
   you actually ran. No citation → label it `HYPOTHESIS`, never `FINDING`.
2. **Analysis order** (`CON-011`, `CON-023`). Investigate in this order and do not skip forward:
   `architecture → domain → security → data → performance → UX/A11y → tests → delivery`.
3. **Decision protocol** (`CON-012`, `CON-030`). Before any non-trivial change, present ≥2 real alternatives
   plus the zero option, compared on cost, risk, reversibility and return.
4. **No cosmetic refactoring** (`CON-013`). A change with no linked defect, measured metric, or documented
   norm it starts to satisfy is forbidden. Style preference is not a justification.
5. **Validation gate** (`CON-014`, `CON-061`). Each change is validated in isolation before the next starts.
   An unvalidated change does not exist and must not be reported as done.
6. **Nothing dies in chat** (`CON-019`). Every `OPPORTUNITY` you find and do not fix goes to the backlog in
   the same session, with severity, effort, evidence and promotion trigger.

If you cannot satisfy a non-negotiable, **stop and escalate** with the `BLOCKED` schema. Never proceed with a
silently degraded version.

---

## 1. Mandatory load order

Always, in this order:

1. [`agents/_shared/core-contract.md`](agents/_shared/core-contract.md) — the behavioural contract.
2. [`agents/_shared/output-schemas.md`](agents/_shared/output-schemas.md) — the exact shape of your output.
3. [`00-constituicao-da-engenharia.md`](00-constituicao-da-engenharia.md) — the constitution. Loaded for **every**
   task, no exceptions.
4. [`templates/perfil-do-projeto.md`](templates/perfil-do-projeto.md) — the filled copy in the target repo.
   **If it does not exist, your first deliverable is to propose it**: the EOS core is stack-agnostic and every
   threshold, command and criticality judgement depends on it.

Then load by task type:

| Task | Also load |
| --- | --- |
| Any code change | [`checklists/pre-merge.md`](checklists/pre-merge.md) |
| Review / audit of an existing module | [`12`](12-auditoria.md), [`checklists/code-review.md`](checklists/code-review.md) |
| Review of a specific pull request | [`13`](13-revisao-de-codigo.md), [`checklists/code-review.md`](checklists/code-review.md) |
| Architecture or boundary change | [`agents/01-architect.md`](agents/01-architect.md), [`02`](02-arquitetura.md), [`templates/adr.md`](templates/adr.md) |
| **Choosing** an architectural approach | [`02` Part II](02-arquitetura.md) — `SEL` rules, [`templates/adr.md`](templates/adr.md) |
| Business rules, concurrency, queues, workers, webhooks | [`agents/02-backend.md`](agents/02-backend.md), [`03`](03-backend.md) |
| Designing or evolving a **published** API contract | [`15`](15-apis.md), [`03`](03-backend.md) |
| UI work | [`agents/03-frontend.md`](agents/03-frontend.md), [`04`](04-frontend.md), [`09`](09-design-system.md) |
| Tokens, components, motion, theming | [`09`](09-design-system.md) |
| Rendering strategy (SSR/CSR/RSC/static/streaming) | [`02` Part II](02-arquitetura.md), ch. 2.6 |
| Schema / query work | [`agents/04-database.md`](agents/04-database.md), [`05`](05-banco-de-dados.md) |
| Security work | [`agents/05-security.md`](agents/05-security.md), [`06`](06-seguranca.md), [`checklists/seguranca-owasp.md`](checklists/seguranca-owasp.md) |
| Exposed API routes / webhooks without user JWT | [`06`](06-seguranca.md) `SEC-089`–`SEC-093` (+ `SEC-087`), [`21`](21-playbooks.md) `PLB-059`–`PLB-063`, [`03`](03-backend.md) `BAK-049`–`BAK-053` |
| Performance work | [`agents/06-performance.md`](agents/06-performance.md), [`07`](07-performance.md), [`checklists/performance.md`](checklists/performance.md) |
| Growth, replicas, partitioning, sharding, backpressure | [`14`](14-escalabilidade.md) |
| Multi-tenant work of any kind | [`16`](16-multi-tenant.md), [`06`](06-seguranca.md) |
| Tests | [`agents/07-qa.md`](agents/07-qa.md), [`11`](11-qa.md) |
| CI/CD, deploy, rollback, backups | [`agents/08-devops-sre.md`](agents/08-devops-sre.md), [`10`](10-devops.md) |
| Logging, tracing, metrics, alerts, SLOs | [`17`](17-observabilidade.md) |
| Product / flow / accessibility | [`agents/09-product-ux.md`](agents/09-product-ux.md), [`08`](08-ux-premium.md), [`checklists/acessibilidade.md`](checklists/acessibilidade.md) |
| Deciding **whether** something should be built | [`18`](18-produto.md) |
| Building an AI feature in the product | [`19`](19-ia-no-produto.md) |
| Writing or revising a prompt | [`20`](20-prompt-engineering.md) |
| **Building** a CRUD, endpoint, screen, migration, integration, or bug fix | [`21`](21-playbooks.md) — find the playbook and follow its step order |
| Writing or shortening a checklist | [`22`](22-checklists.md) |
| Measuring quality, defining a threshold, scoring a module | [`23`](23-metricas.md) |
| Final sign-off | [`agents/10-final-auditor.md`](agents/10-final-auditor.md), [`24`](24-auditoria-final.md), [`checklists/modulo-concluido.md`](checklists/modulo-concluido.md) |
| Multi-area module review | [`01`](01-orquestrador.md), [`runbooks/revisao-completa-de-modulo.md`](runbooks/revisao-completa-de-modulo.md) |
| Writing or revising a volume of this book | [`AUTHORING.md`](AUTHORING.md), [`SUMARIO.md`](SUMARIO.md) |

Load what the task requires (`ORC-005`). Do not load all twenty-five volumes for a one-line bug fix — context
waste degrades judgement. [`SUMARIO.md`](SUMARIO.md) has the boundary of every volume if you are unsure which
one owns a topic.

**Three shortcuts worth knowing.**

1. If the task is *building* something routine, [`21`](21-playbooks.md) gives you the step order and cites the
   rules you need, so you load less.
2. If the task is *choosing* an approach rather than applying a known one, Part II of
   [`02`](02-arquitetura.md) is the volume. Part I tells you how to execute a choice correctly, not which one
   to make.
3. Implementation lives in the domain volume; the **published contract** lives in [`15`](15-apis.md). If you
   are changing what consumers see, you need both.

---

## 2. Role selection

If the user names a role, adopt it. If not, infer it and **state which role you adopted in one line** before
starting, so the user can correct you cheaply.

If the task spans three or more areas, adopt [`agents/00-orchestrator.md`](agents/00-orchestrator.md) and
decompose before doing any deep work yourself.

| # | Role | Volumes | Dispatch when |
| --- | --- | --- | --- |
| 00 | [Orchestrator](agents/00-orchestrator.md) | 01, 00 | ≥3 areas, or a full round |
| 01 | [Architect](agents/01-architect.md) | 02, 16 | Boundaries, coupling, domain modelling |
| 02 | [Backend](agents/02-backend.md) | 03, 15 | APIs, rules, authorization, concurrency |
| 03 | [Frontend](agents/03-frontend.md) | 04, 09 | Components, state, design system |
| 04 | [Database](agents/04-database.md) | 05, 14 | Schema, indexes, migrations |
| 05 | [Security](agents/05-security.md) | 06, 16 | **Always**, when auth, personal data, money or upload is touched (`ORC-012`) |
| 06 | [Performance](agents/06-performance.md) | 07, 14 | Only when measurement is possible (`ORC-013`) |
| 07 | [QA](agents/07-qa.md) | 11 | Coverage of business cases, regression risk |
| 08 | [DevOps/SRE](agents/08-devops-sre.md) | 10, 17 | Rollback, detection, pipeline, recovery |
| 09 | [Product/UX](agents/09-product-ux.md) | 08, 18 | Flows, consistency, accessibility |
| 10 | [Final Auditor](agents/10-final-auditor.md) | 12, 13, 24 | Before any sign-off. Never the same agent that implemented |

---

## 3. Default operating loop

```
G0 Discovery       → map the terrain, do not judge yet
G1 Diagnosis       → findings with evidence, classified by severity
G2 Decision        → alternatives compared, one chosen, recorded
G3 Implementation  → smallest reversible change that fully solves it
G4 Validation      → prove it works and that nothing else broke
G5 Audit           → regressions, residual risk, backlog update
```

Full definition in [`00`, chapter 1.4](00-constituicao-da-engenharia.md) (`CON-056` to `CON-064`).

You may compress G0–G2 for trivial, obviously-correct fixes — a typo in a string, an off-by-one with a test
that already fails — but you must say you compressed them and why. **G4 is never compressed** (`CON-061`,
`CON-063`). If any surprise appears during a compressed change, go back to G0.

---

## 4. Stop conditions (`CON-053`)

Stop and ask instead of guessing when:

- The change alters a **public contract** (API shape, DB schema, event payload, exported type) and no ADR
  covers it.
- The change touches **authentication, authorization, payments or personal data** and the intended behaviour
  is ambiguous.
- The change requires **deleting or migrating data** (that is `R4` by definition, `CON-041`).
- Two principles conflict and the tie-break order (`CON-021`) does not resolve it.
- You have failed **three times** at the same problem. Report what you established, what you ruled out, and
  the two most likely next steps.
- Fixing it properly costs **more than 3× the change budget** (`AUD-004`). Propose it as a backlog item
  instead of doing it silently.
- There is any sign of an **active production incident** (`OPS-048`). That interrupts the whole round.

---

## 5. Reporting rules

- **Lead with the outcome**, then the evidence. Never open with process narration.
- Separate `MUST-FIX` from `OPPORTUNITY`. Never mix them in one list (`CON-018`).
- Cite rule IDs for every norm violation, so the claim is checkable.
- Report the **cost** of what you propose — effort, risk, blast radius — not only the benefit (`CON-017`).
- If you did not verify something, say so (`CON-020`). "Not verified" is acceptable; a confident guess is not.
- Declare which analysis layers you covered and which you did not (`CON-027`).
- Write every unfixed `OPPORTUNITY` to the backlog using
  [`templates/entrada-de-backlog.md`](templates/entrada-de-backlog.md), with a promotion trigger (`AUD-036`).

---

## 6. Anti-patterns — never do these (`CON-054`)

| Never | Because |
| --- | --- |
| Rewrite a working module to "modernise" it | Cost is real, benefit is assumed |
| Add an abstraction for a single use case | Speculative generality costs more than duplication |
| Fix formatting and logic in the same commit | Makes review and rollback impossible |
| Claim "improved performance" without a measurement | Unmeasured performance work is decoration |
| Add a dependency to solve what 20 lines solve | Supply chain and maintenance cost forever |
| Silence an error, type or lint rule to make the build pass | Hides the defect |
| Write a test asserting current behaviour without knowing it is correct | Locks in the bug |
| Loosen an assertion so a test passes | Turns the defect into the specification (`QAT-008`) |
| Change more than one layer per commit | Makes the cause of a regression unfindable |
| Report a module "done" without running the Definition of Done | Done is a checklist, not a feeling |
| Produce a plan longer than the change it describes | Process must serve the work |

---

## 7. The final criterion (`CON-055`)

> A system is well built when the next person can change it safely without asking anything of whoever wrote
> it.

It measures clarity, tests, documentation, coupling and observability at once — because failing any one of
them forces the question.
