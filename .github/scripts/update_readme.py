#!/usr/bin/env python3
import os
import urllib.parse
from pathlib import Path

# Configuration
# Note: REPO_URL should be the raw domain for the proxy to work best
REPO_RAW_HOST = "raw.githubusercontent.com/adityastomar67/Wallpapers/main"
STATIC_DIR = "Static"
README_PATH = "README.md"

# Markers for auto-generated content
START_MARKER = "<!-- AUTO-GENERATED-STATIC-START -->"
END_MARKER = "<!-- AUTO-GENERATED-STATIC-END -->"

def generate_static_section():
    static_path = Path(STATIC_DIR)

    # Get all image files
    files = sorted([
        f for f in static_path.glob("*")
        if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']
    ])

    if not files:
        return ""

    # Start building the HTML Table
    html = "<table>\n"
    columns = 3

    # Process files in chunks of 3
    for i in range(0, len(files), columns):
        batch = files[i:i+columns]
        html += "  <tr>\n"

        for f in batch:
            # handle filenames with spaces
            safe_name = urllib.parse.quote(f.name)

            # 1. Direct Link (Opens the original large file)
            raw_url = f"https://{REPO_RAW_HOST}/{STATIC_DIR}/{safe_name}"

            # 2. Proxy Link (Resizes to 400x400 square for fast loading)
            thumb_url = f"https://wsrv.nl/?url={REPO_RAW_HOST}/{STATIC_DIR}/{safe_name}&w=400&h=400&fit=cover&a=attention&output=webp"

            html += f"""    <td align="center" width="33%">
      <a href="{raw_url}">
        <img src="{thumb_url}" alt="{f.stem}" width="100%">
      </a>
      <br><sub>{f.stem}</sub>
    </td>\n"""

        html += "  </tr>\n"

    html += "</table>"
    return html

def update_readme():
    if not os.path.exists(README_PATH):
        print(f"Error: {README_PATH} not found.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    # Generate the new grid content
    new_grid = generate_static_section()

    if START_MARKER in readme and END_MARKER in readme:
        # Split and inject the new grid between the existing markers
        before = readme.split(START_MARKER)[0]
        after = readme.split(END_MARKER)[1]
        new_content = f"{before}{START_MARKER}\n{new_grid}\n{END_MARKER}{after}"
    else:
        # Fallback: If markers are missing, append to the end
        print("Markers not found. Appending to end of file.")
        new_content = f"{readme}\n\n{START_MARKER}\n{new_grid}\n{END_MARKER}"

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("✅ README.md updated successfully with optimized grid!")

if __name__ == "__main__":
    update_readme()
