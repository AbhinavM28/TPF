import subprocess
from gtts import gTTS
import pygame

def run_speech_to_text():
    # Command to activate the virtual environment for speech-to-text program
    activation_command = ["source", "env1/bin/activate"]
    subprocess.run(activation_command)

    # Command to run the speech-to-text program
    stt_command = ["python", "S2T.py"]
    # Capture the output of the speech-to-text program
    stt_output = subprocess.check_output(stt_command)
    # Decode the output to string (assuming it's in bytes)
    stt_output_str = stt_output.decode("utf-8").strip()
    return stt_output_str

def run_text_generation(input_text):
    # Command to activate the virtual environment for text generation program
    activation_command = ["source", "env2/bin/activate"]
    subprocess.run(activation_command)

    # Command to run the text generation program
    text_generation_command = ["python", "NLP.py", input_text]
    # Capture the output of the text generation program
    text_generation_output = subprocess.check_output(text_generation_command)
    # Decode the output to string (assuming it's in bytes)
    text_generation_output_str = text_generation_output.decode("utf-8").strip()
    return text_generation_output_str

def run_text_to_speech(output_text):
    # Command to activate the virtual environment for text-to-speech program
    activation_command = ["source", "env1/bin/activate"]
    subprocess.run(activation_command)

    # Command to run the text-to-speech program
    tts_command = ["python", "T2S.py", output_text]
    subprocess.run(tts_command)

def play_video(video_file):
    # Command to play the video file with transpose to the left and fitting to screen
    video_command = [
        "ffplay",
        "-loop", "0","-fs",
        video_file
    ]
    subprocess.Popen(video_command)

def main():
    # Video file path
    video_file = "MDay.mp4"
    tts = gTTS(text="Hello!", lang='te', slow=False)
    tts.save("Hello.mp3")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("Hello.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Play the video in a loop
   #  play_video(video_file)

    while True:
        # Run speech-to-text program and capture the recognized text
        recognized_text = run_speech_to_text()

        # Run text generation program with the recognized text
        generated_text = run_text_generation(recognized_text)

        # Run text-to-speech program with the generated text
        run_text_to_speech(generated_text)

        # Break the loop if the generated text is "goodbye"
        if generated_text.lower() == "goodbye":
            break

if __name__ == "__main__":
    main()
