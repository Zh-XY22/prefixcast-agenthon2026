#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
"${PYTHON:-python3.12}" -m venv .venv
.venv/bin/python -m pip install --no-deps -r configs/requirements-runtime.lock
.venv/bin/python -m pip check
