#!/usr/bin/env bash
# Resolve the DoD IL5 OSCAL profile to a fully-flattened catalog.
#
# Requires: oscal-cli  (https://github.com/metaschema-framework/oscal-cli)
# Install:
#   brew install oscal-cli      # macOS
#   # or download a release JAR from the GitHub releases page
#
# Usage:
#   ./scripts/resolve.sh
#
# Output:
#   build/dod-il5-rev5-resolved-catalog.json

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROFILE="${ROOT}/profiles/dod-il5-rev5-profile.json"
OUT_DIR="${ROOT}/build"
OUT_FILE="${OUT_DIR}/dod-il5-rev5-resolved-catalog.json"

mkdir -p "${OUT_DIR}"

if ! command -v oscal-cli >/dev/null 2>&1; then
  echo "ERROR: oscal-cli not found in PATH."
  echo "Install from: https://github.com/metaschema-framework/oscal-cli/releases"
  exit 1
fi

echo "==> Validating profile..."
oscal-cli profile validate "${PROFILE}"

echo "==> Resolving profile to catalog..."
oscal-cli profile resolve "${PROFILE}" "${OUT_FILE}" --to=json

echo "==> Validating resolved catalog..."
oscal-cli catalog validate "${OUT_FILE}"

echo ""
echo "Done. Resolved catalog: ${OUT_FILE}"
echo ""
python3 - <<PY
import json
c = json.load(open("${OUT_FILE}"))
ids = []
def walk(n):
    if 'controls' in n:
        for x in n['controls']:
            ids.append(x['id'])
            walk(x)
    if 'groups' in n:
        for g in n['groups']:
            walk(g)
walk(c['catalog'])
print(f"Resolved catalog contains {len(ids)} controls (incl. enhancements)")
PY
