"""Forge entry point.  Usage: python app.py "Build a Go login backend with JWT" """
import sys
from planner import pipeline

if __name__ == "__main__":
    request = " ".join(sys.argv[1:])
    if not request:
        request = input("What should Forge build? > ").strip()
    pipeline.run(request)
