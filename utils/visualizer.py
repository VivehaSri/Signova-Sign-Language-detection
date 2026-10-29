"""
Visual Overlay & HUD Utilities Module
Part of Signova AI: Basic Sign Language Word Recognition System
Theme: Dark Navy, Cyan, and Violet
"""

from typing import Optional, Tuple
import cv2
import numpy as np


class Visualizer:
    """
    Renders clean, modern HUD overlays, word prediction badges,
    and bounding boxes onto video frames with a Dark Navy, Cyan, and Violet aesthetic.
    """

    # Theme Palette (BGR for OpenCV)
    COLOR_NAVY_DARK = (26, 17, 15)      # Deep Dark Navy #0F111A
    COLOR_NAVY_BAR = (43, 30, 20)       # Navy Surface #141E2B
    COLOR_CYAN = (238, 214, 0)          # Electric Cyan #00D6EE
    COLOR_VIOLET = (226, 75, 147)       # Vibrant Violet #934BE2
    COLOR_SUCCESS_GREEN = (94, 209, 87)  # Verified Sign #57D15E
    COLOR_WARNING_ROSE = (75, 75, 235)   # Sign Not Recognized #EB4B4B
    COLOR_WHITE = (255, 255, 255)
    COLOR_TEXT_DIM = (180, 180, 190)

    @classmethod
    def draw_hud(
        cls,
        frame: np.ndarray,
        gesture_name: str,
        confidence: float,
        fps: Optional[float] = None,
        is_unknown: bool = False,
    ) -> np.ndarray:
        """
        Draw a modern Dark Navy, Cyan, and Violet header and prediction bar.
        """
        h, w, _ = frame.shape
        annotated = frame.copy()

        # Top Header Bar (Semi-transparent dark navy overlay)
        overlay = annotated.copy()
        cv2.rectangle(overlay, (0, 0), (w, 58), cls.COLOR_NAVY_DARK, -1)
        cv2.addWeighted(overlay, 0.85, annotated, 0.15, 0, annotated)

        # Violet accent line under top bar
        cv2.line(annotated, (0, 57), (w, 57), cls.COLOR_VIOLET, 2)

        # Title in clean font
        cv2.putText(
            annotated,
            "SIGNOVA AI",
            (20, 36),
            cv2.FONT_HERSHEY_DUPLEX,
            0.75,
            cls.COLOR_CYAN,
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            annotated,
            "| Basic Word Recognition",
            (175, 36),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.62,
            cls.COLOR_WHITE,
            1,
            cv2.LINE_AA,
        )

        # FPS indicator in cyan
        if fps is not None:
            fps_text = f"FPS: {int(fps)}"
            cv2.putText(
                annotated,
                fps_text,
                (w - 125, 36),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.60,
                cls.COLOR_CYAN,
                2,
                cv2.LINE_AA,
            )

        # Bottom Bar for Recognized Result
        bot_bar_height = 68
        overlay = annotated.copy()
        cv2.rectangle(overlay, (0, h - bot_bar_height), (w, h), cls.COLOR_NAVY_BAR, -1)
        cv2.addWeighted(overlay, 0.88, annotated, 0.12, 0, annotated)

        # Cyan accent line above bottom bar
        cv2.line(annotated, (0, h - bot_bar_height), (w, h - bot_bar_height), cls.COLOR_CYAN, 2)

        # Color and text based on state
        if is_unknown or gesture_name in ("Sign Not Recognized", "Unknown", "Unknown Gesture"):
            badge_color = cls.COLOR_WARNING_ROSE
            status_text = "Sign Not Recognized (Adjust hand pose)"
        elif gesture_name == "No Hand Detected":
            badge_color = cls.COLOR_TEXT_DIM
            status_text = "Waiting for hand in camera view..."
        else:
            badge_color = cls.COLOR_SUCCESS_GREEN
            status_text = f"Word: {gesture_name} ({confidence * 100:.1f}%)"

        # Glowing indicator dot
        cv2.circle(annotated, (30, h - 33), 9, badge_color, -1)
        cv2.circle(annotated, (30, h - 33), 13, badge_color, 1)

        # Subtitle text
        cv2.putText(
            annotated,
            status_text,
            (55, h - 26),
            cv2.FONT_HERSHEY_DUPLEX,
            0.82,
            cls.COLOR_WHITE,
            2,
            cv2.LINE_AA,
        )

        return annotated

    @classmethod
    def draw_hand_box(
        cls,
        frame: np.ndarray,
        bbox: Tuple[int, int, int, int],
        label: str,
        confidence: float,
        is_unknown: bool = False,
    ) -> np.ndarray:
        """
        Draw bounding box around hand with neon label chip.
        """
        xmin, ymin, xmax, ymax = bbox
        annotated = frame.copy()

        box_color = cls.COLOR_WARNING_ROSE if is_unknown else cls.COLOR_CYAN

        # Clean bounding box with corner highlights
        cv2.rectangle(annotated, (xmin, ymin), (xmax, ymax), box_color, 2)

        # Label tag
        chip_text = f"{label} ({int(confidence * 100)}%)" if not is_unknown else "Sign Not Recognized"
        (text_w, text_h), baseline = cv2.getTextSize(
            chip_text, cv2.FONT_HERSHEY_SIMPLEX, 0.58, 2
        )

        chip_y0 = max(0, ymin - text_h - 12)
        chip_y1 = ymin
        chip_x0 = xmin
        chip_x1 = xmin + text_w + 16

        cv2.rectangle(
            annotated,
            (chip_x0, chip_y0),
            (chip_x1, chip_y1),
            box_color,
            -1,
        )
        # Text on badge (dark text for high contrast on bright chip)
        cv2.putText(
            annotated,
            chip_text,
            (chip_x0 + 8, chip_y1 - 6),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            (10, 10, 20),
            2,
            cv2.LINE_AA,
        )

        return annotated
