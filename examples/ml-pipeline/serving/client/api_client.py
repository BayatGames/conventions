#!/usr/bin/env python3
"""
Model API Client

A simple client for the ML model serving API.
"""

import argparse
import json
import time
from typing import Dict, List, Any, Optional
import requests


class ModelAPIClient:
    """Client for interacting with the ML model API."""

    def __init__(self, base_url: str = "http://localhost:8080"):
        """
        Initialize the client.
        
        Args:
            base_url: Base URL of the API
        """
        self.base_url = base_url.rstrip("/")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check if the API is healthy.
        
        Returns:
            Health status
        """
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def get_models(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about available models.
        
        Returns:
            Models information
        """
        response = requests.get(f"{self.base_url}/models")
        response.raise_for_status()
        return response.json()["models"]
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get information about a specific model.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Model information
        """
        response = requests.get(f"{self.base_url}/models/{model_name}")
        response.raise_for_status()
        return response.json()
    
    def predict(
        self, features: List[Dict[str, Any]], model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Make predictions with a model.
        
        Args:
            features: List of feature dictionaries
            model_name: Name of the model to use (optional)
            
        Returns:
            Prediction results
        """
        data = [{"features": f} for f in features]
        payload = {"data": data}
        
        if model_name:
            payload["model"] = model_name
        
        response = requests.post(f"{self.base_url}/predict", json=payload)
        response.raise_for_status()
        return response.json()
    
    def batch_predict(
        self, features: List[Dict[str, Any]], model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Schedule a batch prediction job.
        
        Args:
            features: List of feature dictionaries
            model_name: Name of the model to use (optional)
            
        Returns:
            Batch job information
        """
        data = [{"features": f} for f in features]
        payload = {"data": data}
        
        if model_name:
            payload["model"] = model_name
        
        response = requests.post(f"{self.base_url}/batch-predict", json=payload)
        response.raise_for_status()
        return response.json()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="ML Model API Client")
    
    parser.add_argument(
        "--url", default="http://localhost:8080", help="Base URL for the API"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Health check command
    subparsers.add_parser("health", help="Check API health")
    
    # List models command
    subparsers.add_parser("list-models", help="List available models")
    
    # Get model info command
    model_info_parser = subparsers.add_parser("model-info", help="Get model information")
    model_info_parser.add_argument("model_name", help="Name of the model")
    
    # Predict command
    predict_parser = subparsers.add_parser("predict", help="Make predictions")
    predict_parser.add_argument(
        "--model", help="Name of the model to use", default=None
    )
    predict_parser.add_argument(
        "--features", required=True, help="JSON string or path to JSON file with features"
    )
    
    # Batch predict command
    batch_parser = subparsers.add_parser("batch-predict", help="Schedule batch predictions")
    batch_parser.add_argument(
        "--model", help="Name of the model to use", default=None
    )
    batch_parser.add_argument(
        "--features", required=True, help="JSON string or path to JSON file with features"
    )
    
    return parser.parse_args()


def load_features(features_arg: str) -> List[Dict[str, Any]]:
    """
    Load features from a JSON string or file.
    
    Args:
        features_arg: JSON string or path to JSON file
        
    Returns:
        List of feature dictionaries
    """
    # Try to parse as JSON string
    try:
        return json.loads(features_arg)
    except json.JSONDecodeError:
        # Try to load from file
        try:
            with open(features_arg, "r") as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to load features: {e}")


def main():
    """Run the client with command line arguments."""
    args = parse_args()
    client = ModelAPIClient(args.url)
    
    try:
        if args.command == "health":
            result = client.health_check()
            print("Health status:", result["status"])
        
        elif args.command == "list-models":
            models = client.get_models()
            print("Available models:")
            for name, info in models.items():
                print(f"- {name}: {info['description']} (v{info['version']})")
        
        elif args.command == "model-info":
            info = client.get_model_info(args.model_name)
            print(f"Model: {info['name']}")
            print(f"Description: {info['description']}")
            print(f"Version: {info['version']}")
            print(f"Type: {info['type']}")
            print(f"Features: {', '.join(info['features'])}")
            print(f"Default: {'Yes' if info['is_default'] else 'No'}")
        
        elif args.command == "predict":
            features = load_features(args.features)
            
            start_time = time.time()
            result = client.predict(features, args.model)
            elapsed = time.time() - start_time
            
            print(f"Model: {result['model']}")
            print(f"Prediction time: {result['prediction_time']:.4f}s (API) / {elapsed:.4f}s (total)")
            print(f"Timestamp: {result['timestamp']}")
            print("Predictions:")
            for i, pred in enumerate(result["predictions"]):
                print(f"  {i + 1}: {pred}")
        
        elif args.command == "batch-predict":
            features = load_features(args.features)
            
            result = client.batch_predict(features, args.model)
            
            print(f"Job ID: {result['job_id']}")
            print(f"Status: {result['status']}")
            print(f"Model: {result['model']}")
            print(f"Instances: {result['instances']}")
            print(f"Message: {result['message']}")
        
        else:
            print("No command specified. Run with --help for usage information.")
    
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        if hasattr(e, "response") and e.response is not None:
            try:
                error_detail = e.response.json().get("detail", str(e))
                print(f"Error details: {error_detail}")
            except:
                print(f"Status code: {e.response.status_code}")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 