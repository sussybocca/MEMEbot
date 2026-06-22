"""
MEMEBOT Bot Engagement System - Entry Point
Launches the Flask web server for the bot engagement platform
"""

import os
import sys
import webbrowser
import threading
import time
from pathlib import Path

# Ensure the project root is in the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from server import app


def open_browser():
    """Open the default web browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5050')


def main():
    """Main entry point"""
    print("=" * 60)
    print("  🎭 MEMEBOT Bot Engagement System")
    print("  AI-Powered Skin Review Platform")
    print("=" * 60)
    print()
    print("  Starting server...")
    print(f"  Database location: {project_root / 'data' / 'bot_engagement.db'}")
    print(f"  Upload folder: {project_root / 'uploads'}")
    print()
    print("  Opening browser at: http://127.0.0.1:5050")
    print()
    print("  Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Open browser in a separate thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the Flask app
    app.run(
        host='127.0.0.1',
        port=5050,
        debug=False,
        use_reloader=False
    )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nShutting down MEMEBOT Bot Engagement System...")
        print("Goodbye!")
        sys.exit(0)