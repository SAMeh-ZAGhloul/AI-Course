#!/bin/bash
# Launch the ENHANCED educational Streamlit UI
# Usage: ./run_ui_enhanced.sh

set -e

# Get the directory where this script lives
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create venv if needed
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python venv..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
python -m pip install -q -r requirements.txt

# Add extra deps for enhanced visualization (optional but recommended)
if ! python -c "import plotly" 2>/dev/null; then
    echo "📊 Installing Plotly for visualizations..."
    python -m pip install -q plotly
fi

if ! python -c "import sklearn" 2>/dev/null; then
    echo "🔬 Installing scikit-learn for embedding projection..."
    python -m pip install -q scikit-learn
fi

# Set macOS environment variables to avoid onnx deadlock
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export TOKENIZERS_PARALLELISM=false

# Run the enhanced UI
echo ""
echo "🚀 Starting Enhanced Educational RAG Lab UI..."
echo "📍 Open http://localhost:8501 in your browser"
echo ""

streamlit run streamlit_ui_enhanced.py
