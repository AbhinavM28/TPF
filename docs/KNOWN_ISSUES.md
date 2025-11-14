# Known Issues - V1.0

## Critical Issues

### 1. Unacceptable Latency (32s average)
**Severity**: High
**Impact**: Breaks conversational flow
**Root Cause**: Multiple cloud API round trips
**V2.0 Solution**: Local processing with Ollama + Whisper

### 2. Monthly cost to run ($5 - $20 / month)
**Severity**: High
**Impact**: Cost inefficient and unsustainable
**Root Cause**: Initial framework built around non-local LLM
**V2.0 Solution**: Local processing with Ollama + Whisper (one-time cost)

### 3. Translation errors
**Severity**: Medium
**Impact**: Breaks immersion when forced into an input and output language
**Root Cause**: Static translation model fixed to one input language and one output language
**V2.0 Solution**: Multilingual translation support for various languages with user customization options

### 4. Generic Voice (default robotic female voice 1)
**Severity**: Medium
**Impact**: Breaks immersion especially when voice does not match the familiar face
**Root Cause**: No voice modulation and synthesis worked into V1.0
**V2.0 Solution**: Coqui TTS with XTTS-v2 with sample voice clips for customization

### 5. Single User Curated (V1.0 made specifically for my mother to interact with her mother)
**Severity**: High
**Impact**: Cannot market a single user curated device
**Root Cause**: Hardcoded for prototyping and testing, 
**V2.0 Solution**: Coqui TTS with XTTS-v2 with sample voice clips for customization

### 6. Exit command unable to trigger (99% improper command translation)
**Severity**: High
**Impact**: Causes user to manually trigger keyboard command to kill program, which defeats seamless interaction
**Root Cause**: Not enough training epochs on exit command or ambiguous exit condition
**V2.0 Solution**: Clear exit command with two stage verification to kill program to a seamless resting UI

### 7. Static UI and imagery 
**Severity**: High
**Impact**: Immersion breaks when visuals of UI are static, diminishing emotional touch 
**Root Cause**: V1.0 loops through MP4 file and overlays the executing program in the background
**V2.0 Solution**: face/lip animation using libraries like wav2lip and OpenCV modules for optimized phoneme generation
