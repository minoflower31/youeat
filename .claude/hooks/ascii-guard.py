#!/usr/bin/env python3
"""PostToolUse guard for Edit/Write: enforces CLAUDE.md Plain ASCII on the text just written to a code file.

Reports non-ASCII emoji and symbol characters (Unicode So, Sk, Sm). Korean and other letters stay allowed.
Checks only the written text, not the whole file, so it never asks to touch lines the edit left alone.
Exit 2 hands the report back to Claude, which fixes the file before moving on.
"""

import json
import sys
import unicodedata
from pathlib import Path

DOC_SUFFIXES = {".md", ".txt"}
SYMBOL_CATEGORIES = {"So", "Sk", "Sm"}


def written_text(tool_input):
    if "content" in tool_input:
        return tool_input["content"]
    edits = tool_input.get("edits") or [tool_input]
    return "\n".join(e.get("new_string", "") for e in edits)


def symbol_hits(text):
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        bad = sorted({ch for ch in line if ord(ch) > 127 and unicodedata.category(ch) in SYMBOL_CATEGORIES})
        if bad:
            hits.append(f"line {n} of the written text: " + " ".join(f"{c} U+{ord(c):04X}" for c in bad))
    return hits


def main():
    try:
        tool_input = json.load(sys.stdin).get("tool_input") or {}
    except json.JSONDecodeError:
        return 0
    path = Path(tool_input.get("file_path", ""))
    if not path.suffix or path.suffix in DOC_SUFFIXES:
        return 0
    hits = symbol_hits(written_text(tool_input))
    if not hits:
        return 0
    print(f"Plain ASCII (CLAUDE.md): {path} got emoji or symbol characters. Replace them with ASCII. "
          "When a string must carry one, the file must hold its six-character ASCII escape: one backslash, "
          "u, four hex digits (U+2705 -> \\u2705). Read the line back to confirm, because an escape typed "
          "into the tool input can arrive as the character itself or with two backslashes.\n"
          + "\n".join(hits[:20]), file=sys.stderr)
    return 2


if __name__ == "__main__":
    assert symbol_hits('a = "취소 완료 ✅";') == ["line 1 of the written text: ✅ U+2705"]
    assert symbol_hits('a = "취소 완료 \\u2705"; // 한글 -> ok') == []
    assert symbol_hits("x ≤ y → z") == ["line 1 of the written text: → U+2192 ≤ U+2264"]
    sys.exit(main())
