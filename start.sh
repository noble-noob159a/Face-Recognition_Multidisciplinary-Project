#!/usr/bin/env bash
source .venv/bin/activate
python -m app.dashboard.app & python -m model.inference; wait
