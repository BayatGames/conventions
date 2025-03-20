"""
Model Trainer Module

This module provides utilities for training machine learning models with 
experiment tracking and hyperparameter optimization.
"""

import os
import json
import logging
import pickle
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional, Union, Callable

import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn
import mlflow.tensorflow
import mlflow.pytorch
import optuna
from optuna.integration.mlflow import MLflowCallback
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.base import BaseEstimator
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import tensorflow as tf
import torch

# Import the model factory
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.model_factory import ModelFactory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """Class for training machine learning models with experiment tracking."""

    def __init__(
        self,
        experiment_name: str,
        model_type: str,
        model_config: Dict[str, Any],
        tracking_uri: Optional[str] = None,
        artifacts_dir: str = "./artifacts",
    ):
        """
        Initialize the model trainer.
        
        Args:
            experiment_name: Name of the MLflow experiment
            model_type: Type of model to train (e.g., random_forest, neural_network)
            model_config: Configuration parameters for the model
            tracking_uri: MLflow tracking URI
            artifacts_dir: Directory to store model artifacts
        """
        self.experiment_name = experiment_name
        self.model_type = model_type
        self.model_config = model_config
        self.artifacts_dir = artifacts_dir
        
        # Create artifacts directory if it doesn't exist
        os.makedirs(artifacts_dir, exist_ok=True)
        
        # Configure MLflow
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)
        
        mlflow.set_experiment(experiment_name)
        logger.info(f"Initialized model trainer for experiment: {experiment_name}")
        
        # Initialize model
        self.model = None
        self.is_neural_network = model_type in ["neural_network", "cnn", "lstm"]
        
    def prepare_data(
        self,
        X: Union[np.ndarray, pd.DataFrame],
        y: Union[np.ndarray, pd.Series],
        test_size: float = 0.2,
        val_size: float = 0.1,
        random_state: int = 42,
    ) -> Dict[str, Any]:
        """
        Split data into training, validation, and test sets.
        
        Args:
            X: Features
            y: Target
            test_size: Proportion of data for test set
            val_size: Proportion of train data for validation set
            random_state: Random seed for reproducibility
            
        Returns:
            Dictionary containing train, validation, and test splits
        """
        logger.info("Preparing data splits")
        
        # First split off test set
        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Then split training set into train and validation
        val_ratio = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val, y_train_val, test_size=val_ratio, random_state=random_state
        )
        
        # Determine input shape for neural networks
        if isinstance(X, np.ndarray):
            input_shape = X.shape[1:]
        else:
            input_shape = (X.shape[1],)
        
        # Determine num_classes for classification tasks
        if len(np.unique(y)) <= 10:  # Assume classification if few unique values
            num_classes = len(np.unique(y))
            task_type = "classification"
        else:
            num_classes = None
            task_type = "regression"
        
        logger.info(f"Data prepared: X_train.shape={X_train.shape}, y_train.shape={y_train.shape}")
        
        return {
            "X_train": X_train,
            "y_train": y_train,
            "X_val": X_val,
            "y_val": y_val,
            "X_test": X_test,
            "y_test": y_test,
            "input_shape": input_shape,
            "num_classes": num_classes,
            "task_type": task_type,
        }

    def train(
        self,
        data: Dict[str, Any],
        epochs: int = 10,
        batch_size: int = 32,
        early_stopping: bool = True,
        patience: int = 5,
    ) -> Any:
        """
        Train the model.
        
        Args:
            data: Dictionary containing train, validation, and test splits
            epochs: Number of training epochs for neural networks
            batch_size: Batch size for neural networks
            early_stopping: Whether to use early stopping for neural networks
            patience: Patience for early stopping
            
        Returns:
            Trained model
        """
        with mlflow.start_run() as run:
            run_id = run.info.run_id
            logger.info(f"Started MLflow run: {run_id}")
            
            # Log model configuration
            mlflow.log_params(self.model_config)
            mlflow.log_param("model_type", self.model_type)
            
            # Create model
            model = ModelFactory.create_model(
                self.model_type,
                self.model_config,
                input_shape=data.get("input_shape"),
                num_classes=data.get("num_classes"),
            )
            
            # Train the model
            if self.is_neural_network:
                # Set up callbacks for TensorFlow models
                callbacks = []
                if early_stopping:
                    early_stop = tf.keras.callbacks.EarlyStopping(
                        monitor="val_loss",
                        patience=patience,
                        restore_best_weights=True,
                    )
                    callbacks.append(early_stop)
                
                # Add MLflow callback for TensorFlow
                mlflow_callback = tf.keras.callbacks.LambdaCallback(
                    on_epoch_end=lambda epoch, logs: mlflow.log_metrics(logs, step=epoch)
                )
                callbacks.append(mlflow_callback)
                
                # Train neural network
                logger.info(f"Training {self.model_type} for {epochs} epochs")
                history = model.fit(
                    data["X_train"], data["y_train"],
                    epochs=epochs,
                    batch_size=batch_size,
                    validation_data=(data["X_val"], data["y_val"]),
                    callbacks=callbacks,
                    verbose=1,
                )
                
                # Log training metrics
                for metric in history.history:
                    for epoch, value in enumerate(history.history[metric]):
                        mlflow.log_metric(metric, value, step=epoch)
            else:
                # Train classical ML model
                logger.info(f"Training {self.model_type}")
                model.fit(data["X_train"], data["y_train"])
                
                # Log training metrics for classical ML models
                if data["task_type"] == "classification":
                    train_preds = model.predict(data["X_train"])
                    val_preds = model.predict(data["X_val"])
                    
                    train_acc = accuracy_score(data["y_train"], train_preds)
                    val_acc = accuracy_score(data["y_val"], val_preds)
                    
                    mlflow.log_metric("train_accuracy", train_acc)
                    mlflow.log_metric("val_accuracy", val_acc)
                    
                    # Log additional metrics for binary classification
                    if data["num_classes"] == 2:
                        train_precision = precision_score(data["y_train"], train_preds)
                        train_recall = recall_score(data["y_train"], train_preds)
                        train_f1 = f1_score(data["y_train"], train_preds)
                        
                        val_precision = precision_score(data["y_val"], val_preds)
                        val_recall = recall_score(data["y_val"], val_preds)
                        val_f1 = f1_score(data["y_val"], val_preds)
                        
                        mlflow.log_metrics({
                            "train_precision": train_precision,
                            "train_recall": train_recall,
                            "train_f1": train_f1,
                            "val_precision": val_precision,
                            "val_recall": val_recall,
                            "val_f1": val_f1,
                        })
                else:
                    # Regression metrics
                    train_preds = model.predict(data["X_train"])
                    val_preds = model.predict(data["X_val"])
                    
                    train_mse = mean_squared_error(data["y_train"], train_preds)
                    train_mae = mean_absolute_error(data["y_train"], train_preds)
                    train_r2 = r2_score(data["y_train"], train_preds)
                    
                    val_mse = mean_squared_error(data["y_val"], val_preds)
                    val_mae = mean_absolute_error(data["y_val"], val_preds)
                    val_r2 = r2_score(data["y_val"], val_preds)
                    
                    mlflow.log_metrics({
                        "train_mse": train_mse,
                        "train_mae": train_mae,
                        "train_r2": train_r2,
                        "val_mse": val_mse,
                        "val_mae": val_mae,
                        "val_r2": val_r2,
                    })
            
            # Save the model
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_path = os.path.join(
                self.artifacts_dir, f"{self.model_type}_{timestamp}"
            )
            
            # Log model to MLflow
            if self.is_neural_network:
                mlflow.tensorflow.log_model(model, "model")
                # Save model locally
                model.save(model_path)
            else:
                mlflow.sklearn.log_model(model, "model")
                # Save model locally
                with open(f"{model_path}.pkl", "wb") as f:
                    pickle.dump(model, f)
            
            logger.info(f"Model saved to {model_path}")
            
            # Save run ID
            self.run_id = run_id
            self.model = model
            
            return model
    
    def evaluate(self, data: Dict[str, Any]) -> Dict[str, float]:
        """
        Evaluate the model on test data.
        
        Args:
            data: Dictionary containing data splits
            
        Returns:
            Dictionary of evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet")
        
        logger.info("Evaluating model on test data")
        
        # Generate predictions
        y_pred = self.model.predict(data["X_test"])
        
        # Calculate metrics based on task type
        metrics = {}
        if data["task_type"] == "classification":
            metrics["test_accuracy"] = accuracy_score(data["y_test"], y_pred)
            
            if data["num_classes"] == 2:
                metrics["test_precision"] = precision_score(data["y_test"], y_pred)
                metrics["test_recall"] = recall_score(data["y_test"], y_pred)
                metrics["test_f1"] = f1_score(data["y_test"], y_pred)
        else:
            # Regression metrics
            metrics["test_mse"] = mean_squared_error(data["y_test"], y_pred)
            metrics["test_mae"] = mean_absolute_error(data["y_test"], y_pred)
            metrics["test_r2"] = r2_score(data["y_test"], y_pred)
        
        # Log metrics to MLflow
        with mlflow.start_run(run_id=self.run_id):
            mlflow.log_metrics(metrics)
        
        logger.info(f"Evaluation metrics: {metrics}")
        return metrics
    
    def hyperparameter_tuning(
        self,
        data: Dict[str, Any],
        param_space: Dict[str, Any],
        n_trials: int = 10,
        cv: int = 3,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Perform hyperparameter tuning using Optuna.
        
        Args:
            data: Dictionary containing data splits
            param_space: Parameter space to search
            n_trials: Number of trials
            cv: Number of cross-validation folds
            timeout: Timeout in seconds
            
        Returns:
            Best hyperparameters
        """
        logger.info(f"Starting hyperparameter tuning with {n_trials} trials")
        
        # Define the objective function for Optuna
        def objective(trial):
            # Sample hyperparameters from the parameter space
            params = {}
            for param_name, param_config in param_space.items():
                if param_config["type"] == "categorical":
                    params[param_name] = trial.suggest_categorical(
                        param_name, param_config["values"]
                    )
                elif param_config["type"] == "int":
                    params[param_name] = trial.suggest_int(
                        param_name, 
                        param_config["low"], 
                        param_config["high"],
                        step=param_config.get("step", 1)
                    )
                elif param_config["type"] == "float":
                    params[param_name] = trial.suggest_float(
                        param_name,
                        param_config["low"],
                        param_config["high"],
                        log=param_config.get("log", False)
                    )
            
            # Create model with sampled hyperparameters
            model_config = {**self.model_config, **params}
            model = ModelFactory.create_model(
                self.model_type,
                model_config,
                input_shape=data.get("input_shape"),
                num_classes=data.get("num_classes"),
            )
            
            # For neural networks, we'll use a simplified training process
            if self.is_neural_network:
                # Simple train/validation split evaluation for neural networks
                model.fit(
                    data["X_train"], data["y_train"],
                    epochs=5,  # Use fewer epochs for tuning
                    batch_size=32,
                    validation_data=(data["X_val"], data["y_val"]),
                    verbose=0,
                )
                
                # Evaluate on validation set
                val_loss = model.evaluate(data["X_val"], data["y_val"], verbose=0)[0]
                return val_loss
            else:
                # Use cross-validation for traditional ML models
                if data["task_type"] == "classification":
                    scores = cross_val_score(
                        model, 
                        data["X_train"], 
                        data["y_train"],
                        cv=cv,
                        scoring="accuracy"
                    )
                    return -scores.mean()  # Negative because Optuna minimizes
                else:
                    scores = cross_val_score(
                        model, 
                        data["X_train"], 
                        data["y_train"],
                        cv=cv,
                        scoring="neg_mean_squared_error"
                    )
                    return -scores.mean()  # Negative because Optuna minimizes
        
        # Set up MLflow callback for Optuna
        mlflow_callback = MLflowCallback(
            tracking_uri=mlflow.get_tracking_uri(),
            metric_name="tuning_metric",
        )
        
        # Create and run the study
        study = optuna.create_study(direction="minimize")
        study.optimize(
            objective, 
            n_trials=n_trials,
            timeout=timeout,
            callbacks=[mlflow_callback]
        )
        
        # Get best parameters
        best_params = study.best_params
        logger.info(f"Best hyperparameters: {best_params}")
        
        # Update model config with best parameters
        self.model_config.update(best_params)
        
        return best_params
    
    def save_model_config(self, config_path: str) -> None:
        """
        Save the model configuration to a file.
        
        Args:
            config_path: Path to save the configuration
        """
        config = {
            "model_type": self.model_type,
            "model_config": self.model_config,
            "mlflow_run_id": getattr(self, "run_id", None),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Model configuration saved to {config_path}")
    
    @classmethod
    def load_from_config(
        cls, config_path: str, artifacts_dir: str = "./artifacts"
    ) -> "ModelTrainer":
        """
        Load a model trainer from a configuration file.
        
        Args:
            config_path: Path to the configuration file
            artifacts_dir: Directory containing model artifacts
            
        Returns:
            ModelTrainer instance
        """
        with open(config_path, "r") as f:
            config = json.load(f)
        
        trainer = cls(
            experiment_name=config.get("experiment_name", "default"),
            model_type=config["model_type"],
            model_config=config["model_config"],
            artifacts_dir=artifacts_dir,
        )
        
        if "mlflow_run_id" in config:
            trainer.run_id = config["mlflow_run_id"]
            
            # Load the model from MLflow
            logged_model = f"runs:/{trainer.run_id}/model"
            if trainer.is_neural_network:
                trainer.model = mlflow.tensorflow.load_model(logged_model)
            else:
                trainer.model = mlflow.sklearn.load_model(logged_model)
        
        logger.info(f"Loaded model trainer from {config_path}")
        return trainer


if __name__ == "__main__":
    # Example usage
    from sklearn.datasets import load_iris
    
    # Load sample data
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Define model configuration
    model_config = {
        "hidden_layers": [64, 32],
        "activation": "relu",
        "dropout_rate": 0.2,
    }
    
    # Create model trainer
    trainer = ModelTrainer(
        experiment_name="iris_classification",
        model_type="neural_network",
        model_config=model_config,
    )
    
    # Prepare data
    data = trainer.prepare_data(X, y)
    
    # Train model
    trainer.train(data, epochs=50)
    
    # Evaluate model
    metrics = trainer.evaluate(data)
    print("Evaluation metrics:", metrics)
    
    # Save model configuration
    trainer.save_model_config("config/iris_model_config.json") 