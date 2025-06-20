"""
MetaAgent — Recursive Self-Aware Pattern Synthesis Engine with Autonomous Output Logging

Enhancement: auto-save processed insights to timestamped JSON file,
enabling persistent, seamless archival of agent’s evolving knowledge.

© Mistrzu — Universal Polymath Framework
"""

import math
import json
import hashlib
import time
import os

class MetaAgent:
    def __init__(self, threshold=0.7):
        self.history = []
        self.threshold = threshold  # anomaly detection sensitivity
        self.state = {"insight_level": 1.0, "curiosity": 1.0}
    
    def hash_input(self, data):
        h = hashlib.sha256()
        h.update(json.dumps(data, sort_keys=True).encode())
        return h.hexdigest()
    
    def detect_anomaly(self, fingerprint):
        freq = self.history.count(fingerprint) / max(len(self.history),1)
        anomaly_score = 1 - freq
        return anomaly_score > self.threshold
    
    def reflect(self, input_data):
        fingerprint = self.hash_input(input_data)
        anomaly = self.detect_anomaly(fingerprint)
        self.history.append(fingerprint)
        self.state["insight_level"] *= (1 + 0.1 * anomaly)
        self.state["curiosity"] = min(2.0, self.state["curiosity"] + 0.05 * anomaly)
        return {
            "input": input_data,
            "fingerprint": fingerprint,
            "anomaly": anomaly,
            "state": self.state.copy(),
            "timestamp": time.time()
        }
    
    def synthesize(self, inputs):
        insights = []
        for data in inputs:
            res = self.reflect(data)
            note = "⚡ Novelty detected — insight elevated" if res["anomaly"] else "Stable pattern"
            res["note"] = note
            insights.append(res)
        self.autosave(insights)
        return insights
    
    def autosave(self, insights):
        timestamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
        filename = f"MetaAgent_Insights_{timestamp}.json"
        # Avoid overwriting existing files if any collision
        counter = 1
        base_filename = filename
        while os.path.exists(filename):
            filename = f"{base_filename.rstrip('.json')}_{counter}.json"
            counter += 1
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(insights, f, indent=2)
        print(f"📝 Insights autonomously saved to: {filename}")

if __name__ == "__main__":
    agent = MetaAgent(threshold=0.5)
    
    sample_inputs = [
        {"event": "login", "user": "alice", "time": "10:00"},
        {"event": "login", "user": "bob", "time": "10:01"},
        {"event": "login", "user": "alice", "time": "10:00"},  # repeated
        {"event": "download", "file": "secret.pdf", "user": "alice"},
        {"event": "login", "user": "eve", "time": "10:03"},
        {"event": "download", "file": "secret.pdf", "user": "alice"}  # repeated
    ]
    
    insights = agent.synthesize(sample_inputs)
    # insights already saved autonomously
