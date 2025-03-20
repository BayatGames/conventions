"""
Data Validation Module

This module provides utilities for validating data quality using Great Expectations.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Union, Any, Tuple

import pandas as pd
import numpy as np
import great_expectations as ge
from great_expectations.dataset import PandasDataset

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DataValidator:
    """Data validation class using Great Expectations."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the data validator.
        
        Args:
            config_path: Path to validation configuration
        """
        self.config = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, "r") as f:
                self.config = json.load(f)
        
        logger.info("Initialized data validator")

    def load_data(self, data_path: str) -> PandasDataset:
        """
        Load data from a file and convert to a Great Expectations dataset.
        
        Args:
            data_path: Path to the data file
            
        Returns:
            Great Expectations dataset
        """
        _, ext = os.path.splitext(data_path)
        
        if ext.lower() == ".csv":
            df = pd.read_csv(data_path)
        elif ext.lower() == ".parquet":
            df = pd.read_parquet(data_path)
        elif ext.lower() in (".json", ".jsonl"):
            df = pd.read_json(data_path, lines=ext.lower() == ".jsonl")
        else:
            raise ValueError(f"Unsupported file format: {ext}")
        
        return ge.from_pandas(df)

    def validate(self, data: Union[str, pd.DataFrame, PandasDataset]) -> Tuple[bool, Dict]:
        """
        Validate data against expectations.
        
        Args:
            data: Either a path to a data file, a pandas DataFrame, or a GE dataset
            
        Returns:
            Tuple of (validation passed, validation results)
        """
        # Convert input to GE dataset
        if isinstance(data, str):
            logger.info(f"Loading data from {data}")
            dataset = self.load_data(data)
        elif isinstance(data, pd.DataFrame):
            dataset = ge.from_pandas(data)
        elif isinstance(data, PandasDataset):
            dataset = data
        else:
            raise TypeError("data must be a file path, DataFrame, or PandasDataset")
        
        # Apply schema validation if configured
        schema_expectations = self.config.get("schema", {})
        if schema_expectations:
            self._apply_schema_expectations(dataset, schema_expectations)
        
        # Apply column-specific expectations
        column_expectations = self.config.get("columns", {})
        for column, expectations in column_expectations.items():
            if column in dataset.columns:
                self._apply_column_expectations(dataset, column, expectations)
        
        # Apply table-level expectations
        table_expectations = self.config.get("table", [])
        self._apply_table_expectations(dataset, table_expectations)
        
        # Run validation
        results = dataset.validate()
        
        passed = results["success"]
        if passed:
            logger.info("Data validation passed")
        else:
            logger.warning("Data validation failed")
            failed_expectations = [
                exp for exp in results["results"] if not exp["success"]
            ]
            for exp in failed_expectations:
                logger.warning(f"Failed expectation: {exp['expectation_config']['expectation_type']}")
        
        return passed, results

    def _apply_schema_expectations(
        self, dataset: PandasDataset, schema_expectations: Dict[str, Any]
    ) -> None:
        """
        Apply schema-related expectations.
        
        Args:
            dataset: Great Expectations dataset
            schema_expectations: Schema expectations configuration
        """
        # Check column presence
        if "required_columns" in schema_expectations:
            dataset.expect_table_columns_to_match_ordered_list(
                schema_expectations["required_columns"]
            )
        
        # Check column types
        if "column_types" in schema_expectations:
            for column, dtype in schema_expectations["column_types"].items():
                if column in dataset.columns:
                    dataset.expect_column_values_to_be_of_type(column, dtype)

    def _apply_column_expectations(
        self, dataset: PandasDataset, column: str, expectations: List[Dict[str, Any]]
    ) -> None:
        """
        Apply column-specific expectations.
        
        Args:
            dataset: Great Expectations dataset
            column: Column name
            expectations: List of expectation configurations
        """
        for exp in expectations:
            exp_type = exp.pop("type")
            
            # Map common validation types to GE expectation methods
            if exp_type == "not_null":
                dataset.expect_column_values_to_not_be_null(column)
            elif exp_type == "unique":
                dataset.expect_column_values_to_be_unique(column)
            elif exp_type == "range":
                dataset.expect_column_values_to_be_between(
                    column, exp.get("min"), exp.get("max")
                )
            elif exp_type == "regex":
                dataset.expect_column_values_to_match_regex(column, exp.get("pattern"))
            elif exp_type == "in_set":
                dataset.expect_column_values_to_be_in_set(column, exp.get("values", []))
            elif exp_type == "json_schema":
                dataset.expect_column_values_to_match_json_schema(
                    column, exp.get("schema")
                )
            else:
                logger.warning(f"Unsupported expectation type: {exp_type}")

    def _apply_table_expectations(
        self, dataset: PandasDataset, expectations: List[Dict[str, Any]]
    ) -> None:
        """
        Apply table-level expectations.
        
        Args:
            dataset: Great Expectations dataset
            expectations: List of expectation configurations
        """
        for exp in expectations:
            exp_type = exp.pop("type")
            
            if exp_type == "row_count":
                min_value = exp.get("min")
                max_value = exp.get("max")
                dataset.expect_table_row_count_to_be_between(min_value, max_value)
            elif exp_type == "unique_combination":
                dataset.expect_compound_columns_to_be_unique(
                    exp.get("columns", [])
                )
            else:
                logger.warning(f"Unsupported table expectation type: {exp_type}")


def create_validation_config(
    data: pd.DataFrame, output_path: str, strictness: str = "medium"
) -> None:
    """
    Automatically generate a validation configuration based on data profiling.
    
    Args:
        data: Input DataFrame
        output_path: Path to save the configuration
        strictness: Level of strictness (low, medium, high)
    """
    config = {
        "schema": {
            "required_columns": list(data.columns),
            "column_types": {}
        },
        "columns": {},
        "table": []
    }
    
    # Generate schema expectations
    for col in data.columns:
        dtype = str(data[col].dtype)
        config["schema"]["column_types"][col] = dtype
        
        # Generate column-specific expectations
        col_expectations = []
        
        # Basic expectations for all strictness levels
        if data[col].isnull().sum() == 0:
            col_expectations.append({"type": "not_null"})
        
        # For numeric columns
        if pd.api.types.is_numeric_dtype(data[col]):
            # Add range expectations
            min_val = data[col].min()
            max_val = data[col].max()
            
            # Adjust range based on strictness
            if strictness == "low":
                min_val = min_val * 0.8 if min_val > 0 else min_val * 1.2
                max_val = max_val * 1.2 if max_val > 0 else max_val * 0.8
            elif strictness == "high":
                # Tighter bounds for high strictness
                q1 = data[col].quantile(0.01)
                q99 = data[col].quantile(0.99)
                min_val = q1
                max_val = q99
            
            col_expectations.append({
                "type": "range",
                "min": float(min_val),
                "max": float(max_val)
            })
        
        # For string columns
        elif pd.api.types.is_string_dtype(data[col]):
            # Check if values are from a limited set
            unique_vals = data[col].nunique()
            if unique_vals <= 20 and unique_vals / len(data) < 0.1:
                col_expectations.append({
                    "type": "in_set",
                    "values": data[col].dropna().unique().tolist()
                })
            
            # Check for uniqueness in IDs
            if "id" in col.lower() and data[col].nunique() == len(data):
                col_expectations.append({"type": "unique"})
        
        # Add expectations to config
        if col_expectations:
            config["columns"][col] = col_expectations
    
    # Table-level expectations
    config["table"].append({
        "type": "row_count",
        "min": int(len(data) * 0.8),
        "max": int(len(data) * 1.2)
    })
    
    # Look for potential composite keys
    if strictness in ("medium", "high"):
        for i, col1 in enumerate(data.columns):
            for col2 in data.columns[i+1:]:
                if data.duplicated(subset=[col1, col2]).sum() == 0:
                    config["table"].append({
                        "type": "unique_combination",
                        "columns": [col1, col2]
                    })
                    break
    
    # Write configuration to file
    with open(output_path, "w") as f:
        json.dump(config, f, indent=2)
    
    logger.info(f"Generated validation configuration saved to {output_path}")


if __name__ == "__main__":
    # Example usage
    validator = DataValidator("config/validation_rules.json")
    
    # Validate a CSV file
    valid, results = validator.validate("data/raw/sample_data_20230320_120000.csv")
    
    if not valid:
        print("Validation failed. Results:", json.dumps(results, indent=2))
    else:
        print("Validation passed!")
    
    # Generate a validation config from sample data
    sample_data = pd.read_csv("data/raw/sample_data_20230320_120000.csv")
    create_validation_config(sample_data, "config/generated_validation_rules.json") 