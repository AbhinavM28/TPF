"""
Metrics Analyzer for TPFV1.0 and subsequent version testing
Analyzes performance metrics from conversation sessions
"""
import json
import sys
import glob
from datetime import datetime
import statistics

class MetricsAnalyzer:
    def __init__(self, metrics_file=None):
        """
        Initialize metrics analyzer
        
        Args:
            metrics_file: Path to metrics JSON file, or None to find latest
        """
        if metrics_file is None:
            # Find most recent metrics file
            files = glob.glob("metrics_v1_*.json")
            if not files:
                print("ERROR: No metrics files found")
                sys.exit(1)
            metrics_file = max(files, key=lambda x: x.split('_')[-1])
            print(f"Analyzing: {metrics_file}\n")
        
        with open(metrics_file, 'r') as f:
            self.data = json.load(f)
        
        self.interactions = self.data.get("interactions", [])
    
    def calculate_latency_metrics(self):
        """Calculate latency statistics"""
        if not self.interactions:
            return None
        
        s2t_times = [i.get("s2t_latency", 0) for i in self.interactions if "s2t_latency" in i]
        nlp_times = [i.get("nlp_latency", 0) for i in self.interactions if "nlp_latency" in i]
        t2s_times = [i.get("t2s_latency", 0) for i in self.interactions if "t2s_latency" in i]
        total_times = [i.get("total_latency", 0) for i in self.interactions if "total_latency" in i]
        
        def calc_stats(times):
            if not times:
                return None
            return {
                "mean": statistics.mean(times),
                "median": statistics.median(times),
                "min": min(times),
                "max": max(times),
                "stdev": statistics.stdev(times) if len(times) > 1 else 0,
                "count": len(times)
            }
        
        return {
            "s2t": calc_stats(s2t_times),
            "nlp": calc_stats(nlp_times),
            "t2s": calc_stats(t2s_times),
            "total": calc_stats(total_times)
        }
    
    def calculate_quality_metrics(self):
        """Calculate response quality metrics"""
        successful_interactions = len([i for i in self.interactions if "response" in i])
        total_interactions = len(self.interactions)
        
        # Calculate response lengths
        response_lengths = [len(i.get("response", "")) for i in self.interactions if "response" in i]
        input_lengths = [len(i.get("user_input", "")) for i in self.interactions if "user_input" in i]
        
        return {
            "success_rate": successful_interactions / total_interactions if total_interactions > 0 else 0,
            "total_interactions": total_interactions,
            "successful_interactions": successful_interactions,
            "avg_response_length": statistics.mean(response_lengths) if response_lengths else 0,
            "avg_input_length": statistics.mean(input_lengths) if input_lengths else 0,
        }
    
    def calculate_system_metrics(self):
        """Calculate system-level metrics"""
        if not self.interactions:
            return None
        
        session_start = datetime.fromisoformat(self.data.get("session_start"))
        session_end = datetime.fromisoformat(self.data.get("session_end", datetime.now().isoformat()))
        
        session_duration = (session_end - session_start).total_seconds()
        
        # Calculate throughput
        interactions_per_minute = len(self.interactions) / (session_duration / 60) if session_duration > 0 else 0
        
        return {
            "session_duration_seconds": session_duration,
            "interactions_per_minute": interactions_per_minute,
            "avg_interaction_time": session_duration / len(self.interactions) if self.interactions else 0
        }
    
    def generate_report(self):
        """Generate comprehensive metrics report"""
        print("=" * 60)
        print("TALKING PHOTO FRAME V1.0 - PERFORMANCE METRICS REPORT")
        print("=" * 60)
        
        # Session info
        print(f"\nSession Start: {self.data.get('session_start')}")
        print(f"Session End: {self.data.get('session_end')}")
        
        # System metrics
        print("\n" + "=" * 60)
        print("SYSTEM METRICS")
        print("=" * 60)
        system_metrics = self.calculate_system_metrics()
        if system_metrics:
            print(f"Session Duration: {system_metrics['session_duration_seconds']:.2f} seconds")
            print(f"Total Interactions: {len(self.interactions)}")
            print(f"Interactions/Minute: {system_metrics['interactions_per_minute']:.2f}")
            print(f"Avg Time/Interaction: {system_metrics['avg_interaction_time']:.2f} seconds")
        
        # Latency metrics
        print("\n" + "=" * 60)
        print("LATENCY METRICS (seconds)")
        print("=" * 60)
        latency_metrics = self.calculate_latency_metrics()
        if latency_metrics:
            for component, stats in latency_metrics.items():
                if stats:
                    print(f"\n{component.upper()}:")
                    print(f"  Mean:   {stats['mean']:.3f}s")
                    print(f"  Median: {stats['median']:.3f}s")
                    print(f"  Min:    {stats['min']:.3f}s")
                    print(f"  Max:    {stats['max']:.3f}s")
                    print(f"  StdDev: {stats['stdev']:.3f}s")
        
        # Quality metrics
        print("\n" + "=" * 60)
        print("QUALITY METRICS")
        print("=" * 60)
        quality_metrics = self.calculate_quality_metrics()
        print(f"Success Rate: {quality_metrics['success_rate']*100:.1f}%")
        print(f"Successful Interactions: {quality_metrics['successful_interactions']}/{quality_metrics['total_interactions']}")
        print(f"Avg Input Length: {quality_metrics['avg_input_length']:.0f} characters")
        print(f"Avg Response Length: {quality_metrics['avg_response_length']:.0f} characters")
        
        # Component breakdown
        print("\n" + "=" * 60)
        print("LATENCY BREAKDOWN (% of total time)")
        print("=" * 60)
        if latency_metrics and latency_metrics.get("total"):
            total_avg = latency_metrics["total"]["mean"]
            if latency_metrics.get("s2t"):
                s2t_pct = (latency_metrics["s2t"]["mean"] / total_avg) * 100
                print(f"Speech-to-Text: {s2t_pct:.1f}%")
            if latency_metrics.get("nlp"):
                nlp_pct = (latency_metrics["nlp"]["mean"] / total_avg) * 100
                print(f"NLP Processing: {nlp_pct:.1f}%")
            if latency_metrics.get("t2s"):
                t2s_pct = (latency_metrics["t2s"]["mean"] / total_avg) * 100
                print(f"Text-to-Speech: {t2s_pct:.1f}%")
        
        # Performance rating
        print("\n" + "=" * 60)
        print("PERFORMANCE RATING")
        print("=" * 60)
        self.rate_performance(latency_metrics, quality_metrics)
        
        # Detailed interaction log
        print("\n" + "=" * 60)
        print("DETAILED INTERACTION LOG")
        print("=" * 60)
        for i, interaction in enumerate(self.interactions):
            print(f"\nInteraction {i+1}:")
            print(f"  User: {interaction.get('user_input', 'N/A')}")
            print(f"  Response: {interaction.get('response', 'N/A')}")
            print(f"  Total Latency: {interaction.get('total_latency', 0):.2f}s")
    
    def rate_performance(self, latency_metrics, quality_metrics):
        """Provide performance rating and recommendations"""
        if not latency_metrics or not latency_metrics.get("total"):
            print("Insufficient data for performance rating")
            return
        
        total_latency = latency_metrics["total"]["mean"]
        success_rate = quality_metrics["success_rate"]
        
        print("\nLatency Rating:")
        if total_latency < 5:
            print("  ✓ EXCELLENT - Very responsive system")
        elif total_latency < 10:
            print("  ✓ GOOD - Acceptable response times")
        elif total_latency < 15:
            print("  ⚠ FAIR - Noticeable delays")
        else:
            print("  ✗ POOR - Significant latency issues")
        
        print(f"\nReliability Rating:")
        if success_rate >= 0.95:
            print("  ✓ EXCELLENT - Very reliable")
        elif success_rate >= 0.80:
            print("  ✓ GOOD - Mostly reliable")
        elif success_rate >= 0.60:
            print("  ⚠ FAIR - Some failures")
        else:
            print("  ✗ POOR - Frequent failures")
        
        print("\nBottleneck Analysis:")
        if latency_metrics.get("nlp"):
            nlp_time = latency_metrics["nlp"]["mean"]
            if nlp_time > total_latency * 0.5:
                print("  ⚠ PRIMARY BOTTLENECK: NLP/API calls")
                print("    → Recommendation: Switch to local LLM for V2.0")
        
        if latency_metrics.get("s2t"):
            s2t_time = latency_metrics["s2t"]["mean"]
            if s2t_time > total_latency * 0.4:
                print("  ⚠ BOTTLENECK: Speech recognition")
                print("    → Recommendation: Use local Whisper model for V2.0")
        
        if latency_metrics.get("t2s"):
            t2s_time = latency_metrics["t2s"]["mean"]
            if t2s_time > total_latency * 0.3:
                print("  ⚠ BOTTLENECK: Text-to-speech")
                print("    → Recommendation: Optimize with local TTS + voice cloning")
        
        print("\nRecommendations for V2.0:")
        print("  1. Implement local LLM (Ollama) to eliminate API latency")
        print("  2. Use Whisper for faster local speech recognition")
        print("  3. Add voice cloning for authentic grandmother voice")
        print("  4. Implement face animation for dynamic visuals")
        print("  5. Optimize ambient noise handling for better recognition")

def main():
    if len(sys.argv) > 1:
        metrics_file = sys.argv[1]
    else:
        metrics_file = None
    
    analyzer = MetricsAnalyzer(metrics_file)
    analyzer.generate_report()
    
    # Save summary to file
    summary_file = "metrics_summary.txt"
    sys.stdout = open(summary_file, 'w')
    analyzer.generate_report()
    sys.stdout = sys.__stdout__
    
    print(f"\n\nReport also saved to: {summary_file}")

if __name__ == "__main__":
    main()