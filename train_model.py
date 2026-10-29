"""
Machine Learning Training Pipeline
Trains a Random Forest classifier on collected normalized hand landmarks.
Part of Signova: AI-Based Sign Language Recognition System
"""

import os
import sys
import json
import pickle
import datetime
from typing import Dict, Any, Tuple

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "gestures.csv")
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "gesture_model.pkl")
METADATA_PATH = os.path.join(MODEL_DIR, "model_metadata.json")


def train_gesture_classifier(
    data_path: str = DATA_FILE,
    model_output_path: str = MODEL_PATH,
    metadata_output_path: str = METADATA_PATH,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[Any, LabelEncoder, Dict[str, Any]]:
    """
    Train and evaluate a Random Forest classifier for hand gesture recognition.

    Returns:
        (model, label_encoder, metadata_dict)
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset file not found at: {data_path}. Collect or generate data first.")

    df = pd.read_csv(data_path)
    if df.empty or len(df) < 10:
        raise ValueError("Dataset contains insufficient samples to train a model.")

    print("=" * 65)
    print("  SIGNOVA MACHINE LEARNING MODEL TRAINING PIPELINE")
    print("=" * 65)
    print(f"[+] Loaded dataset: {len(df)} total samples.")

    # Class distribution
    counts = df["label"].value_counts()
    print("\nSample count per gesture class:")
    for label, count in counts.items():
        print(f"  - {label:<15}: {count} samples")

    classes = sorted(df["label"].unique().tolist())
    if len(classes) < 2:
        raise ValueError(f"Need at least 2 distinct gesture classes to train a classifier. Found: {classes}")

    # Features and labels
    feature_cols = [c for c in df.columns if c != "label"]
    if len(feature_cols) != 42:
        raise ValueError(f"Expected 42 normalized features (21 landmarks * 2). Found: {len(feature_cols)}")

    X = df[feature_cols].values.astype(np.float32)
    y_raw = df["label"].values

    # Encode categorical string labels to integers
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y_raw)

    # Train / Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    print(f"\n[+] Dataset split: {len(X_train)} training samples, {len(X_test)} validation samples.")

    # Train Random Forest Classifier
    print("[+] Training Random Forest Classifier (100 estimators, balanced weights)...")
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=16,
        random_state=random_state,
        class_weight="balanced",
        n_jobs=-1,
    )
    clf.fit(X_train, y_train)

    # Evaluation on holdout test set
    y_pred = clf.predict(X_test)
    accuracy = float(accuracy_score(y_test, y_pred))

    target_names = [str(cls) for cls in label_encoder.classes_]
    report_dict = classification_report(
        y_test, y_pred, target_names=target_names, output_dict=True, zero_division=0
    )
    report_text = classification_report(y_test, y_pred, target_names=target_names, zero_division=0)
    conf_matrix = confusion_matrix(y_test, y_pred).tolist()

    print("\n" + "=" * 65)
    print(f"  MODEL EVALUATION RESULTS (Accuracy: {accuracy * 100:.2f}%)")
    print("=" * 65)
    print(report_text)
    print("Confusion Matrix:")
    print(np.array(conf_matrix))
    print("=" * 65)

    # Save model artifacts
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    artifacts = {
        "model": clf,
        "label_encoder": label_encoder,
        "feature_names": feature_cols,
        "classes": target_names,
    }

    with open(model_output_path, "wb") as f:
        pickle.dump(artifacts, f)
    print(f"\n[+] Saved model artifact to: {model_output_path}")

    # Save human-readable and UI-loadable metadata
    metadata = {
        "model_type": "RandomForestClassifier",
        "training_timestamp": datetime.datetime.now().isoformat(),
        "total_samples": int(len(df)),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
        "accuracy": accuracy,
        "classes": target_names,
        "class_distribution": counts.to_dict(),
        "confusion_matrix": conf_matrix,
        "classification_report": report_dict,
    }

    with open(metadata_output_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[+] Saved model metrics metadata to: {metadata_output_path}")

    return clf, label_encoder, metadata


if __name__ == "__main__":
    train_gesture_classifier()
