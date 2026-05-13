#!/usr/bin/env bash
source .venv/bin/activate
py -3.11 -m app.dashboard.app & py -3.11 -m model.inference; 