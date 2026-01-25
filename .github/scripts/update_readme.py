#!/usr/bin/env python3
import os
from pathlib import Path

REPO_URL = "raw.githubusercontent.com/adityastomar67/Wallpapers/main"
STATIC_DIR = "Static"
README_PATH = "README.md"

# Markers for auto-generated content
START_MARKER = "<!-- AUTO-GENERATED-STATIC-START -->"
END_MARKER = "<!-- AUTO-GENERATED-STATIC-END -->"

def generate_static_section():
    static_path = Path(STATIC_DIR)
    files = sorted(static_path.glob("*"))
    images_html = "\n".join([
        f"    <img src='https://wsrv.nl/?url={REPO_URL}/{STATIC_DIR}/{f.name}&w=400&output=webp' alt='{f.stem}'>"
        for f in files if f.suffix.lower() in ['.jpg', '.jpeg', '.png']
    ])
    section = f"<span>\n{images_html}\n  </span>"
    return section

def update_readme():
    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    if START_MARKER in readme and END_MARKER in readme:
        before = readme.split(START_MARKER)[0]
        after = readme.split(END_MARKER)[1]
        new_content = f"{before}{START_MARKER}\n{generate_static_section()}\n{END_MARKER}{after}"
    else:
        # If no markers, just append at the end
        new_content = f"{readme}\n\n{START_MARKER}\n{generate_static_section()}\n{END_MARKER}"

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("✅ README.md updated successfully!")

if __name__ == "__main__":
    update_readme()

