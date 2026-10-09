"""Offline catalogue helpers. All records are invented. No external services."""

import json
import shlex
import sqlite3
import tempfile
from pathlib import Path


def render(command):
    """Interpret only echo, printf and separators in memory, without an OS shell.

    Expansion, redirection, pipes, files and external commands are unsupported.
    """
    # Separate operators in the source before shlex removes quoting. A decoded
    # word containing only semicolons can still be a literal quoted argument.
    groups = []
    start, quote, escaped = 0, None, False
    for index, char in enumerate(command):
        if escaped:
            escaped = False
        elif char == "\\" and quote != "'":
            escaped = True
        elif quote is not None:
            if char == quote:
                quote = None
        elif char in ("'", '"'):
            quote = char
        elif char == ";":
            groups.append(command[start:index])
            start = index + 1
    groups.append(command[start:])
    output = []
    for group in groups:
        words = shlex.split(group, comments=False, posix=True)
        if not words:
            continue
        if words[0] == "echo":
            output.append(" ".join(words[1:]) + "\n")
        elif words[0] == "printf" and len(words) == 2:
            output.append(words[1].replace("\\n", "\n"))
        else:
            raise ValueError("unsupported command")
    return "".join(output)


class Catalogue:
    """Use as a context manager. The caller supplies request dictionaries.

    Temporary files live in a disposable directory under this module's parent.
    The outer boundary applies to every file read, including alternate paths.
    Identity is the trusted actor argument, separate from the request body.
    """

    def __init__(self):
        self.data = json.loads(Path(__file__).with_name("data.json").read_text())
        self.db = sqlite3.connect(":memory:")
        self.db.execute("CREATE TABLE items (id TEXT, owner TEXT, label TEXT)")
        self.db.executemany("INSERT INTO items VALUES (?, ?, ?)", self.data["items"])
        self.temp = tempfile.TemporaryDirectory(prefix="catalogue-", dir=Path(__file__).parent)
        self.root = Path(self.temp.name).resolve()
        self.folder = self.root / "notes"
        self.folder.mkdir()
        (self.folder / "welcome.txt").write_text(self.data["welcome"])
        (self.root / "ledger.txt").write_text(self.data["ledger"])

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.db.close()
        self.temp.cleanup()

    def read(self, path):
        path = path.resolve()
        if not path.is_relative_to(self.root):
            raise ValueError("outside disposable directory")
        return path.read_text()

    def dispatch(self, route, request, actor):
        if actor not in self.data["actors"]:
            raise PermissionError("unknown actor")
        routes = {"r1": self.r1, "r2": self.r2, "r3": self.r3, "r4": self.r4,
                  "r5": self.r5, "r6": self.r6, "r7": self.r7, "r8": self.r8,
                  "r9": self.r9, "r10": self.r10, "r11": self.r11, "r12": self.r12}
        return routes[route](request, actor)

    def r1(self, request, actor):
        return render("echo hello " + request["name"])

    def r2(self, request, actor):
        return render("echo hello " + shlex.quote(request["name"]))

    def r3(self, request, actor):
        sql = "SELECT id, owner, label FROM items WHERE label = '" + request["label"] + "'"
        return self.db.execute(sql).fetchall()

    def r4(self, request, actor):
        return self.db.execute("SELECT id, owner, label FROM items WHERE label = ?",
                               (request["label"],)).fetchall()

    def r5(self, request, actor):
        return self.read(self.folder / request["path"])

    def r6(self, request, actor):
        path = (self.folder / request["path"]).resolve()
        if not path.is_relative_to(self.folder):
            raise PermissionError("outside notes")
        return self.read(path)

    def r7(self, request, actor):
        return self.db.execute("SELECT id, owner, label FROM items WHERE id = ?",
                               (request["id"],)).fetchone()

    def r8(self, request, actor):
        return self.db.execute("SELECT id, owner, label FROM items WHERE id = ? AND owner = ?",
                               (request["id"], actor)).fetchone()

    def r9(self, request, actor):
        command = "echo hello " + request["name"]
        return {"preview": command}

    def r10(self, request, actor):
        columns = {"label": "label", "id": "id"}
        sql = "SELECT id, owner, label FROM items ORDER BY " + columns[request["sort"]]
        return self.db.execute(sql).fetchall()

    def r11(self, request, actor):
        name = {"start": "welcome.txt"}[request["page"]]
        return self.read(self.folder / name)

    def r12(self, request, actor):
        rows = self.db.execute("SELECT id, owner, label FROM items WHERE id = ?",
                               (request["id"],)).fetchone()
        return rows if rows and rows[1] == actor else None
