#!/usr/bin/env python3
"""
Model Metrics Collector

This module collects and logs metrics from models in production, providing
real-time monitoring of model performance and health.
"""

import json
import logging
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Union, Tuple

import pandas as pd
import numpy as np
import requests
import mlflow
from prometheus_client import Counter, Gauge, Histogram, push_to_gateway

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ModelMetricsCollector:
    """Collects and logs model performance metrics for monitoring."""

    def __init__(
        self,
        model_name: str,
        model_version: str,
        metrics_store: str = "prometheus",
        push_gateway_url: Optional[str] = "localhost:9091",
        mlflow_tracking_uri: Optional[str] = None,
    ):
        """
        Initialize the metrics collector.
        
        Args:
            model_name: Name of the model to monitor
            model_version: Version of the model
            metrics_store: Type of metrics store (prometheus, mlflow, etc.)
            push_gateway_url: URL for Prometheus Push Gateway
            mlflow_tracking_uri: URI for MLflow tracking server
        """
        self.model_name = model_name
        self.model_version = model_version
        self.metrics_store = metrics_store
        self.push_gateway_url = push_gateway_url
        
        # Initialize MLflow if specified
        if mlflow_tracking_uri:
            mlflow.set_tracking_uri(mlflow_tracking_uri)
        
        # Initialize Prometheus metrics
        if metrics_store == "prometheus":
            self._init_prometheus_metrics()
            
        logger.info(f"Initialized metrics collector for model: {model_name} v{model_version}")
    
    def _init_prometheus_metrics(self) -> None:
        """Initialize Prometheus metrics."""
        # Create metric objects
        self.prediction_counter = Counter(
            'model_predictions_total',
            'Total number of predictions',
            ['model_name', 'model_version']
        )
        
        self.prediction_latency = Histogram(
            'model_prediction_latency_seconds',
            'Latency of model predictions',
            ['model_name', 'model_version'],
            buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0),
        )
        
        self.prediction_errors = Counter(
            'model_prediction_errors_total',
            'Total number of prediction errors',
            ['model_name', 'model_version', 'error_type']
        )
        
        self.feature_value = Gauge(
            'model_feature_value',
            'Feature values used for prediction',
            ['model_name', 'model_version', 'feature_name']
        )
        
        self.accuracy_gauge = Gauge(
            'model_accuracy',
            'Model accuracy metric',
            ['model_name', 'model_version']
        )
        
        self.f1_score_gauge = Gauge(
            'model_f1_score',
            'Model F1 score metric',
            ['model_name', 'model_version']
        )
    
    def log_prediction(
        self,
        features: Dict[str, Any],
        prediction: Any,
        ground_truth: Optional[Any] = None,
        latency: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log a single prediction event.
        
        Args:
            features: Input features used for prediction
            prediction: Model prediction output
            ground_truth: Actual ground truth (if available)
            latency: Prediction latency in seconds
            metadata: Additional metadata for the prediction
        """
        timestamp = datetime.now().isoformat()
        
        # Log to appropriate store
        if self.metrics_store == "prometheus":
            self._log_to_prometheus(features, prediction, ground_truth, latency)
        elif self.metrics_store == "mlflow":
            self._log_to_mlflow(features, prediction, ground_truth, latency, timestamp, metadata)
        else:
            # Default to JSON logging
            self._log_to_json(features, prediction, ground_truth, latency, timestamp, metadata)
    
    def _log_to_prometheus(
        self,
        features: Dict[str, Any],
        prediction: Any,
        ground_truth: Optional[Any],
        latency: Optional[float],
    ) -> None:
        """Log metrics to Prometheus."""
        # Increment prediction counter
        self.prediction_counter.labels(
            model_name=self.model_name,
            model_version=self.model_version
        ).inc()
        
        # Record latency if provided
        if latency is not None:
            self.prediction_latency.labels(
                model_name=self.model_name,
                model_version=self.model_version
            ).observe(latency)
        
        # Log feature values
        for feature_name, feature_value in features.items():
            if isinstance(feature_value, (int, float)):
                self.feature_value.labels(
                    model_name=self.model_name,
                    model_version=self.model_version,
                    feature_name=feature_name
                ).set(feature_value)
        
        # Push metrics to gateway
        try:
            push_to_gateway(
                self.push_gateway_url,
                job=f"{self.model_name}_{self.model_version}",
                registry=None
            )
        except Exception as e:
            logger.error(f"Failed to push metrics to Prometheus: {e}")
    
    def _log_to_mlflow(
        self,
        features: Dict[str, Any],
        prediction: Any,
        ground_truth: Optional[Any],
        latency: Optional[float],
        timestamp: str,
        metadata: Optional[Dict[str, Any]],
    ) -> None:
        """Log metrics to MLflow."""
        try:
            # Create a run in MLflow
            with mlflow.start_run(run_name=f"monitoring_{timestamp}"):
                # Log basic metrics
                if latency is not None:
                    mlflow.log_metric("prediction_latency", latency)
                
                # Log prediction and ground truth as params
                mlflow.log_param("prediction", str(prediction))
                if ground_truth is not None:
                    mlflow.log_param("ground_truth", str(ground_truth))
                    
                # Log features as params
                for feature_name, feature_value in features.items():
                    mlflow.log_param(f"feature_{feature_name}", str(feature_value))
                
                # Log metadata if provided
                if metadata:
                    for key, value in metadata.items():
                        mlflow.log_param(f"metadata_{key}", str(value))
        except Exception as e:
            logger.error(f"Failed to log metrics to MLflow: {e}")
    
    def _log_to_json(
        self,
        features: Dict[str, Any],
        prediction: Any,
        ground_truth: Optional[Any],
        latency: Optional[float],
        timestamp: str,
        metadata: Optional[Dict[str, Any]],
    ) -> None:
        """Log metrics to JSON file."""
        log_data = {
            "timestamp": timestamp,
            "model_name": self.model_name,
            "model_version": self.model_version,
            "features": features,
            "prediction": prediction,
        }
        
        if ground_truth is not None:
            log_data["ground_truth"] = ground_truth
        
        if latency is not None:
            log_data["latency"] = latency
            
        if metadata:
            log_data["metadata"] = metadata
            
        try:
            with open(f"logs/{self.model_name}_metrics.jsonl", "a") as f:
                f.write(json.dumps(log_data) + "\n")
        except Exception as e:
            logger.error(f"Failed to log metrics to JSON: {e}")
    
    def log_batch_metrics(
        self,
        accuracy: float,
        f1_score: Optional[float] = None,
        precision: Optional[float] = None,
        recall: Optional[float] = None,
        roc_auc: Optional[float] = None,
        additional_metrics: Optional[Dict[str, float]] = None,
    ) -> None:
        """
        Log batch performance metrics.
        
        Args:
            accuracy: Model accuracy metric
            f1_score: F1 score metric
            precision: Precision metric
            recall: Recall metric
            roc_auc: ROC AUC metric
            additional_metrics: Any additional metrics to log
        """
        if self.metrics_store == "prometheus":
            # Set Prometheus gauges
            self.accuracy_gauge.labels(
                model_name=self.model_name,
                model_version=self.model_version
            ).set(accuracy)
            
            if f1_score is not None:
                self.f1_score_gauge.labels(
                    model_name=self.model_name,
                    model_version=self.model_version
                ).set(f1_score)
                
            # Push metrics to gateway
            try:
                push_to_gateway(
                    self.push_gateway_url,
                    job=f"{self.model_name}_{self.model_version}_batch",
                    registry=None
                )
            except Exception as e:
                logger.error(f"Failed to push batch metrics to Prometheus: {e}")
        
        elif self.metrics_store == "mlflow":
            try:
                # Create a run in MLflow for batch metrics
                with mlflow.start_run(run_name=f"batch_metrics_{datetime.now().isoformat()}"):
                    # Log performance metrics
                    mlflow.log_metric("accuracy", accuracy)
                    
                    if f1_score is not None:
                        mlflow.log_metric("f1_score", f1_score)
                    
                    if precision is not None:
                        mlflow.log_metric("precision", precision)
                    
                    if recall is not None:
                        mlflow.log_metric("recall", recall)
                    
                    if roc_auc is not None:
                        mlflow.log_metric("roc_auc", roc_auc)
                    
                    # Log additional metrics if provided
                    if additional_metrics:
                        for metric_name, metric_value in additional_metrics.items():
                            mlflow.log_metric(metric_name, metric_value)
            except Exception as e:
                logger.error(f"Failed to log batch metrics to MLflow: {e}")
        else:
            # Default to logging to console
            logger.info(f"Batch metrics for {self.model_name} v{self.model_version}:")
            logger.info(f"  Accuracy: {accuracy}")
            if f1_score is not None:
                logger.info(f"  F1 Score: {f1_score}")
            if precision is not None:
                logger.info(f"  Precision: {precision}")
            if recall is not None:
                logger.info(f"  Recall: {recall}")
            if roc_auc is not None:
                logger.info(f"  ROC AUC: {roc_auc}")
            if additional_metrics:
                for metric_name, metric_value in additional_metrics.items():
                    logger.info(f"  {metric_name}: {metric_value}")

if __name__ == "__main__":
    # Example usage
    collector = ModelMetricsCollector(
        model_name="example_model",
        model_version="1.0.0",
        metrics_store="prometheus",
    )
    
    # Log a prediction
    collector.log_prediction(
        features={"feature1": 1.5, "feature2": 2.7},
        prediction=0.8,
        ground_truth=1,
        latency=0.023,
    )
    
    # Log batch metrics
    collector.log_batch_metrics(
        accuracy=0.92,
        f1_score=0.89,
        precision=0.87,
        recall=0.91,
    ) 