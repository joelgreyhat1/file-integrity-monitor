import json
import os

BASELINE_FILE = "baseline.json"

def save_baseline(snapshot):
    with open(BASELINE_FILE, "w") as f:
        json.dump(snapshot, f, indent=2)
    print(f"Baseline saved to {BASELINE_FILE} ({len(snapshot)} files)")


def load_baseline():
    if not os.path.exists(BASELINE_FILE):
        return None
    with open(BASELINE_FILE, "r") as f:
        return json.load(f)