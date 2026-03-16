#!/usr/bin/env python3
import os
import urllib.parse
from pathlib import Path

# Configuration
# Note: REPO_URL should be the raw domain for the proxy to work best
REPO_RAW_HOST = "raw.githubusercontent.com/adityastomar67/Wallpapers/main"
STATIC_DIR = "Static"
LIVE_DIR = "Live"
README_PATH = "README.md"

# Markers for auto-generated content
START_MARKER = "<!-- AUTO-GENERATED-STATIC-START -->"
END_MARKER = "<!-- AUTO-GENERATED-STATIC-END -->"
START_MARKER_LIVE = "<!-- AUTO-GENERATED-LIVE-START -->"
END_MARKER_LIVE = "<!-- AUTO-GENERATED-LIVE-END -->"

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
        batch = files[i:i+columns]  # type: ignore
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

def generate_live_section():
    live_path = Path(LIVE_DIR)

    # Get all video/gif files
    files = sorted([
        f for f in live_path.glob("*")
        if f.suffix.lower() in ['.mp4', '.webm', '.gif']
    ])

    if not files:
        return ""

    # Start building the HTML Table
    html = "<table>\n"
    columns = 1

    # Process files
    for i in range(0, len(files), columns):
        batch = files[i:i+columns]
        html += "  <tr>\n"

        for f in batch:
            # handle filenames with spaces
            safe_name = urllib.parse.quote(f.name)

            # Direct Link
            # Note: For GitHub to render videos properly in markdown, using the github.com/.../raw/main format
            # works much better than raw.githubusercontent.com which might not stream properly.
            # Example: https://github.com/adityastomar67/Wallpapers/raw/main/Live/video.mp4
            repo_base = "github.com/adityastomar67/Wallpapers/raw/main"
            raw_url = f"https://{repo_base}/{LIVE_DIR}/{safe_name}"

            html += f'    <td align="center" width="100%">\n'
            # Use img tag for gifs, video for mp4/webm
            if f.suffix.lower() == '.gif':
                html += f'      <img src="{raw_url}" alt="{f.stem}" width="100%">\n'
            else:
                html += f'      <video src="{raw_url}" muted autoplay loop controls width="100%"></video>\n'

            html += f'      <br><sub><a href="{raw_url}">{f.stem}</a></sub>\n'
            html += f'    </td>\n'

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
    new_grid_static = generate_static_section()
    new_grid_live = generate_live_section()

    # Update Static Section
    if START_MARKER in readme and END_MARKER in readme:
        before = readme.split(START_MARKER)[0]
        after = readme.split(END_MARKER)[1]
        readme = f"{before}{START_MARKER}\n{new_grid_static}\n{END_MARKER}{after}"
    else:
        print("Static markers not found. Appending to end of file.")
        readme = f"{readme}\n\n{START_MARKER}\n{new_grid_static}\n{END_MARKER}"

    # Update Live Section
    if START_MARKER_LIVE in readme and END_MARKER_LIVE in readme:
        before = readme.split(START_MARKER_LIVE)[0]
        after = readme.split(END_MARKER_LIVE)[1]
        readme = f"{before}{START_MARKER_LIVE}\n{new_grid_live}\n{END_MARKER_LIVE}{after}"
    else:
        print("Live markers not found. Appending to end of file.")
        readme = f"{readme}\n\n{START_MARKER_LIVE}\n{new_grid_live}\n{END_MARKER_LIVE}"

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme)

    print("✅ README.md updated successfully with optimized grids for Static and Live walls!")

if __name__ == "__main__":
    update_readme()
