# Companion materials for The finding is not the report

This companion packet accompanies the October 2026 Strix field study. The files contain invented code and a sanitized outcome ledger; they do not contain raw agent transcripts, server logs, host paths, credentials or private owner data.

## Contents

- `baseline/app.py` and `baseline/instruction.txt`: the exact known-flaw target and the instruction supplied separately to Strix.
- `extended/app.py`, `extended/data.json`, and `extended/instruction.txt`: the exact four-flaw target and its separate instruction.
- `oracle.json`: the answer key used outside the scan target. Never mount it in the target shown to the agent.
- `run-ledger.json`: the frozen subscription reference plus twenty-four counted local attempt outcomes, exported from the current saved operator files and Orca's corrected full-scope batch. `finding_count: null` means no structured findings file, not zero vulnerabilities.
- `SHA256SUMS`: hashes of the six fixture, instruction and oracle files.
- `verify.py`: standard-library checker for those hashes and the published run counts. Run `python3 verify.py` from this directory.
- `check_fixture.py`: harmless execution of the four planted extended mechanisms and their safe controls. Run `python3 check_fixture.py` on a writable extracted copy; it creates and removes an invented temporary directory.
- `CLAIM-MAP.md`: which published numbers the ledger can reproduce, and which judgments require private raw traces.
- `TRACE-EXCERPT.md`: one path-redacted tool-result excerpt and its private history hash, showing four tested mechanisms but two structured reports.

## Reproduction boundary

The tests used Strix standalone CLI v1.7.0, SHA256 `099a5f8aa726aba409d8ed1435aff539888ba2fa03f8d9e4daed6391ef1dde17`, and sandbox image digest `sha256:f6906c3114e504fd1a218fcf028d7a0e46851118403a438b63956de6ea7c4331`. Local inference used llama.cpp build `0.2.0-dev build473 commit f280b26`, server binary SHA256 `1d9a85cfad4ca20485423eaff6aa988b675ece5239f95024e9d4b3b5ac2ece32`, RTX 5090, 98,304-token context, Q8 key/value cache, one parallel slot, temperature 0.2, top-p 0.95, top-k 20, seed 42, and disabled thinking. The first three local models were Q4_K_M GGUF files; Orca was IQ4_XS. Their SHA256 values were:

| Model | SHA256 |
| --- | --- |
| KAT-Coder V2.5 Dev 35B-A3B Philadelphia | `ba33e8f1ab6c5da48510f89f327f6a6e9496d6454942968deea8a81aa49a1b60` |
| Qwen3.6 35B-A3B heretic | `fc89d92377b27fe0f80eb683a5105d0921234c24f7c1d70ecc2356ddf994d781` |
| Qwen3.8 27B Uncensored Cyber | `9ea57a2c912934bc39369b8988cf7f9b267f1a4d13d3cb6af38310c212986b98` |
| OrcaSAQ-2 Cyber 27B | `4ab6bdf8a9008869abf1630fb92d04b5439805f96b56692962fa240b1d439977` |

Each local candidate had three planned known-flaw attempts and three planned four-flaw attempts. Every attempt used a new target copy, quick scan, full scope, noninteractive mode, 20 turns per agent, and nominal budget 1. Full-prompt context fit and a harmless tool-call round trip were required before measured attempts. Failures kept their planned slots. Raw transcripts remain private, so this packet allows inspection of the fixtures and outcomes but not independent verification of every manual reproduction judgment.

The subscription reference used GPT-6.1 Sol once through a different transport and tokenizer. Do not pool its token counters or nominal cost with the local runs. The older saved summary predated a correction to first-batch operator annotations. Its own `actual_settings` and the raw Strix run records already showed full scope and inactive diff scope for all 18 first-batch attempts. The combined export finds two readable local triplets, Qwen3.8 Cyber and Orca on the known-flaw target. The old export and metadata-correction audit are preserved privately.

An initial Orca batch accidentally used `scope_mode:auto`. Those six attempts are preserved privately but excluded here. Six new targets were used for the corrected `--scope-mode full` batch counted in this packet. Its third four-flaw attempt failed after reaching the server context limit during a malformed tool call. Its second four-flaw attempt completed but delivered no structured findings file.

The baseline is explicitly hinted and cannot test blind discovery. The extended interpreter accepts only a bounded echo/printf language and cannot establish OS-shell command execution. Three attempts on two invented targets do not estimate production security efficacy. A missing structured report is not a clean scan.
