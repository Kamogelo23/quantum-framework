"""
ML Model Training Script
Example training script for anomaly detection model
"""
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os
from datetime import datetime


def generate_sample_data(n_samples=1000):
    """Generate sample training data"""
    # Generate normal data
    normal_data = np.random.randn(n_samples, 5)
    
    # Add some anomalies
    anomalies = np.random.uniform(low=-10, high=10, size=(int(n_samples * 0.1), 5))
    
    data = np.vstack([normal_data, anomalies])
    return data


def train_anomaly_detector():
    """Train isolation forest for anomaly detection"""
    print("🎓 Training anomaly detection model...")
    
    # Generate training data
    X_train = generate_sample_data(1000)
    
    # Train model
    model = IsolationForest(
        contamination=0.1,
        random_state=42,
        n_estimators=100
    )
    model.fit(X_train)
    
    # Save model
    models_dir = "../models"
    os.makedirs(models_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, "anomaly_detector_v1.joblib")
    joblib.dump(model, model_path)
    
    print(f"✅ Model saved to: {model_path}")
    
    # Save metadata
    metadata = {
        "model_name": "anomaly-detector",
        "version": "1.0.0",
        "type": "isolation-forest",
        "trained_date": datetime.now().isoformat(),
        "n_samples": len(X_train),
        "features": 5
    }
    
    metadata_path = os.path.join(models_dir, "anomaly_detector_v1_metadata.json")
    import json
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("✅ Metadata saved!")
    return model


if __name__ == "__main__":
    train_anomaly_detector()
