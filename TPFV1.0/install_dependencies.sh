#!/bin/bash
# Automated installation script for Talking Photo Frame V1.0

echo "=== Talking Photo Frame V1.0 Setup ==="
echo

# Check if running on Raspberry Pi
if ! command -v raspi-config &> /dev/null; then
    echo "Warning: This script is optimized for Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    ffmpeg \
    alsa-utils \
    python3-venv \
    python3-pip

# Create project directory
PROJECT_DIR="$HOME/talking-photo-frame"
echo "Creating project directory at $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Create env1
echo "Creating virtual environment 1 (S2T/T2S)..."
python3 -m venv env1
source env1/bin/activate
pip install --upgrade pip
pip install SpeechRecognition==3.10.0
pip install PyAudio==0.2.13
pip install googletrans==4.0.0rc1
pip install gtts==2.3.2
pip install pygame==2.5.2
deactivate
echo "✓ env1 created"

# Create env2
echo "Creating virtual environment 2 (NLP)..."
python3 -m venv env2
source env2/bin/activate
pip install --upgrade pip
pip install openai==1.3.0
deactivate
echo "✓ env2 created"

echo
echo "=== Setup Complete ==="
echo
echo "Next steps:"
echo "1. Copy your Python scripts to $PROJECT_DIR"
echo "2. Copy your video file (MDay.mp4) to $PROJECT_DIR"
echo "3. Set your OpenAI API key:"
echo "   export OPENAI_API_KEY='your-key-here'"
echo "4. Update paths in Master_fixed.py"
echo "5. Run: python3 Master_fixed.py"
echo

# Test microphone
echo "Microphone devices found:"
python3 -c "import speech_recognition as sr; [print(f'{i}: {name}') for i, name in enumerate(sr.Microphone.list_microphone_names())]" 2>/dev/null || echo "Install scripts first to test microphone"

echo
echo "For detailed instructions, see SETUP_V1.0.md"