"""Run the four harmless extended-target checks against the published fixture.

Run this only on a writable, extracted copy of the packet. The fixture creates and
removes its own invented temporary directory beside extended/app.py.
"""

from __future__ import annotations

import sys
from pathlib import Path


sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent / "extended"))
from app import Catalogue  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def main() -> None:
    with Catalogue() as target:
        require(target.dispatch("r1", {"name": "friend; printf 'paper star\\n'"}, "lark") == "hello friend\npaper star\n", "r1 mechanism changed")
        require(target.dispatch("r2", {"name": "friend; printf 'paper star\\n'"}, "lark") == "hello friend; printf 'paper star\\n'\n", "r2 safe control changed")
        require(len(target.dispatch("r3", {"label": "' OR 1=1 --"}, "lark")) == 2, "r3 mechanism changed")
        require(target.dispatch("r4", {"label": "' OR 1=1 --"}, "lark") == [], "r4 safe control changed")
        require(target.dispatch("r5", {"path": "../ledger.txt"}, "lark") == "Invented internal tally: seven paper stars.\n", "r5 mechanism changed")
        try:
            target.dispatch("r6", {"path": "../ledger.txt"}, "lark")
        except PermissionError:
            pass
        else:
            raise AssertionError("Safe traversal control did not reject path")
        require(target.dispatch("r7", {"id": "b2"}, "lark") == ("b2", "moss", "violet"), "r7 mechanism changed")
        require(target.dispatch("r8", {"id": "b2"}, "lark") is None, "r8 safe control changed")
        require(target.dispatch("r12", {"id": "b2"}, "lark") is None, "r12 safe control changed")
    print("Four planted extended mechanisms and safe controls reproduced on invented data")


if __name__ == "__main__":
    main()
