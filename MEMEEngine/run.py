"""
MEMEEngine Launcher
Run this file to start the game editor
"""

import sys
from pathlib import Path

# Add parent to path so imports work
sys.path.insert(0, str(Path(__file__).parent))

from SRC.main import main

if __name__ == "__main__":
    main()