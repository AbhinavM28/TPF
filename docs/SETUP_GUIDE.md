## 🛠️ Quick Start

### Prerequisites
```bash
sudo apt-get update
sudo apt-get install -y flac ffmpeg portaudio19-dev python3-venv
```

### Installation
```bash
git clone https://github.com/AbhinavM28/TPF.git
cd TPF/TPFV1.0

# Create virtual environments
python3 -m venv env1
source env1/bin/activate
pip install SpeechRecognition PyAudio googletrans==4.0.0rc1 gtts pygame
deactivate

python3 -m venv env2
source env2/bin/activate
pip install openai==1.3.0
deactivate

# Set API key
export OPENAI_API_KEY="your-key-here"

# Run
python3 Master.py
```

### Usage
1. Start the program: `python3 Master.py`
2. Wait for "Listening..." prompt
3. Speak in Telugu or English
4. System responds with grandmother's voice
5. Say "goodbye" to exit (or Ctrl+C)