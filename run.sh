#!/usr/bin/env bash
# Legacy wrapper script for backward compatibility
# Use bin/devstral-container for more options

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

exec "${SCRIPT_DIR}/bin/devstral-container" "$@"
