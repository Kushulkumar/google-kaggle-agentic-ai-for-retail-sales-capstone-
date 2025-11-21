"""Auto-runner generated to execute discovered Python scripts safely.

It will run each script listed in this project in a separate subprocess and
capture stdout/stderr to logs/run_<scriptname>.log
"""
import os
import subprocess
import sys
import shlex
import traceback
from datetime import datetime

py_files = [
    'capstone_extracted/google-kaggle-agentic-ai-for-retail-sales-capstone/src/data_pipeline.py',
    'capstone_extracted/google-kaggle-agentic-ai-for-retail-sales-capstone/src/train.py',
    'capstone_extracted/google-kaggle-agentic-ai-for-retail-sales-capstone/src/predict.py',
]

os.makedirs("logs", exist_ok=True)

results = {}
for rel in py_files:
    script_path = os.path.join(os.path.dirname(__file__), rel)
    logname = "run_" + os.path.basename(rel).replace('.', '_') + ".log"
    logpath = os.path.join(os.path.dirname(__file__), "logs", logname)
    cmd = [sys.executable, script_path]
    # Run the script with its own directory as cwd so relative paths/imports work
    cwd = os.path.dirname(script_path) or os.path.dirname(__file__)
    try:
        with open(logpath, "w", encoding="utf-8") as log:
            log.write(f"Timestamp: {datetime.utcnow().isoformat()}Z\n")
            log.write("Running: " + shlex.join(cmd) + "\n")
            log.write(f"CWD: {cwd}\n\n")
            proc = subprocess.run(cmd, stdout=log, stderr=log, timeout=600, cwd=cwd)
            results[rel] = proc.returncode
    except Exception:
        with open(logpath, "a", encoding="utf-8") as log:
            log.write("\nException when running script:\n")
            traceback.print_exc(file=log)
        results[rel] = "error"

print("Run summary:", results)
