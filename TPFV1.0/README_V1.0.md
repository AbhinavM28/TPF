# Talking Photo Frame V1.0 - Baseline Prototype

> **A Raspberry Pi-based conversational AI system that allows users to have voice conversations with loved ones through AI-generated responses and voice synthesis.**

![Version](https://img.shields.io/badge/version-1.0-blue)
![Status](https://img.shields.io/badge/status-baseline-yellow)
![Python](https://img.shields.io/badge/python-3.11-green)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%204-red)

## 📹 Demo Video

[Watch the V1.0 Demo](./demo_output/TPFV1.0_Demo.mp4)

## 🎯 Project Overview

The Talking Photo Frame (TPF) is a personal project created to help my mother connect with her deceased grandmother through AI-powered conversations. This V1.0 baseline implementation demonstrates the core concept using cloud-based services, and serves to act as a proof of concept.

### Key Features (V1.0)
- **Speech Recognition**: voice input with Google Speech-to-Text
- **Language Translation**: Automatic Telugu ↔ English translation for output
- **AI Responses**: Fine-tuned GPT-3.5 model for grandmother-like personality
- **Voice Synthesis**: Text-to-speech output in Telugu (Google TTS)
- **Visual Display**: Looping video of loved one's photo
- **Performance Metrics**: Automated tracking and analysis

## 📊 V1.0 Performance Metrics

Based on real-world testing with 9 interactions:

| Metric | Value | Notes |
|--------|-------|-------|
| **Average Total Latency** | 32.12s | End-to-end response time |
| **Speech-to-Text** | 14.33s | Includes ambient noise adjustment |
| **LLM Processing** | 7.43s | OpenAI API call + processing |
| **Text-to-Speech** | 10.36s | Translation + audio generation |
| **Range** | 19.89s - 55.48s | Min to max response times |
| **Success Rate** | 100% | All interactions completed |

### Latency Breakdown

```
┌─────────────────────────────────────────────────┐
│  Component          Time     % of Total         │
├─────────────────────────────────────────────────┤
│  Speech-to-Text     14.33s      44.6%           │
│  LLM Processing      7.43s      23.1%           │
│  Text-to-Speech     10.36s      32.3%           │
├─────────────────────────────────────────────────┤
│  TOTAL              32.12s     100.0%           │
└─────────────────────────────────────────────────┘
```

## 🔧 Technical Architecture

### System Components

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Microphone  │────▶│ Google STT   │────▶│   Translate  │
│   (Telugu)   │     │   (Cloud)    │     │  (Te → En)   │
└──────────────┘     └──────────────┘     └──────────────┘
                                                    │
                                                    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Speaker    │◀────│ Google TTS   │◀────│  OpenAI GPT  │
│   (Telugu)   │     │   (Cloud)    │     │  (Fine-tuned)│
└──────────────┘     └──────────────┘     └──────────────┘
        │                    ▲
        │                    │
        ▼                    │
┌──────────────┐     ┌──────────────┐
│  LCD Display │     │   Translate  │
│ (Video Loop) │     │  (En → Te)   │
└──────────────┘     └──────────────┘
```

### Hardware
- **Board**: Raspberry Pi 4 Model B (8GB RAM)
- **Storage**: 64GB microSD card
- **Display**: 7" LCD screen (non-touch)
- **Microphone**: SunFounder USB 2.0 Mini Microphone
- **Enclosure**: Custom 3D-printed frame
- **Power**: 5.1V 3000mA power adapter (model: HT39B-0513000US)

### Software Stack
- **OS**: Raspberry Pi OS (64-bit)
- **Language**: Python 3.11
- **Speech Recognition**: Google Speech-to-Text API
- **Translation**: Google Translate API
- **LLM**: OpenAI GPT-3.5-turbo (fine-tuned)
- **TTS**: Google Text-to-Speech (gTTS)
- **Video**: FFmpeg/ffplay

## 🚨 Known Issues & Limitations

### Critical Issues
1. **High Latency**: 32s average response time (unacceptable for natural conversation)
2. **Internet Dependency**: Requires constant connection; fails offline
3. **Translation Quality**: Telugu ↔ English loses meaning and nuance. Not suited for casual conversation or "slang" / vernacular
4. **Recognition Accuracy**: Struggles with "goodbye" command (often hears "good boy", "Dubai", etc.)
5. **Voice Quality**: Generic female voice, not personalized
6. **Static Visual**: No lip-sync or facial animation

### Technical Debt
- Multiple virtual environments (dependency conflicts)
- Subprocess-based inter-process communication
- No error recovery or retry logic
- Hard dependency on external APIs
- Ongoing API costs (~$5-20/month)

### User Experience Issues
- Translation sounds "too proper" for casual conversation
- Telugu speech recognition fails frequently
- English-only input works better than native Telugu
- Long pauses feel unnatural
- Limited response variety
- Limited language options

## 💰 Cost Analysis

### V1.0 Operational Costs
- **Hardware** (one-time): $180
- **OpenAI API**: $5-20/month
- **Internet**: Required
- **Annual Cost**: $240-420/year

## 🎓 Lessons Learned

### What Worked
✅ Core concept validation - family loved it despite issues
✅ Successful integration of multiple APIs
✅ Automated metrics collection
✅ Reproducible setup process and reproducible product
✅ Potential market within the division of mental health and technology

### What Didn't Work
❌ Cloud-based approach too slow for real-time feel
❌ Translation layer adds latency and errors
❌ Generic TTS voice lacks emotional connection
❌ Static video doesn't enhance engagement
❌ Exit command nearly impossible to trigger

### Key Insights
- **Latency kills immersion**: >10s feels like conversation, >30s feels like waiting
- **Voice matters more than words**: Generic voice reduces emotional impact
- **Visual feedback is critical**: Users need to see the system is "thinking" or "listening"
- **Edge computing is essential**: Can't rely on internet for this use case (except potentially for initial setup)
- **Translation is a bottleneck**: Direct multilingual models would be better

## 🚀 Roadmap to V2.0

### Performance Goals
| Metric | V1.0 Baseline | V2.0 Target | Improvement |
|--------|---------------|-------------|-------------|
| Total Latency | 32.12s | <8s | **75% reduction** |
| Internet Required | Yes | No | **100% offline** |
| Voice Quality | Generic | Cloned | **Personalized** |
| Visual | Static | Animated | **Lip-sync** |
| Setup Time | 2-4 hours | <15 min | **80% faster** |
| Monthly Cost | $5-20 | $0 | **Zero ongoing cost** |

### Planned Improvements

#### 1. Local LLM (Target: -50% LLM latency)
- **Technology**: Ollama with Llama 2/3 (7B parameter)
- **Benefit**: No API calls, zero cost, offline operation
- **Challenge**: RAM constraints on Pi 4

#### 2. Local Speech Recognition (Target: -60% STT latency)
- **Technology**: OpenAI Whisper (local)
- **Benefit**: Better multilingual support, faster, offline
- **Challenge**: Processing power on edge device

#### 3. Voice Cloning (Target: Authentic voice)
- **Technology**: Coqui TTS with XTTS-v2
- **Benefit**: Grandmother's actual voice from 30s sample
- **Challenge**: Quality vs speed tradeoff

#### 4. Facial Animation (Target: Natural conversation)
- **Technology**: SadTalker or Wav2Lip
- **Benefit**: Lip-synced video, more engaging
- **Challenge**: Real-time generation overhead

#### 5. Single Environment (Target: Simple setup)
- **Technology**: Unified dependency management
- **Benefit**: One-command installation
- **Challenge**: Resolving package conflicts

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

## 📈 Performance Data

See `metrics/` directory for detailed session logs.

Example analysis:
```bash
python3 metrics_analyzer.py metrics/metrics_v1_20251025_003331.json
```

## 🤝 Contributing

This is a personal project, but I welcome feedback and suggestions! If you're building something similar or have ideas for V2.0, please open an issue.

## 🙏 Acknowledgments

- **Inspiration**: My grandmother, whose memory inspired this project
- **Support**: My mother, the primary user and tester
- **Tools**: OpenAI, Google Cloud, Raspberry Pi Foundation

## 📬 Contact

For questions or collaboration: abhinav.maddisetty@outlook.com || https://www.linkedin.com/in/abhimaddisetty/

---

**Note**: This is V1.0 - a functional prototype with significant room for improvement. V2.0 will address all known issues with local edge computing and advanced AI techniques. Stay tuned!

## 🎯 For Recruiters

This project demonstrates:
- **Full-stack development**: Hardware + software + AI integration
- **Problem-solving**: Real-world problem with technical solution
- **Performance optimization**: Data-driven improvement planning
- **User-centric design**: Built for actual user (my mother)
- **Documentation**: Clear metrics, issues, and roadmap
- **Iterative development**: V1.0 baseline → V2.0 improvements

**Next Steps**: See `V2.0_ROADMAP.md` for detailed implementation plan with timelines and technical specifications.
