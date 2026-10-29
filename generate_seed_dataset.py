"""
Generate Seed Training Dataset for Signova AI
Canonical ASL / ISL Basic Vocabulary:
  YES, NO, STOP, HELP, PLEASE, THANK YOU, HELLO
Ensures identical 42D normalized feature vectors to HandDetector.extract_features
Includes Left/Right hand reflection, angular variance, and scale jitter.
"""

import os
import sys
import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.hand_detector import HandDetector

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DATA_FILE = os.path.join(DATA_DIR, "gestures.csv")

FEATURE_COLUMNS = ["label"] + [
    f"lm_{i}_{coord}" for i in range(21) for coord in ("x", "y")
]

# The Official Core Vocabulary for Signova AI
SUPPORTED_WORDS = ["YES", "NO", "STOP", "HELP", "PLEASE", "THANK YOU", "HELLO", "LOVE", "PEACE"]


def get_canonical_hand_pose(gesture: str) -> np.ndarray:
    """
    Returns 21 (x, y) coordinates for canonical sign word representations.
    MediaPipe landmark indices:
      0: Wrist
      1-4: Thumb (CMC, MCP, IP, Tip)
      5-8: Index (MCP, PIP, DIP, Tip)
      9-12: Middle (MCP, PIP, DIP, Tip)
      13-16: Ring (MCP, PIP, DIP, Tip)
      17-20: Pinky (MCP, PIP, DIP, Tip)
    """
    # Base neutral hand (Open Palm / HELLO)
    # Wrist at (0.50, 0.85)
    pts = np.array([
        [0.50, 0.85],  # 0: Wrist
        # Thumb
        [0.43, 0.77],  # 1: Thumb CMC
        [0.36, 0.68],  # 2: Thumb MCP
        [0.30, 0.59],  # 3: Thumb IP
        [0.24, 0.51],  # 4: Thumb Tip
        # Index
        [0.44, 0.55],  # 5: Index MCP
        [0.42, 0.40],  # 6: Index PIP
        [0.41, 0.28],  # 7: Index DIP
        [0.40, 0.16],  # 8: Index Tip
        # Middle
        [0.50, 0.53],  # 9: Middle MCP
        [0.50, 0.37],  # 10: Middle PIP
        [0.50, 0.24],  # 11: Middle DIP
        [0.50, 0.12],  # 12: Middle Tip
        # Ring
        [0.56, 0.55],  # 13: Ring MCP
        [0.58, 0.40],  # 14: Ring PIP
        [0.60, 0.28],  # 15: Ring DIP
        [0.61, 0.18],  # 16: Ring Tip
        # Pinky
        [0.62, 0.60],  # 17: Pinky MCP
        [0.66, 0.48],  # 18: Pinky PIP
        [0.68, 0.38],  # 19: Pinky DIP
        [0.70, 0.28],  # 20: Pinky Tip
    ], dtype=np.float32)

    g = gesture.strip().upper()

    if g == "HELLO":
        # All 5 fingers extended upward with natural spread
        pass

    elif g == "YES":
        # Thumbs-Up: 4 fingers curled into fist, thumb pointing straight UP
        pts[5:9] = [[0.46, 0.62], [0.45, 0.56], [0.47, 0.64], [0.49, 0.70]]
        pts[9:13] = [[0.51, 0.63], [0.51, 0.56], [0.53, 0.64], [0.54, 0.71]]
        pts[13:17] = [[0.56, 0.64], [0.56, 0.58], [0.57, 0.65], [0.57, 0.72]]
        pts[17:21] = [[0.61, 0.67], [0.61, 0.62], [0.61, 0.68], [0.60, 0.73]]
        # Thumb pointing straight UP (high y coordinate / lowest number)
        pts[1:5] = [[0.43, 0.76], [0.40, 0.66], [0.40, 0.50], [0.40, 0.34]]

    elif g == "NO":
        # Pointing Index Finger: Index extended UP, other 3 fingers curled into palm
        pts[5:9] = [[0.45, 0.55], [0.44, 0.40], [0.43, 0.28], [0.42, 0.16]]
        # Middle, Ring, Pinky curled down
        pts[9:13] = [[0.51, 0.63], [0.51, 0.56], [0.53, 0.64], [0.54, 0.71]]
        pts[13:17] = [[0.56, 0.64], [0.56, 0.58], [0.57, 0.65], [0.57, 0.72]]
        pts[17:21] = [[0.61, 0.67], [0.61, 0.62], [0.61, 0.68], [0.60, 0.73]]
        # Thumb folded across middle finger
        pts[1:5] = [[0.44, 0.75], [0.41, 0.68], [0.45, 0.62], [0.49, 0.60]]

    elif g == "HELP":
        # Solid Closed Fist: ALL 4 fingers curled, thumb folded across fingers
        pts[5:9] = [[0.45, 0.62], [0.44, 0.55], [0.46, 0.63], [0.47, 0.69]]
        pts[9:13] = [[0.50, 0.62], [0.50, 0.54], [0.50, 0.63], [0.50, 0.70]]
        pts[13:17] = [[0.55, 0.63], [0.55, 0.56], [0.54, 0.64], [0.53, 0.70]]
        pts[17:21] = [[0.60, 0.66], [0.60, 0.60], [0.58, 0.67], [0.56, 0.72]]
        # Thumb folded across fingers (fist)
        pts[1:5] = [[0.44, 0.75], [0.41, 0.68], [0.43, 0.60], [0.48, 0.58]]

    elif g == "STOP":
        # Flat B-Hand facing camera: 4 fingers straight together pointing UP, thumb extended OUT to side
        pts[5:9] = [[0.45, 0.55], [0.44, 0.40], [0.44, 0.28], [0.44, 0.16]]
        pts[9:13] = [[0.49, 0.54], [0.49, 0.38], [0.49, 0.26], [0.49, 0.14]]
        pts[13:17] = [[0.53, 0.55], [0.53, 0.40], [0.53, 0.28], [0.53, 0.16]]
        pts[17:21] = [[0.57, 0.58], [0.57, 0.45], [0.57, 0.35], [0.57, 0.24]]
        # Thumb extended outward away from palm
        pts[1:5] = [[0.43, 0.76], [0.36, 0.70], [0.30, 0.64], [0.24, 0.58]]

    elif g == "PLEASE":
        # Flat vertical hand (Namaste): 4 fingers straight together, thumb folded flat against palm
        pts[5:9] = [[0.46, 0.54], [0.45, 0.40], [0.44, 0.29], [0.44, 0.17]]
        pts[9:13] = [[0.50, 0.53], [0.50, 0.38], [0.50, 0.26], [0.50, 0.15]]
        pts[13:17] = [[0.54, 0.54], [0.55, 0.39], [0.55, 0.28], [0.55, 0.17]]
        pts[17:21] = [[0.58, 0.58], [0.59, 0.46], [0.60, 0.36], [0.60, 0.25]]
        # Thumb tucked flat against index knuckle / palm
        pts[1:5] = [[0.43, 0.77], [0.41, 0.70], [0.46, 0.65], [0.50, 0.62]]

    elif g == "THANK YOU":
        # Flat hand forward: 4 fingers straight together, angled forward toward viewer
        pts[5:9] = [[0.46, 0.55], [0.45, 0.42], [0.44, 0.31], [0.44, 0.22]]
        pts[9:13] = [[0.50, 0.54], [0.50, 0.40], [0.50, 0.28], [0.50, 0.20]]
        pts[13:17] = [[0.54, 0.55], [0.55, 0.41], [0.55, 0.30], [0.55, 0.22]]
        pts[17:21] = [[0.58, 0.59], [0.59, 0.47], [0.60, 0.37], [0.60, 0.28]]
        # Thumb relaxed alongside palm
        pts[1:5] = [[0.42, 0.77], [0.38, 0.70], [0.36, 0.62], [0.34, 0.56]]

    elif g == "LOVE":
        # ASL "I LOVE YOU" (ILY sign 🤟): Thumb, Index, Pinky extended; Middle & Ring curled
        pts[5:9] = [[0.44, 0.55], [0.42, 0.40], [0.41, 0.28], [0.40, 0.16]]    # Index extended UP
        pts[9:13] = [[0.51, 0.63], [0.51, 0.56], [0.53, 0.64], [0.54, 0.71]]   # Middle curled DOWN
        pts[13:17] = [[0.56, 0.64], [0.56, 0.58], [0.57, 0.65], [0.57, 0.72]]  # Ring curled DOWN
        pts[17:21] = [[0.62, 0.60], [0.66, 0.48], [0.68, 0.38], [0.70, 0.26]]  # Pinky extended UP
        pts[1:5] = [[0.43, 0.77], [0.36, 0.68], [0.28, 0.58], [0.20, 0.50]]    # Thumb extended OUTWARD

    elif g == "PEACE":
        # "PEACE" / Victory (V-Sign ✌️): Index and Middle extended forming a V
        pts[5:9] = [[0.45, 0.55], [0.42, 0.39], [0.39, 0.27], [0.36, 0.16]]    # Index extended angled left
        pts[9:13] = [[0.51, 0.54], [0.54, 0.39], [0.57, 0.27], [0.60, 0.16]]   # Middle extended angled right
        pts[13:17] = [[0.56, 0.64], [0.56, 0.58], [0.57, 0.65], [0.57, 0.72]]  # Ring curled
        pts[17:21] = [[0.61, 0.67], [0.61, 0.62], [0.61, 0.68], [0.60, 0.73]]  # Pinky curled
        pts[1:5] = [[0.44, 0.75], [0.41, 0.68], [0.46, 0.62], [0.52, 0.60]]    # Thumb folded over ring

    return pts


def normalize_simulated_points(pts: np.ndarray) -> np.ndarray:
    """
    Translates relative to wrist (point 0) and normalizes by max distance.
    Identical transformation to HandDetector.extract_features.
    """
    base_x = pts[0, 0]
    base_y = pts[0, 1]

    dx = pts[:, 0] - base_x
    dy = pts[:, 1] - base_y

    distances = np.hypot(dx, dy)
    d_max = np.max(distances)
    if d_max == 0:
        d_max = 1.0

    nx = dx / d_max
    ny = dy / d_max

    features = []
    for i in range(21):
        features.append(float(nx[i]))
        features.append(float(ny[i]))
    return np.array(features, dtype=np.float32)


def generate_seed_dataset(samples_per_class: int = 200, force_regenerate: bool = True):
    """
    Generate clean, diverse training data for the official 7 sign language words:
    - Left Hand & Right Hand Invariance (50% horizontal reflection)
    - Rotation (-25 to +25 degrees)
    - Scale stretch (0.85x to 1.15x)
    - Random joint jitter / sensor noise (MediaPipe tracking variance)
    """
    os.makedirs(DATA_DIR, exist_ok=True)

    np.random.seed(42)
    all_rows = []

    for word in SUPPORTED_WORDS:
        canonical = get_canonical_hand_pose(word)

        for _ in range(samples_per_class):
            pts = canonical.copy()

            # 1. Left Hand & Right Hand Invariance (Horizontal Flip)
            # Ensures 50% left-hand and 50% right-hand coverage so any hand is recognized
            if np.random.rand() > 0.5:
                wrist_x = pts[0, 0]
                pts[:, 0] = 2.0 * wrist_x - pts[:, 0]

            # 2. Random rotation between -25 and +25 degrees around hand center (Middle MCP)
            center = pts[9]
            angle_deg = np.random.uniform(-25.0, 25.0)
            theta = np.radians(angle_deg)
            cos_t, sin_t = np.cos(theta), np.sin(theta)

            shifted = pts - center
            rot_x = shifted[:, 0] * cos_t - shifted[:, 1] * sin_t
            rot_y = shifted[:, 0] * sin_t + shifted[:, 1] * cos_t
            pts = np.column_stack([rot_x, rot_y]) + center

            # 3. Scale variation (0.85x to 1.15x)
            scale_x = np.random.uniform(0.85, 1.15)
            scale_y = np.random.uniform(0.85, 1.15)
            pts[:, 0] *= scale_x
            pts[:, 1] *= scale_y

            # 4. Micro joint jitter / sensor noise (MediaPipe tracking variance)
            noise = np.random.normal(0.0, 0.015, size=pts.shape)
            noise[0] = 0.0  # Keep wrist relatively stable
            pts += noise

            # 5. Extract normalized features
            feats = normalize_simulated_points(pts)
            all_rows.append([word] + feats.tolist())

    df = pd.DataFrame(all_rows, columns=FEATURE_COLUMNS)
    df.to_csv(DATA_FILE, index=False)
    print(f"[+] Generated {len(df)} realistic samples for words: {SUPPORTED_WORDS}")
    print(f"[+] Saved dataset to: {DATA_FILE}")


if __name__ == "__main__":
    generate_seed_dataset(samples_per_class=200, force_regenerate=True)
