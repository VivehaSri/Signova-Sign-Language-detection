"""
Hand Landmark Detection & Coordinate Normalization Module
Part of Signova: AI-Based Sign Language Recognition System
"""

import math
from typing import List, Optional, Tuple
import cv2
import numpy as np


class HandDetector:
    """
    Wrapper around MediaPipe Hands to detect hand landmarks,
    draw visual tracking indicators, and extract normalized feature vectors.
    """

    def __init__(
        self,
        static_mode: bool = False,
        max_num_hands: int = 1,
        min_detection_confidence: float = 0.7,
        min_tracking_confidence: float = 0.5,
    ):
        """
        Initialize the MediaPipe Hands model.
        """
        try:
            import mediapipe as mp
            if hasattr(mp, "solutions"):
                self.mp_hands = mp.solutions.hands
                self.mp_drawing = mp.solutions.drawing_utils
                self.mp_drawing_styles = mp.solutions.drawing_styles
            else:
                from mediapipe.python.solutions import hands as mp_hands
                from mediapipe.python.solutions import drawing_utils as mp_drawing
                from mediapipe.python.solutions import drawing_styles as mp_drawing_styles
                self.mp_hands = mp_hands
                self.mp_drawing = mp_drawing
                self.mp_drawing_styles = mp_drawing_styles
        except Exception:
            from mediapipe.python.solutions import hands as mp_hands
            from mediapipe.python.solutions import drawing_utils as mp_drawing
            from mediapipe.python.solutions import drawing_styles as mp_drawing_styles
            self.mp_hands = mp_hands
            self.mp_drawing = mp_drawing
            self.mp_drawing_styles = mp_drawing_styles

        self.hands = self.mp_hands.Hands(
            static_image_mode=static_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def find_hands(
        self, image: np.ndarray, draw: bool = True
    ) -> Tuple[np.ndarray, any]:
        """
        Process an image frame, detect hand landmarks, and optionally draw them.

        Args:
            image: OpenCV BGR image frame.
            draw: Whether to render landmark points and connecting lines.

        Returns:
            Tuple of (annotated_image, mediapipe_results).
        """
        # Convert BGR to RGB for MediaPipe processing
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = self.hands.process(image_rgb)
        image_rgb.flags.writeable = True

        annotated_image = image.copy()

        if results.multi_hand_landmarks and draw:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    annotated_image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style(),
                )

        return annotated_image, results

    @staticmethod
    def extract_features(hand_landmarks) -> List[float]:
        """
        Extract 21 (x, y) coordinates from MediaPipe hand landmarks,
        and normalize them to achieve translation and scale invariance.

        Normalization Steps:
        1. Origin Shift: Translate all coordinates so wrist (landmark 0) is at (0, 0):
           x'_i = x_i - x_0,  y'_i = y_i - y_0
        2. Scale Normalization: Divide by maximum Euclidean distance from the wrist:
           d_max = max(sqrt((x'_i)^2 + (y'_i)^2))
           x_norm_i = x'_i / d_max,  y_norm_i = y'_i / d_max

        Returns:
            List of 42 normalized float values [x0, y0, x1, y1, ..., x20, y20].
        """
        # 1. Translate relative to wrist (landmark 0)
        base_x = hand_landmarks.landmark[0].x
        base_y = hand_landmarks.landmark[0].y

        relative_coords: List[Tuple[float, float]] = []
        max_dist = 0.0

        for lm in hand_landmarks.landmark:
            dx = lm.x - base_x
            dy = lm.y - base_y
            dist = math.hypot(dx, dy)
            if dist > max_dist:
                max_dist = dist
            relative_coords.append((dx, dy))

        # Avoid zero division if hand landmarks collapse
        if max_dist == 0.0:
            max_dist = 1.0

        # 2. Scale normalize into range [-1.0, 1.0]
        normalized_features: List[float] = []
        for dx, dy in relative_coords:
            normalized_features.append(dx / max_dist)
            normalized_features.append(dy / max_dist)

        return normalized_features

    @staticmethod
    def get_bounding_box(
        image: np.ndarray, hand_landmarks, padding: int = 20
    ) -> Tuple[int, int, int, int]:
        """
        Compute pixel bounding box (xmin, ymin, xmax, ymax) around hand landmarks.
        """
        h, w, _ = image.shape
        x_coords = [int(lm.x * w) for lm in hand_landmarks.landmark]
        y_coords = [int(lm.y * h) for lm in hand_landmarks.landmark]

        xmin = max(0, min(x_coords) - padding)
        ymin = max(0, min(y_coords) - padding)
        xmax = min(w, max(x_coords) + padding)
        ymax = min(h, max(y_coords) + padding)

        return xmin, ymin, xmax, ymax

    def close(self):
        """Release MediaPipe resources."""
        if hasattr(self, "hands") and self.hands:
            self.hands.close()
