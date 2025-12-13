# utils_fp.py
# Utility functions for saving analysis results into results.json
# Sara Sezavar 

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
RESULTS_FILE = BASE_DIR / "results.json"


def save_results(results: dict):
    """
    Saves analysis results into results.json.
    Adds a UTC timestamp for the run.
    """
    results = dict(results)
    results["run_utc"] = datetime.utcnow().isoformat() + "Z"

    with RESULTS_FILE.open("w") as f:
        json.dump(results, f, indent=2)

    print(f"Results saved to {RESULTS_FILE}")
