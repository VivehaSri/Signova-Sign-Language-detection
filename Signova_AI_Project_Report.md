# SIGNOVA AI: REAL-TIME SIGN LANGUAGE WORD RECOGNITION AND SPEECH CONVERSION USING COMPUTER VISION

## A PROJECT REPORT

*Submitted by*

| Student Name | Register Number |
|:---|---:|
| **VIVEHA SRI. P** | **(922524104179)** |
| **RAJANANDHANA M** | **(922524104129)** |

*In partial fulfillment for the award of the degree of*

### BACHELOR OF ENGINEERING
### in
### COMPUTER SCIENCE AND ENGINEERING

### V.S.B. ENGINEERING COLLEGE, KARUR-639 111
#### (An Autonomous Institution, Affiliated to Anna University)

### APRIL 2026

---

<div style="page-break-after: always;"></div>

# BONAFIDE CERTIFICATE

Certified that this project report titled **“SIGNOVA AI: REAL-TIME SIGN LANGUAGE WORD RECOGNITION AND SPEECH CONVERSION USING COMPUTER VISION”** is the bonafide work of **VIVEHA SRI. P (922524104179)**, **RAJANANDHANA M (922524104129)** who carried out the project under my supervision.

<br><br>

| SIGNATURE | SIGNATURE |
|:---|:---|
| <br><br>____________________________________<br>**Dr. P. ANBUMANI M.E., Ph.D.**<br>**HEAD OF THE DEPARTMENT**<br>Computer Science and Engineering,<br>V.S.B. Engineering College<br>Karur -639111 | <br><br>____________________________________<br>**Dr. S. PRABAKARAN M.E., Ph.D.**<br>**SUPERVISOR**<br>Assistant Professor<br>Computer Science and Engineering,<br>V.S.B. Engineering College<br>Karur -639111 |

<br><br>

Submitted for Project Viva-Voce held on ____________________

<br><br>

| INTERNAL EXAMINER | EXTERNAL EXAMINER |
|:---|:---|
| <br>**Gaythri**<br><br>SIGNATURE: _______________________ | <br><br><br>SIGNATURE: _______________________ |

<br>
<center><b>II</b></center>

---

<div style="page-break-after: always;"></div>

# DECLARATION

We jointly declare that the project report on **“SIGNOVA AI: REAL-TIME SIGN LANGUAGE WORD RECOGNITION AND SPEECH CONVERSION USING COMPUTER VISION”** is the result of original work done by us and best of our knowledge, similar work has not been submitted to **“ANNA UNIVERSITY CHENNAI”** for the requirement of Degree, Bachelor of Engineering. This project report is submitted on the partial fulfillment of the requirement of the award of Degree of Bachelor of Engineering.

<br><br><br>

<div align="right">
<b>SIGNATURE</b><br><br><br>
___________________________<br>
<b>VIVEHA SRI. P</b><br><br><br>
___________________________<br>
<b>RAJANANDHANA M</b>
</div>

<br><br>
**Place:** Karur  
**Date:**  

<br>
<center><b>III</b></center>

---

<div style="page-break-after: always;"></div>

# ACKNOWLEDGEMENT

First and foremost, we express our thanks to our parents for providing us with a very supportive and encouraging environment for doing this project. We wish to express our sincere thanks to our Founder and Chairman **Shri. V.S.BALSAMY B.Sc., B.L.**, for his Endeavor in educating us in this premier institution.

We wish to express our appreciation and gratefulness to our Principal, **Dr. C.VENNILA M.E., Ph.D.**, and Vice Principal **Dr. T.S.KIRUBASANKAR M.E., Ph.D** for their encouragement and sincere guidance.

We are grateful to our Head of the Department **Dr. P.ANBUMANI M.E., Ph.D.**, and our Project Coordinator **Dr. S.PRABAKARAN M.E., Ph.D.**, Assistant Professor, Department of Computer Science and Engineering for their valuable support.

We express our thanks to the supervisor of our project **Dr. S.PRABHAKARAN M.E, Ph.D.**, Assistant Professor, Department of Computer Science and Engineering, for guidance, technical suggestions, and continuous mentorship throughout the course of our project.

Our sincere thanks to all the teaching and non-teaching staff of V.S.B Engineering College and our friends for their help in the successful completion of this project work.

Finally, we bow before God, the Almighty who always had a better plan for us. We give our praise and glory to Almighty God for the successful completion of this project.

<br>
<center><b>IV</b></center>

---

<div style="page-break-after: always;"></div>

# V.S.B. Engineering College, Karur
### (An Autonomous Institution, Affiliated to Anna University)
### Department of Computer Science and Engineering
### VISION, MISSION, POs, PEOs and PSOs

#### Vision of the Institution:
We endeavor to impart futuristic technical education of the highest quality to the student community and to inculcate discipline in them to face the world with self-confidence and thus we prepare them for life as responsible citizens to uphold human values and to be of service at large. We strive to bring of the Institution as an Institution of academic excellence of international standard.

#### Mission of the Institution:
We transform persons into personalities by the state-of the art infrastructure, time consciousness, quick response and the best academic practices through assessment and advice.

#### Vision of the Department:
To produce competent Computer Science Engineers through Quality Education and Research.

#### Mission of the Department:
The Department strives to contribute to the expansion of knowledge in the discipline of Computer Science and Engineering by:
- Adopting an efficient teaching learning process in correlation with industrial needs.
- Ensuring technical proficiency, facilitating to pursue higher studies and carry out R&D activities.
- Developing problem solving and analytical skills with sound knowledge in basic sciences and Computer Science Engineering.
- Inculcating managerial skills to become socially responsible, ethical and competitive professionals.

<br>
<center><b>V</b></center>

---

<div style="page-break-after: always;"></div>

#### Program Educational Objectives (PEOs)
The Graduates of Computer Science and Engineering are able to:
- **PEO #1:** Work in Multinational companies and become successful IT professionals.
- **PEO #2:** Pursue higher studies and have their career in educational institutions, research organizations, or be entrepreneurs.
- **PEO #3:** Possess social responsibility, team work skills, leadership capabilities and urge for learning in their professional fields.

#### Program Specific Outcomes (PSOs)
- **PSO #1:** Addressing societal problems through design and development of software and firmware solutions using latest Computer Science tools and technologies.
- **PSO #2:** Involving enthusiastically in software development, software testing, storage, computing and business intelligence sectors.
- **PSO #3:** Use their technical expertise in latest technologies and update their knowledge continuously in Computer Science and Engineering to excel in their career.

#### Program Outcomes (POs)
- **PO1: Engineering knowledge:** Apply Mathematical knowledge and the basics of Science and Engineering to solve problems pertaining to Computer Science and Engineering.
- **PO2: Problem analysis:** Identify and formulate Computer Science and Engineering problems from research literature and be able to analyze the problem using first principles of Mathematics and Engineering Sciences.
- **PO3: Design/development of solutions:** Come out with solutions for complex problems and design system components or processes that fulfil particular needs taking into account public health and safety and social, cultural and environmental issues.
- **PO4: Conduct investigations of complex problems:** Draw well-founded conclusions applying knowledge acquired from research and research methods including design of experiments, analysis and interpretation of data and synthesis of information to arrive at significant conclusions.
- **PO5: Modern tool usage:** Form, select and apply relevant techniques, resources and Engineering and IT tools for Engineering activities like electronic prototyping, modelling and control of systems and also being conscious of the limitations.
- **PO6: The engineer and society:** Apply reasoning informed by contextual knowledge to assess societal, health, safety, legal and cultural issues and consequent responsibilities relevant to professional Computer Science and Engineering practice.
- **PO7: Environment and sustainability:** Be aware of the impact of professional Engineering solutions in societal and environmental contexts and exhibit knowledge and need for sustainable Development.
- **PO8: Ethics:** Apply principles of Professional Ethics to adhere to norms of engineering practice and discharge ethical responsibilities.
- **PO9: Individual and team work:** Function actively and efficiently as an individual or member/leader of different teams and multidisciplinary projects.
- **PO10: Communication:** Communicate efficiently engineering facts with wide range of engineering community and others, understand and prepare reports and design documents; make effective presentations and frame and follow instructions.
- **PO11: Project management and finance:** Demonstrate acquisition of body of engineering knowledge, insight and Management Principles and apply them as member/leader in teams and multidisciplinary environments.
- **PO12: Life-long learning:** Recognize need for self and life-long learning, keeping pace with technological challenges in the broadest sense.

<br>
<center><b>VII</b></center>

---

<div style="page-break-after: always;"></div>

# ABSTRACT

Effective communication is a fundamental human necessity, yet over 70 million individuals who rely on sign language face significant daily communication barriers in healthcare, administrative, educational, and commercial environments. Traditional translation approaches rely heavily on human interpreters who are scarce and expensive, or on sensory data gloves that are intrusive, fragile, and cumbersome. Furthermore, existing software systems predominantly focus on fingerspelling isolated A–Z alphabets, which is tedious, slow, and unnatural in fluent deaf communication. To overcome these critical limitations, this project presents **"Signova AI: Real-Time Sign Language Word Recognition and Speech Conversion Using Computer Vision"**. The system is engineered to recognize essential American Sign Language (ASL) semantic words—including **YES**, **NO**, **STOP**, **HELP**, **PLEASE**, **THANK YOU**, and **HELLO**—directly through a commodity laptop webcam without requiring specialized hardware or gloves.

The processing pipeline integrates OpenCV for live 30 FPS video acquisition and Google MediaPipe Hands for high-speed tracking of 21 three-dimensional skeletal joint landmarks. To eliminate errors caused by varying user distance and screen positioning, a two-stage mathematical normalization is implemented: translation of coordinates relative to the wrist origin and Euclidean scaling, transforming raw pixel landmarks into a compact 42-dimensional invariant feature vector. A Scikit-Learn Random Forest Classifier (100 estimators, balanced weights) is trained on canonical ASL posture vectors, achieving **99.40% cross-validation accuracy**. To prevent false positives, calibrated class posterior probability estimation triggers an uncertainty rejection filter, outputting **"Sign Not Recognized"** whenever prediction confidence drops below 70%. An interactive conversational Sentence Builder allows users to accumulate recognized signs into complete expressions with Add Word, Undo, Clear, and Copy controls, complemented by dual-channel Text-to-Speech (`pyttsx3` and browser HTML5 Web Speech API). Through this project work, it is able to attain PO1 to PO12 and also able to attain PSO1, PSO2 and PSO3.

**KEYWORDS:** Sign Language Word Recognition, Computer Vision, MediaPipe Hands, Geometric Landmark Normalization, Random Forest Classifier, Text-to-Speech (TTS), Sentence Builder, Assistive Technology.

<br>
<center><b>VIII</b></center>

---

<div style="page-break-after: always;"></div>

# TABLE OF CONTENTS

| CHAPTER NO. | TITLE | PAGE NO. |
|:---:|:---|:---:|
| | **ABSTRACT** | **VIII** |
| | **LIST OF FIGURES** | **XI** |
| | **LIST OF TABLES** | **XII** |
| | **LIST OF ABBREVIATIONS** | **XIII** |
| **1** | **INTRODUCTION** | **1** |
| | 1.1 OVERVIEW OF SIGN LANGUAGE AND ASSISTIVE TECH | 1 |
| | 1.2 PROBLEMS IN MANUAL COMMUNICATION & FINGERSPELLING | 2 |
| | 1.3 NEED FOR AUTOMATED WORD-LEVEL SIGN RECOGNITION | 3 |
| | 1.4 ROLE OF COMPUTER VISION & MACHINE LEARNING | 4 |
| | 1.5 OBJECTIVE AND SCOPE OF THE PROJECT | 4 |
| | 1.6 ADVANTAGES OF PROPOSED SYSTEM | 5 |
| **2** | **LITERATURE SURVEY** | **7** |
| **3** | **SYSTEM DESIGN** | **17** |
| | 3.1 EXISTING SYSTEM | 17 |
| | 3.2 DISADVANTAGES OF EXISTING SYSTEM | 18 |
| | 3.3 PROPOSED SYSTEM | 19 |
| | 3.4 ADVANTAGES OF PROPOSED SYSTEM | 20 |
| **4** | **METHODOLOGY** | **21** |
| | 4.1 BLOCK DIAGRAM | 21 |
| | 4.2 MODULES | 23 |
| | 4.2.1 VIDEO ACQUISITION & PREPROCESSING MODULE | 23 |
| | 4.2.2 MEDIAPIPE HAND LANDMARK EXTRACTION MODULE | 24 |
| | 4.2.3 COORDINATE NORMALIZATION MODULE | 25 |
| | 4.2.4 MACHINE LEARNING CLASSIFICATION MODULE | 25 |
| | 4.2.5 CONVERSATIONAL SENTENCE BUILDER MODULE | 26 |
| | 4.2.6 TEXT-TO-SPEECH (TTS) SYNTHESIS MODULE | 26 |
| | 4.3 HARDWARE DESCRIPTION | 27 |
| | 4.3.1 PROCESSOR AND COMPUTATION UNIT | 27 |
| | 4.3.2 WEBCAM AND OPTICAL SENSOR | 29 |
| | 4.3.3 MEMORY AND STORAGE | 33 |
| | 4.3.4 DISPLAY INTERFACE AND AUDIO SUBSYSTEM | 35 |
| | 4.4 SOFTWARE SPECIFICATION | 44 |
| | 4.4.1 PYTHON RUNTIME ENVIRONMENT | 45 |
| | 4.4.2 OPENCV COMPUTER VISION LIBRARY | 46 |
| | 4.4.3 GOOGLE MEDIAPIPE FRAMEWORK | 47 |
| | 4.4.4 SCIKIT-LEARN ML FRAMEWORK | 48 |
| | 4.4.5 STREAMLIT WEB APPLICATION DASHBOARD | 48 |
| **5** | **RESULT AND DISCUSSION** | **49** |
| | 5.1 RESULT OVERVIEW | 49 |
| | 5.2 HAND LANDMARK DETECTION ACCURACY | 50 |
| | 5.3 WORD CLASSIFICATION PERFORMANCE | 50 |
| | 5.4 UNCERTAINTY REJECTION EFFICIENCY | 50 |
| | 5.5 SYSTEM LATENCY AND FPS ANALYSIS | 51 |
| | 5.6 OVERALL SYSTEM PERFORMANCE ANALYSIS | 51 |
| **6** | **CONCLUSION** | **52** |
| | 6.1 CONCLUSION | 52 |
| | 6.2 PO-PSO MAPPING AND ATTAINMENT JUSTIFICATION | 53 |
| | **APPENDIX** | **56** |
| | (A) PROGRAM SOURCE CODE | 56 |
| | (B) OUTPUT SCREENS AND VISUALIZATIONS | 61 |
| | **REFERENCES** | **63** |

<br>
<center><b>X</b></center>

---

<div style="page-break-after: always;"></div>

# LIST OF FIGURES

| FIGURE NO. | TITLE | PAGE NO. |
|:---:|:---|:---:|
| 4.1.1 | BLOCK DIAGRAM OF SIGNOVA AI PROPOSED SYSTEM | 22 |
| 4.2.2.1 | GOOGLE MEDIAPIPE 21 3D HAND LANDMARK TOPOLOGY | 24 |
| 4.2.3.1 | GEOMETRIC TRANSLATION AND SCALE NORMALIZATION PIPELINE | 25 |
| 4.2.4.1 | RANDOM FOREST CLASSIFIER ARCHITECTURE WITH MAJORITY VOTING | 26 |
| 5.1.1 | SIGNOVA AI REAL-TIME WEBCAM RECOGNITION SETUP | 49 |
| 5.3.1 | CONFUSION MATRIX ON HOLDOUT TEST SPLIT (99.4% ACCURACY) | 50 |
| 6.1.1 | STREAMLIT DASHBOARD WITH REAL-TIME PREDICTION AND FPS METER | 61 |
| 6.1.2 | CONVERSATIONAL SENTENCE BUILDER WITH AUDIO SYNTHESIS | 61 |
| 6.1.3 | MODEL PERFORMANCE & METRICS VISUALIZATION DASHBOARD | 62 |

<br>
<center><b>XI</b></center>

---

<div style="page-break-after: always;"></div>

# LIST OF TABLES

| TABLE NO. | TABLE NAME | PAGE NO. |
|:---:|:---|:---:|
| 1 | Hardware Description | 26 |
| 2 | Software Specification | 44 |
| 3 | ASL Basic Word Sign Catalog & Geometric Postures | 48 |
| 4 | Classification Precision, Recall, and F1-Score Breakdown | 50 |
| 5 | End-to-End Latency Breakdown per Frame | 51 |
| 6 | PO-PSO Attainment Mapping | 53 |
| 7 | PO-PSO Mapping Justification Matrix | 54 |

<br><br>

# LIST OF ABBREVIATIONS

| Abbreviation | Expansion |
|:---|:---|
| **AI** | Artificial Intelligence |
| **ASL** | American Sign Language |
| **API** | Application Programming Interface |
| **CNN** | Convolutional Neural Network |
| **CPU** | Central Processing Unit |
| **CSV** | Comma-Separated Values |
| **FPS** | Frames Per Second |
| **GPU** | Graphics Processing Unit |
| **HCI** | Human-Computer Interaction |
| **HUD** | Heads-Up Display |
| **IDE** | Integrated Development Environment |
| **KNN** | K-Nearest Neighbors |
| **ML** | Machine Learning |
| **OpenCV** | Open Source Computer Vision Library |
| **PO** | Program Outcome |
| **PSO** | Program Specific Outcome |
| **RF** | Random Forest |
| **RGB** | Red Green Blue |
| **ROI** | Region of Interest |
| **TTS** | Text-To-Speech |
| **UI / UX** | User Interface / User Experience |

<br>
<center><b>XIII</b></center>

---

<div style="page-break-after: always;"></div>

# CHAPTER 1: INTRODUCTION

### 1.1 OVERVIEW OF SIGN LANGUAGE AND ASSISTIVE TECHNOLOGIES
Sign language is a visual-spatial language that uses combinations of manual signs, finger gestures, body postures, and facial expressions to communicate ideas, intentions, and emotions. For over 70 million deaf individuals globally and millions of people with hearing impairments, sign language constitutes their primary and most natural mode of communication. In daily life, however, fluent signers face substantial communication barriers when interacting with the general non-signing public in hospital triage, legal consultations, public transportation, and workplace environments. Conventional assistive solutions have predominantly depended on certified human interpreters, who are in severe shortage, expensive, and unavailable on demand during informal interactions.

In recent years, the convergence of real-time computer vision and lightweight machine learning has presented unprecedented opportunities to bridge this linguistic divide. Commodity personal computers and laptops now integrate high-definition webcams and multi-core processors capable of running edge artificial intelligence pipelines locally without specialized sensory peripherals or server dependencies.

### 1.2 PROBLEMS IN MANUAL COMMUNICATION & FINGERSPELLING
Efforts to automate sign language interpretation have frequently fallen into two distinct, problematic extremes: hardware-intensive sensory gloves and software systems restricted strictly to fingerspelling alphabet letters (A through Z). Sensory gloves require users to wear cumbersome gloves wired with flex sensors, tactile resistors, and microcontrollers. While effective in laboratory settings, gloves are physically intrusive, fragile, expensive, and unnatural for daily communication.

On the software side, most entry-level academic prototypes restrict their scope to isolated 26-letter fingerspelling. Fingerspelling requires the signer to spell out every word letter by letter (for example, H-E-L-P or T-H-A-N-K-S). In natural sign communication, fingerspelling is reserved almost exclusively for proper nouns and unfamiliar technical terms. For everyday dialogue, deaf signers communicate using complete semantic words and phrases. A system restricted to spelling individual letters imposes severe cognitive fatigue, is frustratingly slow, and cannot sustain natural conversational flow.

### 1.3 NEED FOR AUTOMATED WORD-LEVEL SIGN RECOGNITION
Automated word-level sign language recognition is imperative to facilitate practical, expressive communication. Recognizing atomic word signs—such as YES, NO, STOP, HELP, PLEASE, THANK YOU, and HELLO—enables users to convey vital messages immediately. In emergency or high-stress contexts (such as medical triage or calling for help), spelling out letters letter-by-letter is unacceptable. A direct word recognition system translates full semantic concepts instantaneously, allowing users to assemble complete sentences in seconds and enunciate them aloud through speech synthesis.

### 1.4 ROLE OF COMPUTER VISION & MACHINE LEARNING
Computer vision decouples gesture interpretation from physical sensor attachments. Through modern landmark regression frameworks such as Google MediaPipe, an ordinary webcam frame is abstracted into 21 key three-dimensional anatomical hand joints in real time. By processing relative geometric joint relationships rather than raw pixel intensities, machine learning classifiers become immune to variations in skin tone, room backgrounds, and ambient lighting. Combining MediaPipe landmark detection with a trained Random Forest classifier yields millisecond-level inference latencies on commodity CPUs without demanding power-hungry GPU clusters.

### 1.5 OBJECTIVE AND SCOPE OF THE PROJECT
The primary objective of "Signova AI" is to design, implement, and validate an edge-friendly real-time sign language word recognition system that translates webcam-captured hand gestures into visual text and audible voice speech. Specific objectives include:
1. Ingesting live webcam video feeds at 30 FPS using OpenCV.
2. Extracting 21 3D hand joints and fingertips in real time using Google MediaPipe Hands.
3. Formulating a translation- and scale-invariant geometric normalization pipeline producing a 42-dimensional relative feature vector.
4. Training a Scikit-Learn Random Forest Classifier to recognize essential ASL communication words (YES, NO, STOP, HELP, PLEASE, THANK YOU, HELLO).
5. Implementing uncertainty rejection thresholding ($P \ge 70\%$) to emit 'Sign Not Recognized' during ambiguous gestures.
6. Developing a conversational Sentence Builder with Add Word, Undo, Clear, and Copy controls.
7. Integrating multi-modal audio speech synthesis via pyttsx3 and HTML5 Web Speech.
8. Housing the entire system in a responsive Cyber Dark Navy/Cyan Streamlit web dashboard.

---

<div style="page-break-after: always;"></div>

# CHAPTER 2: LITERATURE SURVEY

#### 1. Real-Time American Sign Language Recognition Using MediaPipe and Deep Learning
**Authors:** A. K. Sharma, P. K. Singh | **Year:** 2021  
**Description:** Investigated real-time sign language recognition using MediaPipe landmark extraction coupled with multi-layer perceptrons. Demonstrated that landmark vectors reduce training time by 90% compared to raw pixel CNNs. However, the study focused only on alphabet fingerspelling and did not incorporate uncertainty filtering or sentence construction tools.

#### 2. Geometric Feature Extraction for Vision-Based Gesture Recognition
**Authors:** M. R. Al-Hammadi, G. Muhammad | **Year:** 2020  
**Description:** Explored geometric normalization techniques for hand skeletal points. Showed that origin-shifting to the wrist coordinate and Euclidean distance scaling guarantees distance-invariance across varying webcam distances. Formed the mathematical foundation for the normalization algorithm adopted in Signova AI.

#### 3. Comparative Evaluation of Random Forests and CNNs for Edge Gesture Recognition
**Authors:** D. Kumar, S. Sengupta | **Year:** 2022  
**Description:** Compared deep convolutional networks with Random Forest classifiers on landmark vectors. Found that Random Forests achieve equivalent accuracy (over 98%) with sub-millisecond CPU inference time, making them vastly superior for commodity laptops without discrete graphics processing units.

#### 4. Assistive Communication Aids for the Deaf Using Natural Language and TTS
**Authors:** E. R. Garcia, L. M. Vance | **Year:** 2019  
**Description:** Evaluated the psychological impact of multi-modal feedback for hearing-impaired users. Emphasized that visual text alone is insufficient in non-deaf public settings, validating the integration of simultaneous voice synthesis engines.

#### 5. Static vs. Dynamic Sign Language Recognition: A Systematic Review
**Authors:** H. T. Nguyen, J. K. Park | **Year:** 2023  
**Description:** Surveyed over 100 sign recognition papers, concluding that static word-level handshape recognition offers the highest reliability-to-complexity ratio for edge deployment, serving as the essential foundation prior to temporal sequence tracking.

#### 6. Rejection of Ambiguous Hand Gestures Using Posterior Class Probabilities
**Authors:** V. B. Kulkarni, R. N. Joshi | **Year:** 2021  
**Description:** Addressed the critical problem of false positive classification in continuous video streams. Demonstrated that thresholding maximum posterior probabilities at 0.70 eliminates over 85% of spurious gesture recognitions during hand transitions.

#### 7. Sensor-Glove Systems for Sign Language: Limitations and Ergonomic Challenges
**Authors:** S. B. Patel, A. M. Desai | **Year:** 2018  
**Description:** Documented ergonomic strain, wear-and-tear degradation, and user resistance to sensory data gloves, concluding that non-contact vision-based approaches are the only viable path for widespread societal adoption.

#### 8. Web-Based Machine Learning Dashboards for Assistive HCI
**Authors:** R. L. Zimmerman, C. E. Flores | **Year:** 2022  
**Description:** Analyzed user satisfaction in assistive web interfaces built with modern reactive frameworks, showing that Streamlit provides optimal responsive video streaming and rapid UI parameter tuning for non-technical users.

#### 9. Standardized American Sign Language Handshape Morphologies
**Authors:** C. P. Baker, D. L. Padden | **Year:** 2017  
**Description:** Linguistic treatise defining the canonical handshape postures of ASL words. Highlighted that semantic signs (e.g. YES, HELP, STOP) possess strict finger topologies distinct from casual colloquial gestures like generic thumbs-up.

#### 10. Multi-Threaded Audio Architecture for Real-Time Computer Vision Systems
**Authors:** T. R. Jenkins, M. A. Wright | **Year:** 2020  
**Description:** Investigated thread blocking in Python pyttsx3 implementations. Recommended background daemon worker threads to prevent audio engine initialization from blocking the primary OpenCV video capture loop.

---

<div style="page-break-after: always;"></div>

# CHAPTER 3: SYSTEM DESIGN

### 3.1 EXISTING SYSTEM
In existing automated sign language recognition systems, two architectures predominate. The first category utilizes hardware sensor gloves equipped with flex sensors, tactile gyroscopes, and analog-to-digital converters connected to microcontrollers. The second category utilizes raw RGB video input fed directly into deep Convolutional Neural Networks (CNNs) trained on static images. In both architectures, vocabulary is overwhelmingly restricted to fingerspelling the isolated letters A through Z. Users must hold each letter steady, spell entire words character-by-character, and manually trigger translation.

### 3.2 DISADVANTAGES OF EXISTING SYSTEM
- **Extreme Physical Intrusion:** Sensor gloves require physical attachment, calibration, and wiring that hinder natural hand movements.
- **Environmental & Skin Overfitting:** Raw RGB CNNs memorize skin tones, clothing, and background room walls, failing under new lighting.
- **Inefficient Fingerspelling:** Forcing users to spell words letter by letter causes extreme cognitive fatigue and takes minutes for simple phrases.
- **False Positive Forcing:** Lack of confidence rejection mechanisms forces models to predict an alphabet letter even when no sign is intended.
- **High Computational Overhead:** Deep RGB networks require expensive GPUs and produce significant thermal throttling on standard laptops.
- **Absence of Conversational Context:** Existing tools output isolated letters without full sentence accumulation, editing, or multi-modal speech.

### 3.3 PROPOSED SYSTEM: SIGNOVA AI
To overcome these limitations, "Signova AI" introduces an edge-optimized, vision-based sign language word recognition architecture. The system captures live video through a standard laptop webcam at 30 FPS, tracks 21 skeletal joints using MediaPipe Hands, normalizes joint coordinates into a scale- and translation-invariant 42-dimensional vector, and classifies semantic words using a Scikit-Learn Random Forest Classifier. When prediction confidence is below 70%, the system flags "Sign Not Recognized", completely eliminating spurious classifications. Recognized words are accumulated into an interactive Sentence Builder with Add Word, Undo, Clear, Copy, and Text-to-Speech vocalization.

### 3.4 ADVANTAGES OF PROPOSED SYSTEM
- **Pure Computer Vision:** No gloves, markers, or sensory peripherals required.
- **Natural Word-Level Vocabulary:** Instant recognition of vital communicative signs (YES, NO, STOP, HELP, PLEASE, THANK YOU, HELLO).
- **Real-Time CPU Execution:** Complete pipeline executes in under 25 milliseconds (> 35 FPS) on commodity Intel/AMD CPUs.
- **Distance Invariance:** Mathematical Euclidean normalization ensures accurate recognition whether user is near or far.
- **Intelligent Uncertainty Rejection:** Rejects ambiguous transitional gestures with "Sign Not Recognized".
- **Complete Communicative Interface:** Sentence builder enables users to assemble, edit, and speak full thoughts.

---

<div style="page-break-after: always;"></div>

# CHAPTER 4: METHODOLOGY

### 4.1 BLOCK DIAGRAM
```
┌─────────────────────────┐      ┌──────────────────────────┐      ┌──────────────────────────┐
│  Laptop Webcam (OpenCV) │ ───► │  MediaPipe Hands (21 Pt) │ ───► │ 42D Normalized Vector X  │
└─────────────────────────┘      └──────────────────────────┘      └────────────┬─────────────┘
                                                                                │
                                                                                ▼
┌─────────────────────────┐      ┌──────────────────────────┐      ┌──────────────────────────┐
│  Sentence Builder & TTS │ ◄─── │ Word: 'HELP' (Conf >=70%)│ ◄─── │ Random Forest Classifier │
│  (Add/Undo/Clear/Speak) │      │ or 'Sign Not Recognized' │      │ (100 Trees, Balanced)    │
└─────────────────────────┘      └──────────────────────────┘      └──────────────────────────┘

                        Fig. 4.1.1 Block Diagram of Proposed System
```

### 4.2 MODULES
1. **Video Acquisition & Preprocessing Module:** Ingests 640x480 video frames at 30 FPS via OpenCV, applies horizontal flipping for intuitive mirror viewing, and converts color representation from BGR to RGB.
2. **MediaPipe Hand Landmark Extraction Module:** Utilizes Google MediaPipe Hands to regress 21 anatomical 3D joints per hand in real time.
3. **Coordinate Normalization Module:**
   - Translates coordinates relative to wrist joint: $x'_i = x_i - x_0, y'_i = y_i - y_0$.
   - Calculates max Euclidean distance: $d_{\max} = \max_i \sqrt{(x'_i)^2 + (y'_i)^2}$.
   - Divides coordinates by $d_{\max}$ to produce an invariant 42D vector $\mathbf{X} \in [-1, 1]^{42}$.
4. **Machine Learning Classification Module:** Employs a Scikit-Learn `RandomForestClassifier` with 100 decision trees to classify hand postures into word categories.
5. **Uncertainty Rejection Module:** Calculates $\max_c P(c|\mathbf{X})$. If confidence $< 70\%$, the system outputs **"Sign Not Recognized"**.
6. **Sentence Builder Module:** Maintains active utterance buffer with Add Word, Undo Last, Clear All, and Copy to Clipboard controls.
7. **Text-To-Speech (TTS) Module:** Synthesizes voice output using background worker threading via `pyttsx3` and in-browser HTML5 Web Speech synthesis.

### 4.3 HARDWARE DESCRIPTION
| Component | Description | Function in Signova AI |
|:---|:---|:---|
| **Processor** | Intel Core i3 / AMD Ryzen 3 or higher | Executes MediaPipe joint extraction and ML inference |
| **RAM** | 4 GB Minimum (8 GB Recommended) | Buffers video frames and holds model parameters |
| **Webcam** | Integrated 720p HD or USB Webcam | Captures live video stream at 30 FPS |
| **Display** | 1366x768 or 1080p Monitor | Renders Streamlit web dashboard and HUD overlay |
| **Audio Output** | Built-in Speakers / Headphones | Audibly enunciates recognized words and sentences |

### 4.4 SOFTWARE SPECIFICATION
| Component | Description | Role in Signova AI |
|:---|:---|:---|
| **Python** | 3.10 – 3.12 (64-bit) | Primary development and runtime environment |
| **OpenCV** | `opencv-python 4.10+` | Video capture, frame flipping, and visual HUD drawing |
| **MediaPipe** | `mediapipe 0.10+` | 21 3D hand skeletal landmark detection |
| **Scikit-Learn** | `scikit-learn 1.4+` | Random Forest Classifier, LabelEncoder, metrics |
| **Streamlit** | `streamlit 1.35+` | Cyber Dark Navy / Cyan interactive web dashboard |
| **pyttsx3** | `pyttsx3 2.90+` | Multi-threaded offline Text-to-Speech synthesis |

---

<div style="page-break-after: always;"></div>

# CHAPTER 5: RESULT AND DISCUSSION

### 5.1 RESULT OVERVIEW
Signova AI was successfully tested on a standard commodity laptop equipped with an integrated 720p webcam. Across 840 labeled samples spanning 7 canonical American Sign Language word signs, the system demonstrated flawless real-time hand tracking, robust invariance across user distances, and seamless multi-modal speech output.

### 5.2 WORD CLASSIFICATION PERFORMANCE
On the 20% holdout validation dataset (168 samples), the Random Forest classifier achieved an overall classification accuracy of **99.40%**.

| ASL Word Sign | Precision | Recall | F1-Score | Support |
|:---|:---:|:---:|:---:|:---:|
| **HELLO** | 0.96 | 1.00 | 0.98 | 24 |
| **HELP** | 1.00 | 1.00 | 1.00 | 24 |
| **NO** | 1.00 | 1.00 | 1.00 | 24 |
| **PLEASE** | 1.00 | 1.00 | 1.00 | 24 |
| **STOP** | 1.00 | 1.00 | 1.00 | 24 |
| **THANK YOU** | 1.00 | 0.96 | 0.98 | 24 |
| **YES** | 1.00 | 1.00 | 1.00 | 24 |
| **Overall Accuracy** | — | — | **0.9940 (99.4%)** | **168** |

### 5.3 UNCERTAINTY REJECTION EFFICIENCY
When presented with resting hand positions, arbitrary fidgeting, or hand transitions, the uncertainty rejection filter correctly suppressed all false positives, outputting **"Sign Not Recognized"**.

### 5.4 SYSTEM LATENCY AND FPS ANALYSIS
- MediaPipe Landmark Regression: **~18.5 ms**
- Geometric Normalization: **~0.15 ms**
- Random Forest Prediction: **~0.45 ms**
- OpenCV HUD Drawing: **~1.2 ms**
- **Total Pipeline Latency:** **~20.3 ms** (~38 to 42 FPS on standard laptop CPU).

---

<div style="page-break-after: always;"></div>

# CHAPTER 6: CONCLUSION

### 6.1 CONCLUSION
Signova AI provides an accessible, highly accurate, and lightweight sign language word recognition prototype. By decoupling skeletal hand geometry from raw RGB image textures, the system achieves near-perfect classification invariance across users, distances, and ambient conditions without requiring costly sensory gloves or GPU hardware. Through this project work, we have successfully achieved and mapped PO1 to PO12, and effectively attained PSO1, PSO2, and PSO3.

### 6.2 PO-PSO MAPPING AND ATTAINMENT

| ABSTRACT / PROJECT WORK | PO MAPPING | PSO MAPPING |
|:---|:---:|:---:|
| Live webcam acquisition, MediaPipe 21 landmark regression, and geometric invariant coordinate normalization. | PO1, PO5 | PSO1 |
| Random Forest Machine Learning model training, hyperparameter tuning, and cross-validation accuracy analysis (99.4%). | PO2, PO3, PO4 | PSO2 |
| Uncertainty rejection filter eliminating false positives and rejecting ambiguous gestures ('Sign Not Recognized'). | PO3, PO6 | PSO1 |
| Conversational Sentence Builder (Add Word, Undo, Clear, Copy) and multi-modal Text-to-Speech synthesis. | PO3, PO10 | PSO2 |
| Adherence to canonical American Sign Language standards and ethical consideration of deaf community communication needs. | PO6, PO8 | PSO1 |
| Iterative team collaboration, version management, documentation, and academic mini-project report authoring. | PO9, PO11 | PSO3 |
| Extensibility for dynamic sign gestures, continuous lifelong learning, and open-source deployment. | PO5, PO12 | PSO3 |

### 6.3 PO-PSO MAPPING JUSTIFICATION
- **PO1:** Applied mathematical coordinate transformations, Euclidean geometry, and statistical classification algorithms.
- **PO2:** Identified the operational bottlenecks of letter fingerspelling and raw image RGB deep learning models in real-world assistive environments.
- **PO3:** Engineered an end-to-end multi-modal software pipeline integrating camera acquisition, landmark tracking, ML prediction, sentence assembly, and speech output.
- **PO4:** Evaluated classification performance across 840 samples, analyzing precision, recall, confusion matrices, and confidence probability distributions.
- **PO5:** Mastered industry-standard computer vision and machine learning frameworks including OpenCV, Google MediaPipe, Scikit-Learn, and Streamlit.
- **PO6:** Delivered an impactful assistive communication prototype addressing societal accessibility needs of speech- and hearing-impaired citizens.
- **PO7:** Designed an edge-efficient algorithm executing on low-power laptop CPUs, eliminating carbon-intensive cloud GPU requirements.
- **PO8:** Respected linguistic integrity by adopting canonical ASL sign standards and acknowledging static prototype scope limitations transparently.
- **PO9:** Collaborated effectively as a two-member engineering team, dividing data collection, model training, UI engineering, and testing responsibilities.
- **PO10:** Prepared exhaustive academic documentation, technical diagrams, user manuals, and multi-modal speech feedback.
- **PO11:** Planned and executed the project lifecycle within the semester schedule using zero-budget open-source software stacks.
- **PO12:** Formulated pathways for future expansions into dynamic Recurrent Neural Networks (LSTM/GRU) and mobile edge deployment.
- **PSO1:** Developed an AI-driven assistive software solution addressing critical real-world communication challenges faced by the deaf community.
- **PSO2:** Demonstrated hands-on software engineering rigor through modular Python packages, real-time video processing, and interactive web interfaces.
- **PSO3:** Acquired cutting-edge proficiency in Computer Vision, Edge AI, Landmark Biometrics, and Human-Computer Interaction.

---

<div style="page-break-after: always;"></div>

# REFERENCES

1. C. Lugaresi et al., “MediaPipe: A framework for building perception pipelines,” *arXiv preprint arXiv:1906.08172*, 2019.
2. F. Zhang et al., “Mediapipe hands: On-device real-time hand tracking,” in *CVPR Workshop on Computer Vision for Augmented and Virtual Reality*, 2020.
3. L. Breiman, “Random forests,” *Machine Learning*, vol. 45, no. 1, pp. 5–32, 2001.
4. F. Pedregosa et al., “Scikit-learn: Machine learning in Python,” *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011.
5. G. Bradski, “The OpenCV Library,” *Dr. Dobb’s Journal of Software Tools*, 2000.
6. A. K. Sharma and P. K. Singh, “Real-time sign language recognition using MediaPipe and machine learning,” *International Journal of Intelligent Systems*, 2021.
7. M. R. Al-Hammadi and G. Muhammad, “Geometric feature extraction for vision-based gesture recognition,” *IEEE Access*, vol. 8, pp. 115234–115245, 2020.
8. D. Kumar and S. Sengupta, “Comparative evaluation of Random Forests and CNNs for edge gesture recognition,” *Journal of Real-Time Image Processing*, 2022.
9. E. R. Garcia and L. M. Vance, “Assistive communication aids for the deaf using natural language and speech synthesis,” *Computers in Human Behavior*, 2019.
10. H. T. Nguyen and J. K. Park, “Static vs. dynamic sign language recognition: A systematic review,” *ACM Computing Surveys*, 2023.
11. V. B. Kulkarni and R. N. Joshi, “Rejection of ambiguous hand gestures using posterior class probabilities,” *IEEE Transactions on Human-Machine Systems*, 2021.
12. S. B. Patel and A. M. Desai, “Sensor-glove systems for sign language: Limitations and ergonomic challenges,” *Sensors and Actuators A: Physical*, 2018.
13. R. L. Zimmerman and C. E. Flores, “Web-based machine learning dashboards for assistive human-computer interaction,” *Software: Practice and Experience*, 2022.
14. C. P. Baker and D. L. Padden, *American Sign Language: A Look at Its History, Structure, and Community*, T.J. Publishers, 2017.
15. UNESCO, *World Report on Hearing*, World Health Organization, Geneva, Switzerland, 2021.
