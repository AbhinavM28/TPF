#!/bin/bash
# Talking Photo Frame V1.0 - Quick Start Script
# This script helps you get TPF running quickly 

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Banner
echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════╗
║   Talking Photo Frame V1.0 Quick Start       ║
╚═══════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Get project directory
PROJECT_DIR="${PROJECT_DIR:-$HOME/talking-photo-frame}"

# Check if we're in the project directory
if [ -f "Master.py" ]; then
    PROJECT_DIR=$(pwd)
    print_info "Using current directory: $PROJECT_DIR"
elif [ -d "$PROJECT_DIR" ]; then
    print_info "Using project directory: $PROJECT_DIR"
    cd "$PROJECT_DIR"
else
    print_error "Project directory not found!"
    print_info "Please run this from the project directory or set PROJECT_DIR"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
print_info "Checking prerequisites..."

if ! command_exists python3; then
    print_error "Python 3 not found!"
    exit 1
fi
print_success "Python 3: $(python3 --version)"

if ! command_exists ffplay; then
    print_warning "ffplay not found - video playback may not work"
    print_info "Install with: sudo apt-get install ffmpeg"
fi

# Check virtual environments
print_info "Checking virtual environments..."

if [ ! -d "env1" ]; then
    print_warning "env1 not found!"
    print_info "Run install_dependencies.sh first"
    exit 1
fi
print_success "env1 found"

if [ ! -d "env2" ]; then
    print_warning "env2 not found!"
    print_info "Run install_dependencies.sh first"
    exit 1
fi
print_success "env2 found"

# Check required scripts
print_info "Checking required scripts..."
REQUIRED_SCRIPTS=("S2T.py" "NLP.py" "T2S.py" "Master.py")
for script in "${REQUIRED_SCRIPTS[@]}"; do
    if [ ! -f "$script" ]; then
        print_error "$script not found!"
        exit 1
    fi
done
print_success "All scripts found"

# Check for video file
if [ ! -f "MDay.mp4" ]; then
    print_warning "Video file MDay.mp4 not found"
    print_info "The system will work but without video playback"
fi

# Check for API key
print_info "Checking OpenAI API key..."
if [ -z "$OPENAI_API_KEY" ]; then
    print_warning "OPENAI_API_KEY not set!"
    echo
    read -p "Enter your OpenAI API key (or press Enter to skip): " api_key
    if [ -n "$api_key" ]; then
        export OPENAI_API_KEY="$api_key"
        print_success "API key set for this session"
        print_info "To persist, add to ~/.bashrc:"
        echo "  export OPENAI_API_KEY='$api_key'"
    else
        print_error "API key required for operation"
        exit 1
    fi
else
    print_success "API key found"
fi

# Test microphone
print_info "Testing microphone..."
echo
print_info "Available microphones:"
source env1/bin/activate
python3 << 'PYPYTHON'
import speech_recognition as sr
try:
    mics = sr.Microphone.list_microphone_names()
    for i, name in enumerate(mics):
        print(f"  {i}: {name}")
except Exception as e:
    print(f"Error listing microphones: {e}")
PYPYTHON
deactivate

echo
read -p "Enter microphone device index (default: 2): " mic_index
mic_index=${mic_index:-2}
print_info "Using microphone index: $mic_index"

# Update S2T_fixed.py with correct device index if needed
if [ "$mic_index" != "2" ]; then
    print_info "Updating S2T_fixed.py with device index $mic_index"
    sed -i "s/device_index=2/device_index=$mic_index/g" S2T_fixed.py
fi

# Run mode selection
echo
echo "Select mode:"
echo "  1) Run full system (Master_fixed.py)"
echo "  2) Test Speech-to-Text only"
echo "  3) Test Text-to-Speech only"
echo "  4) Test NLP only"
echo "  5) Analyze metrics"
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        print_info "Starting Talking Photo Frame..."
        print_info "Say 'goodbye' to exit gracefully"
        print_info "Press Ctrl+C to force stop"
        echo
        sleep 2
        python3 Master.py
        ;;
    2)
        print_info "Testing Speech-to-Text..."
        print_info "Speak in Telugu when prompted"
        echo
        source env1/bin/activate
        python3 S2T.py
        deactivate
        ;;
    3)
        print_info "Testing Text-to-Speech..."
        read -p "Enter text to speak (in English): " test_text
        test_text=${test_text:-"Hello, this is a test"}
        echo
        source env1/bin/activate
        python3 T2S.py "$test_text"
        deactivate
        ;;
    4)
        print_info "Testing NLP..."
        read -p "Enter prompt: " test_prompt
        test_prompt=${test_prompt:-"How are you today?"}
        echo
        source env2/bin/activate
        python3 NLP.py "$test_prompt"
        deactivate
        ;;
    5)
        print_info "Analyzing metrics..."
        if [ ! -f "metrics_analyzer.py" ]; then
            print_error "metrics_analyzer.py not found"
            exit 1
        fi
        python3 metrics_analyzer.py
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

print_success "Done!"
echo
print_info "For more options, see COMMAND_REFERENCE.md"