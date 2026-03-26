#!/bin/bash
# Garry Dashboard Auto-Update — regenerates dashboards from live state and pushes to GitHub Pages
# Runs every 30 minutes via LaunchAgent

cd "$(dirname "$0")"

# Regenerate dashboards from live state
python3 generate.py 2>/dev/null

# Only push if something changed
if git diff --quiet index.html garry.html health.html 2>/dev/null; then
    exit 0
fi

# Commit and push
git add index.html garry.html health.html system-map.html
git commit -m "Auto-update $(date '+%Y-%m-%d %H:%M')" --quiet 2>/dev/null
git push --quiet 2>/dev/null

echo "Dashboards updated and pushed at $(date)"
