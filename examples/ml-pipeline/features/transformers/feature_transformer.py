"""
Feature Transformer Module

This module provides utilities for feature engineering and preprocessing.
"""

import os
import json
import logging
import pickle
from typing import Dict, List, Union, Any, Optional, Tuple, Callable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    RobustScaler,
    OneHotEncoder,
    LabelEncoder,
    OrdinalEncoder,
)
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectKBest, f_classif, f_regression, RFE
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import PCA, TruncatedSVD
import category_encoders as ce

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class FeatureSelector(BaseEstimator, TransformerMixin):
    """Selects specified columns from a DataFrame."""

    def __init__(self, columns: List[str]):
        """
        Initialize the feature selector.
        
        Args:
            columns: List of column names to select
        """
        self.columns = columns

    def fit(self, X: pd.DataFrame, y=None):
        """
        Fit the transformer (no-op).
        
        Args:
            X: Input DataFrame
            y: Target variable (not used)
            
        Returns:
            self
        """
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Select columns from the DataFrame.
        
        Args:
            X: Input DataFrame
            
        Returns:
            DataFrame with selected columns
        """
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
            
        # Check if all columns exist
        missing_cols = [col for col in self.columns if col not in X.columns]
        if missing_cols:
            raise ValueError(f"Columns not found in input data: {missing_cols}")
            
        return X[self.columns]


class DataFrameImputer(BaseEstimator, TransformerMixin):
    """Imputes missing values in a DataFrame while preserving data types."""

    def __init__(
        self,
        numeric_strategy: str = "mean",
        categorical_strategy: str = "most_frequent",
        datetime_strategy: str = "most_frequent",
        knn_impute: bool = False,
        knn_k: int = 5,
    ):
        """
        Initialize the imputer.
        
        Args:
            numeric_strategy: Strategy for imputing numeric values
            categorical_strategy: Strategy for imputing categorical values
            datetime_strategy: Strategy for imputing datetime values
            knn_impute: Whether to use KNN imputation for numeric features
            knn_k: Number of neighbors for KNN imputation
        """
        self.numeric_strategy = numeric_strategy
        self.categorical_strategy = categorical_strategy
        self.datetime_strategy = datetime_strategy
        self.knn_impute = knn_impute
        self.knn_k = knn_k
        self.imputers = {}
        self.dtypes = None

    def fit(self, X: pd.DataFrame, y=None):
        """
        Fit the imputer on the data.
        
        Args:
            X: Input DataFrame
            y: Target variable (not used)
            
        Returns:
            self
        """
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        
        # Store original data types
        self.dtypes = X.dtypes.to_dict()
        
        # Create imputers for different column types
        numeric_cols = X.select_dtypes(include=["number"]).columns
        categorical_cols = X.select_dtypes(include=["object", "category"]).columns
        datetime_cols = X.select_dtypes(include=["datetime"]).columns
        
        # Numeric imputer
        if len(numeric_cols) > 0:
            if self.knn_impute:
                self.imputers["numeric"] = KNNImputer(n_neighbors=self.knn_k)
            else:
                self.imputers["numeric"] = SimpleImputer(strategy=self.numeric_strategy)
            self.imputers["numeric"].fit(X[numeric_cols])
        
        # Categorical imputer
        if len(categorical_cols) > 0:
            self.imputers["categorical"] = SimpleImputer(
                strategy=self.categorical_strategy, fill_value="missing"
            )
            self.imputers["categorical"].fit(X[categorical_cols])
        
        # Datetime imputer
        if len(datetime_cols) > 0:
            # Convert datetimes to integers (timestamps) for imputation
            datetime_values = X[datetime_cols].copy()
            datetime_values = datetime_values.applymap(
                lambda x: int(x.timestamp()) if pd.notnull(x) else np.nan
            )
            self.imputers["datetime"] = SimpleImputer(strategy=self.datetime_strategy)
            self.imputers["datetime"].fit(datetime_values)
        
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Impute missing values in the DataFrame.
        
        Args:
            X: Input DataFrame
            
        Returns:
            DataFrame with imputed values
        """
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        
        result = X.copy()
        
        # Impute numeric columns
        numeric_cols = X.select_dtypes(include=["number"]).columns
        if len(numeric_cols) > 0 and "numeric" in self.imputers:
            result[numeric_cols] = self.imputers["numeric"].transform(X[numeric_cols])
        
        # Impute categorical columns
        categorical_cols = X.select_dtypes(include=["object", "category"]).columns
        if len(categorical_cols) > 0 and "categorical" in self.imputers:
            result[categorical_cols] = self.imputers["categorical"].transform(X[categorical_cols])
        
        # Impute datetime columns
        datetime_cols = X.select_dtypes(include=["datetime"]).columns
        if len(datetime_cols) > 0 and "datetime" in self.imputers:
            # Convert to timestamps for imputation
            datetime_values = X[datetime_cols].copy()
            datetime_values = datetime_values.applymap(
                lambda x: int(x.timestamp()) if pd.notnull(x) else np.nan
            )
            
            # Apply imputation
            imputed_timestamps = self.imputers["datetime"].transform(datetime_values)
            
            # Convert back to datetime
            for i, col in enumerate(datetime_cols):
                result[col] = pd.to_datetime(imputed_timestamps[:, i], unit="s")
        
        # Restore original data types
        for col, dtype in self.dtypes.items():
            if col in result.columns:
                try:
                    result[col] = result[col].astype(dtype)
                except (ValueError, TypeError):
                    # If conversion fails, keep the imputed type
                    pass
        
        return result


class OutlierHandler(BaseEstimator, TransformerMixin):
    """Handles outliers in numeric data."""

    def __init__(
        self,
        method: str = "clip",
        threshold: float = 3.0,
        replace_with: Optional[str] = None,
    ):
        """
        Initialize the outlier handler.
        
        Args:
            method: Method for handling outliers ('clip', 'remove', or 'winsorize')
            threshold: Z-score threshold for identifying outliers
            replace_with: Value to replace outliers with (None, 'mean', 'median')
        """
        self.method = method
        self.threshold = threshold
        self.replace_with = replace_with
        self.stats = {}

    def fit(self, X: pd.DataFrame, y=None):
        """
        Compute statistics for outlier detection.
        
        Args:
            X: Input DataFrame
            y: Target variable (not used)
            
        Returns:
            self
        """
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        
        numeric_cols = X.select_dtypes(include=["number"]).columns
        
        for col in numeric_cols:
            values = X[col].dropna()
            self.stats[col] = {
                "mean": values.mean(),
                "std": values.std(),
                "median": values.median(),
                "q1": values.quantile(0.25),
                "q3": values.quantile(0.75),
                "iqr": values.quantile(0.75) - values.quantile(0.25),
            }
        
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Handle outliers in the DataFrame.
        
        Args:
            X: Input DataFrame
            
        Returns:
            DataFrame with outliers handled
        """
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        
        result = X.copy()
        numeric_cols = X.select_dtypes(include=["number"]).columns
        
        for col in numeric_cols:
            if col not in self.stats:
                continue
            
            # Calculate z-scores
            mean = self.stats[col]["mean"]
            std = self.stats[col]["std"]
            z_scores = (X[col] - mean) / std
            
            # Identify outliers
            outlier_mask = np.abs(z_scores) > self.threshold
            
            if outlier_mask.sum() == 0:
                continue
            
            if self.method == "clip":
                # Clip values to the threshold
                lower_bound = mean - self.threshold * std
                upper_bound = mean + self.threshold * std
                result[col] = result[col].clip(lower_bound, upper_bound)
            
            elif self.method == "remove":
                # Replace outliers with NaN (to be handled by imputation)
                result.loc[outlier_mask, col] = np.nan
            
            elif self.method == "winsorize":
                # Winsorize data (replace with percentiles)
                q1, q3, iqr = (
                    self.stats[col]["q1"],
                    self.stats[col]["q3"],
                    self.stats[col]["iqr"],
                )
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                result[col] = result[col].clip(lower_bound, upper_bound)
            
            # Replace outliers with a specific value
            if self.replace_with and self.method == "remove":
                if self.replace_with == "mean":
                    result.loc[outlier_mask, col] = mean
                elif self.replace_with == "median":
                    result.loc[outlier_mask, col] = self.stats[col]["median"]
        
        return result


class CategoricalEncoder(BaseEstimator, TransformerMixin):
    """Encodes categorical variables using various methods."""

    def __init__(
        self,
        method: str = "onehot",
        handle_unknown: str = "ignore",
        max_categories: Optional[int] = None,
    ):
        """
        Initialize the categorical encoder.
        
        Args:
            method: Encoding method ('onehot', 'label', 'ordinal', 'binary', 'target')
            handle_unknown: How to handle unknown categories ('ignore' or 'error')
            max_categories: Maximum number of categories to consider (rest grouped as 'other')
        """
        self.method = method
        self.handle_unknown = handle_unknown
        self.max_categories = max_categories
        self.encoders = {}
        self.top_categories = {}

    def fit(self, X: pd.DataFrame, y=None):
        """
        Fit the encoder on the data.
        
        Args:
            X: Input DataFrame
            y: Target variable (used for target encoding)
            
        Returns:
            self
        """
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        
        categorical_cols = X.select_dtypes(include=["object", "category"]).columns
        
        for col in categorical_cols:
            # Determine top categories if max_categories is set
            if self.max_categories:
                value_counts = X[col].value_counts()
                if len(value_counts) > self.max_categories:
                    self.top_categories[col] = set(
                        value_counts.nlargest(self.max_categories).index
                    )
            
            # Create the appropriate encoder
            if self.method == "onehot":
                self.encoders[col] = OneHotEncoder(
                    sparse=False, handle_unknown=self.handle_unknown
                )
                values = X[col].fillna("missing").values.reshape(-1, 1)
                self.encoders[col].fit(values)
            
            elif self.method == "label":
                self.encoders[col] = LabelEncoder()
                values = X[col].fillna("missing").astype(str)
                self.encoders[col].fit(values)
            
            elif self.method == "ordinal":
                self.encoders[col] = OrdinalEncoder(
                    handle_unknown=self.handle_unknown
                )
                values = X[col].fillna("missing").values.reshape(-1, 1)
                self.encoders[col].fit(values)
            
            elif self.method == "binary":
                self.encoders[col] = ce.BinaryEncoder()
                values = X[col].fillna("missing").astype(str)
                self.encoders[col].fit(values.values.reshape(-1, 1))
            
            elif self.method == "target":
                if y is None:
                    raise ValueError("Target encoding requires a target variable")
                self.encoders[col] = ce.TargetEncoder()
                values = X[col].fillna("missing").astype(str)
                self.encoders[col].fit(values.values.reshape(-1, 1), y)
        
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Encode categorical variables in the DataFrame.
        
        Args:
            X: Input DataFrame
            
        Returns:
            Transformed DataFrame with encoded variables
        """
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        
        result = X.copy()
        categorical_cols = X.select_dtypes(include=["object", "category"]).columns
        
        for col in categorical_cols:
            if col not in self.encoders:
                continue
            
            # Handle max_categories if set
            if col in self.top_categories:
                result[col] = result[col].apply(
                    lambda x: x if x in self.top_categories[col] else "other"
                )
            
            # Apply the encoder
            values = result[col].fillna("missing")
            
            if self.method == "onehot":
                encoded = self.encoders[col].transform(values.values.reshape(-1, 1))
                columns = [
                    f"{col}_{cat}" for cat in self.encoders[col].categories_[0]
                ]
                encoded_df = pd.DataFrame(encoded, index=result.index, columns=columns)
                result = pd.concat([result.drop(col, axis=1), encoded_df], axis=1)
            
            elif self.method == "label":
                result[col] = self.encoders[col].transform(values.astype(str))
            
            elif self.method == "ordinal":
                result[col] = self.encoders[col].transform(
                    values.values.reshape(-1, 1)
                )
            
            elif self.method in ["binary", "target"]:
                encoded = self.encoders[col].transform(values.astype(str))
                if isinstance(encoded, np.ndarray):
                    columns = [f"{col}_{i}" for i in range(encoded.shape[1])]
                    encoded_df = pd.DataFrame(
                        encoded, index=result.index, columns=columns
                    )
                    result = pd.concat([result.drop(col, axis=1), encoded_df], axis=1)
                else:
                    result[col] = encoded
        
        return result


class DateTimeFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extracts features from datetime columns."""

    def __init__(
        self,
        features: List[str] = None,
        drop_original: bool = False,
    ):
        """
        Initialize the datetime feature extractor.
        
        Args:
            features: List of features to extract (e.g., 'year', 'month', 'day', 'hour')
            drop_original: Whether to drop the original datetime column
        """
        self.features = features or ["year", "month", "day", "dayofweek", "hour"]
        self.drop_original = drop_original
        self.datetime_cols = None

    def fit(self, X: pd.DataFrame, y=None):
        """
        Identify datetime columns.
        
        Args:
            X: Input DataFrame
            y: Target variable (not used)
            
        Returns:
            self
        """
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        
        self.datetime_cols = X.select_dtypes(include=["datetime"]).columns
        
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features from datetime columns.
        
        Args:
            X: Input DataFrame
            
        Returns:
            DataFrame with extracted datetime features
        """
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        
        result = X.copy()
        
        if not self.datetime_cols:
            return result
        
        for col in self.datetime_cols:
            if col in result.columns:
                # Extract each requested feature
                for feature in self.features:
                    if feature == "year":
                        result[f"{col}_year"] = result[col].dt.year
                    elif feature == "month":
                        result[f"{col}_month"] = result[col].dt.month
                    elif feature == "day":
                        result[f"{col}_day"] = result[col].dt.day
                    elif feature == "hour":
                        result[f"{col}_hour"] = result[col].dt.hour
                    elif feature == "minute":
                        result[f"{col}_minute"] = result[col].dt.minute
                    elif feature == "second":
                        result[f"{col}_second"] = result[col].dt.second
                    elif feature == "dayofweek":
                        result[f"{col}_dayofweek"] = result[col].dt.dayofweek
                    elif feature == "dayofyear":
                        result[f"{col}_dayofyear"] = result[col].dt.dayofyear
                    elif feature == "quarter":
                        result[f"{col}_quarter"] = result[col].dt.quarter
                    elif feature == "is_weekend":
                        result[f"{col}_is_weekend"] = (
                            result[col].dt.dayofweek >= 5
                        ).astype(int)
                    elif feature == "is_month_start":
                        result[f"{col}_is_month_start"] = result[
                            col
                        ].dt.is_month_start.astype(int)
                    elif feature == "is_month_end":
                        result[f"{col}_is_month_end"] = result[
                            col
                        ].dt.is_month_end.astype(int)
                
                # Drop original column if requested
                if self.drop_original:
                    result = result.drop(col, axis=1)
        
        return result


class TextFeatureExtractor(BaseEstimator, TransformerMixin):
    """Extracts features from text columns."""

    def __init__(
        self,
        method: str = "tfidf",
        max_features: int = 100,
        ngram_range: Tuple[int, int] = (1, 1),
        drop_original: bool = True,
    ):
        """
        Initialize the text feature extractor.
        
        Args:
            method: Method for feature extraction ('tfidf' or 'bow')
            max_features: Maximum number of features to extract
            ngram_range: Range of n-grams to consider
            drop_original: Whether to drop the original text column
        """
        self.method = method
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.drop_original = drop_original
        self.extractors = {}

    def fit(self, X: pd.DataFrame, y=None):
        """
        Fit the text feature extractor on the data.
        
        Args:
            X: Input DataFrame
            y: Target variable (not used)
            
        Returns:
            self
        """
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        
        # Identify text columns (object type with string values)
        for col in X.select_dtypes(include=["object"]).columns:
            # Check if column contains text (average length > 20 chars)
            sample = X[col].dropna().astype(str)
            if len(sample) > 0 and sample.str.len().mean() > 20:
                # Create appropriate extractor
                if self.method == "tfidf":
                    self.extractors[col] = TfidfVectorizer(
                        max_features=self.max_features,
                        ngram_range=self.ngram_range,
                    )
                else:  # bow (bag of words)
                    self.extractors[col] = CountVectorizer(
                        max_features=self.max_features,
                        ngram_range=self.ngram_range,
                    )
                
                # Fit the extractor
                self.extractors[col].fit(sample)
        
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features from text columns.
        
        Args:
            X: Input DataFrame
            
        Returns:
            DataFrame with extracted text features
        """
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        
        result = X.copy()
        
        for col, extractor in self.extractors.items():
            if col in result.columns:
                # Extract features
                text_data = result[col].fillna("").astype(str)
                features = extractor.transform(text_data)
                
                # Convert to DataFrame
                feature_names = [f"{col}_{name}" for name in extractor.get_feature_names_out()]
                features_df = pd.DataFrame(
                    features.toarray(), index=result.index, columns=feature_names
                )
                
                # Combine with result
                result = pd.concat([result, features_df], axis=1)
                
                # Drop original column if requested
                if self.drop_original:
                    result = result.drop(col, axis=1)
        
        return result


class FeatureTransformer:
    """Main class for feature engineering and preprocessing."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the feature transformer.
        
        Args:
            config_path: Path to a JSON configuration file
        """
        self.config = self._load_config(config_path) if config_path else {}
        self.pipeline = None
        self.feature_names = None
        
        logger.info("Initialized feature transformer")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from a JSON file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Configuration dictionary
        """
        with open(config_path, "r") as f:
            config = json.load(f)
        
        logger.info(f"Loaded configuration from {config_path}")
        return config

    def build_pipeline(self) -> Pipeline:
        """
        Build a preprocessing pipeline based on configuration.
        
        Returns:
            Scikit-learn pipeline
        """
        steps = []
        
        # Feature selection
        if "feature_selection" in self.config:
            feature_selection = self.config["feature_selection"]
            if feature_selection["method"] == "specified":
                steps.append(
                    ("selector", FeatureSelector(feature_selection["columns"]))
                )
        
        # Imputation
        if "imputation" in self.config:
            imputation = self.config["imputation"]
            steps.append(
                (
                    "imputer",
                    DataFrameImputer(
                        numeric_strategy=imputation.get("numeric_strategy", "mean"),
                        categorical_strategy=imputation.get(
                            "categorical_strategy", "most_frequent"
                        ),
                        knn_impute=imputation.get("knn_impute", False),
                    ),
                )
            )
        
        # Outlier handling
        if "outlier_handling" in self.config:
            outlier_config = self.config["outlier_handling"]
            steps.append(
                (
                    "outlier_handler",
                    OutlierHandler(
                        method=outlier_config.get("method", "clip"),
                        threshold=outlier_config.get("threshold", 3.0),
                        replace_with=outlier_config.get("replace_with"),
                    ),
                )
            )
        
        # Datetime feature extraction
        if "datetime_features" in self.config:
            datetime_config = self.config["datetime_features"]
            steps.append(
                (
                    "datetime_extractor",
                    DateTimeFeatureExtractor(
                        features=datetime_config.get("features"),
                        drop_original=datetime_config.get("drop_original", False),
                    ),
                )
            )
        
        # Text feature extraction
        if "text_features" in self.config:
            text_config = self.config["text_features"]
            steps.append(
                (
                    "text_extractor",
                    TextFeatureExtractor(
                        method=text_config.get("method", "tfidf"),
                        max_features=text_config.get("max_features", 100),
                        ngram_range=tuple(text_config.get("ngram_range", [1, 1])),
                        drop_original=text_config.get("drop_original", True),
                    ),
                )
            )
        
        # Categorical encoding
        if "categorical_encoding" in self.config:
            cat_config = self.config["categorical_encoding"]
            steps.append(
                (
                    "categorical_encoder",
                    CategoricalEncoder(
                        method=cat_config.get("method", "onehot"),
                        handle_unknown=cat_config.get("handle_unknown", "ignore"),
                        max_categories=cat_config.get("max_categories"),
                    ),
                )
            )
        
        # Scaling
        if "scaling" in self.config:
            scaling = self.config["scaling"]
            method = scaling.get("method", "standard")
            
            if method == "standard":
                steps.append(("scaler", StandardScaler()))
            elif method == "minmax":
                steps.append(
                    (
                        "scaler",
                        MinMaxScaler(
                            feature_range=tuple(scaling.get("feature_range", [0, 1]))
                        ),
                    )
                )
            elif method == "robust":
                steps.append(("scaler", RobustScaler()))
        
        # Dimensionality reduction
        if "dimensionality_reduction" in self.config:
            dim_config = self.config["dimensionality_reduction"]
            method = dim_config.get("method", "pca")
            n_components = dim_config.get("n_components", 10)
            
            if method == "pca":
                steps.append(("reducer", PCA(n_components=n_components)))
            elif method == "svd":
                steps.append(("reducer", TruncatedSVD(n_components=n_components)))
        
        # Create pipeline
        self.pipeline = Pipeline(steps)
        logger.info(f"Built pipeline with steps: {[step[0] for step in steps]}")
        
        return self.pipeline

    def fit(self, X: pd.DataFrame, y=None) -> "FeatureTransformer":
        """
        Fit the feature transformation pipeline.
        
        Args:
            X: Input DataFrame
            y: Target variable (used for some transformations)
            
        Returns:
            self
        """
        if self.pipeline is None:
            self.build_pipeline()
        
        logger.info("Fitting feature transformation pipeline")
        self.pipeline.fit(X, y)
        
        # Save feature names after transformation (if possible)
        try:
            transformed = self.pipeline.transform(X.head(1))
            if isinstance(transformed, pd.DataFrame):
                self.feature_names = transformed.columns.tolist()
        except Exception as e:
            logger.warning(f"Could not determine output feature names: {e}")
        
        return self

    def transform(self, X: pd.DataFrame) -> Union[pd.DataFrame, np.ndarray]:
        """
        Apply the feature transformation pipeline.
        
        Args:
            X: Input DataFrame
            
        Returns:
            Transformed data
        """
        if self.pipeline is None:
            raise ValueError("Pipeline is not fitted. Call fit() first.")
        
        logger.info("Transforming data using the pipeline")
        transformed = self.pipeline.transform(X)
        
        # Convert to DataFrame if feature names are available
        if self.feature_names and isinstance(transformed, np.ndarray):
            if transformed.shape[1] == len(self.feature_names):
                transformed = pd.DataFrame(
                    transformed, index=X.index, columns=self.feature_names
                )
        
        return transformed

    def fit_transform(self, X: pd.DataFrame, y=None) -> Union[pd.DataFrame, np.ndarray]:
        """
        Fit and transform the data in one step.
        
        Args:
            X: Input DataFrame
            y: Target variable (used for some transformations)
            
        Returns:
            Transformed data
        """
        return self.fit(X, y).transform(X)

    def save(self, path: str) -> None:
        """
        Save the transformer to a file.
        
        Args:
            path: Path to save the transformer
        """
        if self.pipeline is None:
            raise ValueError("Pipeline is not fitted. Call fit() first.")
        
        data = {
            "pipeline": self.pipeline,
            "config": self.config,
            "feature_names": self.feature_names,
        }
        
        with open(path, "wb") as f:
            pickle.dump(data, f)
        
        logger.info(f"Saved feature transformer to {path}")

    @classmethod
    def load(cls, path: str) -> "FeatureTransformer":
        """
        Load a transformer from a file.
        
        Args:
            path: Path to the saved transformer
            
        Returns:
            FeatureTransformer instance
        """
        with open(path, "rb") as f:
            data = pickle.load(f)
        
        transformer = cls()
        transformer.pipeline = data["pipeline"]
        transformer.config = data["config"]
        transformer.feature_names = data["feature_names"]
        
        logger.info(f"Loaded feature transformer from {path}")
        return transformer


if __name__ == "__main__":
    # Example usage
    from sklearn.datasets import fetch_california_housing
    
    # Load sample data
    housing = fetch_california_housing()
    df = pd.DataFrame(
        housing.data, columns=housing.feature_names
    )
    
    # Define configuration
    config = {
        "imputation": {
            "numeric_strategy": "mean",
            "categorical_strategy": "most_frequent",
        },
        "outlier_handling": {
            "method": "clip",
            "threshold": 3.0,
        },
        "scaling": {
            "method": "standard",
        },
    }
    
    # Create and apply transformer
    transformer = FeatureTransformer()
    transformer.config = config
    
    transformed_data = transformer.fit_transform(df)
    print(f"Original shape: {df.shape}")
    print(f"Transformed shape: {transformed_data.shape}")
    
    # Save and reload
    transformer.save("housing_transformer.pkl")
    loaded_transformer = FeatureTransformer.load("housing_transformer.pkl")
    
    # Apply loaded transformer
    transformed_again = loaded_transformer.transform(df)
    print("Transformation successful after loading:", 
          np.allclose(transformed_data, transformed_again)) 