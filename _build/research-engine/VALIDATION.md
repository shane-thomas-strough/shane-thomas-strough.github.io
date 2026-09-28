# Validation and delivery record

Measured 2026-09-27 EDT / 2026-09-28 UTC. No production writes or external search submissions.

| Check | Result |
|---|---|
| CONSENSUS focused SIGNAL, MIRROR, seam, enumeration, custody | 97 passed; sandbox-stalled run interrupted, permitted rerun passed; deprecation warnings |
| AEGIS research, goals, scheduled tasks, Sentinel | 43 passed |
| Edge attack and visibility scoring | 38 passed; sandbox pnpm database error resolved by permitted rerun |
| HELM lessons and lesson seam | 45 passed, 1 failed (local-date vs UTC assertion) |
| HELM failing test alone with TZ=UTC | passed; code remains unchanged |
| Workflow YAML and shell syntax | passed |
| IndexNow status branches 200/202/400/403/429/500 | all expected exit codes; no POST performed |
| Restricted Google submission endpoint/secret absent | passed |
| IndexNow endpoint retained | passed |
| Local HTML metadata census | 38 files including existing dirty draft; all contain expected basic metadata and parseable JSON-LD |
| Git whitespace check | passed |

## Commands

```bash
# CONSENSUS (97)
.venv/bin/python -m pytest -q tests/test_signal.py tests/test_mirror.py tests/test_aegis_seam.py tests/test_first_party_enumeration.py tests/test_evidence_custody.py
# AEGIS (43)
.venv/bin/python -m pytest -q tests/test_research.py tests/test_scheduled_tasks.py tests/test_goals.py tests/test_sentinel.py
# Current Edge (38)
pnpm --filter @elevare/scoring exec vitest run src/attack.test.ts src/visibility.test.ts
# HELM (45 pass / 1 fail)
.venv/bin/python -m pytest -q tests/test_lessons.py tests/test_lessons_seam.py
TZ=UTC .venv/bin/python -m pytest -q tests/test_lessons.py::test_source_identity_survives_aggregation
# This worktree
python3 _build/research-engine/check_indexing_workflow.py
python3 _build/research-engine/inventory.py --site ../shanestrough-com --consensus ../elevare-consensus --out /tmp/publication-inventory
```

## Live read-only observations

Direct HTTP, 2026-09-28 ~01:29–01:31 UTC:

* `https://shanestrough.com/stale-state.html`: GET 200.
* `https://shanestrough.com/sitemap.xml`: GET 200; 26 URLs, including both homepage aliases and the missing Poetry/Press routes.
* `https://shanestrough.com/robots.txt`: GET 200; `User-agent: *`, `Allow: /`, sitemap declaration.
* `https://shanestrough.com/poetry.html`: HEAD 404 (GitHub.com).
* `https://shanestrough.com/press.html`: GET 404.
* Browser/search fetch exposed Insights and The Comprehension Horizon, with a five-day crawl age; not counted as fresh direct HTTP indexing evidence.
* Local timer inspection: active; last trigger 2026-09-27 07:30:50 EDT; next 2026-09-28 07:25:41 EDT. Per-provider success not checked.

No live Search Console, Bing Webmaster, paid demand data, AI-provider visibility survey, AEGIS box health or performance analytics were accessed. The test counts do not claim full-suite or production commissioning.

## Source preservation and review

Worktree: `/home/s/projects_root/shanestrough-research-engine`.
Branch: `research/publication-engine-recon`.
Base: `7fe2bd235c4eaaa2300bc91a0e7d013cd5b913b0`.

The original website worktree's `insights.html`, `sitemap.xml`, untracked Bake-Off files and image were preserved. AEGIS/current Edge ahead commits and AEGIS untracked benchmark outputs were not touched. Historical Edge was cloned read-only under `/tmp`.

All changes are local on this branch. No remote PR, merge, publish or deploy. The reconnaissance includes cross-system architectural information; inspect it before deciding whether to place it in the public website repository. `_build/` exclusion from Pages is not repository confidentiality.

Final commit identifiers are available with `git log -2 --oneline research/publication-engine-recon` and in the mission return.
