import sys
import string
import pygame
from gtts import gTTS
from googletrans import Translator

translator = Translator()

def sanitize_text(input_text):
    # Remove punctuation and special characters from the input text
    sanitized_text = ''.join(char for char in input_text if char.isalnum() or char.isspace())
    return sanitized_text

def text_to_speech(input_text, output_file):
    translated_text = translator.translate(input_text, src='en', dest='te').text
    tts = gTTS(text=translated_text, lang='te', slow=False)
    tts.save(output_file)
    
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Load and play the audio file
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Control playback speed

if __name__ == "__main__":
    input_text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "No input text provided"  # Get input text from command-line arguments
    sanitized_text = sanitize_text(input_text)
    output_file = "output_audio.mp3"
    text_to_speech(sanitized_text, output_file)
