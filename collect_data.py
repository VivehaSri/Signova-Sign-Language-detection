"""
Sign Language Word Data Collector Module
Interactive tool to capture real webcam hand landmark samples and label them for basic words.
Supported ASL Vocabulary: YES, NO, STOP, HELP, PLEASE, THANK YOU, HELLO.
Part of Signova AI: Basic Sign Language Word Recognition System
"""

import os
import sys
import time
import argparse
from typing import List
import cv2
import pandas as pd
import numpy as np

# Ensure local imports work regardless of execution directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.hand_detector import HandDetector
from utils.visualizer import Visualizer

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DATA_FILE = os.path.join(DATA_DIR, "gestures.csv")

# Standard landmark column headers: label, x0, y0, x1, y1, ... x20, y20
FEATURE_COLUMNS = ["label"] + [
    f"lm_{i}_{coord}" for i in range(21) for coord in ("x", "y")
]

ASL_POSTURE_TIPS = {
    "YES": "ASL 'S' Fist: Closed fist facing camera with thumb across front fingers.",
    "NO": "ASL 'NO': Index and middle fingers extended together, tapping thumb tip.",
    "STOP": "ASL 'STOP': Open flat 'B' hand, all 4 fingers straight together, thumb alongside.",
    "HELP": "ASL 'HELP': Closed fist with thumb pointing vertically upward along index.",
    "PLEASE": "ASL 'PLEASE': Flat open hand held upright at chest plane, thumb folded flat across palm.",
    "THANK YOU": "ASL 'THANK YOU': Flat open hand angled forward towards viewer, thumb extended naturally.",
    "HELLO": "ASL 'HELLO': Open palm facing forward, all 5 fingers spread naturally upright.",
}


def ensure_dataset_file():
    """Ensure data directory and gestures.csv exist with appropriate header."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=FEATURE_COLUMNS)
        df.to_csv(DATA_FILE, index=False)
        print(f"[+] Initialized new dataset file at: {DATA_FILE}")


def collect_samples(
    gesture_name: str,
    target_samples: int = 60,
    camera_index: int = 0,
):
    """
    Capture live hand samples from webcam for a specific sign word label.

    Args:
        gesture_name: Name of the sign word to collect (e.g. "YES", "STOP", "HELP").
        target_samples: Number of valid frames to record.
        camera_index: Webcam index (default: 0).
    """
    ensure_dataset_file()
    gesture_name = gesture_name.strip().upper()
    if not gesture_name:
        print("[-] Error: Word name cannot be empty.")
        return

    posture_tip = ASL_POSTURE_TIPS.get(gesture_name, f"Hold canonical hand shape for '{gesture_name}'.")

    print("=" * 70)
    print(f"  SIGNOVA AI - COLLECTING SAMPLES FOR WORD: '{gesture_name}'")
    print("=" * 70)
    print(f"  ASL Guidance : {posture_tip}")
    print("  Instructions :")
    print("    1. Position your hand inside the webcam frame.")
    print("    2. Form the proper ASL hand shape.")
    print("    3. Press 'S' on your keyboard to START recording (3s countdown).")
    print("    4. While recording, slowly tilt/vary your hand angle slightly.")
    print("    5. Press 'Q' at any time to quit.")
    print("=" * 70)

    detector = HandDetector(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"[-] Failed to open webcam at index {camera_index}. Trying index 1...")
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
            print("[-] Unable to open webcam. Exiting.")
            return

    recorded_features: List[List[float]] = []
    is_recording = False
    countdown_start = None
    countdown_seconds = 3

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[-] Video capture stream ended.")
            break

        # Flip horizontally for natural mirror feel
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        annotated_frame, results = detector.find_hands(frame, draw=True)
        hand_detected = bool(results.multi_hand_landmarks)

        # Status text rendering (Dark navy overlay with cyan accent)
        status_bar = annotated_frame.copy()
        cv2.rectangle(status_bar, (0, 0), (w, 65), (26, 17, 15), -1)
        cv2.addWeighted(status_bar, 0.85, annotated_frame, 0.15, 0, annotated_frame)
        cv2.line(annotated_frame, (0, 64), (w, 64), (226, 75, 147), 2)

        # Header info
        title_text = f"Recording: {gesture_name} | Target: {target_samples}"
        cv2.putText(
            annotated_frame,
            title_text,
            (20, 36),
            cv2.FONT_HERSHEY_DUPLEX,
            0.75,
            (238, 214, 0),  # Cyan
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            annotated_frame,
            posture_tip[:60] + ("..." if len(posture_tip) > 60 else ""),
            (20, 56),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (200, 200, 220),
            1,
            cv2.LINE_AA,
        )

        # Handle countdown before recording starts
        if countdown_start is not None:
            elapsed = time.time() - countdown_start
            remaining = countdown_seconds - int(elapsed)
            if remaining > 0:
                cd_text = f"Get Ready: {remaining}..."
                cv2.putText(
                    annotated_frame,
                    cd_text,
                    (w // 2 - 170, h // 2),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1.3,
                    (238, 214, 0),
                    3,
                    cv2.LINE_AA,
                )
            else:
                countdown_start = None
                is_recording = True

        # Recording logic
        if is_recording:
            if hand_detected:
                features = detector.extract_features(results.multi_hand_landmarks[0])
                recorded_features.append([gesture_name] + features)
                current_count = len(recorded_features)

                # Progress bar at bottom
                progress = current_count / target_samples
                bar_w = int(w * progress)
                cv2.rectangle(annotated_frame, (0, h - 25), (bar_w, h), (94, 209, 87), -1)
                cv2.putText(
                    annotated_frame,
                    f"Recording: {current_count}/{target_samples} ({int(progress*100)}%)",
                    (20, h - 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (94, 209, 87),
                    2,
                )

                if current_count >= target_samples:
                    print(f"[+] Reached target count of {target_samples} samples for '{gesture_name}'.")
                    break
            else:
                cv2.putText(
                    annotated_frame,
                    "Hand lost! Bring hand back into camera view",
                    (20, h - 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (75, 75, 235),
                    2,
                )
        else:
            # Not recording yet - show instruction prompt
            cv2.putText(
                annotated_frame,
                "Press 'S' to Start Recording | 'Q' to Quit",
                (20, h - 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.68,
                (240, 240, 240),
                2,
            )

        cv2.imshow("Signova AI Data Collector", annotated_frame)
        key = cv2.waitKey(1) & 0xFF

        if key in (ord("q"), ord("Q"), 27):  # 'q' or ESC
            print("[*] Collection cancelled by user.")
            break
        elif key in (ord("s"), ord("S")) and not is_recording and countdown_start is None:
            if not hand_detected:
                print("[-] Please hold your hand in front of the camera before pressing 'S'.")
            else:
                countdown_start = time.time()

    cap.release()
    cv2.destroyAllWindows()
    detector.close()

    # Save to CSV
    if recorded_features:
        new_df = pd.DataFrame(recorded_features, columns=FEATURE_COLUMNS)
        new_df.to_csv(DATA_FILE, mode="a", header=not os.path.exists(DATA_FILE), index=False)
        print(f"[+] Successfully saved {len(recorded_features)} samples for '{gesture_name}' to {DATA_FILE}")

        total_df = pd.read_csv(DATA_FILE)
        print("\n--- Current Dataset Distribution ---")
        print(total_df["label"].value_counts().to_string())
        print("------------------------------------\n")
    else:
        print("[-] No samples were recorded.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect basic sign language word samples for Signova AI")
    parser.add_argument("--gesture", type=str, default="YES", help="Name of the word sign (e.g. YES, NO, STOP, HELP, PLEASE, THANK YOU)")
    parser.add_argument("--samples", type=int, default=60, help="Number of frames to record")
    parser.add_argument("--cam", type=int, default=0, help="Webcam camera index")
    args = parser.parse_args()

    collect_samples(gesture_name=args.gesture, target_samples=args.samples, camera_index=args.cam)
