#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CENTRAL_SCRIPT="$(dirname "$SCRIPT_DIR")/stellar-harvest-ie-deployment/deployment/scripts/redeploy-service.sh"

if [[ ! -f "$CENTRAL_SCRIPT" ]]; then
  echo "Central redeploy script not found at: $CENTRAL_SCRIPT"
  echo "Make sure stellar-harvest-ie-deployment is cloned as a sibling of this module."
  exit 1
fi

exec bash "$CENTRAL_SCRIPT" "$@"