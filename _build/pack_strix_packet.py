"""Create a deterministic ZIP from the approved public Strix packet files."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


SITE = Path(__file__).resolve().parents[1]
ROOT = SITE / "research/strix-workflow-2026"
OUTPUT = SITE / "research/strix-workflow-2026.zip"
PUBLIC_FILES = (
    "README.md",
    "README.txt",
    "CLAIM-MAP.md",
    "CLAIM-MAP.txt",
    "TRACE-EXCERPT.md",
    "TRACE-EXCERPT.txt",
    "index.html",
    "run-ledger.json",
    "SHA256SUMS",
    "verify.py",
    "check_fixture.py",
    "oracle.json",
    "baseline/app.py",
    "baseline/instruction.txt",
    "extended/app.py",
    "extended/data.json",
    "extended/instruction.txt",
)


def main() -> None:
    with ZipFile(OUTPUT, "w") as archive:
        for relative in sorted(PUBLIC_FILES):
            path = ROOT / relative
            info = ZipInfo(relative, (1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    print(f"Wrote {OUTPUT} with {len(PUBLIC_FILES)} approved files")


if __name__ == "__main__":
    main()
