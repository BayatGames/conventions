"""
Model Evaluation Module

This module provides utilities for comprehensive model evaluation.
"""

import os
import json
import logging
from typing import Dict, List, Tuple, Any, Optional, Union, Callable
import pickle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    confusion_matrix, 
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    roc_curve, 
    roc_auc_score, 
    precision_recall_curve, 
    average_precision_score,
    mean_squared_error, 
    mean_absolute_error, 
    r2_score,
    classification_report,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Class for comprehensive model evaluation."""

    def __init__(self, output_dir: str = "./evaluation_results"):
        """
        Initialize the model evaluator.
        
        Args:
            output_dir: Directory to store evaluation results
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info(f"Initialized model evaluator with output directory: {output_dir}")
    
    def evaluate_classifier(
        self,
        model: Any,
        X_test: Union[np.ndarray, pd.DataFrame],
        y_test: Union[np.ndarray, pd.Series],
        class_names: Optional[List[str]] = None,
        threshold: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Evaluate a classification model.
        
        Args:
            model: Trained classification model
            X_test: Test features
            y_test: True labels
            class_names: Names of classes
            threshold: Threshold for binary classification
            
        Returns:
            Dictionary of evaluation metrics and paths to generated plots
        """
        logger.info("Evaluating classification model")
        
        # Get predictions
        try:
            # For models with predict_proba method (most sklearn models)
            y_prob = model.predict_proba(X_test)
            if y_prob.shape[1] == 2:  # Binary classification
                y_prob = y_prob[:, 1]  # Probability of positive class
                y_pred = (y_prob >= threshold).astype(int)
            else:  # Multi-class
                y_pred = np.argmax(y_prob, axis=1)
        except (AttributeError, NotImplementedError):
            # For models without predict_proba
            y_pred = model.predict(X_test)
            y_prob = None
        
        # Determine number of classes
        n_classes = len(np.unique(y_test))
        
        # Set class names if not provided
        if class_names is None:
            class_names = [f"Class {i}" for i in range(n_classes)]
        
        # Calculate metrics
        metrics = {}
        metrics["accuracy"] = accuracy_score(y_test, y_pred)
        
        # Binary classification specific metrics
        if n_classes == 2:
            metrics["precision"] = precision_score(y_test, y_pred)
            metrics["recall"] = recall_score(y_test, y_pred)
            metrics["f1"] = f1_score(y_test, y_pred)
            
            if y_prob is not None:
                metrics["roc_auc"] = roc_auc_score(y_test, y_prob)
                metrics["average_precision"] = average_precision_score(y_test, y_prob)
        
        # Multi-class metrics
        else:
            metrics["precision_macro"] = precision_score(y_test, y_pred, average="macro")
            metrics["recall_macro"] = recall_score(y_test, y_pred, average="macro")
            metrics["f1_macro"] = f1_score(y_test, y_pred, average="macro")
            
            # Per-class metrics
            class_report = classification_report(y_test, y_pred, output_dict=True)
            metrics["classification_report"] = class_report
        
        logger.info(f"Classification metrics: {metrics}")
        
        # Generate plots
        plots = {}
        
        # Confusion matrix
        plots["confusion_matrix"] = self._plot_confusion_matrix(
            y_test, y_pred, class_names
        )
        
        # ROC curve for binary classification
        if n_classes == 2 and y_prob is not None:
            plots["roc_curve"] = self._plot_roc_curve(y_test, y_prob)
            plots["precision_recall_curve"] = self._plot_precision_recall_curve(
                y_test, y_prob
            )
        
        # Save results
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        results = {
            "metrics": metrics,
            "plots": plots,
            "timestamp": timestamp,
        }
        
        # Save metrics to JSON
        metrics_path = os.path.join(
            self.output_dir, f"classification_metrics_{timestamp}.json"
        )
        with open(metrics_path, "w") as f:
            json.dump(
                {k: v for k, v in metrics.items() if isinstance(v, (int, float, str, list))},
                f,
                indent=2,
            )
        
        return results
    
    def evaluate_regressor(
        self,
        model: Any,
        X_test: Union[np.ndarray, pd.DataFrame],
        y_test: Union[np.ndarray, pd.Series],
    ) -> Dict[str, Any]:
        """
        Evaluate a regression model.
        
        Args:
            model: Trained regression model
            X_test: Test features
            y_test: True values
            
        Returns:
            Dictionary of evaluation metrics and paths to generated plots
        """
        logger.info("Evaluating regression model")
        
        # Get predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        metrics = {}
        metrics["mse"] = mean_squared_error(y_test, y_pred)
        metrics["rmse"] = np.sqrt(metrics["mse"])
        metrics["mae"] = mean_absolute_error(y_test, y_pred)
        metrics["r2"] = r2_score(y_test, y_pred)
        
        # Calculate additional metrics
        metrics["median_absolute_error"] = np.median(np.abs(y_test - y_pred))
        metrics["mean_absolute_percentage_error"] = np.mean(
            np.abs((y_test - y_pred) / np.maximum(np.abs(y_test), 1e-10))
        ) * 100
        
        logger.info(f"Regression metrics: {metrics}")
        
        # Generate plots
        plots = {}
        
        # Actual vs Predicted plot
        plots["actual_vs_predicted"] = self._plot_actual_vs_predicted(y_test, y_pred)
        
        # Residual plot
        plots["residuals"] = self._plot_residuals(y_test, y_pred)
        
        # Save results
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        results = {
            "metrics": metrics,
            "plots": plots,
            "timestamp": timestamp,
        }
        
        # Save metrics to JSON
        metrics_path = os.path.join(
            self.output_dir, f"regression_metrics_{timestamp}.json"
        )
        with open(metrics_path, "w") as f:
            json.dump(metrics, f, indent=2)
        
        return results
    
    def _plot_confusion_matrix(
        self,
        y_true: Union[np.ndarray, pd.Series],
        y_pred: np.ndarray,
        class_names: List[str],
    ) -> str:
        """
        Generate and save a confusion matrix plot.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            class_names: Names of classes
            
        Returns:
            Path to the saved plot
        """
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=class_names,
            yticklabels=class_names,
        )
        plt.ylabel("True Label")
        plt.xlabel("Predicted Label")
        plt.title("Confusion Matrix")
        
        # Save the plot
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        plot_path = os.path.join(self.output_dir, f"confusion_matrix_{timestamp}.png")
        plt.savefig(plot_path, bbox_inches="tight")
        plt.close()
        
        return plot_path
    
    def _plot_roc_curve(
        self,
        y_true: Union[np.ndarray, pd.Series],
        y_prob: np.ndarray,
    ) -> str:
        """
        Generate and save a ROC curve plot.
        
        Args:
            y_true: True labels
            y_prob: Predicted probabilities
            
        Returns:
            Path to the saved plot
        """
        fpr, tpr, thresholds = roc_curve(y_true, y_prob)
        roc_auc = roc_auc_score(y_true, y_prob)
        
        plt.figure(figsize=(10, 8))
        plt.plot(
            fpr, tpr, color="darkorange", lw=2, label=f"ROC curve (AUC = {roc_auc:.3f})"
        )
        plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Receiver Operating Characteristic (ROC) Curve")
        plt.legend(loc="lower right")
        
        # Save the plot
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        plot_path = os.path.join(self.output_dir, f"roc_curve_{timestamp}.png")
        plt.savefig(plot_path, bbox_inches="tight")
        plt.close()
        
        return plot_path
    
    def _plot_precision_recall_curve(
        self,
        y_true: Union[np.ndarray, pd.Series],
        y_prob: np.ndarray,
    ) -> str:
        """
        Generate and save a precision-recall curve plot.
        
        Args:
            y_true: True labels
            y_prob: Predicted probabilities
            
        Returns:
            Path to the saved plot
        """
        precision, recall, thresholds = precision_recall_curve(y_true, y_prob)
        average_precision = average_precision_score(y_true, y_prob)
        
        plt.figure(figsize=(10, 8))
        plt.plot(
            recall,
            precision,
            color="blue",
            lw=2,
            label=f"Precision-Recall curve (AP = {average_precision:.3f})",
        )
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title("Precision-Recall Curve")
        plt.legend(loc="lower left")
        
        # Save the plot
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        plot_path = os.path.join(self.output_dir, f"precision_recall_curve_{timestamp}.png")
        plt.savefig(plot_path, bbox_inches="tight")
        plt.close()
        
        return plot_path
    
    def _plot_actual_vs_predicted(
        self,
        y_true: Union[np.ndarray, pd.Series],
        y_pred: np.ndarray,
    ) -> str:
        """
        Generate and save an actual vs predicted values plot.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Path to the saved plot
        """
        plt.figure(figsize=(10, 8))
        plt.scatter(y_true, y_pred, alpha=0.5)
        
        # Plot the perfect prediction line
        min_val = min(np.min(y_true), np.min(y_pred))
        max_val = max(np.max(y_true), np.max(y_pred))
        plt.plot([min_val, max_val], [min_val, max_val], "r--", lw=2)
        
        plt.xlabel("Actual Values")
        plt.ylabel("Predicted Values")
        plt.title("Actual vs Predicted Values")
        
        # Add R² value to the plot
        r2 = r2_score(y_true, y_pred)
        plt.annotate(f"R² = {r2:.3f}", xy=(0.05, 0.95), xycoords="axes fraction")
        
        # Save the plot
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        plot_path = os.path.join(self.output_dir, f"actual_vs_predicted_{timestamp}.png")
        plt.savefig(plot_path, bbox_inches="tight")
        plt.close()
        
        return plot_path
    
    def _plot_residuals(
        self,
        y_true: Union[np.ndarray, pd.Series],
        y_pred: np.ndarray,
    ) -> str:
        """
        Generate and save a residual plot.
        
        Args:
            y_true: True values
            y_pred: Predicted values
            
        Returns:
            Path to the saved plot
        """
        residuals = y_true - y_pred
        
        plt.figure(figsize=(10, 8))
        
        # Scatter plot of predicted values vs residuals
        plt.scatter(y_pred, residuals, alpha=0.5)
        plt.axhline(y=0, color="r", linestyle="--", lw=2)
        
        plt.xlabel("Predicted Values")
        plt.ylabel("Residuals")
        plt.title("Residual Plot")
        
        # Save the plot
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        plot_path = os.path.join(self.output_dir, f"residuals_{timestamp}.png")
        plt.savefig(plot_path, bbox_inches="tight")
        plt.close()
        
        return plot_path
    
    def compare_models(
        self,
        models: Dict[str, Any],
        X_test: Union[np.ndarray, pd.DataFrame],
        y_test: Union[np.ndarray, pd.Series],
        task_type: str = "classification",
    ) -> Dict[str, Any]:
        """
        Compare multiple models on the same test data.
        
        Args:
            models: Dictionary of model names to model objects
            X_test: Test features
            y_test: True labels/values
            task_type: Type of task ('classification' or 'regression')
            
        Returns:
            Dictionary of comparison results and plots
        """
        logger.info(f"Comparing {len(models)} models on {task_type} task")
        
        results = {}
        metrics_comparison = {}
        
        for name, model in models.items():
            logger.info(f"Evaluating model: {name}")
            
            if task_type == "classification":
                model_results = self.evaluate_classifier(model, X_test, y_test)
                metrics_comparison[name] = model_results["metrics"]
            else:
                model_results = self.evaluate_regressor(model, X_test, y_test)
                metrics_comparison[name] = model_results["metrics"]
            
            results[name] = model_results
        
        # Create comparison plots
        plots = {}
        
        # Bar plot of key metrics
        key_metrics = (
            ["accuracy", "precision", "recall", "f1"]
            if task_type == "classification"
            else ["mse", "mae", "r2"]
        )
        
        plots["metrics_comparison"] = self._plot_metrics_comparison(
            metrics_comparison, key_metrics
        )
        
        # Save comparison results
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        comparison_path = os.path.join(
            self.output_dir, f"model_comparison_{timestamp}.json"
        )
        
        # Extract only serializable metrics
        serializable_metrics = {}
        for model_name, model_metrics in metrics_comparison.items():
            serializable_metrics[model_name] = {
                k: v for k, v in model_metrics.items() 
                if isinstance(v, (int, float, str, list))
            }
        
        with open(comparison_path, "w") as f:
            json.dump(serializable_metrics, f, indent=2)
        
        return {
            "model_results": results,
            "comparison_plots": plots,
            "comparison_file": comparison_path,
        }
    
    def _plot_metrics_comparison(
        self,
        metrics_comparison: Dict[str, Dict[str, float]],
        key_metrics: List[str],
    ) -> str:
        """
        Generate and save a bar plot comparing key metrics across models.
        
        Args:
            metrics_comparison: Dictionary of model names to metrics
            key_metrics: List of metrics to include in the comparison
            
        Returns:
            Path to the saved plot
        """
        # Filter metrics to include only those that exist for all models
        valid_metrics = []
        for metric in key_metrics:
            if all(metric in model_metrics for model_metrics in metrics_comparison.values()):
                valid_metrics.append(metric)
        
        if not valid_metrics:
            logger.warning("No common metrics found for comparison")
            return None
        
        # Create a DataFrame for plotting
        data = []
        for model_name, model_metrics in metrics_comparison.items():
            for metric in valid_metrics:
                data.append({
                    "Model": model_name,
                    "Metric": metric,
                    "Value": model_metrics[metric],
                })
        
        df = pd.DataFrame(data)
        
        # Create the plot
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x="Metric", y="Value", hue="Model", data=df)
        
        plt.title("Model Comparison")
        plt.xlabel("Metric")
        plt.ylabel("Value")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the plot
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        plot_path = os.path.join(self.output_dir, f"metrics_comparison_{timestamp}.png")
        plt.savefig(plot_path, bbox_inches="tight")
        plt.close()
        
        return plot_path


if __name__ == "__main__":
    # Example usage
    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    
    # Load sample data
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Train models
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    lr = LogisticRegression(multi_class="auto", solver="lbfgs", random_state=42)
    
    rf.fit(X_train, y_train)
    lr.fit(X_train, y_train)
    
    # Create evaluator
    evaluator = ModelEvaluator()
    
    # Compare models
    comparison = evaluator.compare_models(
        {"Random Forest": rf, "Logistic Regression": lr},
        X_test,
        y_test,
        task_type="classification",
    )
    
    print("Comparison results saved to:", comparison["comparison_file"]) 