"""
Master control script for TPFV1.0
Coordinates S2T, NLP, and T2S modules with metrics tracking
"""
import subprocess
import time
import os
import sys
import json
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
env1_path = os.path.join(SCRIPT_DIR, "env1")
env2_path = os.path.join(SCRIPT_DIR, "env2")
video_path = os.path.join(SCRIPT_DIR, "MDay.mp4")

class TalkingPhotoFrame:
    def __init__(self, env1_path, env2_path, video_path="MDay.mp4"):
        self.env1_path = env1_path
        self.env2_path = env2_path
        self.video_path = video_path
        self.video_process = None
        self.metrics = {
            "session_start": datetime.now().isoformat(),
            "interactions": []
        }
        
    def run_in_env(self, env_path, script_path, args=""):
        """
        Run a Python script in a specific virtual environment
        """
        python_path = os.path.join(env_path, "bin", "python")
        
        if not os.path.exists(python_path):
            print(f"ERROR: Python not found at {python_path}")
            return None
        
        command = f"{python_path} {script_path} {args}"
        print(f"Running: {command}", file=sys.stderr)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"ERROR: Script failed with code {result.returncode}", file=sys.stderr)
                print(f"STDERR: {result.stderr}", file=sys.stderr)
                return None
                
        except subprocess.TimeoutExpired:
            print("ERROR: Command timed out", file=sys.stderr)
            return None
        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return None
    
    def play_video(self):
        """Start video playback in background"""
        if not os.path.exists(self.video_path):
            print(f"WARNING: Video file not found: {self.video_path}", file=sys.stderr)
            return
        
        video_command = [
            "ffplay",
            "-vf", "transpose=2",
            "-loop", "0",
            "-fs",
            "-autoexit",
            self.video_path
        ]
        
        try:
            self.video_process = subprocess.Popen(
                video_command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("Video playback started", file=sys.stderr)
        except Exception as e:
            print(f"ERROR: Could not start video: {e}", file=sys.stderr)
    
    def stop_video(self):
        """Stop video playback"""
        if self.video_process:
            self.video_process.terminate()
            self.video_process = None
    
    def run_conversation_loop(self, max_iterations=None):
        """
        Main conversation loop
        """
        print("\n=== Talking Photo Frame V1.0 ===")
        print("Say 'goodbye' to exit\n")
        
        # Play initial greeting
        print("Playing greeting...", file=sys.stderr)
        self.run_in_env(self.env1_path, "T2S_fixed.py", "Hello! I'm so happy to talk with you.")
        time.sleep(1)
        
        # Start video
        self.play_video()
        
        iteration = 0
        while True:
            if max_iterations and iteration >= max_iterations:
                break
            
            interaction_metrics = {
                "iteration": iteration,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"\n--- Interaction {iteration + 1} ---")
            
            # Step 1: Speech to Text
            print("Listening for speech...", file=sys.stderr)
            t_start_s2t = time.time()
            user_input = self.run_in_env(self.env1_path, "S2T_fixed.py")
            t_end_s2t = time.time()
            
            if not user_input:
                print("No input received, trying again...", file=sys.stderr)
                continue
            
            interaction_metrics["s2t_latency"] = t_end_s2t - t_start_s2t
            interaction_metrics["user_input"] = user_input
            print(f"User said: {user_input}")
            
            # Check for exit condition
            if "goodbye" in user_input.lower() or "bye" in user_input.lower():
                print("\nGoodbye!", file=sys.stderr)
                self.run_in_env(self.env1_path, "T2S_fixed.py", "Goodbye my dear. I love you!")
                interaction_metrics["exit_triggered"] = True
                self.metrics["interactions"].append(interaction_metrics)
                break
            
            # Step 2: Generate Response
            print("Generating response...", file=sys.stderr)
            t_start_nlp = time.time()
            response = self.run_in_env(self.env2_path, "NLP_fixed.py", f"'{user_input}'")
            t_end_nlp = time.time()
            
            if not response:
                response = "I didn't quite catch that, dear."
            
            interaction_metrics["nlp_latency"] = t_end_nlp - t_start_nlp
            interaction_metrics["response"] = response
            print(f"Response: {response}")
            
            # Step 3: Text to Speech
            print("Speaking response...", file=sys.stderr)
            t_start_t2s = time.time()
            self.run_in_env(self.env1_path, "T2S_fixed.py", f"'{response}'")
            t_end_t2s = time.time()
            
            interaction_metrics["t2s_latency"] = t_end_t2s - t_start_t2s
            interaction_metrics["total_latency"] = t_end_t2s - t_start_s2t
            
            print(f"Total latency: {interaction_metrics['total_latency']:.2f}s", file=sys.stderr)
            
            # Save interaction metrics
            self.metrics["interactions"].append(interaction_metrics)
            
            iteration += 1
            time.sleep(1)  # Brief pause between interactions
        
        # Cleanup
        self.stop_video()
        
        # Save metrics
        self.save_metrics()
        
    def save_metrics(self):
        """Save metrics to JSON file"""
        self.metrics["session_end"] = datetime.now().isoformat()
        
        metrics_file = f"metrics_v1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        print(f"\nMetrics saved to: {metrics_file}", file=sys.stderr)
        
        # Print summary
        self.print_metrics_summary()
    
    def print_metrics_summary(self):
        """Print a summary of metrics"""
        if not self.metrics["interactions"]:
            return
        
        print("\n=== Session Metrics Summary ===")
        print(f"Total interactions: {len(self.metrics['interactions'])}")
        
        s2t_latencies = [i.get("s2t_latency", 0) for i in self.metrics["interactions"] if "s2t_latency" in i]
        nlp_latencies = [i.get("nlp_latency", 0) for i in self.metrics["interactions"] if "nlp_latency" in i]
        t2s_latencies = [i.get("t2s_latency", 0) for i in self.metrics["interactions"] if "t2s_latency" in i]
        total_latencies = [i.get("total_latency", 0) for i in self.metrics["interactions"] if "total_latency" in i]
        
        if s2t_latencies:
            print(f"\nAverage S2T latency: {sum(s2t_latencies)/len(s2t_latencies):.2f}s")
        if nlp_latencies:
            print(f"Average NLP latency: {sum(nlp_latencies)/len(nlp_latencies):.2f}s")
        if t2s_latencies:
            print(f"Average T2S latency: {sum(t2s_latencies)/len(t2s_latencies):.2f}s")
        if total_latencies:
            print(f"Average total latency: {sum(total_latencies)/len(total_latencies):.2f}s")
            print(f"Min total latency: {min(total_latencies):.2f}s")
            print(f"Max total latency: {max(total_latencies):.2f}s")

def main():
    # Check for environment variables
    if not os.getenv('OPENAI_API_KEY'):
        print("WARNING: OPENAI_API_KEY not set. Please export it:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        print()
    
    # Use the paths defined at the top of the file
    # (already calculated as SCRIPT_DIR relative paths)
    
    # Check if paths exist
    if not os.path.exists(env1_path):
        print(f"ERROR: env1 not found at {env1_path}")
        print("Please create virtual environments in the script directory")
        sys.exit(1)
    
    if not os.path.exists(env2_path):
        print(f"ERROR: env2 not found at {env2_path}")
        print("Please create virtual environments in the script directory")
        sys.exit(1)
    
    # Create and run the talking photo frame
    frame = TalkingPhotoFrame(env1_path, env2_path, video_path)
    
    try:
        frame.run_conversation_loop()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        frame.stop_video()
        frame.save_metrics()
    except Exception as e:
        print(f"ERROR: {e}")
        frame.stop_video()
        frame.save_metrics()

if __name__ == "__main__":
    main()