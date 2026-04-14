#!/bin/bash
# Garry Dashboard — Single source of truth for all dashboards
# Runs every 30 minutes via com.patrick.garry-dashboards LaunchAgent
#
# Pipeline: data-refresh.py → refresh-state.py → generate.py → git push

cd "$(dirname "$0")"
INFRA="/Users/patrickdickson/AI/Claude/Infrastructure"

# Step 1: Refresh ALL data files from live sources
python3 "$INFRA/data-refresh.py" 2>&1

# Step 2: Refresh CURRENT-STATE.md from updated data
python3 "$(dirname "$0")/refresh-state.py" 2>/dev/null

# Step 3: Regenerate ALL dashboards from fresh data
python3 generate.py 2>/dev/null

# Step 3b: Regenerate health dashboard from live health-summary.json
# health-dashboard-generator.py is the authoritative source — generate.py is now neutered for health.html
python3 "$INFRA/health-dashboard-generator.py" 2>/dev/null

# Step 4: Push ALL dashboard files + data directory
git add index.html garry.html health.html command-centre.html system-map.html health-data.json journey.html journey-data.json data/ 2>/dev/null

# Only push if something changed
if git diff --cached --quiet 2>/dev/null; then
    echo "No dashboard changes to push"
    exit 0
fi

git commit -m "Auto-update $(date '+%Y-%m-%d %H:%M')" --quiet 2>/dev/null
git push --quiet 2>/dev/null

echo "Dashboards updated and pushed at $(date)"
