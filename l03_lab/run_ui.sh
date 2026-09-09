#!/usr/bin/env bash
# L03 — launch the Streamlit UI with the pinned venv (no segfault).
# Run:  ./run_ui.sh
cd "$(dirname "$0")"
if [ ! -x ".venv/bin/streamlit" ]; then
  echo "Creating venv and installing pinned requirements (one time)…"
  python3 -m venv .venv
  ./.venv/bin/pip install --upgrade pip
  ./.venv/bin/pip install -r requirements.txt
fi
# macOS ONNX/tokenizers deadlock fix (also set inside streamlit_ui.py as fallback).
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false
# Unbuffered logs so [Gold] encode/inserting/done lines appear immediately.
export PYTHONUNBUFFERED=1
exec ./.venv/bin/streamlit run streamlit_ui.py
