#!/usr/bin/env python3
"""Polish POAMS papers - fix metadata junk, basic cleanup."""
import re, sys, os

def clean_main(html):
    """Extract and clean main content."""
    m = re.search(r'(<main>)(.*?)(</main>)', html, re.DOTALL)
    if not m:
        return html, False
    
    main = m.group(2)
    original = main
    
    # Remove common metadata junk patterns
    junk_patterns = [
        r'<p>\s*D:\\[^<]*</p>\s*',  # D:\ file paths
        r'<p>\s*C:\\[^<]*</p>\s*',  # C:\ file paths
        r'<p>\s*Last printed[^<]*</p>\s*',
        r'<p>\s*Last saved[^<]*</p>\s*',
        r'<p>D:\\[^<]*Last saved by[^<]*</p>\s*',
        r'<p>\s*\?\s*C:\\[^<]*</p>\s*',  # ? C:\...
        r'<p>C:LAMIPRO[^<]*</p>\s*',
    ]
    
    for pat in junk_patterns:
        main = re.sub(pat, '', main)
    
    # Remove inline metadata junk
    main = re.sub(r'D:\\[A-Z][^<\n]*?\.doc\s*(?:Last saved by [A-Za-z ]+)?', '', main)
    
    changed = main != original
    if changed:
        html = html[:m.start()] + '<main>' + main + '</main>' + html[m.end():]
    
    return html, changed

files = sys.argv[1:]
for f in files:
    path = f
    with open(path, 'r') as fh:
        html = fh.read()
    html2, changed = clean_main(html)
    if changed:
        with open(path, 'w') as fh:
            fh.write(html2)
        print(f"CLEANED: {f}")
    else:
        print(f"no change: {f}")
