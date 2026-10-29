"""
Signova System & Hardware Diagnostic Utility
Run this script to verify your webcam, MediaPipe, OpenCV, and pyttsx3 installation.
"""

import sys
import time

def run_diagnostics():
    print("=" * 60)
    print("  SIGNOVA SYSTEM & WEBCAM DIAGNOSTICS")
    print("=" * 60)
    print(f"[1/4] Checking Python environment: {sys.version.split()[0]} ({sys.executable})")

    # 1. Test OpenCV & MediaPipe imports
    try:
        import cv2
        print(f"[2/4] OpenCV version: {cv2.__version__} - SUCCESS")
    except ImportError as e:
        print(f"[2/4] OpenCV import error: {e}")
        return False

    try:
        import mediapipe as mp
        print(f"[3/4] MediaPipe version: {getattr(mp, '__version__', 'detected')} - SUCCESS")
    except ImportError as e:
        print(f"[3/4] MediaPipe import error: {e}")
        return False

    # 2. Test pyttsx3
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.stop()
        print("[4/4] Text-To-Speech (pyttsx3) engine initialized - SUCCESS")
    except Exception as e:
        print(f"[4/4] pyttsx3 warning (browser fallback will be active): {e}")

    # 3. Test Camera Access
    print("-" * 60)
    print("Testing Webcam Access (Index 0)...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[-] Camera Index 0 failed. Testing Index 1...")
        cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("[-] ERROR: Could not open any webcam. Please ensure your webcam is connected")
        print("    and not used by another application (e.g., Zoom, Teams, Camera app).")
        return False

    ret, frame = cap.read()
    if ret and frame is not None:
        h, w, _ = frame.shape
        print(f"[+] Webcam successfully captured a frame! Resolution: {w}x{h}")
    else:
        print("[-] ERROR: Opened camera device but failed to capture a video frame.")
        cap.release()
        return False

    cap.release()
    print("=" * 60)
    print("  DIAGNOSTICS PASSED! All core components are ready.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    run_diagnostics()
