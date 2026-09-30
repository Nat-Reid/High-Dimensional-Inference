"""Sanity check: run this after setup and compare output with your collaborator.

    uv run python scripts/check_env.py
"""
import platform
import sys
from importlib.metadata import version

from myproject import DATA_DIR, PROJECT_ROOT

print(f"OS:            {platform.system()}")
print(f"Python:        {sys.version.split()[0]}")
print(f"Interpreter:   {sys.executable}")
print(f"Project root:  {PROJECT_ROOT}")
print(f"Data dir:      {DATA_DIR}")
for pkg in ("numpy", "pandas", "matplotlib"):
    print(f"{pkg:<14} {version(pkg)}")
