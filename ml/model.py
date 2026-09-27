"""
AdaptiveLearn AI - Machine Learning Model
Decision Tree Classifier to predict ML Learning State:
- IMPROVING
- STABLE
- NEEDS_SUPPORT

Ground truth training generator simulates pedagogical patterns:
- Low scores + repeated failures + declining trend => NEEDS_SUPPORT
- High scores + upward trend => IMPROVING
- Mid scores + consistent attempts => STABLE
"""

import os
import joblib
import numpy as np
from sklearn.tree import DecisionTreeClassifier

MODEL_PATH = os.path.join(os.path.dirname(__file__), "decision_tree_model.joblib")

def generate_synthetic_training_data():
    """Generates synthetic student performance data grounded in educational learning curves."""
    np.random.seed(42)
    X = []
    y = []
    
    # 1. NEEDS_SUPPORT Cluster (struggling students like Rahul)
    for _ in range(350):
        assessment = np.random.uniform(20.0, 55.0)
        practice = np.random.uniform(25.0, 58.0)
        attempts = np.random.randint(3, 10)
        failed_attempts = np.random.randint(2, attempts + 1)
        prev_mastery = np.random.uniform(30.0, 65.0)
        trend = np.random.choice([-1.0, 0.0], p=[0.75, 0.25])
        video_eng = np.random.uniform(0.1, 0.6)
        time_between = np.random.uniform(1.0, 72.0)
        X.append([assessment, practice, attempts, failed_attempts, prev_mastery, trend, video_eng, time_between])
        y.append("NEEDS_SUPPORT")

    # 2. IMPROVING Cluster (excelling / progressing students like Priya & Ananya)
    for _ in range(350):
        assessment = np.random.uniform(72.0, 98.0)
        practice = np.random.uniform(75.0, 100.0)
        attempts = np.random.randint(1, 5)
        failed_attempts = np.random.randint(0, 2)
        prev_mastery = np.random.uniform(55.0, 85.0)
        trend = np.random.choice([1.0, 0.0], p=[0.85, 0.15])
        video_eng = np.random.uniform(0.6, 1.2)
        time_between = np.random.uniform(2.0, 48.0)
        X.append([assessment, practice, attempts, failed_attempts, prev_mastery, trend, video_eng, time_between])
        y.append("IMPROVING")

    # 3. STABLE Cluster (steady students like Arjun)
    for _ in range(300):
        assessment = np.random.uniform(58.0, 74.0)
        practice = np.random.uniform(60.0, 78.0)
        attempts = np.random.randint(2, 6)
        failed_attempts = np.random.randint(0, 2)
        prev_mastery = np.random.uniform(55.0, 75.0)
        trend = 0.0
        video_eng = np.random.uniform(0.4, 0.9)
        time_between = np.random.uniform(4.0, 48.0)
        X.append([assessment, practice, attempts, failed_attempts, prev_mastery, trend, video_eng, time_between])
        y.append("STABLE")

    return np.array(X), np.array(y)

def train_or_load_model():
    """Trains a DecisionTreeClassifier if not already saved, or loads existing model."""
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            pass

    X, y = generate_synthetic_training_data()
    clf = DecisionTreeClassifier(max_depth=5, min_samples_split=8, random_state=42)
    clf.fit(X, y)
    
    try:
        joblib.dump(clf, MODEL_PATH)
    except Exception:
        pass
    return clf

# Global instance
decision_tree_model = train_or_load_model()
