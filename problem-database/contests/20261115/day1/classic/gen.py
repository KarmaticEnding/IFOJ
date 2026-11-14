#!/usr/bin/env python3
"""Reproduce classic data only after independent verification has passed."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parent
subprocess.run([sys.executable,str(root/'tools/verify.py')],check=True)
subprocess.run([sys.executable,str(root/'tools/generate.py')],check=True)
