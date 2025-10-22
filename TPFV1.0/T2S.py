"""
Text to Speech module with English to Telugu translation
Run this in env1
"""
import sys
import os
import pygame
from gtts import gTTS
from googletrans import Translator
import time

def text_to_speech(input_text, output_file="output_audio.mp3", lang='te'):
    """
    Convert text to speech in Telugu
    
    Args:
        input_text: Text to convert (in English)
        output_file: Output audio file path
        lang: Target language code
    
    Returns:
        Path to audio file or None on error
    """
    try:
        # Translate from English to Telugu
        translator = Translator()
        print(f"Translating: {input_text}", file=sys.stderr)
        
        translated = translator.translate(input_text, src='en', dest='te')
        translated_text = translated.text
        print(f"Translated (Telugu): {translated_text}", file=sys.stderr)
        
        # Generate speech
        tts = gTTS(text=translated_text, lang=lang, slow=False)
        tts.save(output_file)
        print(f"Audio saved to: {output_file}", file=sys.stderr)
        
        # Play audio
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        pygame.mixer.quit()
        return output_file
        
    except Exception as e:
        print(f"ERROR: Text-to-speech error: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: No input text provided", file=sys.stderr)
        print("Usage: python T2S_fixed.py <text>", file=sys.stderr)
        sys.exit(1)
    
    input_text = " ".join(sys.argv[1:])
    output_file = text_to_speech(input_text)
    
    if output_file:
        print(output_file)
        sys.exit(0)
    else:
        sys.exit(1)