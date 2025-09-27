import subprocess

def run_speech_to_text():
    try:
        # Command to activate the virtual environment for speech-to-text program
        activation_command = ["env1/bin/activate"]
        process = subprocess.Popen(activation_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr:
            print("Error:", stderr.decode("utf-8"))

        # Command to run the speech-to-text program
        stt_command = ["python", "S2T.py"]
        process = subprocess.Popen(stt_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Read the output of the speech-to-text program from stdout
        stt_output_str = process.stdout.read().decode("utf-8").strip()
        
        # Wait for the process to finish and capture any errors
        process.wait()
        stderr = process.stderr.read().decode("utf-8")
        if stderr:
            print("Error:", stderr)
        
        # Return the output of the speech-to-text program
        return stt_output_str
        
    except Exception as e:
        print("Error:", e)
        return None  # Return None in case of an exception

def main():
    recognized_text = run_speech_to_text()
    print("Speech-to-text output:", recognized_text)

if __name__ == "__main__":
    main()

