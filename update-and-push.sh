#!/bin/bash
# Garry Dashboard Auto-Update — regenerates dashboards from live state and pushes to GitHub Pages
# Runs every 30 minutes via LaunchAgent

cd "$(dirname "$0")"

# Step 1: Refresh CURRENT-STATE.md from live data (ALWAYS before generating)
python3 "$(dirname "$0")/refresh-state.py" 2>/dev/null || \
  python3 /Users/patrickdickson/AI/Claude/Infrastructure/garry-dashboards/refresh-state.py 2>/dev/null

# Step 2: Regenerate dashboards from live state
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
