"""
Speech to Text module with Telugu to English translation
Run this in env1
"""
import speech_recognition as sr
from googletrans import Translator
import sys
import time

def speech_to_text(device_index=2, timeout=10):
    """
    Capture speech and translate from Telugu to English
    
    Args:
        device_index: Microphone device index
        timeout: Maximum time to wait for speech
    
    Returns:
        Translated text in English or None
    """
    r = sr.Recognizer()
    
    # Adjust these parameters for better noise handling
    r.energy_threshold = 4000  # Increase if too sensitive
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1.0  # Seconds of silence to consider end of phrase
    
    try:
        with sr.Microphone(device_index=device_index) as source:
            print("Adjusting for ambient noise... Please wait.", file=sys.stderr)
            r.adjust_for_ambient_noise(source, duration=2)
            print(f"Energy threshold: {r.energy_threshold}", file=sys.stderr)
            print("Listening... Speak now!", file=sys.stderr)
            
            # Listen with timeout
            audio = r.listen(source, timeout=timeout, phrase_time_limit=15)
            print("Processing speech...", file=sys.stderr)
        
        # Recognize speech in Telugu
        text_te = r.recognize_google(audio, language="te-IN")
        print(f"Recognized (Telugu): {text_te}", file=sys.stderr)
        
        # Translate to English
        translator = Translator()
        text_en = translator.translate(text_te, src='te', dest='en')
        translated_text = text_en.text
        print(f"Translated (English): {translated_text}", file=sys.stderr)
        
        return translated_text
        
    except sr.WaitTimeoutError:
        print("ERROR: No speech detected within timeout period", file=sys.stderr)
        return None
    except sr.UnknownValueError:
        print("ERROR: Could not understand the audio", file=sys.stderr)
        return None
    except sr.RequestError as e:
        print(f"ERROR: Could not request results from Google; {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    # Get device index from command line if provided
    device_index = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    
    translated_text = speech_to_text(device_index=device_index)
    
    if translated_text:
        # Output only the translated text to stdout (for piping)
        print(translated_text)
        sys.exit(0)
    else:
        # Exit with error code
        sys.exit(1)