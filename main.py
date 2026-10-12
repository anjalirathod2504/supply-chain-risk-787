"""Run this file to run the whole project.

It runs the exposure index, FMEA and Monte Carlo tariff model,
and tells you where the results are.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / "src"))

from scrisk import run_analysis  # noqa: E402

print("Running all three analyses (takes a few seconds)...")
run_analysis.main()
print()
print("DONE. Results:")
print(f"  Report : {ROOT / 'reports' / 'analysis.md'}")
print(f"  Charts : {ROOT / 'reports' / 'ttr_tts.png'}")
print(f"           {ROOT / 'reports' / 'landed_cost.png'}")
