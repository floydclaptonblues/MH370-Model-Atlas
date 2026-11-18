#!/usr/bin/env python3
"""The published site is built by GitHub Pages, which passes every Markdown file
through a template engine. An opening double brace or a brace-percent pair in a
Markdown file is read as template syntax; an unterminated one stops the whole
site build. This check fails if any tracked Markdown file contains either."""
import json, subprocess, sys

files = subprocess.run(["git", "ls-files", "*.md"], capture_output=True, text=True, check=True).stdout.split("\n")
bad = []
for f in filter(None, files):
    text = open(f, encoding="utf-8", errors="replace").read()
    for i, line in enumerate(text.split("\n"), 1):
        if "{" + "{" in line or "{" + "%" in line:
            bad.append(dict(file=f, line=i))
print(json.dumps(dict(markdown_files_checked=len([f for f in files if f]), template_syntax=bad, passed=not bad), indent=2))
sys.exit(1 if bad else 0)
