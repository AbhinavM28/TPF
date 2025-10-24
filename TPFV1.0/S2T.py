#!/usr/bin/env python3
"""
Speech to Text module with Telugu to English translation
Run this in env1
"""
import speech_recognition as sr
from googletrans import Translator
import sys
import os

# Suppress ALSA warnings
os.environ['PYTHONWARNINGS'] = 'ignore'
from ctypes import *
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
try:
    asound = cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
except:
    pass

def find_usb_microphone():
    """
    Find the first USB microphone automatically
    """
    try:
        mic_list = sr.Microphone.list_microphone_names()
        for i, name in enumerate(mic_list):
            # Look for USB microphones
            if 'USB' in name.upper() or 'MICROPHONE' in name.upper():
                return i
        # If no USB mic found, return default
        return None
    except:
        return None

def speech_to_text(device_index=None, timeout=10):
    """
    Capture speech and translate from Telugu to English
    
    Args:
        device_index: Microphone device index (None for auto-detect)
        timeout: Maximum time to wait for speech
    
    Returns:
        Translated text in English or None
    """
    r = sr.Recognizer()
    
    # Adjust these parameters for better noise handling
    r.energy_threshold = 4000
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1.0
    
    # Auto-detect USB microphone if not specified
    if device_index is None:
        device_index = find_usb_microphone()
    
    try:
        with sr.Microphone(device_index=device_index) as source:
            # Suppress the adjustment message
            r.adjust_for_ambient_noise(source, duration=2)
            
            # Listen with timeout
            audio = r.listen(source, timeout=timeout, phrase_time_limit=15)
        
        # Recognize speech in Telugu
        text_te = r.recognize_google(audio, language="te-IN")
        
        # Translate to English
        translator = Translator()
        text_en = translator.translate(text_te, src='te', dest='en')
        translated_text = text_en.text
        
        return translated_text
        
    except sr.WaitTimeoutError:
        print("ERROR: No speech detected", file=sys.stderr)
        return None
    except sr.UnknownValueError:
        print("ERROR: Could not understand audio", file=sys.stderr)
        return None
    except sr.RequestError as e:
        print(f"ERROR: Google API error: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    # Auto-detect microphone or use command line argument
    device_index = int(sys.argv[1]) if len(sys.argv) > 1 else None
    
    translated_text = speech_to_text(device_index=device_index)
    
    if translated_text:
        print(translated_text)
        sys.exit(0)
    else:
        sys.exit(1)