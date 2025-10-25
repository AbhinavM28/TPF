#!/usr/bin/env python3
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
import warnings
warnings.filterwarnings("ignore")

# Get script directory and set paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
env1_path = os.path.join(SCRIPT_DIR, "env1")
env2_path = os.path.join(SCRIPT_DIR, "env2")
video_path = os.path.join(SCRIPT_DIR, "MDay.mp4")
metrics_dir = os.path.join(SCRIPT_DIR, "metrics")

# Create metrics directory if it doesn't exist
os.makedirs(metrics_dir, exist_ok=True)

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
        """Run a Python script in a specific virtual environment"""
        python_path = os.path.join(env_path, "bin", "python")
        
        if not os.path.exists(python_path):
            print(f"[ERROR] Python not found at {python_path}")
            return None
        
        command = f"{python_path} {script_path} {args}"
        
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
                # Only show critical errors, suppress JACK/ALSA warnings
                if "ERROR:" in result.stderr and "Cannot connect to server" not in result.stderr:
                    print(f"[ERROR] {result.stderr.split('ERROR:')[-1].strip()}")
                return None
                
        except subprocess.TimeoutExpired:
            print("[ERROR] Command timed out")
            return None
        except Exception as e:
            print(f"[ERROR] {e}")
            return None
    
    def play_video(self):
        """Start video playback in background"""
        if not os.path.exists(self.video_path):
            print(f"[WARNING] Video file not found: {self.video_path}")
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
            print("[INFO] Video playback started")
        except Exception as e:
            print(f"[ERROR] Could not start video: {e}")
    
    def stop_video(self):
        """Stop video playback"""
        if self.video_process:
            self.video_process.terminate()
            self.video_process = None
    
    def run_conversation_loop(self, max_iterations=None):
        """Main conversation loop"""
        print("\n" + "="*60)
        print("   TALKING PHOTO FRAME V1.0 - BASELINE")
        print("="*60)
        print("Say 'goodbye' to exit")
        print("="*60 + "\n")
        
        # Play initial greeting
        print("[1/3] Initializing greeting...")
        self.run_in_env(self.env1_path, "T2S.py", "Hello! I'm so happy to talk with you.")
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
            
            print(f"\n{'='*60}")
            print(f"Interaction #{iteration + 1}")
            print(f"{'='*60}")
            
            # Step 1: Speech to Text
            print("[1/3] Listening for speech...")
            t_start_s2t = time.time()
            user_input = self.run_in_env(self.env1_path, "S2T.py")
            t_end_s2t = time.time()
            
            if not user_input:
                print("[WARNING] No input received, retrying...")
                continue
            
            interaction_metrics["s2t_latency"] = t_end_s2t - t_start_s2t
            interaction_metrics["user_input"] = user_input
            print(f"      USER: {user_input}")
            print(f"      Time: {interaction_metrics['s2t_latency']:.2f}s")
            
            # Check for exit condition
            if "goodbye" in user_input.lower() or "bye" in user_input.lower():
                print("\n[INFO] Goodbye detected, exiting...")
                self.run_in_env(self.env1_path, "T2S.py", "Goodbye my dear. I love you!")
                interaction_metrics["exit_triggered"] = True
                self.metrics["interactions"].append(interaction_metrics)
                break
            
            # Step 2: Generate Response
            print("[2/3] Generating response...")
            t_start_nlp = time.time()
            response = self.run_in_env(self.env2_path, "NLP.py", f"'{user_input}'")
            t_end_nlp = time.time()
            
            if not response:
                response = "I didn't quite catch that, dear."
            
            interaction_metrics["nlp_latency"] = t_end_nlp - t_start_nlp
            interaction_metrics["response"] = response
            print(f"      GRANDMOTHER: {response}")
            print(f"      Time: {interaction_metrics['nlp_latency']:.2f}s")
            
            # Step 3: Text to Speech
            print("[3/3] Speaking response...")
            t_start_t2s = time.time()
            self.run_in_env(self.env1_path, "T2S.py", f"'{response}'")
            t_end_t2s = time.time()
            
            interaction_metrics["t2s_latency"] = t_end_t2s - t_start_t2s
            interaction_metrics["total_latency"] = t_end_t2s - t_start_s2t
            
            print(f"      Time: {interaction_metrics['t2s_latency']:.2f}s")
            print(f"\n      TOTAL TIME: {interaction_metrics['total_latency']:.2f}s")
            
            # Save interaction metrics
            self.metrics["interactions"].append(interaction_metrics)
            
            iteration += 1
            time.sleep(0.5)
        
        # Cleanup
        self.stop_video()
        
        # Save metrics
        self.save_metrics()
        
    def save_metrics(self):
        """Save metrics to JSON file in metrics directory"""
        self.metrics["session_end"] = datetime.now().isoformat()
        
        metrics_filename = f"metrics_v1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        metrics_filepath = os.path.join(metrics_dir, metrics_filename)
        
        with open(metrics_filepath, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        print(f"\n[SAVE] Metrics: metrics/{metrics_filename}")
        
        # Print summary
        self.print_metrics_summary()
    
    def print_metrics_summary(self):
        """Print a summary of metrics"""
        if not self.metrics["interactions"]:
            print("\n[WARNING] No interactions recorded")
            return
        
        print("\n" + "="*60)
        print("   SESSION SUMMARY")
        print("="*60)
        print(f"Total Interactions: {len(self.metrics['interactions'])}")
        
        s2t_latencies = [i.get("s2t_latency", 0) for i in self.metrics["interactions"] if "s2t_latency" in i]
        nlp_latencies = [i.get("nlp_latency", 0) for i in self.metrics["interactions"] if "nlp_latency" in i]
        t2s_latencies = [i.get("t2s_latency", 0) for i in self.metrics["interactions"] if "t2s_latency" in i]
        total_latencies = [i.get("total_latency", 0) for i in self.metrics["interactions"] if "total_latency" in i]
        
        if total_latencies:
            print(f"\nComponent Latencies:")
            if s2t_latencies:
                print(f"  Speech-to-Text:  {sum(s2t_latencies)/len(s2t_latencies):>6.2f}s avg")
            if nlp_latencies:
                print(f"  LLM Processing:  {sum(nlp_latencies)/len(nlp_latencies):>6.2f}s avg")
            if t2s_latencies:
                print(f"  Text-to-Speech:  {sum(t2s_latencies)/len(t2s_latencies):>6.2f}s avg")
            print(f"  {'─'*30}")
            print(f"  Total Response:  {sum(total_latencies)/len(total_latencies):>6.2f}s avg")
            print(f"  Range: {min(total_latencies):.2f}s - {max(total_latencies):.2f}s")
        
        print("="*60 + "\n")

def main():
    # Check for environment variables
    if not os.getenv('OPENAI_API_KEY'):
        print("\n[ERROR] OPENAI_API_KEY not set!")
        print("Please export it: export OPENAI_API_KEY='your-api-key-here'\n")
        sys.exit(1)
    
    # Check if paths exist
    if not os.path.exists(env1_path):
        print(f"[ERROR] env1 not found at {env1_path}")
        sys.exit(1)
    
    if not os.path.exists(env2_path):
        print(f"[ERROR] env2 not found at {env2_path}")
        sys.exit(1)
    
    # Create and run the talking photo frame
    frame = TalkingPhotoFrame(env1_path, env2_path, video_path)
    
    try:
        frame.run_conversation_loop()
    except KeyboardInterrupt:
        print("\n\n[INFO] Interrupted by user")
        frame.stop_video()
        frame.save_metrics()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        frame.stop_video()
        frame.save_metrics()

if __name__ == "__main__":
    main()