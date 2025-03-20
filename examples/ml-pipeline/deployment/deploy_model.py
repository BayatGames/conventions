#!/usr/bin/env python3
"""
Model Deployment Script

This script automates the deployment of machine learning models to production.
It handles model registration, validation, configuration updates, and deployment to the model server.
"""

import os
import sys
import json
import logging
import argparse
import subprocess
import tempfile
import time
from datetime import datetime
from typing import Dict, Any, Optional

import mlflow
import mlflow.pyfunc
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ModelDeployer:
    """Handles the deployment of machine learning models."""

    def __init__(
        self,
        config_path: str,
        mlflow_tracking_uri: Optional[str] = None,
        deployment_env: str = "production",
    ):
        """
        Initialize the deployer.
        
        Args:
            config_path: Path to the deployment configuration file
            mlflow_tracking_uri: URI for the MLflow tracking server
            deployment_env: Deployment environment (e.g., production, staging)
        """
        self.config_path = config_path
        self.deployment_env = deployment_env
        
        # Load configuration
        with open(config_path, "r") as f:
            self.config = json.load(f)
        
        # Set MLflow tracking URI
        if mlflow_tracking_uri:
            mlflow.set_tracking_uri(mlflow_tracking_uri)
        elif "mlflow_tracking_uri" in self.config:
            mlflow.set_tracking_uri(self.config["mlflow_tracking_uri"])
        
        logger.info(f"Initialized ModelDeployer for {deployment_env} environment")
    
    def register_model(
        self,
        run_id: str,
        model_name: str,
        model_version: Optional[str] = None,
        description: Optional[str] = None,
        metrics: Optional[Dict[str, float]] = None,
        features: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Register a model with the model registry.
        
        Args:
            run_id: MLflow run ID
            model_name: Name for the model
            model_version: Version of the model
            description: Description of the model
            metrics: Performance metrics
            features: List of features used by the model
            
        Returns:
            Model configuration
        """
        logger.info(f"Registering model {model_name} from run {run_id}")
        
        # Get run info
        client = mlflow.tracking.MlflowClient()
        run = client.get_run(run_id)
        run_metrics = run.data.metrics
        
        # Combine with provided metrics
        if metrics:
            all_metrics = {**run_metrics, **metrics}
        else:
            all_metrics = run_metrics
        
        # Create model configuration
        model_config = {
            "type": "mlflow",
            "run_id": run_id,
            "description": description or f"Model {model_name} registered on {datetime.now().isoformat()}",
            "version": model_version or datetime.now().strftime("%Y%m%d%H%M%S"),
            "metrics": {k: float(v) for k, v in all_metrics.items()},
            "features": features or [],
            "registered_at": datetime.now().isoformat(),
            "environment": self.deployment_env,
        }
        
        # Update configuration
        models_config = self.config.get("models", {})
        models_config[model_name] = model_config
        self.config["models"] = models_config
        
        # Save updated configuration
        self._save_config()
        
        logger.info(f"Registered model {model_name} with version {model_config['version']}")
        return model_config
    
    def validate_model(
        self,
        model_name: str,
        validation_data: Optional[str] = None,
        threshold_metrics: Optional[Dict[str, float]] = None,
    ) -> bool:
        """
        Validate a model before deployment.
        
        Args:
            model_name: Name of the model to validate
            validation_data: Path to validation data
            threshold_metrics: Metrics thresholds for validation
            
        Returns:
            True if validation passes, False otherwise
        """
        logger.info(f"Validating model {model_name}")
        
        # Check if model exists in configuration
        if model_name not in self.config.get("models", {}):
            logger.error(f"Model {model_name} not found in configuration")
            return False
        
        model_config = self.config["models"][model_name]
        
        # Get model URI
        run_id = model_config.get("run_id")
        if not run_id:
            logger.error(f"Run ID not found for model {model_name}")
            return False
        
        model_uri = f"runs:/{run_id}/model"
        
        try:
            # Load model
            model = mlflow.pyfunc.load_model(model_uri)
            
            # If validation data provided, evaluate model
            if validation_data:
                # Load validation data
                if validation_data.endswith(".csv"):
                    data = pd.read_csv(validation_data)
                elif validation_data.endswith(".parquet"):
                    data = pd.read_parquet(validation_data)
                elif validation_data.endswith(".json"):
                    data = pd.read_json(validation_data)
                else:
                    logger.error(f"Unsupported validation data format: {validation_data}")
                    return False
                
                # Assume last column is target if not specified
                X = data.iloc[:, :-1]
                y = data.iloc[:, -1]
                
                # Make predictions
                try:
                    predictions = model.predict(X)
                    
                    # Evaluate predictions
                    # This would be more comprehensive in a real implementation
                    if len(predictions) != len(y):
                        logger.error("Prediction length mismatch")
                        return False
                    
                    # Check against threshold metrics if provided
                    if threshold_metrics:
                        # In a real implementation, we would calculate metrics here
                        # For simplicity, we'll just check against stored metrics
                        for metric_name, threshold in threshold_metrics.items():
                            if metric_name in model_config.get("metrics", {}):
                                actual = model_config["metrics"][metric_name]
                                if actual < threshold:
                                    logger.error(
                                        f"Metric {metric_name} below threshold: {actual} < {threshold}"
                                    )
                                    return False
                    
                    logger.info("Model predictions successful")
                
                except Exception as e:
                    logger.error(f"Error making predictions: {e}")
                    return False
            
            logger.info(f"Model {model_name} validation passed")
            return True
        
        except Exception as e:
            logger.error(f"Error validating model: {e}")
            return False
    
    def set_default_model(self, model_name: str) -> bool:
        """
        Set a model as the default model.
        
        Args:
            model_name: Name of the model to set as default
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Setting {model_name} as default model")
        
        # Check if model exists in configuration
        if model_name not in self.config.get("models", {}):
            logger.error(f"Model {model_name} not found in configuration")
            return False
        
        # Set as default
        self.config["default_model"] = model_name
        
        # Save updated configuration
        self._save_config()
        
        logger.info(f"Set {model_name} as default model")
        return True
    
    def deploy_model(
        self,
        model_name: str,
        set_as_default: bool = False,
        restart_server: bool = False,
        server_url: Optional[str] = None,
    ) -> bool:
        """
        Deploy a model to the model server.
        
        Args:
            model_name: Name of the model to deploy
            set_as_default: Whether to set the model as the default
            restart_server: Whether to restart the model server
            server_url: URL of the model server for health check
            
        Returns:
            True if deployment is successful, False otherwise
        """
        logger.info(f"Deploying model {model_name}")
        
        # Validate model first
        if not self.validate_model(model_name):
            logger.error(f"Model {model_name} validation failed")
            return False
        
        # Set as default if requested
        if set_as_default:
            if not self.set_default_model(model_name):
                logger.error(f"Failed to set {model_name} as default model")
                return False
        
        # In a real implementation, we might copy files, update configuration
        # on the server, etc. For simplicity, we'll just restart the server if requested.
        if restart_server:
            try:
                logger.info("Restarting model server")
                # This would be custom to your deployment infrastructure
                # For example, using Docker, Kubernetes, etc.
                self._restart_model_server()
                
                # Wait for server to start and check health
                if server_url:
                    self._check_server_health(server_url)
            
            except Exception as e:
                logger.error(f"Error restarting model server: {e}")
                return False
        
        logger.info(f"Model {model_name} deployed successfully")
        return True
    
    def _save_config(self) -> None:
        """Save the updated configuration."""
        # Create backup of current config
        backup_path = f"{self.config_path}.bak"
        try:
            with open(self.config_path, "r") as src, open(backup_path, "w") as dst:
                dst.write(src.read())
        except Exception as e:
            logger.warning(f"Failed to create config backup: {e}")
        
        # Save updated config
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)
    
    def _restart_model_server(self) -> None:
        """Restart the model server."""
        # This is a placeholder - implementation depends on your infrastructure
        logger.info("Model server restart command would be executed here")
        # Example:
        # subprocess.run(["docker", "restart", "model-api-container"], check=True)
    
    def _check_server_health(self, server_url: str, max_retries: int = 5, retry_delay: int = 2) -> bool:
        """
        Check if the model server is healthy.
        
        Args:
            server_url: URL of the model server
            max_retries: Maximum number of health check retries
            retry_delay: Delay between retries in seconds
            
        Returns:
            True if server is healthy, False otherwise
        """
        import requests
        
        health_url = f"{server_url.rstrip('/')}/health"
        
        for i in range(max_retries):
            try:
                logger.info(f"Checking server health ({i+1}/{max_retries})")
                response = requests.get(health_url, timeout=5)
                
                if response.status_code == 200 and response.json().get("status") == "healthy":
                    logger.info("Server is healthy")
                    return True
                
                logger.warning(f"Server not healthy yet: {response.text}")
            
            except requests.exceptions.RequestException as e:
                logger.warning(f"Health check failed: {e}")
            
            time.sleep(retry_delay)
        
        logger.error(f"Server health check failed after {max_retries} attempts")
        return False


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="ML Model Deployment")
    
    parser.add_argument(
        "--config", 
        default="../serving/config/model_serving_config.json", 
        help="Path to model serving configuration file"
    )
    
    parser.add_argument(
        "--mlflow-uri", 
        help="MLflow tracking URI"
    )
    
    parser.add_argument(
        "--environment", 
        default="production", 
        choices=["development", "staging", "production"],
        help="Deployment environment"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Register model command
    register_parser = subparsers.add_parser("register", help="Register a model")
    register_parser.add_argument("--run-id", required=True, help="MLflow run ID")
    register_parser.add_argument("--name", required=True, help="Model name")
    register_parser.add_argument("--version", help="Model version")
    register_parser.add_argument("--description", help="Model description")
    
    # Validate model command
    validate_parser = subparsers.add_parser("validate", help="Validate a model")
    validate_parser.add_argument("--name", required=True, help="Model name")
    validate_parser.add_argument("--data", help="Path to validation data")
    
    # Set default model command
    default_parser = subparsers.add_parser("set-default", help="Set default model")
    default_parser.add_argument("--name", required=True, help="Model name")
    
    # Deploy model command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy a model")
    deploy_parser.add_argument("--name", required=True, help="Model name")
    deploy_parser.add_argument("--set-default", action="store_true", help="Set as default model")
    deploy_parser.add_argument("--restart", action="store_true", help="Restart model server")
    deploy_parser.add_argument("--server-url", default="http://localhost:8080", help="Model server URL")
    
    return parser.parse_args()


def main():
    """Run the deployment process."""
    args = parse_args()
    
    try:
        deployer = ModelDeployer(
            config_path=args.config,
            mlflow_tracking_uri=args.mlflow_uri,
            deployment_env=args.environment,
        )
        
        if args.command == "register":
            result = deployer.register_model(
                run_id=args.run_id,
                model_name=args.name,
                model_version=args.version,
                description=args.description,
            )
            print(f"Model registered: {json.dumps(result, indent=2)}")
        
        elif args.command == "validate":
            result = deployer.validate_model(
                model_name=args.name,
                validation_data=args.data,
            )
            print(f"Validation {'passed' if result else 'failed'}")
        
        elif args.command == "set-default":
            result = deployer.set_default_model(args.name)
            print(f"Set default model: {'success' if result else 'failed'}")
        
        elif args.command == "deploy":
            result = deployer.deploy_model(
                model_name=args.name,
                set_as_default=args.set_default,
                restart_server=args.restart,
                server_url=args.server_url,
            )
            print(f"Deployment {'succeeded' if result else 'failed'}")
        
        else:
            print("No command specified. Run with --help for usage information.")
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 