"""
Signova AI: Basic Sign Language Word Recognition System
Interactive Streamlit Web Application
Standard: American Sign Language (ASL) Basic Vocabulary:
  YES, NO, STOP, HELP, PLEASE, THANK YOU, HELLO
Theme: Dark Navy, Cyan, and Violet
"""

import os
import sys
import time
import pickle
import json
from collections import deque
from typing import Optional, Tuple, Dict, Any, List

import cv2
import numpy as np
import pandas as pd
import streamlit as st

# Ensure project root is in system path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.hand_detector import HandDetector
from utils.tts_engine import TTSEngine
from utils.visualizer import Visualizer

# Paths
MODEL_PATH = os.path.join(ROOT_DIR, "models", "gesture_model.pkl")
METADATA_PATH = os.path.join(ROOT_DIR, "models", "model_metadata.json")
DATA_FILE = os.path.join(ROOT_DIR, "data", "gestures.csv")

# Standard Core Sign Language Vocabulary
BASIC_WORDS = ["YES", "NO", "STOP", "HELP", "PLEASE", "THANK YOU", "HELLO", "LOVE", "PEACE"]

# Streamlit Page Configuration
st.set_page_config(
    page_title="Signova AI | Basic Word Recognition",
    page_icon="🖐️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling: Modern Premium Light Theme (Royal Blue #2563EB, Teal #0D9488, Sky Blue #0284C7, Navy #0F172A)
st.markdown(
    """
    <style>
        /* Hide Streamlit default chrome & deploy button */
        #MainMenu {visibility: hidden !important;}
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        .stDeployButton {display: none !important;}
        [data-testid="stToolbar"] {visibility: hidden !important;}
        
        /* Base page light styling */
        .stApp {
            background-color: #F8FAFC !important;
            color: #1E293B !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        /* Global text styling */
        h1, h2, h3, h4, h5, h6 {
            color: #0F172A !important;
            font-weight: 700 !important;
        }
        p, span, div, label {
            color: #334155;
        }

        /* Top Hero Header */
        .hero-badge {
            display: inline-block;
            background: #F0FDFA;
            border: 1px solid #99F6E4;
            color: #0D9488;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        .main-header {
            font-size: 2.2rem;
            font-weight: 800;
            color: #0F172A !important;
            margin-bottom: 4px;
            letter-spacing: -0.5px;
        }
        .sub-header {
            font-size: 0.98rem;
            color: #64748B !important;
            margin-bottom: 22px;
        }

        /* Clean White Cards */
        .white-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
            margin-bottom: 20px;
        }
        .white-card:hover {
            border-color: #CBD5E1;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.05);
            transition: all 0.25s ease;
        }

        /* Camera Viewport Standby Screen */
        .camera-standby-box {
            background: #FFFFFF;
            border: 2px dashed #CBD5E1;
            border-radius: 16px;
            padding: 48px 24px;
            text-align: center;
            min-height: 420px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        }
        .camera-standby-icon {
            width: 72px;
            height: 72px;
            border-radius: 50%;
            background: #EFF6FF;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.2rem;
            margin-bottom: 16px;
            color: #2563EB;
            border: 1px solid #BFDBFE;
        }
        .camera-standby-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 6px;
        }
        .camera-standby-subtitle {
            font-size: 0.92rem;
            color: #64748B;
            max-width: 420px;
            line-height: 1.5;
            margin-bottom: 18px;
        }
        .camera-pill-tag {
            background: #F1F5F9;
            border: 1px solid #E2E8F0;
            color: #475569;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.78rem;
            font-weight: 600;
        }

        /* Recognized word banner (Light Theme) */
        .prediction-badge-success {
            font-size: 2.2rem;
            font-weight: 800;
            color: #1D4ED8 !important;
            padding: 16px 12px;
            border-radius: 14px;
            text-align: center;
            background: #EFF6FF;
            border: 2px solid #2563EB;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.10);
            letter-spacing: 0.5px;
        }
        .prediction-badge-warning {
            font-size: 1.6rem;
            font-weight: 700;
            color: #DC2626 !important;
            padding: 16px 12px;
            border-radius: 14px;
            text-align: center;
            background: #FEF2F2;
            border: 2px solid #F87171;
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.08);
        }
        .prediction-badge-idle {
            font-size: 1.5rem;
            font-weight: 600;
            color: #64748B !important;
            padding: 18px 12px;
            border-radius: 14px;
            text-align: center;
            background: #F8FAFC;
            border: 2px dashed #CBD5E1;
        }

        /* Streamlit Buttons Overrides (Light Theme) */
        div.stButton > button:first-child {
            border-radius: 10px;
            font-weight: 600;
            padding: 9px 18px;
            font-size: 0.92rem;
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
        }

        /* Primary Button (Start Camera): Fresh Teal / Blue */
        div.stButton > button[kind="primary"] {
            background-color: #0D9488 !important;
            color: #FFFFFF !important;
            border: none !important;
            font-weight: 700 !important;
            box-shadow: 0 2px 6px rgba(13, 148, 136, 0.25) !important;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #0F766E !important;
            box-shadow: 0 4px 12px rgba(13, 148, 136, 0.35) !important;
        }

        /* Secondary Button (Stop Camera): Neutral Light */
        div.stButton > button[kind="secondary"] {
            background-color: #FFFFFF !important;
            color: #334155 !important;
            border: 1px solid #CBD5E1 !important;
        }
        div.stButton > button[kind="secondary"]:hover {
            background-color: #F8FAFC !important;
            border-color: #DC2626 !important;
            color: #DC2626 !important;
        }
        
        /* Sentence box (Light Theme) */
        .sentence-box {
            background: #F8FAFC;
            border: 1.5px solid #BAE6FD;
            border-radius: 12px;
            padding: 16px 20px;
            font-size: 1.15rem;
            font-weight: 600;
            color: #0F172A;
            min-height: 56px;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.04);
        }

        /* Metric card (Light Theme) */
        .metric-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 18px 22px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        }
        .metric-card:hover {
            border-color: #93C5FD;
            box-shadow: 0 6px 16px rgba(37, 99, 235, 0.08);
            transform: translateY(-2px);
            transition: all 0.22s ease-in-out;
        }

        /* Progress Bar Light Styling */
        .stProgress > div > div > div > div {
            background-color: #0D9488 !important;
            border-radius: 6px;
        }

        /* ================= SIDEBAR LIGHT THEME ================= */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0 !important;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.02) !important;
        }

        /* Hide default radio circle buttons */
        [data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }

        /* Style radio items as modern interactive nav cards (Light Theme) */
        [data-testid="stSidebar"] div[role="radiogroup"] {
            gap: 6px !important;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] > label {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 10px !important;
            padding: 11px 14px !important;
            margin-bottom: 6px !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background-color: #F8FAFC !important;
            border-color: #CBD5E1 !important;
            transform: translateX(3px) !important;
        }

        /* Active Navigation Tab (Royal Blue Pill) */
        [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
            background-color: #EFF6FF !important;
            border: 1.5px solid #2563EB !important;
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.12) !important;
            transform: translateX(3px) !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] > label p {
            font-size: 0.92rem !important;
            font-weight: 600 !important;
            color: #475569 !important;
            margin: 0 !important;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p {
            color: #1D4ED8 !important;
            font-weight: 700 !important;
        }

        /* Sidebar Inputs & Sliders (Light Theme) */
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
            background-color: #F8FAFC !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
            color: #0F172A !important;
        }
        [data-testid="stSidebar"] .stSlider {
            padding-top: 6px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_ml_model():
    """Load the trained machine learning model and label encoder."""
    if not os.path.exists(MODEL_PATH):
        return None, None, None

    try:
        with open(MODEL_PATH, "rb") as f:
            artifacts = pickle.load(f)
        return artifacts.get("model"), artifacts.get("label_encoder"), artifacts.get("classes")
    except Exception as e:
        st.error(f"Error loading model artifact: {e}")
        return None, None, None


@st.cache_resource
def get_tts_engine():
    """Initialize Text-To-Speech engine singleton."""
    return TTSEngine(rate=145, volume=1.0)


def load_metadata() -> Dict[str, Any]:
    """Load evaluation metrics and training metadata."""
    if os.path.exists(METADATA_PATH):
        try:
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


# Initialize Session State
if "camera_running" not in st.session_state:
    st.session_state.camera_running = False
if "recognized_word" not in st.session_state:
    st.session_state.recognized_word = "No Hand Detected"
if "confidence" not in st.session_state:
    st.session_state.confidence = 0.0
if "sentence_words" not in st.session_state:
    st.session_state.sentence_words = []
if "auto_speak_last" not in st.session_state:
    st.session_state.auto_speak_last = ""
if "trigger_browser_speech" not in st.session_state:
    st.session_state.trigger_browser_speech = None
if "copy_status" not in st.session_state:
    st.session_state.copy_status = False

tts = get_tts_engine()
model, label_encoder, model_classes = load_ml_model()
metadata = load_metadata()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px; padding: 4px 0;">
            <div style="width: 44px; height: 44px; border-radius: 12px; background: #EFF6FF; border: 1.5px solid #BFDBFE; display: flex; align-items: center; justify-content: center; font-size: 24px; color: #2563EB; flex-shrink: 0;">
                🖐️
            </div>
            <div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #0F172A; letter-spacing: -0.5px;">
                    Signova <span style="color: #2563EB;">AI</span>
                </div>
                <div style="font-size: 0.78rem; color: #64748B; font-weight: 500;">ISL & ASL Word Recognition</div>
            </div>
        </div>
        <div style="height: 1px; background: #E2E8F0; margin-bottom: 16px;"></div>
        <div style="font-size: 0.72rem; font-weight: 700; color: #475569; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 8px;">Navigation</div>
        """,
        unsafe_allow_html=True,
    )

    mode = st.radio(
        "Navigation",
        [
            "📸 Live Word Recognition",
            "🖐️ Word Sign Catalog",
            "📥 Collect Word Samples",
            "⚙️ Train ML Model",
            "🎓 Project Viva Guide",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div style="height: 1px; background: #E2E8F0; margin: 20px 0 16px 0;"></div>
        <div style="font-size: 0.72rem; font-weight: 700; color: #475569; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 10px;">Camera & Settings</div>
        """,
        unsafe_allow_html=True,
    )

    cam_index = st.selectbox("Webcam Index", options=[0, 1, 2], index=0)
    confidence_threshold = (
        st.slider(
            "Confidence Threshold (%)",
            min_value=40,
            max_value=95,
            value=60,
            step=5,
            help="Gestures with lower probability than this threshold will be flagged as 'Sign Not Recognized'.",
        )
        / 100.0
    )

    enable_auto_speak = st.checkbox(
        "Auto-Speak confirmed word",
        value=False,
        help="Automatically speaks when a recognized sign is held steadily for several frames.",
    )

    if model is not None:
        acc = metadata.get("accuracy", 0.0) * 100
        words_count = len(model_classes) if model_classes else 0
        st.markdown(
            f"""
            <div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 12px; padding: 14px 16px; margin-top: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                    <span style="font-size: 0.8rem; font-weight: 700; color: #15803D;">🟢 System Online</span>
                    <span style="font-size: 0.74rem; background: #DCFCE7; color: #166534; padding: 2px 7px; border-radius: 6px; font-weight: 700;">{acc:.1f}% ACC</span>
                </div>
                <div style="font-size: 0.78rem; color: #475569; line-height: 1.5;">
                    Classifier: <b style="color: #0F172A;">Random Forest (100T)</b><br>
                    Active Signs: <b style="color: #0D9488;">{words_count} Words Ready</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("⚠️ No trained model found. Please run 'Train ML Model'.")


# ================= TAB 1: LIVE WORD RECOGNITION =================
if mode == "📸 Live Word Recognition":
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <span class="hero-badge">AI-powered computer vision</span>
            <div class="main-header">Signova AI</div>
            <div class="sub-header">Real-Time Sign Language Recognition & Speech Conversion</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Top Controls
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2.5, 2.5, 4.0])
    with col_ctrl1:
        start_btn = st.button("▶️ Start Webcam", use_container_width=True, type="primary")
    with col_ctrl2:
        stop_btn = st.button("⏹️ Stop Webcam", use_container_width=True, type="secondary")

    if start_btn:
        st.session_state.camera_running = True
    if stop_btn:
        st.session_state.camera_running = False

    # Layout: Left video stream, Right results & controls
    col_video, col_panel = st.columns([3, 2], gap="large")

    with col_panel:
        st.markdown(
            '<div style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin-bottom: 10px;">🎯 Recognized Sign Word</div>',
            unsafe_allow_html=True,
        )
        prediction_placeholder = st.empty()
        confidence_placeholder = st.empty()
        status_tag_placeholder = st.empty()

        st.markdown("<div style='height: 1px; background: #E2E8F0; margin: 18px 0;'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin-bottom: 10px;">🔊 Speech Output</div>',
            unsafe_allow_html=True,
        )

        speak_col1, speak_col2 = st.columns(2)
        with speak_col1:
            speak_word_btn = st.button("🗣️ Speak Word", use_container_width=True)
        with speak_col2:
            speak_sentence_btn = st.button("📢 Speak Sentence", use_container_width=True)

        if speak_word_btn:
            cur_word = st.session_state.recognized_word
            if cur_word not in ("No Hand Detected", "Sign Not Recognized", "Unknown", ""):
                tts.speak_async(cur_word)
                st.session_state.trigger_browser_speech = cur_word

        # Sentence Builder
        st.markdown("<div style='height: 1px; background: #E2E8F0; margin: 18px 0;'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin-bottom: 10px;">📝 Sentence Builder</div>',
            unsafe_allow_html=True,
        )

        sentence_str = " ".join(st.session_state.sentence_words)
        if sentence_str:
            st.markdown(
                f'<div class="sentence-box">💬 {sentence_str}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="sentence-box" style="color: #64748B;">(Sentence is empty. Click "➕ Add" to append words.)</div>',
                unsafe_allow_html=True,
            )

        # Sentence Builder Buttons: Add Word, Undo, Clear, Copy
        s_btn_col1, s_btn_col2, s_btn_col3, s_btn_col4 = st.columns(4)
        with s_btn_col1:
            if st.button("➕ Add", use_container_width=True, help="Add current recognized word to sentence"):
                cur = st.session_state.recognized_word
                if cur not in ("No Hand Detected", "Sign Not Recognized", "Unknown", ""):
                    st.session_state.sentence_words.append(cur)
                    st.rerun()
        with s_btn_col2:
            if st.button("↩️ Undo", use_container_width=True, help="Remove last word"):
                if st.session_state.sentence_words:
                    st.session_state.sentence_words.pop()
                    st.rerun()
        with s_btn_col3:
            if st.button("🗑️ Clear", use_container_width=True, help="Clear all words"):
                st.session_state.sentence_words = []
                st.rerun()
        with s_btn_col4:
            copy_btn = st.button("📋 Copy", use_container_width=True, help="Copy sentence text")
            if copy_btn and sentence_str:
                # Browser clipboard injection
                clean_copy = sentence_str.replace('"', '\\"')
                st.components.v1.html(
                    f"""
                    <script>
                        navigator.clipboard.writeText("{clean_copy}").then(function() {{
                            console.log("Sentence copied to clipboard");
                        }});
                    </script>
                    """,
                    height=0,
                    width=0,
                )
                st.toast("✅ Sentence copied to clipboard!", icon="📋")

        if speak_sentence_btn and st.session_state.sentence_words:
            full_text = " ".join(st.session_state.sentence_words)
            tts.speak_async(full_text)
            st.session_state.trigger_browser_speech = full_text

    # Render Browser Speech JS if triggered
    if st.session_state.trigger_browser_speech:
        st.components.v1.html(
            tts.get_browser_speech_html(st.session_state.trigger_browser_speech),
            height=0,
            width=0,
        )
        st.session_state.trigger_browser_speech = None

    with col_video:
        video_placeholder = st.empty()

        if not st.session_state.camera_running:
            video_placeholder.markdown(
                """
                <div class="camera-standby-box">
                    <div class="camera-standby-icon">📷</div>
                    <div class="camera-standby-title">Webcam Stream Offline</div>
                    <div class="camera-standby-subtitle">
                        Click <b>▶ Start Webcam</b> above to launch real-time hand landmark tracking and speech conversion.
                    </div>
                    <div style="margin-top: 12px;">
                        <span class="camera-pill-tag">MediaPipe 21 Landmarks</span>
                        <span class="camera-pill-tag" style="margin-left: 8px;">Random Forest ML</span>
                        <span class="camera-pill-tag" style="margin-left: 8px;">ISL & ASL Signs</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            prediction_placeholder.markdown(
                '<div class="prediction-badge-idle">⚡ Ready to Detect</div>',
                unsafe_allow_html=True,
            )
            confidence_placeholder.progress(0, text="Confidence: 0%")
            status_tag_placeholder.markdown(
                '<div style="color: #64748B; font-size: 0.9rem; margin-top: 6px;">Status: Standby • Click Start Webcam to begin</div>',
                unsafe_allow_html=True,
            )

        else:
            if model is None:
                video_placeholder.error(
                    "❌ No trained model found! Please go to **⚙️ Train ML Model** first."
                )
            else:
                # Active Webcam Inference Loop
                cap = cv2.VideoCapture(cam_index)
                if not cap.isOpened():
                    cap = cv2.VideoCapture(1)

                if not cap.isOpened():
                    video_placeholder.error(
                        f"❌ Failed to access camera (Index {cam_index}). "
                        "Check if another application is using the webcam."
                    )
                    st.session_state.camera_running = False
                else:
                    detector = HandDetector(
                        min_detection_confidence=0.7, min_tracking_confidence=0.5
                    )
                    prediction_window = deque(maxlen=6)
                    fps_time = time.time()
                    frame_count = 0
                    fps = 0.0

                    try:
                        while st.session_state.camera_running:
                            ret, frame = cap.read()
                            if not ret:
                                st.warning("Camera stream interrupted.")
                                break

                            frame = cv2.flip(frame, 1)
                            frame_count += 1
                            if time.time() - fps_time >= 1.0:
                                fps = frame_count / (time.time() - fps_time)
                                fps_time = time.time()
                                frame_count = 0

                            # Detect hands
                            annotated_frame, results = detector.find_hands(frame, draw=True)

                            current_label = "No Hand Detected"
                            conf_val = 0.0
                            is_unknown = False

                            if results.multi_hand_landmarks:
                                hand_lms = results.multi_hand_landmarks[0]
                                features = detector.extract_features(hand_lms)

                                # Model inference
                                feat_array = np.array([features], dtype=np.float32)
                                probs = model.predict_proba(feat_array)[0]
                                best_idx = int(np.argmax(probs))
                                conf_val = float(probs[best_idx])
                                raw_label = str(label_encoder.inverse_transform([best_idx])[0])

                                if conf_val >= confidence_threshold:
                                    prediction_window.append(raw_label)
                                else:
                                    prediction_window.append("Sign Not Recognized")

                                # Majority vote smoothing over recent frames
                                if prediction_window:
                                    current_label = max(
                                        set(prediction_window), key=prediction_window.count
                                    )

                                is_unknown = (current_label == "Sign Not Recognized")

                                # Draw bounding box & badge
                                bbox = detector.get_bounding_box(annotated_frame, hand_lms)
                                annotated_frame = Visualizer.draw_hand_box(
                                    annotated_frame,
                                    bbox,
                                    label=current_label,
                                    confidence=conf_val,
                                    is_unknown=is_unknown,
                                )
                            else:
                                prediction_window.clear()

                            # Draw HUD
                            annotated_frame = Visualizer.draw_hud(
                                annotated_frame,
                                gesture_name=current_label,
                                confidence=conf_val,
                                fps=fps,
                                is_unknown=is_unknown,
                            )

                            # Update State
                            st.session_state.recognized_word = current_label
                            st.session_state.confidence = conf_val

                            # Auto-speak trigger
                            if enable_auto_speak:
                                if (
                                    current_label not in ("No Hand Detected", "Sign Not Recognized")
                                    and current_label != st.session_state.auto_speak_last
                                    and conf_val >= 0.85
                                ):
                                    st.session_state.auto_speak_last = current_label
                                    tts.speak_async(current_label)

                            # Streamlit video display
                            frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                            video_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)

                            # Update side panel values
                            if is_unknown:
                                prediction_placeholder.markdown(
                                    '<div class="prediction-badge-warning">Sign Not Recognized</div>',
                                    unsafe_allow_html=True,
                                )
                                status_tag_placeholder.warning("⚠️ Adjust hand angle or distance")
                            elif current_label == "No Hand Detected":
                                prediction_placeholder.markdown(
                                    '<div class="prediction-badge-idle">No Hand Detected</div>',
                                    unsafe_allow_html=True,
                                )
                                status_tag_placeholder.info("Bring hand into camera frame")
                            else:
                                prediction_placeholder.markdown(
                                    f'<div class="prediction-badge-success">{current_label}</div>',
                                    unsafe_allow_html=True,
                                )
                                status_tag_placeholder.success("✅ Sign Confirmed")

                            confidence_placeholder.progress(
                                min(1.0, max(0.0, conf_val)),
                                text=f"Confidence Score: {int(conf_val * 100)}%",
                            )

                    finally:
                        cap.release()
                        detector.close()


# ================= TAB 2: WORD SIGN CATALOG =================
elif mode == "🖐️ Word Sign Catalog":
    st.markdown('<p class="main-header">Basic Word Sign Catalog (ISL & ASL)</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Supported basic word signs based on standard Indian Sign Language (ISL) & American Sign Language (ASL) learning guide.</p>',
        unsafe_allow_html=True,
    )

    guide_img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures", "sign_guide_isl_asl.jpg")
    if os.path.exists(guide_img_path):
        with st.expander("📖 View Official ISL vs ASL Reference Chart", expanded=True):
            st.image(guide_img_path, caption="ISL & ASL Basic Signs Learning Guide Reference", use_container_width=True)

    catalog = [
        {
            "word": "YES",
            "icon": "👍",
            "asl_handshape": "Thumbs-Up (ISL / ASL)",
            "desc": "Move your thumb upwards with four fingers curled into a solid fist.",
            "note": "Standard affirmative sign in Indian Sign Language (ISL) and basic communicative sign guides.",
        },
        {
            "word": "NO",
            "icon": "☝️",
            "asl_handshape": "Index Finger Upright",
            "desc": "Shake your index finger side to side; other fingers curled into palm.",
            "note": "Classic negative/refusal indicator across ISL and universal non-verbal communication.",
        },
        {
            "word": "STOP",
            "icon": "🛑",
            "asl_handshape": "Flat Palm Outward",
            "desc": "Open flat palm facing directly toward the camera with fingers held upright and thumb out.",
            "note": "Universal halt gesture recognized globally in vision-based interfaces.",
        },
        {
            "word": "HELP",
            "icon": "✊",
            "asl_handshape": "Closed Fist / Wrist Grip",
            "desc": "Solid closed fist held upright ('Grip your wrist and move it upwards' as shown in guide).",
            "note": "Represents the dominant fist in the dual-hand wrist-lift assistance sign.",
        },
        {
            "word": "PLEASE",
            "icon": "🙏",
            "asl_handshape": "Joined Palms / Namaste",
            "desc": "Join your palms together and press lightly, or hold a flat vertical hand with thumb tucked.",
            "note": "Polite request gesture deeply rooted in Indian culture (Namaste) and ISL.",
        },
        {
            "word": "THANK YOU",
            "icon": "🤚",
            "asl_handshape": "Flat Hand Forward",
            "desc": "Touch your chest/chin and move your flat hand forward towards the person.",
            "note": "Gratitude sign across Indian Sign Language and American Sign Language.",
        },
        {
            "word": "HELLO",
            "icon": "🖐️",
            "asl_handshape": "Open 5-Hand Wave",
            "desc": "Wave your hand side to side with open palm and all 5 fingers spread naturally.",
            "note": "Universal conversational greeting sign across ISL and ASL.",
        },
        {
            "word": "LOVE",
            "icon": "🤟",
            "asl_handshape": "ILY Sign (Thumb+Index+Pinky)",
            "desc": "Thumb, index finger, and pinky finger fully extended upright; middle and ring curled down.",
            "note": "Globally recognized iconic 'I Love You' sign in ASL.",
        },
        {
            "word": "PEACE",
            "icon": "✌️",
            "asl_handshape": "V-Sign (Index + Middle)",
            "desc": "Index and middle fingers extended upward forming a 'V'; ring and pinky folded with thumb.",
            "note": "Universal peace and victory emblem.",
        },
    ]

    cols = st.columns(3)
    for i, item in enumerate(catalog):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="metric-card" style="margin-bottom: 20px; text-align: left; min-height: 230px; background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px 20px; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);">
                    <div style="font-size: 1.8rem; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
                        <span>{item['icon']}</span>
                        <span style="font-weight: 800; font-size: 1.3rem; color: #0F172A; letter-spacing: -0.3px;">{item['word']}</span>
                    </div>
                    <div style="display: inline-block; font-size: 0.78rem; background: #EFF6FF; color: #2563EB; font-weight: 700; padding: 3px 9px; border-radius: 6px; margin-bottom: 10px; border: 1px solid #DBEAFE;">
                        {item['asl_handshape']}
                    </div>
                    <div style="font-size: 0.88rem; color: #334155; line-height: 1.45; margin-bottom: 10px;">{item['desc']}</div>
                    <div style="font-size: 0.78rem; color: #64748B; font-style: italic; border-top: 1px solid #F1F5F9; padding-top: 8px;">ℹ️ {item['note']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.info("💡 **Important Prototype Note**: Sign languages naturally incorporate motion trajectories, two-handed coordination, and facial expressions. Signova AI tracks the distinct canonical static handshapes of these basic words for high-reliability webcam recognition.")


# ================= TAB 3: COLLECT WORD SAMPLES =================
elif mode == "📥 Collect Word Samples":
    st.markdown('<p class="main-header">Collect & Label Sign Language Words</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Expand and personalize the dataset by recording real webcam samples for specific words.</p>',
        unsafe_allow_html=True,
    )

    col_input1, col_input2, col_input3 = st.columns([3, 2, 2])
    with col_input1:
        selected_word_preset = st.selectbox(
            "Select Word to Collect",
            options=BASIC_WORDS + ["(Custom Word)"],
            index=0,
        )
        if selected_word_preset == "(Custom Word)":
            custom_word_name = st.text_input("Enter Custom Word Name", placeholder="e.g. SORRY, WATER, GOOD").strip().upper()
        else:
            custom_word_name = selected_word_preset

    with col_input2:
        samples_to_record = st.number_input("Number of Frames", min_value=20, max_value=200, value=60, step=10)

    with col_input3:
        st.write("")
        st.write("")
        record_cli_btn = st.button("🚀 Launch Collector Tool", type="primary", use_container_width=True)

    # Context guidance card
    if custom_word_name in BASIC_WORDS:
        from collect_data import ASL_POSTURE_TIPS
        tip = ASL_POSTURE_TIPS.get(custom_word_name, "")
        st.markdown(
            f"""
            <div style="background: #F0FDFA; border: 1px solid #99F6E4; border-radius: 10px; padding: 12px 18px; margin: 14px 0;">
                <span style="color: #0D9488; font-weight: 700;">💡 Posture Guidance for {custom_word_name}:</span>
                <span style="color: #334155; margin-left: 8px;">{tip}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if record_cli_btn:
        if not custom_word_name:
            st.error("Please enter or select a valid word name before starting collection.")
        else:
            st.info(
                f"Opening collection tool for **'{custom_word_name}'** ({samples_to_record} frames).\n\n"
                "A camera window will appear. Hold your hand in proper posture, press **'S'** to start recording (3-second countdown), and rotate slightly for angle diversity!"
            )
            # Run collect_data script
            import subprocess
            cmd = [
                sys.executable,
                os.path.join(ROOT_DIR, "collect_data.py"),
                "--gesture",
                custom_word_name,
                "--samples",
                str(samples_to_record),
                "--cam",
                str(cam_index),
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                st.success(f"Successfully recorded samples for '{custom_word_name}'!")
                st.code(res.stdout)
            else:
                st.error("Collection failed or was closed by user.")
                st.code(res.stderr)

    st.markdown("---")
    st.subheader("📊 Dataset Distribution (data/gestures.csv)")
    if os.path.exists(DATA_FILE):
        df_data = pd.read_csv(DATA_FILE)
        st.write(f"Total labeled samples in dataset: **{len(df_data)}**")
        counts_df = df_data["label"].value_counts().reset_index()
        counts_df.columns = ["Sign Word", "Sample Count"]
        st.dataframe(counts_df, use_container_width=True)
    else:
        st.warning("No dataset file found yet. Generate or record samples.")


# ================= TAB 4: TRAIN ML MODEL =================
elif mode == "⚙️ Train ML Model":
    st.markdown('<p class="main-header">Model Training & Performance Metrics</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Train the Random Forest classifier on landmark features with stratified cross-validation.</p>',
        unsafe_allow_html=True,
    )

    col_btn1, col_btn2 = st.columns([2, 4])
    with col_btn1:
        if st.button("⚡ Retrain Model Now", type="primary", use_container_width=True):
            with st.spinner("Training Random Forest Classifier on word dataset..."):
                try:
                    from train_model import train_gesture_classifier
                    clf, le, meta = train_gesture_classifier()
                    st.success(f"🎉 Model successfully trained with **{meta['accuracy']*100:.2f}%** accuracy!")
                    st.cache_resource.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Training failed: {e}")

    st.markdown("---")
    if metadata:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Test Accuracy", f"{metadata.get('accuracy', 0.0) * 100:.1f}%")
        with col_m2:
            st.metric("Total Samples", metadata.get("total_samples", 0))
        with col_m3:
            st.metric("Training Samples", metadata.get("train_samples", 0))
        with col_m4:
            st.metric("Validation Samples", metadata.get("test_samples", 0))

        st.subheader("📈 Detailed Classification Report per Word")
        rep = metadata.get("classification_report", {})
        if rep:
            rows = []
            for cls_name, vals in rep.items():
                if isinstance(vals, dict):
                    rows.append({
                        "Word Sign": cls_name,
                        "Precision": f"{vals.get('precision', 0):.2f}",
                        "Recall": f"{vals.get('recall', 0):.2f}",
                        "F1-Score": f"{vals.get('f1-score', 0):.2f}",
                        "Support": int(vals.get('support', 0)),
                    })
            st.dataframe(pd.DataFrame(rows), use_container_width=True)

        st.subheader("🎯 Confusion Matrix")
        cm = metadata.get("confusion_matrix", [])
        if cm and "classes" in metadata:
            cm_df = pd.DataFrame(cm, index=metadata["classes"], columns=metadata["classes"])
            st.dataframe(cm_df, use_container_width=True)
    else:
        st.info("No training metadata available. Click 'Retrain Model Now' above to build model artifacts.")


# ================= TAB 5: PROJECT VIVA GUIDE =================
elif mode == "🎓 Project Viva Guide":
    st.markdown('<p class="main-header">Academic Viva & Project Defense Guide</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Technical concepts, architectural justification, and anticipated questions for 3rd-year CSE viva.</p>',
        unsafe_allow_html=True,
    )

    with st.expander("📌 1. Word Recognition vs. Alphabet Fingerspelling", expanded=True):
        st.markdown(
            """
            - **Alphabet (Fingerspelling)**: Requires spelling words letter by letter (A-B-O-U-T), which is tedious and rarely used in fluent deaf communication except for proper nouns.
            - **Word Recognition (Signova AI)**: Recognizes full semantic communication units (e.g. **YES, NO, STOP, HELP, PLEASE, THANK YOU**), enabling real-time conversation and rapid sentence formation.
            """
        )

    with st.expander("🔬 2. MediaPipe Hand Landmark Architecture & Normalization"):
        st.markdown(
            r"""
            - **Landmark Topology**: MediaPipe extracts 21 3D joint coordinates using BlazePalm and 2.5D regression.
            - **Two-Stage Invariant Normalization**:
              1. **Origin Translation**: Subtract wrist coordinates $(x_0, y_0)$ from all points: $x'_i = x_i - x_0$. Wrist becomes $(0, 0)$.
              2. **Scale Invariance**: Divide by maximum Euclidean distance: $d_{max} = \max_i \sqrt{(x'_i)^2 + (y'_i)^2}$.
              - This transforms 21 coordinates into a **42-dimensional feature vector** completely invariant to camera distance and screen positioning.
            """
        )

    with st.expander("🧠 3. Machine Learning Classification & Uncertainty Handling"):
        st.markdown(
            r"""
            - **Classifier**: Scikit-Learn `RandomForestClassifier` with 100 decision trees and balanced class weights.
            - **Why Random Forest over CNN?**
              - Raw image CNNs overfit to skin color, clothing, and background walls.
              - Landmark feature vectors abstract away background pixels, enabling instantaneous training (< 1s) and high-speed CPU inference (< 1ms).
            - **Uncertainty Checking**: Uses `predict_proba()` to evaluate maximum class likelihood. If $\max P(y|X) < \tau$ (default 70%), the system outputs **"Sign Not Recognized"**, eliminating false positive detections.
            """
        )

    with st.expander("❓ 4. Frequently Asked Viva Voce Questions"):
        st.markdown(
            """
            1. **Q: How does Signova AI map gestures like Thumbs-Up, Pointing, and Fist according to sign language standards?**
               - *A*: Based on official Indian Sign Language (ISL) and American Sign Language (ASL) basic learning guides: **Thumbs-Up** (thumb upward) maps to **YES**; single pointing **Index Finger** maps to **NO**; solid **Closed Fist** (representing the upward wrist-grip gesture) maps to **HELP**; open **5-Finger Hand** maps to **HELLO**; **Flat Hand Forward** maps to **THANK YOU**; and **Joined Palms / Namaste** maps to **PLEASE**.
            2. **Q: What are the limitations of the current prototype?**
               - *A*: Full natural sign language includes continuous dynamic motion trajectories (e.g., circular rubbing for PLEASE, chin-to-outward for THANK YOU) and two-handed interaction. Signova tracks the canonical handshape postures as a robust single-hand static prototype, with dual-hand LSTM sequence modeling planned for future scope.
            3. **Q: How does the Sentence Builder facilitate communication?**
               - *A*: Individual recognized words can be appended into a full sentence with Add Word, Undo, Clear, Copy, and Text-to-Speech capabilities, allowing speech-impaired individuals to express complete thoughts.
            """
        )
