"""Shared code importable from both notebooks and scripts:

    from myproject import PROJECT_ROOT, DATA_DIR
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
