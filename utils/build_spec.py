#!/usr/bin/env python3
"""Compile SPEC_TEMPLATE.md + sections/ into SPEC.md."""
import re
import sys
import runpy
from pathlib import Path

docs_dir = Path(__file__).parent.parent

runpy.run_path(str(docs_dir / "utils" / "build_appendix_b.py"))
template_path = docs_dir / "SPEC_TEMPLATE.md"
output_path = docs_dir / "SPEC.md"
pattern = re.compile(r"^\{\{>\s*(.+?)\s*\}\}\s*$")
autogen_comment = re.compile(r"<!--\s*AUTO-GENERATED\b.*?-->\n?")

lines = []
with open(template_path, encoding="utf-8") as f:
    for line in f:
        m = pattern.match(line.rstrip("\n"))
        if m:
            include_path = docs_dir / m.group(1).strip()
            if not include_path.exists():
                print(f"ERROR: include not found: {include_path}", file=sys.stderr)
                sys.exit(1)
            content = include_path.read_text(encoding="utf-8")
            content = autogen_comment.sub("", content)
            lines.append(content if content.endswith("\n") else content + "\n")
        else:
            lines.append(line)

output_path.write_text("".join(lines), encoding="utf-8")
print(f"Built {output_path} ({output_path.stat().st_size} bytes)")
