""" 
import subprocess
import time

def run_env_script(env_name, script_path):
    activate_path = f"{env_name}/bin/activate"
    command = f". {activate_path} && python {script_path}"
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()  # Strip whitespace from the output
    except subprocess.CalledProcessError as e:
        print(f"Error running script {script_path}: {e.stderr}")
        return None

print("test1")

def play_video(video_file):
    # Command to play the video file with transpose to the left and fitting to screen
    video_command = [
        "ffplay","-vf","transpose=2",
        "-loop","0","-fs",
        video_file
    ]
    subprocess.Popen(video_command)

play_video("MDay.mp4")

while True:
    # Activate env1 and run speech-to-text program
    user_input = run_env_script("env1", "S2T.py")
    print("test2")

    if user_input.strip().lower() == "goodbye":
        print("Goodbye!")
        break

    # Activate env2 and run NLP program
    nlp_response = run_env_script("env2", f"NLP.py '{user_input}'")
    print("test3")

    # Activate env1 and run text-to-speech program
    output_audio_file = run_env_script("env1", f"T2S.py '{nlp_response}'")
    print("test4")

    time.sleep(2)  # Add a small delay before listening for the next input

print("End of conversation.")

"""

