"""
Model Serving API

This module provides a FastAPI application for serving machine learning models.
"""

import os
import sys
import json
import logging
import pickle
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

import numpy as np
import pandas as pd
import mlflow
import mlflow.pyfunc
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import uvicorn
from prometheus_client import Counter, Histogram, start_http_server

# Configure path to access feature transformer
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from features.transformers.feature_transformer import FeatureTransformer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize metrics
PREDICTION_COUNT = Counter("predictions_total", "Total number of predictions", ["model", "status"])
PREDICTION_LATENCY = Histogram(
    "prediction_latency_seconds", "Prediction latency in seconds", ["model"]
)
FEATURE_COUNT = Counter("feature_count", "Number of features used for prediction", ["model"])

# Create FastAPI app
app = FastAPI(
    title="ML Model API",
    description="API for serving machine learning models",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configuration
class ModelConfig:
    """Configuration for model serving."""

    def __init__(self, config_path: str):
        """
        Initialize configuration from a JSON file.
        
        Args:
            config_path: Path to configuration JSON file
        """
        with open(config_path, "r") as f:
            config = json.load(f)
        
        self.model_registry = config.get("model_registry", "./model_registry")
        self.models = config.get("models", {})
        self.default_model = config.get("default_model")
        self.feature_transformer_path = config.get("feature_transformer_path")
        self.mlflow_tracking_uri = config.get("mlflow_tracking_uri")
        
        # Set MLflow tracking URI if provided
        if self.mlflow_tracking_uri:
            mlflow.set_tracking_uri(self.mlflow_tracking_uri)
        
        logger.info(f"Loaded configuration from {config_path}")


# Initialize configuration
try:
    config = ModelConfig("config/model_serving_config.json")
except Exception as e:
    # Use default configuration if file is not found
    logger.warning(f"Could not load configuration: {e}. Using default configuration.")
    config = ModelConfig.__new__(ModelConfig)
    config.model_registry = "./model_registry"
    config.models = {}
    config.default_model = None
    config.feature_transformer_path = None
    config.mlflow_tracking_uri = None


# Load models and transformers
loaded_models = {}
feature_transformer = None


def load_model(model_name: str) -> Any:
    """
    Load a model by name.
    
    Args:
        model_name: Name of the model to load
        
    Returns:
        Loaded model
        
    Raises:
        HTTPException: If model is not found
    """
    if model_name in loaded_models:
        return loaded_models[model_name]
    
    if model_name not in config.models:
        raise HTTPException(
            status_code=404, 
            detail=f"Model '{model_name}' not found in configuration"
        )
    
    model_config = config.models[model_name]
    model_type = model_config.get("type", "mlflow")
    
    try:
        if model_type == "mlflow":
            # Load from MLflow
            run_id = model_config.get("run_id")
            if not run_id:
                raise ValueError("run_id is required for MLflow models")
            
            model_uri = f"runs:/{run_id}/model"
            model = mlflow.pyfunc.load_model(model_uri)
        
        elif model_type == "pickle":
            # Load from pickle file
            model_path = model_config.get("path")
            if not model_path:
                raise ValueError("path is required for pickle models")
            
            with open(model_path, "rb") as f:
                model = pickle.load(f)
        
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        # Store for future use
        loaded_models[model_name] = model
        logger.info(f"Loaded model '{model_name}'")
        
        return model
    
    except Exception as e:
        logger.error(f"Error loading model '{model_name}': {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading model: {str(e)}"
        )


def get_feature_transformer() -> Optional[FeatureTransformer]:
    """
    Get the feature transformer.
    
    Returns:
        Feature transformer instance or None if not configured
    """
    global feature_transformer
    
    if feature_transformer is not None:
        return feature_transformer
    
    if config.feature_transformer_path:
        try:
            feature_transformer = FeatureTransformer.load(config.feature_transformer_path)
            logger.info(f"Loaded feature transformer from {config.feature_transformer_path}")
            return feature_transformer
        except Exception as e:
            logger.error(f"Error loading feature transformer: {e}")
    
    return None


def get_default_model() -> Any:
    """
    Get the default model for predictions.
    
    Returns:
        Default model
        
    Raises:
        HTTPException: If no default model is configured
    """
    if not config.default_model:
        raise HTTPException(
            status_code=500, 
            detail="No default model configured"
        )
    
    return load_model(config.default_model)


# Pydantic models for API
class PredictionFeatures(BaseModel):
    """Model for prediction feature data."""
    
    features: Dict[str, Any] = Field(..., description="Feature values as key-value pairs")


class PredictionRequest(BaseModel):
    """Model for prediction request."""
    
    data: List[PredictionFeatures] = Field(..., description="List of instances to predict")
    model: Optional[str] = Field(None, description="Model to use for prediction")
    
    @validator("data")
    def validate_data_not_empty(cls, v):
        if not v:
            raise ValueError("data cannot be empty")
        return v


class PredictionResponse(BaseModel):
    """Model for prediction response."""
    
    predictions: List[Any] = Field(..., description="Predicted values")
    model: str = Field(..., description="Model used for prediction")
    prediction_time: float = Field(..., description="Time taken for prediction in seconds")
    timestamp: str = Field(..., description="Timestamp of prediction")


# API routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ML Model API",
        "docs_url": "/docs",
        "available_models": list(config.models.keys()),
        "default_model": config.default_model,
    }


@app.get("/models")
async def list_models():
    """List available models."""
    models_info = {}
    
    for name, model_config in config.models.items():
        models_info[name] = {
            "description": model_config.get("description", ""),
            "version": model_config.get("version", ""),
            "type": model_config.get("type", ""),
            "is_default": name == config.default_model,
            "features": model_config.get("features", []),
        }
    
    return {"models": models_info}


@app.get("/models/{model_name}")
async def get_model_info(model_name: str):
    """Get information about a specific model."""
    if model_name not in config.models:
        raise HTTPException(
            status_code=404, 
            detail=f"Model '{model_name}' not found"
        )
    
    model_config = config.models[model_name]
    return {
        "name": model_name,
        "description": model_config.get("description", ""),
        "version": model_config.get("version", ""),
        "type": model_config.get("type", ""),
        "is_default": model_name == config.default_model,
        "features": model_config.get("features", []),
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    background_tasks: BackgroundTasks,
):
    """
    Make predictions using a model.
    
    Args:
        request: Prediction request
        background_tasks: FastAPI background tasks
        
    Returns:
        Prediction response
    """
    start_time = datetime.now()
    model_name = request.model or config.default_model
    
    if not model_name:
        raise HTTPException(
            status_code=400, 
            detail="No model specified and no default model configured"
        )
    
    try:
        # Load model
        model = load_model(model_name)
        
        # Process input data
        data = []
        for item in request.data:
            data.append(item.features)
        
        # Convert to DataFrame
        input_df = pd.DataFrame(data)
        
        # Apply feature transformer if available
        transformer = get_feature_transformer()
        if transformer:
            try:
                input_df = transformer.transform(input_df)
            except Exception as e:
                logger.error(f"Error applying feature transformer: {e}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Error applying feature transformer: {str(e)}"
                )
        
        # Make predictions
        try:
            predictions = model.predict(input_df).tolist()
        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            PREDICTION_COUNT.labels(model=model_name, status="error").inc()
            raise HTTPException(
                status_code=500, 
                detail=f"Error making predictions: {str(e)}"
            )
        
        # Track metrics
        prediction_time = (datetime.now() - start_time).total_seconds()
        PREDICTION_COUNT.labels(model=model_name, status="success").inc()
        PREDICTION_LATENCY.labels(model=model_name).observe(prediction_time)
        FEATURE_COUNT.labels(model=model_name).inc(input_df.shape[1])
        
        # Log prediction asynchronously
        background_tasks.add_task(
            log_prediction, model_name, input_df, predictions, prediction_time
        )
        
        # Prepare response
        return PredictionResponse(
            predictions=predictions,
            model=model_name,
            prediction_time=prediction_time,
            timestamp=start_time.isoformat(),
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        PREDICTION_COUNT.labels(model=model_name, status="error").inc()
        raise HTTPException(
            status_code=500, 
            detail=f"Unexpected error: {str(e)}"
        )


@app.post("/batch-predict")
async def batch_predict(request: PredictionRequest):
    """
    Schedule a batch prediction job.
    
    Args:
        request: Prediction request
        
    Returns:
        Job information
    """
    model_name = request.model or config.default_model
    
    if not model_name:
        raise HTTPException(
            status_code=400, 
            detail="No model specified and no default model configured"
        )
    
    # In a real implementation, this would create a background job
    # For simplicity, we'll just return a mock response
    job_id = f"batch-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return {
        "job_id": job_id,
        "status": "scheduled",
        "model": model_name,
        "instances": len(request.data),
        "message": "Batch prediction job scheduled",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    # Check if we can access the default model
    try:
        if config.default_model:
            _ = load_model(config.default_model)
        
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"status": "unhealthy", "error": str(e)},
        )


# Helper functions
def log_prediction(
    model_name: str, features: pd.DataFrame, predictions: List[Any], latency: float
) -> None:
    """
    Log a prediction to a file or database.
    
    Args:
        model_name: Name of the model used
        features: Input features
        predictions: Predicted values
        latency: Prediction latency in seconds
    """
    # In a real application, you might log to a database or monitoring system
    # For simplicity, we'll just log to a file
    try:
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"predictions_{datetime.now().strftime('%Y%m%d')}.jsonl")
        
        with open(log_file, "a") as f:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "model": model_name,
                "features_shape": features.shape,
                "num_predictions": len(predictions),
                "latency": latency,
            }
            f.write(json.dumps(log_entry) + "\n")
    
    except Exception as e:
        logger.error(f"Error logging prediction: {e}")


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("Starting ML Model API")
    
    # Start Prometheus metrics server
    try:
        start_http_server(8000)
        logger.info("Started Prometheus metrics server on port 8000")
    except Exception as e:
        logger.error(f"Failed to start Prometheus metrics server: {e}")
    
    # Preload default model if configured
    if config.default_model:
        try:
            load_model(config.default_model)
            logger.info(f"Preloaded default model '{config.default_model}'")
        except Exception as e:
            logger.error(f"Failed to preload default model: {e}")
    
    # Load feature transformer if configured
    if config.feature_transformer_path:
        try:
            get_feature_transformer()
        except Exception as e:
            logger.error(f"Failed to load feature transformer: {e}")


if __name__ == "__main__":
    # Run the API server
    uvicorn.run(
        "model_api:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    ) 