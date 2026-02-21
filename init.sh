#!/bin/bash

set -e  # Exit immediately if a command fails

echo "Detecting Python version..."

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")

echo "Python version detected: $PYTHON_VERSION"

echo "Installing required venv package if not installed..."
sudo apt update
sudo apt install -y python$PYTHON_VERSION-venv python3-pip

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting FastAPI server..."
uvicorn app:app --reload