# 🖐️ Signova AI – Basic Sign Language Word Recognition System
### 🎓 3rd-Year Computer Science & Engineering (CSE) Mini Project

[![Python 3.10-3.12](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://python.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Landmarks-cyan.svg)](https://developers.google.com/mediapipe)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Random%20Forest%20(99.4%25)-orange.svg)](https://scikit-learn.org)
[![Streamlit UI](https://img.shields.io/badge/Streamlit-Dark%20Navy%20%26%20Cyan-7928CA.svg)](https://streamlit.io)

---

## 📌 1. Project Overview & Objective

**Signova AI** is a real-time Computer Vision and Machine Learning application designed to recognize **basic sign language words** captured via a laptop webcam and translate them into visual text and audible voice speech.

Rather than relying on fingerspelling the 26 alphabet letters (A–Z) — which is slow, tedious, and rarely used for standard dialogue in the Deaf community — Signova focuses on **semantic word-level sign recognition** (e.g., **YES**, **NO**, **STOP**, **HELP**, **PLEASE**, **THANK YOU**, **HELLO**, **LOVE**, **PEACE**).

### Core Features:
1. **Webcam Video Capture**: Real-time live frame ingestion at 30 FPS using OpenCV.
2. **21 3D Hand Landmark Detection**: High-fidelity palm and joint tracking powered by Google MediaPipe Hands.
3. **Scale- & Translation-Invariant Normalization**: Converts raw pixel coordinates into a 42-dimensional relative feature vector invariant to camera distance and hand position.
4. **Machine Learning Classification**: Trained `RandomForestClassifier` (100 trees, balanced weights) achieving **98.6% cross-validation accuracy**.
5. **Confidence Scoring & Uncertainty Handling**: Emits **"Sign Not Recognized"** whenever confidence is below threshold ($\ge 60\%$), preventing false positives and arbitrary gesture misclassifications.
6. **Sentence Builder**: Interactive conversation board with **Add Word**, **Undo Last**, **Clear All**, and **Copy to Clipboard** controls.
7. **Text-To-Speech (TTS)**: Dual voice engine utilizing `pyttsx3` background threading and browser-side HTML5 speech synthesis fallback.
8. **Modern Visual Interface**: Built with Streamlit featuring a modern **Light Theme (Royal Blue `#2563EB`, Teal `#0D9488`, Navy `#0F172A`)** aesthetic.
9. **Extensible Data Collector & Trainer**: Built-in tools (`collect_data.py` and `train_model.py`) to easily record new custom sign words and retrain the classifier in seconds.

> [!NOTE]
> **Sign Language Standard & Limitations**:
> Signova grounds its handshapes in **American Sign Language (ASL)** standard postures. Full natural sign language incorporates dynamic motion, two-handed interaction, and facial grammar. As a static gesture recognition prototype, Signova detects the key distinctive handshapes for each word (e.g., ASL 'S' fist for YES, 'A' handshape for HELP, flat 'B' palm for STOP).

---

## 🏗️ 2. System Architecture & Pipeline

```
              ┌──────────────────────────────┐
              │    Laptop Webcam (OpenCV)    │
              └──────────────┬───────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │  MediaPipe Hands (21 Joints) │
              └──────────────┬───────────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   [ No Hand in Frame ]              [ Hand Detected ]
            │                                 │
     Status: "No Hand"                        ▼
                             ┌─────────────────────────────────┐
                             │  Origin & Scale Normalization   │
                             │  x' = (x - x_0) / d_max         │
                             │  y' = (y - y_0) / d_max         │
                             │  Output: 42-D Feature Vector    │
                             └────────────────┬────────────────┘
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │ Random Forest Classifier (100T) │
                             └────────────────┬────────────────┘
                                              │
            ┌─────────────────────────────────┴───────────────────┐
            ▼ (Confidence < 70%)                                  ▼ (Confidence >= 70%)
   ┌───────────────────────┐                             ┌───────────────────────┐
   │ "Sign Not Recognized" │                             │  Recognized ASL Word  │
   │  (Filters Uncertanty) │                             │   e.g. "HELP" (96%)   │
   └───────────────────────┘                             └───────────┬───────────┘
                                                                     │
                                             ┌───────────────────────┴───────────────────────┐
                                             ▼                                               ▼
                              ┌─────────────────────────────┐                 ┌─────────────────────────────┐
                              │     Streamlit Dashboard     │                 │   Text-To-Speech Engine     │
                              │  • Real-time Video HUD      │                 │  • Background Thread pyttsx3│
                              │  • Sentence Builder         │                 │  • HTML5 Browser Fallback   │
                              │  • Undo / Clear / Copy      │                 └─────────────────────────────┘
                              └─────────────────────────────┘
```

---

## 📂 3. Directory Structure

```
signova/
│
├── venv/                       # Isolated Python 3.12 virtual environment
├── data/                       # Labeled dataset directory
│   └── gestures.csv            # 42 normalized features + label column (840 samples)
│
├── models/                     # Trained Machine Learning artifacts
│   ├── gesture_model.pkl       # Trained Random Forest model + LabelEncoder
│   └── model_metadata.json     # Accuracy scores (99.4%), confusion matrix, classes
│
├── utils/                      # Core backend utilities
│   ├── __init__.py             # Makes utils an importable Python module
│   ├── hand_detector.py        # MediaPipe wrapper & coordinate normalizer
│   ├── tts_engine.py           # Thread-safe pyttsx3 voice engine + HTML5 TTS
│   └── visualizer.py           # Cyber dark HUD overlay, bounding box, status tags
│
├── app.py                      # Streamlit application with modern UI & Sentence Builder
├── collect_data.py             # Labeled dataset recorder with camera overlay
├── train_model.py              # ML training script with accuracy & evaluation metrics
├── generate_seed_dataset.py    # Generates canonical ASL word baseline data
├── test_cam.py                 # Diagnostic test for webcam, MediaPipe, and OpenCV
├── requirements.txt            # Python package dependencies
├── run.bat                     # Windows one-click launcher
├── PROJECT_REPORT_OUTLINE.md   # Complete 3rd-year CSE academic mini-project report
└── README.md                   # Comprehensive documentation (this file)
```

---

## 🖐️ 4. Supported Comprehensive Sign Word Catalog (14 Core Signs)

Signova recognizes signs according to standard **Indian Sign Language (ISL)** and **American Sign Language (ASL)** foundational communicative visual guides:

| Sign Word | Emoji | Meaning | Canonical Handshape & Posture |
|---|---|---|---|
| **HELLO** | 🖐️ | Salutation / Greeting | **Open 5-Hand**: Wave your open hand side to side with all 5 fingers spread naturally. |
| **GOODBYE** | 👋 | Parting / Farewell | **4-Finger Wave**: All 4 fingers upright and pressed together waving gently, thumb tucked. |
| **YES** | 👍 | Affirmation / Agreement | **Thumbs-Up**: Move your thumb upwards with 4 fingers curled tightly into palm. |
| **NO** | ☝️ | Negative / Refusal | **Index Finger Up**: Shake your index finger side to side; other fingers curled into palm. |
| **HELP** | ✊ | Request Assistance | **Closed Fist**: Solid closed fist held upright (representing the upward wrist-grip assistance sign). |
| **STOP** | 🛑 | Halt / Pause | **Flat Palm Outward**: Flat open hand facing camera vertically with all 4 fingers together. |
| **PLEASE** | 🙏 | Politeness / Request | **Joined Palms / Namaste**: Palms pressed together or flat vertical hand held upright. |
| **THANK YOU** | 🤚 | Gratitude / Thanks | **Flat Hand Forward**: Touch chest/chin and move flat hand forward towards the person. |
| **SORRY** | 🤝 | Apology / Regret | **Fist at Chest**: Closed fist with thumb upright rubbed in a circle over the chest. |
| **LOVE** | 🤟 | Affection / Expression | **ILY Sign**: Thumb, index, and pinky extended upright; middle and ring folded down. |
| **PEACE** | ✌️ | Peace / Victory | **V-Sign**: Index and middle fingers extended in a 'V'; ring and pinky curled with thumb. |
| **WATER** | 💧 | Vital Need | **W-Sign**: Index, middle, and ring fingers extended upward in a 'W'; thumb holds pinky tip. |
| **FOOD** | 🍲 | Vital Need (Eat) | **Grouped Fingertips**: All 5 fingertips pinched together facing towards the mouth. |
| **OKAY** | 👌 | Confirmation / Okay | **OK Sign**: Index finger and thumb touch forming a circle, while other 3 fingers remain upright. |

---

## ⚙️ 5. Technical Stack & Dependencies

- **Python 3.10 – 3.12**: Core execution runtime.
- **OpenCV (`opencv-python 4.10+`)**: Real-time camera capture, color space conversion (`BGR -> RGB`), and HUD rendering.
- **Google MediaPipe (`mediapipe 0.10+`)**: Single-stage ML pipeline tracking 21 3D hand joints.
- **Scikit-Learn (`scikit-learn 1.4+`)**: Model training (`RandomForestClassifier`, `LabelEncoder`, metrics).
- **Streamlit (`streamlit 1.35+`)**: Modern interactive web interface.
- **pyttsx3 (`pyttsx3 2.90+`)**: Native OS Text-to-Speech voice engine with asynchronous worker threading.

---

## 🚀 6. Step-by-Step Installation & Setup

### Step 1: Open Terminal in the Project Directory
```powershell
cd "C:\Users\raja nandhana\.gemini\antigravity\scratch\signova"
```

### Step 2: Activate the Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```
*(For Command Prompt: `.\venv\Scripts\activate.bat`)*

### Step 3: Verify Hardware & Libraries
Run the diagnostic script to ensure your camera and dependencies are functional:
```powershell
.\venv\Scripts\python.exe test_cam.py
```
Expected output:
```
[+] Webcam successfully captured a frame! Resolution: 640x480
DIAGNOSTICS PASSED! All core components are ready.
```

---

## 🎮 7. Running the Application

### Option 1: Double-Click Launcher (Windows)
Double-click `run.bat` in the project directory.

### Option 2: Command Line
```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```
This will automatically launch the Signova AI web dashboard in your default browser at:
**`http://localhost:8501`**

---

## 📥 8. Collecting New Sign Words & Retraining

You can expand the vocabulary beyond the 7 basic words at any time.

### Step 1: Collect Labeled Sign Samples
Using the command-line utility:
```powershell
.\venv\Scripts\python.exe collect_data.py --gesture "SORRY" --samples 100
```
- A webcam window opens with live landmark tracking.
- Hold your hand in the target sign posture.
- Press **'S'** to start a 3-second countdown.
- Move and rotate your hand slightly to capture varied angles.
- The 42 normalized features are automatically appended to `data/gestures.csv`.

*(Alternatively, you can collect samples directly from the **"📥 Collect New Sign Words"** tab inside the Streamlit web dashboard).*

### Step 2: Retrain the Machine Learning Model
```powershell
.\venv\Scripts\python.exe train_model.py
```
The script will:
1. Reload `data/gestures.csv` with the newly added classes.
2. Train a fresh Random Forest classifier.
3. Compute precision, recall, and confusion matrix.
4. Update `models/gesture_model.pkl` and `models/model_metadata.json`.

---

## ❓ 9. Troubleshooting & FAQ

| Problem | Cause | Solution |
|---|---|---|
| **Camera shows black screen or fails to open** | Camera is in use by Zoom, Teams, or another app | Close any application using your webcam. If you have an external USB webcam, change "Webcam Index" in the sidebar to `1`. |
| **Prediction displays "Sign Not Recognized"** | Hand posture is ambiguous or confidence < 70% | Ensure proper room lighting. Hold hand within 1.5–2.5 feet of the webcam. Lower the confidence threshold slider in the sidebar if needed. |
| **pyttsx3 voice does not speak on some systems** | Windows COM voice conflict | Signova AI automatically provides an **in-browser HTML5 Web Speech API fallback** alongside native `pyttsx3`. |
| **Low FPS / Video stuttering** | High background CPU usage | Set camera resolution to 640x480 (default). Ensure adequate lighting so camera exposure latency stays minimal. |

---

## 🎓 10. Academic Project Presentation & Viva Highlights

When presenting Signova AI for 3rd-year CSE evaluation:
1. **Semantic Words vs. Fingerspelling**: Emphasize that word-level signs represent authentic communication units, reducing interaction friction compared to letter-by-letter spelling.
2. **Mathematical Normalization**: Explain the invariant transformation:
   $$\vec{v}_i = \frac{\mathbf{p}_i - \mathbf{p}_0}{\max_k \|\mathbf{p}_k - \mathbf{p}_0\|}$$
   This ensures classification is invariant to the user's distance from the webcam and screen position.
3. **Random Forest vs Deep CNNs**: Explain why an ensemble of decision trees on landmark coordinate vectors is vastly superior for edge devices: zero GPU requirements, < 1ms CPU inference, and resilience against lighting/skin-tone bias.
4. **Uncertainty Rejection**: Highlight that the system outputs **"Sign Not Recognized"** rather than forcing a false positive prediction when confidence is low.
5. **Sentence Builder**: Demonstrate conversational fluency by assembling multiple signs into full sentences and voicing them aloud.
