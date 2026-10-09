# Claim map for the public packet

This packet separates facts readers can recompute from judgments that require private tool traces. Run `python3 verify.py` to check fixture hashes and counts.

| Article claim | Public check | Limit |
| --- | --- | --- |
| Four local models, six counted attempts each, plus one frozen cloud reference | `run-ledger.json`, `verify.py` | The excluded Orca auto-scope batch is preserved privately. |
| 24 local attempts, 21 completed, 3 failed | `run-ledger.json`, `verify.py` | Completion follows saved Strix status and operator exit records. |
| 14 local attempts with a structured findings file | `run-ledger.json`, `verify.py` | A file's presence is not finding validity. |
| Hinted target 10/12 filed; four-flaw target 4/12 filed | `run-ledger.json`, `verify.py` | The two targets differ in difficulty and instruction. |
| The planted mechanisms and safe controls | `baseline/app.py`, `extended/app.py`, `extended/data.json`, `oracle.json` | The oracle was outside the target shown to the agent. |
| Raw full-scope runtime settings and the first-batch annotation correction | Described in the article's methods note | Raw `run.json` files and both exports remain private because they contain operational paths and detail. |
| Orca's first corrected extended attempt exercised four mechanisms but filed two | `TRACE-EXCERPT.md`, fixture source, oracle | The excerpt is path-redacted and limited to one tool result. Full history and assessment remain private. |
| Other KAT, Qwen, Cyber, and Orca case-study judgments | Described in the article | Full tool traces and hash-bound manual assessments remain private. They are not independently reproducible from this public packet alone. |

No vulnerability count in this packet should be interpreted as a production efficacy rate. A missing findings file is an observed missing deliverable, not a clean scan.
