"""Verify the public Strix field-study packet and reproduce artifact counts.

Run: python3 verify.py
This checks published fixture hashes and ledger arithmetic. It cannot independently
verify the private raw tool traces or the human assessment of individual findings.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_LOCAL = 24
EXPECTED_REFERENCE = 1


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    for line in (ROOT / "SHA256SUMS").read_text().splitlines():
        if not line.strip():
            continue
        expected, relative = line.split(maxsplit=1)
        path = ROOT / relative.removeprefix("*")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == expected, f"Hash mismatch: {relative}")

    ledger = json.loads((ROOT / "run-ledger.json").read_text())
    runs = ledger["runs"]
    local = [run for run in runs if run["cohort"] == "local"]
    reference = [run for run in runs if run["cohort"] == "cloud_reference"]
    require(len(local) == EXPECTED_LOCAL, "Local attempt count changed")
    require(len(reference) == EXPECTED_REFERENCE, "Reference count changed")
    require(len({run["model"] for run in local}) == 4, "Expected four local models")
    require(Counter(run["model"] for run in local) == {model: 6 for model in {r["model"] for r in local}}, "Each local model must have six attempts")

    completed = sum(run["status"] == "completed" for run in local)
    failed = sum(run["status"] == "failed" for run in local)
    filed = sum(run["finding_count"] is not None for run in local)
    baseline = [run for run in local if run["suite"] == "baseline"]
    extended = [run for run in local if run["suite"] == "extended"]
    require((completed, failed, filed) == (21, 3, 14), "Status or findings-file totals changed")
    require((len(baseline), len(extended)) == (12, 12), "Suite denominators changed")
    require(sum(run["finding_count"] is not None for run in baseline) == 10, "Baseline filing count changed")
    require(sum(run["finding_count"] is not None for run in extended) == 4, "Extended filing count changed")

    print("Fixture and instruction hashes: verified")
    print(f"Observations: {len(runs)} ({len(local)} local, {len(reference)} frozen reference)")
    print(f"Local status: {completed} completed, {failed} failed")
    print(f"Structured findings files: {filed} of {len(local)} local attempts")
    print("Hinted target: 10 of 12 filed; four-flaw target: 4 of 12 filed")
    print("These are artifact counts, not finding-accuracy scores.")


if __name__ == "__main__":
    main()
