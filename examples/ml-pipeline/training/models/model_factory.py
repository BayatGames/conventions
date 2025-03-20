"""
Model Factory Module

This module provides a factory for creating different machine learning models.
"""

import logging
from typing import Dict, Any, List, Tuple, Optional, Union, Callable

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
import xgboost as xgb

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ModelFactory:
    """Factory for creating different types of machine learning models."""

    @staticmethod
    def create_model(
        model_type: str, 
        model_config: Dict[str, Any],
        input_shape: Optional[Tuple] = None,
        num_classes: Optional[int] = None
    ) -> Union[BaseEstimator, tf.keras.Model]:
        """
        Create a model based on the specified type and configuration.
        
        Args:
            model_type: Type of model to create
            model_config: Configuration parameters for the model
            input_shape: Shape of input features (for neural networks)
            num_classes: Number of output classes (for classification)
            
        Returns:
            A machine learning model instance
        """
        if model_type == "random_forest":
            return ModelFactory.create_random_forest(model_config)
        elif model_type == "logistic_regression":
            return ModelFactory.create_logistic_regression(model_config)
        elif model_type == "linear_regression":
            return ModelFactory.create_linear_regression(model_config)
        elif model_type == "gradient_boosting":
            return ModelFactory.create_gradient_boosting(model_config)
        elif model_type == "xgboost":
            return ModelFactory.create_xgboost(model_config)
        elif model_type == "neural_network":
            return ModelFactory.create_neural_network(model_config, input_shape, num_classes)
        elif model_type == "cnn":
            return ModelFactory.create_cnn(model_config, input_shape, num_classes)
        elif model_type == "lstm":
            return ModelFactory.create_lstm(model_config, input_shape, num_classes)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    @staticmethod
    def create_random_forest(config: Dict[str, Any]) -> RandomForestClassifier:
        """
        Create a random forest model.
        
        Args:
            config: Model configuration
            
        Returns:
            RandomForestClassifier instance
        """
        params = {
            "n_estimators": config.get("n_estimators", 100),
            "max_depth": config.get("max_depth"),
            "min_samples_split": config.get("min_samples_split", 2),
            "min_samples_leaf": config.get("min_samples_leaf", 1),
            "random_state": config.get("random_state", 42),
            "n_jobs": config.get("n_jobs", -1),
        }
        
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        logger.info(f"Creating RandomForestClassifier with params: {params}")
        return RandomForestClassifier(**params)
    
    @staticmethod
    def create_logistic_regression(config: Dict[str, Any]) -> LogisticRegression:
        """
        Create a logistic regression model.
        
        Args:
            config: Model configuration
            
        Returns:
            LogisticRegression instance
        """
        params = {
            "C": config.get("C", 1.0),
            "penalty": config.get("penalty", "l2"),
            "solver": config.get("solver", "lbfgs"),
            "max_iter": config.get("max_iter", 100),
            "random_state": config.get("random_state", 42),
            "n_jobs": config.get("n_jobs", -1),
        }
        
        logger.info(f"Creating LogisticRegression with params: {params}")
        return LogisticRegression(**params)
    
    @staticmethod
    def create_linear_regression(config: Dict[str, Any]) -> LinearRegression:
        """
        Create a linear regression model.
        
        Args:
            config: Model configuration
            
        Returns:
            LinearRegression instance
        """
        params = {
            "fit_intercept": config.get("fit_intercept", True),
            "n_jobs": config.get("n_jobs", -1),
        }
        
        logger.info(f"Creating LinearRegression with params: {params}")
        return LinearRegression(**params)
    
    @staticmethod
    def create_gradient_boosting(config: Dict[str, Any]) -> GradientBoostingRegressor:
        """
        Create a gradient boosting regressor.
        
        Args:
            config: Model configuration
            
        Returns:
            GradientBoostingRegressor instance
        """
        params = {
            "n_estimators": config.get("n_estimators", 100),
            "learning_rate": config.get("learning_rate", 0.1),
            "max_depth": config.get("max_depth", 3),
            "min_samples_split": config.get("min_samples_split", 2),
            "min_samples_leaf": config.get("min_samples_leaf", 1),
            "random_state": config.get("random_state", 42),
        }
        
        logger.info(f"Creating GradientBoostingRegressor with params: {params}")
        return GradientBoostingRegressor(**params)
    
    @staticmethod
    def create_xgboost(config: Dict[str, Any]) -> xgb.XGBModel:
        """
        Create an XGBoost model.
        
        Args:
            config: Model configuration
            
        Returns:
            XGBoost model instance
        """
        params = {
            "n_estimators": config.get("n_estimators", 100),
            "learning_rate": config.get("learning_rate", 0.1),
            "max_depth": config.get("max_depth", 3),
            "subsample": config.get("subsample", 1.0),
            "colsample_bytree": config.get("colsample_bytree", 1.0),
            "objective": config.get("objective", "reg:squarederror"),
            "random_state": config.get("random_state", 42),
            "n_jobs": config.get("n_jobs", -1),
        }
        
        if config.get("task_type") == "classification":
            if config.get("num_classes", 2) > 2:
                params["objective"] = "multi:softprob"
                params["num_class"] = config.get("num_classes")
            else:
                params["objective"] = "binary:logistic"
                
            logger.info(f"Creating XGBClassifier with params: {params}")
            return xgb.XGBClassifier(**params)
        else:
            logger.info(f"Creating XGBRegressor with params: {params}")
            return xgb.XGBRegressor(**params)
    
    @staticmethod
    def create_neural_network(
        config: Dict[str, Any],
        input_shape: Tuple,
        num_classes: Optional[int] = None
    ) -> tf.keras.Model:
        """
        Create a simple neural network.
        
        Args:
            config: Model configuration
            input_shape: Shape of input features
            num_classes: Number of output classes (None for regression)
            
        Returns:
            Keras neural network
        """
        if input_shape is None:
            raise ValueError("input_shape must be provided for neural networks")
        
        hidden_layers = config.get("hidden_layers", [64, 32])
        activation = config.get("activation", "relu")
        dropout_rate = config.get("dropout_rate", 0.2)
        
        model = models.Sequential()
        
        # Input layer
        model.add(layers.InputLayer(input_shape=input_shape))
        
        # Hidden layers
        for units in hidden_layers:
            model.add(layers.Dense(units, activation=activation))
            if dropout_rate > 0:
                model.add(layers.Dropout(dropout_rate))
        
        # Output layer
        if num_classes is not None:
            if num_classes == 2:
                model.add(layers.Dense(1, activation="sigmoid"))
            else:
                model.add(layers.Dense(num_classes, activation="softmax"))
        else:
            model.add(layers.Dense(1))  # Regression
        
        # Compile model
        optimizer_config = config.get("optimizer", {"type": "adam", "learning_rate": 0.001})
        optimizer_type = optimizer_config.get("type", "adam")
        learning_rate = optimizer_config.get("learning_rate", 0.001)
        
        if optimizer_type == "adam":
            optimizer = optimizers.Adam(learning_rate=learning_rate)
        elif optimizer_type == "sgd":
            optimizer = optimizers.SGD(learning_rate=learning_rate)
        elif optimizer_type == "rmsprop":
            optimizer = optimizers.RMSprop(learning_rate=learning_rate)
        else:
            raise ValueError(f"Unsupported optimizer: {optimizer_type}")
        
        if num_classes is not None:
            if num_classes == 2:
                loss = "binary_crossentropy"
                metrics = ["accuracy"]
            else:
                loss = "sparse_categorical_crossentropy"
                metrics = ["accuracy"]
        else:
            loss = "mse"
            metrics = ["mae"]
        
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        
        logger.info(f"Created neural network with {len(hidden_layers)} hidden layers")
        return model
    
    @staticmethod
    def create_cnn(
        config: Dict[str, Any],
        input_shape: Tuple,
        num_classes: Optional[int] = None
    ) -> tf.keras.Model:
        """
        Create a convolutional neural network.
        
        Args:
            config: Model configuration
            input_shape: Shape of input images (height, width, channels)
            num_classes: Number of output classes (None for regression)
            
        Returns:
            Keras CNN
        """
        if input_shape is None or len(input_shape) != 3:
            raise ValueError("input_shape must be a 3D tuple (height, width, channels) for CNNs")
        
        filters = config.get("filters", [32, 64, 128])
        kernel_sizes = config.get("kernel_sizes", [3, 3, 3])
        pool_sizes = config.get("pool_sizes", [2, 2, 2])
        dense_layers = config.get("dense_layers", [128])
        activation = config.get("activation", "relu")
        dropout_rate = config.get("dropout_rate", 0.2)
        
        model = models.Sequential()
        
        # Input layer
        model.add(layers.InputLayer(input_shape=input_shape))
        
        # Convolutional layers
        for i, (f, k, p) in enumerate(zip(filters, kernel_sizes, pool_sizes)):
            model.add(layers.Conv2D(f, (k, k), activation=activation, padding="same"))
            model.add(layers.MaxPooling2D((p, p)))
        
        # Flatten before dense layers
        model.add(layers.Flatten())
        
        # Dense layers
        for units in dense_layers:
            model.add(layers.Dense(units, activation=activation))
            if dropout_rate > 0:
                model.add(layers.Dropout(dropout_rate))
        
        # Output layer
        if num_classes is not None:
            if num_classes == 2:
                model.add(layers.Dense(1, activation="sigmoid"))
            else:
                model.add(layers.Dense(num_classes, activation="softmax"))
        else:
            model.add(layers.Dense(1))  # Regression
        
        # Compile the model
        optimizer_config = config.get("optimizer", {"type": "adam", "learning_rate": 0.001})
        optimizer_type = optimizer_config.get("type", "adam")
        learning_rate = optimizer_config.get("learning_rate", 0.001)
        
        if optimizer_type == "adam":
            optimizer = optimizers.Adam(learning_rate=learning_rate)
        elif optimizer_type == "sgd":
            optimizer = optimizers.SGD(learning_rate=learning_rate)
        elif optimizer_type == "rmsprop":
            optimizer = optimizers.RMSprop(learning_rate=learning_rate)
        else:
            raise ValueError(f"Unsupported optimizer: {optimizer_type}")
        
        if num_classes is not None:
            if num_classes == 2:
                loss = "binary_crossentropy"
                metrics = ["accuracy"]
            else:
                loss = "sparse_categorical_crossentropy"
                metrics = ["accuracy"]
        else:
            loss = "mse"
            metrics = ["mae"]
        
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        
        logger.info(f"Created CNN with {len(filters)} convolutional layers")
        return model
    
    @staticmethod
    def create_lstm(
        config: Dict[str, Any],
        input_shape: Tuple,
        num_classes: Optional[int] = None
    ) -> tf.keras.Model:
        """
        Create an LSTM model for sequence data.
        
        Args:
            config: Model configuration
            input_shape: Shape of input sequences (timesteps, features)
            num_classes: Number of output classes (None for regression)
            
        Returns:
            Keras LSTM model
        """
        if input_shape is None or len(input_shape) != 2:
            raise ValueError("input_shape must be a 2D tuple (timesteps, features) for LSTMs")
        
        lstm_units = config.get("lstm_units", [64, 32])
        dense_layers = config.get("dense_layers", [32])
        activation = config.get("activation", "relu")
        dropout_rate = config.get("dropout_rate", 0.2)
        
        model = models.Sequential()
        
        # Input layer
        model.add(layers.InputLayer(input_shape=input_shape))
        
        # LSTM layers
        for i, units in enumerate(lstm_units):
            return_sequences = i < len(lstm_units) - 1
            model.add(layers.LSTM(units, return_sequences=return_sequences))
            if dropout_rate > 0:
                model.add(layers.Dropout(dropout_rate))
        
        # Dense layers
        for units in dense_layers:
            model.add(layers.Dense(units, activation=activation))
            if dropout_rate > 0:
                model.add(layers.Dropout(dropout_rate))
        
        # Output layer
        if num_classes is not None:
            if num_classes == 2:
                model.add(layers.Dense(1, activation="sigmoid"))
            else:
                model.add(layers.Dense(num_classes, activation="softmax"))
        else:
            model.add(layers.Dense(1))  # Regression
        
        # Compile the model
        optimizer_config = config.get("optimizer", {"type": "adam", "learning_rate": 0.001})
        optimizer_type = optimizer_config.get("type", "adam")
        learning_rate = optimizer_config.get("learning_rate", 0.001)
        
        if optimizer_type == "adam":
            optimizer = optimizers.Adam(learning_rate=learning_rate)
        elif optimizer_type == "sgd":
            optimizer = optimizers.SGD(learning_rate=learning_rate)
        elif optimizer_type == "rmsprop":
            optimizer = optimizers.RMSprop(learning_rate=learning_rate)
        else:
            raise ValueError(f"Unsupported optimizer: {optimizer_type}")
        
        if num_classes is not None:
            if num_classes == 2:
                loss = "binary_crossentropy"
                metrics = ["accuracy"]
            else:
                loss = "sparse_categorical_crossentropy"
                metrics = ["accuracy"]
        else:
            loss = "mse"
            metrics = ["mae"]
        
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        
        logger.info(f"Created LSTM with {len(lstm_units)} LSTM layers")
        return model


if __name__ == "__main__":
    # Example usage
    # Create a random forest classifier
    rf_config = {
        "n_estimators": 100,
        "max_depth": 10,
        "random_state": 42
    }
    rf_model = ModelFactory.create_model("random_forest", rf_config)
    
    # Create a neural network for classification
    nn_config = {
        "hidden_layers": [128, 64],
        "activation": "relu",
        "dropout_rate": 0.3,
        "optimizer": {
            "type": "adam",
            "learning_rate": 0.001
        }
    }
    nn_model = ModelFactory.create_model(
        "neural_network", 
        nn_config, 
        input_shape=(10,),  # 10 features
        num_classes=3       # 3 classes
    )
    
    print(nn_model.summary()) 