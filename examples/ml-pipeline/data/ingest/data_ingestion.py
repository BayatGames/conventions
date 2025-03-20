"""
Data Ingestion Module

This module contains utilities for fetching data from various sources.
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union, Any

import pandas as pd
import requests
from pyspark.sql import SparkSession, DataFrame as SparkDataFrame

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DataIngestion:
    """Base class for data ingestion sources."""

    def __init__(
        self, config: Dict[str, Any], output_dir: str = "./data/raw"
    ) -> None:
        """
        Initialize the data ingestion source.

        Args:
            config: Configuration for the data source
            output_dir: Directory where the raw data will be stored
        """
        self.config = config
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        logger.info(f"Initialized data ingestion with output directory: {output_dir}")

    def ingest(self) -> str:
        """
        Ingest data from the source.
        
        Returns:
            Path to the ingested data file
        """
        raise NotImplementedError("Subclasses must implement this method")

    def validate(self, data_path: str) -> bool:
        """
        Validate the ingested data.
        
        Args:
            data_path: Path to the ingested data
            
        Returns:
            True if validation passes, False otherwise
        """
        logger.info(f"Validating data at {data_path}")
        return True  # Default implementation always passes


class CSVIngestion(DataIngestion):
    """Ingestion source for CSV files."""

    def ingest(self) -> str:
        """
        Ingest data from a CSV file.
        
        Returns:
            Path to the ingested data file
        """
        file_path = self.config.get("file_path")
        if not file_path:
            raise ValueError("file_path is required for CSVIngestion")
        
        logger.info(f"Ingesting CSV data from {file_path}")
        
        # Read the CSV file
        df = pd.read_csv(file_path, **self.config.get("read_options", {}))
        
        # Save to output directory with timestamp
        output_path = os.path.join(
            self.output_dir, 
            f"{os.path.basename(file_path).split('.')[0]}_{self.timestamp}.csv"
        )
        df.to_csv(output_path, index=False)
        
        logger.info(f"CSV data saved to {output_path}")
        return output_path


class DatabaseIngestion(DataIngestion):
    """Ingestion source for database connections."""

    def ingest(self) -> str:
        """
        Ingest data from a database.
        
        Returns:
            Path to the ingested data file
        """
        query = self.config.get("query")
        connection_string = self.config.get("connection_string")
        
        if not query or not connection_string:
            raise ValueError("query and connection_string are required for DatabaseIngestion")
        
        logger.info(f"Ingesting data from database with query: {query}")
        
        # Create a Spark session
        spark = SparkSession.builder.appName("DataIngestion").getOrCreate()
        
        # Read from the database
        df = spark.read \
            .format("jdbc") \
            .option("url", connection_string) \
            .option("query", query) \
            .load()
            
        # Save as parquet
        output_path = os.path.join(
            self.output_dir, 
            f"db_extract_{self.timestamp}.parquet"
        )
        df.write.parquet(output_path)
        
        logger.info(f"Database data saved to {output_path}")
        return output_path


class APIIngestion(DataIngestion):
    """Ingestion source for API endpoints."""

    def ingest(self) -> str:
        """
        Ingest data from an API endpoint.
        
        Returns:
            Path to the ingested data file
        """
        url = self.config.get("url")
        headers = self.config.get("headers", {})
        params = self.config.get("params", {})
        
        if not url:
            raise ValueError("url is required for APIIngestion")
        
        logger.info(f"Ingesting data from API: {url}")
        
        # Make the API request
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Convert to DataFrame
        df = pd.json_normalize(data)
        
        # Save to output directory
        output_path = os.path.join(
            self.output_dir, 
            f"api_data_{self.timestamp}.json"
        )
        df.to_json(output_path, orient="records", lines=True)
        
        logger.info(f"API data saved to {output_path}")
        return output_path


def create_ingestion_source(
    source_type: str, config: Dict[str, Any], output_dir: str = "./data/raw"
) -> DataIngestion:
    """
    Factory function to create an appropriate ingestion source.
    
    Args:
        source_type: Type of ingestion source (csv, database, api)
        config: Configuration for the data source
        output_dir: Directory where the raw data will be stored
        
    Returns:
        An instance of DataIngestion
    """
    sources = {
        "csv": CSVIngestion,
        "database": DatabaseIngestion,
        "api": APIIngestion,
    }
    
    if source_type not in sources:
        raise ValueError(f"Unsupported source type: {source_type}")
    
    return sources[source_type](config, output_dir)


if __name__ == "__main__":
    # Example usage
    csv_config = {
        "file_path": "./sample_data/example.csv",
        "read_options": {
            "sep": ",",
            "header": 0,
        },
    }
    
    ingestion = create_ingestion_source("csv", csv_config)
    data_path = ingestion.ingest()
    ingestion.validate(data_path) 