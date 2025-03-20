#!/usr/bin/env python3
"""
Model Drift Detector

This module detects drift in model inputs and outputs over time, allowing for
early detection of model degradation and triggering retraining when needed.
"""

import json
import logging
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Union, Tuple

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
from prometheus_client import Gauge, push_to_gateway

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DriftDetector:
    """Detects data and concept drift in model inputs and outputs."""

    def __init__(
        self,
        model_name: str,
        model_version: str,
        reference_data_path: Optional[str] = None,
        metrics_store: str = "prometheus",
        push_gateway_url: Optional[str] = "localhost:9091",
        drift_threshold: float = 0.05,
        window_size: int = 1000,
    ):
        """
        Initialize the drift detector.
        
        Args:
            model_name: Name of the model to monitor
            model_version: Version of the model
            reference_data_path: Path to reference data distribution
            metrics_store: Type of metrics store (prometheus, local, etc.)
            push_gateway_url: URL for Prometheus Push Gateway
            drift_threshold: Threshold for detecting significant drift
            window_size: Number of observations to collect before checking drift
        """
        self.model_name = model_name
        self.model_version = model_version
        self.reference_data_path = reference_data_path
        self.metrics_store = metrics_store
        self.push_gateway_url = push_gateway_url
        self.drift_threshold = drift_threshold
        self.window_size = window_size
        
        # Initialize data containers
        self.reference_features = {}
        self.reference_predictions = []
        self.current_features = {}
        self.current_predictions = []
        
        # Initialize anomaly detection model
        self.isolation_forest = None
        
        # Initialize Prometheus metrics if needed
        if metrics_store == "prometheus":
            self._init_prometheus_metrics()
        
        # Load reference data if provided
        if reference_data_path:
            self._load_reference_data(reference_data_path)
            
        logger.info(f"Initialized drift detector for model: {model_name} v{model_version}")
    
    def _init_prometheus_metrics(self) -> None:
        """Initialize Prometheus metrics for drift detection."""
        # Feature drift gauges
        self.feature_drift_gauge = Gauge(
            'model_feature_drift',
            'Feature drift score',
            ['model_name', 'model_version', 'feature_name']
        )
        
        # Prediction drift gauge
        self.prediction_drift_gauge = Gauge(
            'model_prediction_drift',
            'Prediction drift score',
            ['model_name', 'model_version']
        )
        
        # Concept drift gauge
        self.concept_drift_gauge = Gauge(
            'model_concept_drift',
            'Concept drift score',
            ['model_name', 'model_version']
        )
        
        # Anomaly score gauge
        self.anomaly_score_gauge = Gauge(
            'model_anomaly_score',
            'Anomaly score of recent data',
            ['model_name', 'model_version']
        )
    
    def _load_reference_data(self, reference_data_path: str) -> None:
        """Load reference data distribution."""
        try:
            data = pd.read_csv(reference_data_path)
            
            # Extract features (all columns except 'prediction')
            feature_columns = [col for col in data.columns if col != 'prediction']
            for col in feature_columns:
                self.reference_features[col] = data[col].values
                # Initialize current feature container
                self.current_features[col] = []
            
            # Extract predictions
            if 'prediction' in data.columns:
                self.reference_predictions = data['prediction'].values
                
            # Train isolation forest for anomaly detection
            self._train_anomaly_detector(data[feature_columns])
                
            logger.info(f"Loaded reference data from {reference_data_path}")
        except Exception as e:
            logger.error(f"Failed to load reference data: {e}")
    
    def _train_anomaly_detector(self, reference_features: pd.DataFrame) -> None:
        """Train an anomaly detection model on reference data."""
        try:
            self.isolation_forest = IsolationForest(
                n_estimators=100,
                contamination=0.01,
                random_state=42
            )
            self.isolation_forest.fit(reference_features)
            logger.info("Trained anomaly detection model")
        except Exception as e:
            logger.error(f"Failed to train anomaly detection model: {e}")
    
    def add_observation(
        self,
        features: Dict[str, Any],
        prediction: Any,
        ground_truth: Optional[Any] = None,
    ) -> None:
        """
        Add a new observation for drift detection.
        
        Args:
            features: Input features used for prediction
            prediction: Model prediction output
            ground_truth: Actual ground truth (if available)
        """
        # Add features to current window
        for feature_name, feature_value in features.items():
            if isinstance(feature_value, (int, float)):
                if feature_name in self.current_features:
                    self.current_features[feature_name].append(feature_value)
                else:
                    self.current_features[feature_name] = [feature_value]
        
        # Add prediction to current window
        self.current_predictions.append(prediction)
        
        # Check if we have enough data to detect drift
        if len(self.current_predictions) >= self.window_size:
            self.detect_drift()
    
    def detect_drift(self) -> Dict[str, Any]:
        """
        Detect drift in current data compared to reference data.
        
        Returns:
            Dict containing drift metrics
        """
        drift_metrics = {
            "timestamp": datetime.now().isoformat(),
            "model_name": self.model_name,
            "model_version": self.model_version,
            "feature_drift": {},
            "prediction_drift": 0.0,
            "concept_drift": 0.0,
            "anomaly_score": 0.0
        }
        
        # Detect data drift in features
        for feature_name, current_values in self.current_features.items():
            if feature_name in self.reference_features and len(current_values) > 0:
                drift_score = self._calculate_distribution_drift(
                    self.reference_features[feature_name],
                    current_values
                )
                drift_metrics["feature_drift"][feature_name] = drift_score
                
                # Update Prometheus metrics if configured
                if self.metrics_store == "prometheus":
                    self.feature_drift_gauge.labels(
                        model_name=self.model_name,
                        model_version=self.model_version,
                        feature_name=feature_name
                    ).set(drift_score)
                    
                # Check if drift exceeds threshold
                if drift_score > self.drift_threshold:
                    logger.warning(f"Detected significant drift in feature {feature_name}: {drift_score}")
        
        # Detect drift in predictions
        if len(self.reference_predictions) > 0 and len(self.current_predictions) > 0:
            prediction_drift = self._calculate_distribution_drift(
                self.reference_predictions,
                self.current_predictions
            )
            drift_metrics["prediction_drift"] = prediction_drift
            
            # Update Prometheus metrics if configured
            if self.metrics_store == "prometheus":
                self.prediction_drift_gauge.labels(
                    model_name=self.model_name,
                    model_version=self.model_version
                ).set(prediction_drift)
                
            # Check if drift exceeds threshold
            if prediction_drift > self.drift_threshold:
                logger.warning(f"Detected significant drift in predictions: {prediction_drift}")
        
        # Check for anomalies if isolation forest is trained
        if self.isolation_forest is not None:
            try:
                # Prepare feature data
                feature_df = pd.DataFrame({
                    feature_name: current_values[-self.window_size:]
                    for feature_name, current_values in self.current_features.items()
                    if len(current_values) >= self.window_size
                })
                
                # Calculate anomaly scores
                anomaly_scores = self.isolation_forest.score_samples(feature_df)
                avg_anomaly_score = np.mean(anomaly_scores) * -1  # Convert to positive anomaly score
                
                drift_metrics["anomaly_score"] = avg_anomaly_score
                
                # Update Prometheus metrics if configured
                if self.metrics_store == "prometheus":
                    self.anomaly_score_gauge.labels(
                        model_name=self.model_name,
                        model_version=self.model_version
                    ).set(avg_anomaly_score)
                    
                # Check if anomaly score exceeds threshold
                if avg_anomaly_score > 0.7:  # Typical threshold for isolation forest
                    logger.warning(f"Detected anomalies in recent data: {avg_anomaly_score}")
            except Exception as e:
                logger.error(f"Failed to calculate anomaly scores: {e}")
        
        # Push metrics to Prometheus if configured
        if self.metrics_store == "prometheus":
            try:
                push_to_gateway(
                    self.push_gateway_url,
                    job=f"{self.model_name}_{self.model_version}_drift",
                    registry=None
                )
            except Exception as e:
                logger.error(f"Failed to push drift metrics to Prometheus: {e}")
        
        # Log drift metrics
        self._log_drift_metrics(drift_metrics)
        
        # Clear current data after drift detection
        self._reset_current_data()
        
        return drift_metrics
    
    def _calculate_distribution_drift(
        self,
        reference_values: List[float],
        current_values: List[float]
    ) -> float:
        """
        Calculate distribution drift using statistical tests.
        
        Args:
            reference_values: Values from reference distribution
            current_values: Values from current distribution
            
        Returns:
            Drift score between 0 and 1, where higher values indicate more drift
        """
        try:
            # Kolmogorov-Smirnov test for distribution similarity
            ks_stat, p_value = stats.ks_2samp(reference_values, current_values)
            
            # Convert p-value to drift score (1 - p_value)
            # Lower p-values indicate higher probability of different distributions
            drift_score = 1.0 - p_value
            
            return drift_score
        except Exception as e:
            logger.error(f"Failed to calculate distribution drift: {e}")
            return 0.0
    
    def _log_drift_metrics(self, drift_metrics: Dict[str, Any]) -> None:
        """Log drift metrics."""
        # Default to JSON logging
        try:
            with open(f"logs/{self.model_name}_drift.jsonl", "a") as f:
                f.write(json.dumps(drift_metrics) + "\n")
        except Exception as e:
            logger.error(f"Failed to log drift metrics: {e}")
    
    def _reset_current_data(self) -> None:
        """Reset current data containers after drift detection."""
        # Keep a small buffer to avoid abrupt changes
        buffer_size = min(100, self.window_size // 10)
        
        for feature_name in self.current_features:
            if len(self.current_features[feature_name]) > buffer_size:
                self.current_features[feature_name] = self.current_features[feature_name][-buffer_size:]
            else:
                self.current_features[feature_name] = []
        
        if len(self.current_predictions) > buffer_size:
            self.current_predictions = self.current_predictions[-buffer_size:]
        else:
            self.current_predictions = []
    
    def generate_drift_report(self, output_path: str = "reports") -> str:
        """
        Generate a comprehensive drift report with visualizations.
        
        Args:
            output_path: Directory to save the report
            
        Returns:
            Path to the generated report
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"{output_path}/{self.model_name}_drift_report_{timestamp}.html"
        
        try:
            # Create basic HTML report
            with open(report_path, "w") as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Drift Report - {self.model_name} v{self.model_version}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1, h2, h3 {{ color: #333; }}
        .chart {{ margin: 20px 0; }}
        .metric {{ margin: 10px 0; }}
        .drift-high {{ color: red; }}
        .drift-medium {{ color: orange; }}
        .drift-low {{ color: green; }}
    </style>
</head>
<body>
    <h1>Model Drift Report</h1>
    <p>Model: {self.model_name} v{self.model_version}</p>
    <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    
    <h2>Feature Drift Summary</h2>
""")

                # Add feature drift metrics
                for feature_name, drift_score in self.detect_drift()["feature_drift"].items():
                    drift_class = "drift-low"
                    if drift_score > self.drift_threshold:
                        drift_class = "drift-high"
                    elif drift_score > self.drift_threshold / 2:
                        drift_class = "drift-medium"
                        
                    f.write(f"""    <div class="metric">
        <h3>{feature_name}</h3>
        <p>Drift Score: <span class="{drift_class}">{drift_score:.4f}</span></p>
        <div class="chart">
            <!-- Placeholder for chart image -->
            <img src="charts/{feature_name}_distribution.png" alt="{feature_name} Distribution" />
        </div>
    </div>
""")
                
                # Add prediction drift metrics
                pred_drift = self.detect_drift()["prediction_drift"]
                drift_class = "drift-low"
                if pred_drift > self.drift_threshold:
                    drift_class = "drift-high"
                elif pred_drift > self.drift_threshold / 2:
                    drift_class = "drift-medium"
                    
                f.write(f"""    <h2>Prediction Drift Summary</h2>
    <div class="metric">
        <p>Drift Score: <span class="{drift_class}">{pred_drift:.4f}</span></p>
        <div class="chart">
            <!-- Placeholder for chart image -->
            <img src="charts/prediction_distribution.png" alt="Prediction Distribution" />
        </div>
    </div>
""")

                # Add anomaly score
                anomaly_score = self.detect_drift()["anomaly_score"]
                anomaly_class = "drift-low"
                if anomaly_score > 0.7:
                    anomaly_class = "drift-high"
                elif anomaly_score > 0.5:
                    anomaly_class = "drift-medium"
                    
                f.write(f"""    <h2>Anomaly Detection</h2>
    <div class="metric">
        <p>Anomaly Score: <span class="{anomaly_class}">{anomaly_score:.4f}</span></p>
    </div>
""")

                # Close HTML
                f.write("""</body>
</html>
""")
                
            # Generate charts directory
            os.makedirs(f"{output_path}/charts", exist_ok=True)
            
            # Create distribution charts for features
            for feature_name in self.current_features:
                if feature_name in self.reference_features:
                    plt.figure(figsize=(10, 6))
                    sns.kdeplot(self.reference_features[feature_name], label="Reference")
                    sns.kdeplot(self.current_features[feature_name], label="Current")
                    plt.title(f"{feature_name} Distribution Comparison")
                    plt.legend()
                    plt.savefig(f"{output_path}/charts/{feature_name}_distribution.png")
                    plt.close()
            
            # Create prediction distribution chart
            plt.figure(figsize=(10, 6))
            sns.kdeplot(self.reference_predictions, label="Reference")
            sns.kdeplot(self.current_predictions, label="Current")
            plt.title("Prediction Distribution Comparison")
            plt.legend()
            plt.savefig(f"{output_path}/charts/prediction_distribution.png")
            plt.close()
            
            logger.info(f"Generated drift report at: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"Failed to generate drift report: {e}")
            return ""

if __name__ == "__main__":
    # Example usage
    import os
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Initialize drift detector
    detector = DriftDetector(
        model_name="example_model",
        model_version="1.0.0",
        drift_threshold=0.05,
        window_size=100  # Smaller window for demo
    )
    
    # Simulate adding observations
    import random
    
    # Reference distribution: normal with mean=0, std=1
    reference_data = {
        "feature1": np.random.normal(0, 1, 1000),
        "feature2": np.random.normal(5, 2, 1000),
    }
    reference_predictions = np.random.normal(0.5, 0.2, 1000)
    
    # Create reference data CSV
    ref_df = pd.DataFrame(reference_data)
    ref_df["prediction"] = reference_predictions
    os.makedirs("data", exist_ok=True)
    ref_df.to_csv("data/reference_data.csv", index=False)
    
    # Initialize with reference data
    detector = DriftDetector(
        model_name="example_model",
        model_version="1.0.0",
        reference_data_path="data/reference_data.csv"
    )
    
    # Simulate current data (with some drift)
    for i in range(200):
        # Introduce gradual drift by shifting the mean
        shift = i / 100.0
        features = {
            "feature1": np.random.normal(0 + shift, 1, 1),
            "feature2": np.random.normal(5, 2 + shift/2, 1),
        }
        prediction = np.random.normal(0.5 + shift/10, 0.2, 1)[0]
        
        detector.add_observation(
            features={k: v[0] for k, v in features.items()},
            prediction=prediction
        )
    
    # Generate drift report
    os.makedirs("reports", exist_ok=True)
    detector.generate_drift_report() 