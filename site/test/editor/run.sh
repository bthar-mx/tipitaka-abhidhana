#!/bin/sh
# Test editor mode locally (docs/editor-mode.md §6): build the site, serve it with `wrangler pages dev`
# and an empty local D1, stand in for Cloudflare Access, run the API and browser tests. Everything
# goes to a temporary folder; nothing in the repository changes.
#   sh site/test/editor/run.sh            (needs node, npx and Playwright with a Chromium)
# Env: WRANGLER (default: npx --yes wrangler@4), PLAYWRIGHT (module path), CHROME (browser binary),
#      ABH_FONTS (a folder with fonts.css and its .woff2 files, used instead of Google Fonts; for a machine offline).
set -e
REPO=$(cd "$(dirname "$0")/../../.." && pwd)
HERE="$REPO/site/test/editor"
W=$(mktemp -d); export TMPDIR="$W" SHOTS="$W"
WR=${WRANGLER:-"npx --yes wrangler@4"}
echo "work folder: $W"
ABHIDHANA_SITE_OUT="$W/dist" python3 "$REPO/tools/abhidhana_site.py" | tail -1
mkdir -p "$W/pg" && cd "$W/pg"
ln -s "$REPO/functions" functions && ln -s "$W/dist" dist
cat > wrangler.toml <<TOML
name = "abhidhana-editor-test"
pages_build_output_dir = "dist"
compatibility_date = "2026-09-01"
[[d1_databases]]
binding = "DB"
database_name = "abhidhana-edits"
database_id = "00000000-0000-0000-0000-000000000000"
[vars]
ACCESS_TEAM_DOMAIN = "http://127.0.0.1:8799"
ACCESS_AUD = "test-aud"
TOML
$WR d1 execute abhidhana-edits --local --persist-to "$W/state" --file "$REPO/site/d1/schema.sql" > /dev/null
node "$HERE/access-mock.js" > "$W/mock.log" 2>&1 & MOCK=$!
$WR pages dev --port 8788 --persist-to "$W/state" > "$W/dev.log" 2>&1 & DEV=$!
trap 'kill $MOCK $DEV 2>/dev/null' EXIT
i=0; until curl -s -o /dev/null http://127.0.0.1:8788/data/version.json; do i=$((i+1)); [ $i -gt 60 ] && { tail "$W/dev.log"; exit 1; }; sleep 2; done
node "$HERE/api-test.js"
node "$HERE/ui-test.js"
echo "screenshots in $W"
