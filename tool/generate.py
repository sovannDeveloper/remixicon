#!/usr/bin/env python3
"""Regenerate lib/remixicon.dart from fonts/remixicon.css.

Usage (from the repo root):  python3 tool/generate.py
Do NOT run `dart format` on the output; see KNOWLEDGE_BASE.md.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "fonts" / "remixicon.css"
OUT = ROOT / "lib" / "remixicon.dart"

# Dart identifiers cannot start with a digit.
EXCEPTIONS = {
    "24-hours-fill": "twenty_four_hours_fill",
    "24-hours-line": "twenty_four_hours_line",
    "4k-fill": "four_k_fill",
    "4k-line": "four_k_line",
}

css = CSS.read_text()
header = re.match(r"/\*.*?\*/", css, re.S).group(0).replace("-", "_")
icons = re.findall(r'\.ri-([a-z0-9-]+):before\s*\{\s*content:\s*"\\([0-9a-f]+)";', css)

lines = [header, "import 'package:flutter/widgets.dart';", "", "class Remix {", "  Remix._();", "",
         "  static const String _family = 'Remix';", "  static const String? _pkg = 'remixicon';", ""]
for name, hexcode in icons:
    ident = EXCEPTIONS.get(name, name.replace("-", "_"))
    decl = f"  static const IconData {ident} ="
    value = f"IconData(0x{hexcode}, fontFamily: _family, fontPackage: _pkg);"
    one = f"{decl} {value}"
    lines.append(one if len(one) <= 100 else f"{decl}\n      {value}")
lines.append("}")
OUT.write_text("\n".join(lines) + "\n")
print(f"Wrote {len(icons)} icons to {OUT.relative_to(ROOT)}")
