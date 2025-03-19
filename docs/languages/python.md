<!--
Document: Python Coding Standards
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Python Coding Standards

This document outlines the coding standards and best practices for Python development across all Bayat projects. Following these guidelines ensures code consistency, quality, and maintainability.

## Table of Contents

- [Python Version](#python-version)
- [Code Style](#code-style)
- [Project Structure](#project-structure)
- [Dependencies Management](#dependencies-management)
- [Documentation](#documentation)
- [Testing](#testing)
- [Error Handling](#error-handling)
- [Performance Considerations](#performance-considerations)
- [Security Best Practices](#security-best-practices)
- [Packaging and Deployment](#packaging-and-deployment)
- [Environment Management](#environment-management)
- [IDE Configuration](#ide-configuration)

## Python Version

- Use Python 3.9+ for all new projects
- Python 3.8 is the minimum supported version for existing projects
- Document Python version requirements in project README and `pyproject.toml` or `setup.py`

## Code Style

All Python code should follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with the following specifics:

### Formatting

- Use 4 spaces for indentation (no tabs)
- Maximum line length of 88 characters (consistent with Black formatter)
- Use Black for automated code formatting
- Use isort for import sorting with the Black-compatible configuration

### Naming Conventions

- **Packages**: lowercase, short, no underscores (e.g., `utils`, `models`)
- **Modules**: lowercase with underscores (e.g., `data_processor.py`)
- **Classes**: CamelCase (e.g., `DataProcessor`)
- **Functions/Methods**: lowercase with underscores (e.g., `process_data()`)
- **Variables**: lowercase with underscores (e.g., `user_input`)
- **Constants**: uppercase with underscores (e.g., `MAX_CONNECTIONS`)
- **Private attributes/methods**: prefixed with underscore (e.g., `_internal_method()`)

### Imports

- Group imports in the following order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application/library specific imports
- Use absolute imports for external modules and relative imports for internal modules
- Avoid wildcard imports (`from module import *`)

Example:
```python
# Standard library
import os
import sys
from datetime import datetime

# Third-party
import numpy as np
import pandas as pd
from sqlalchemy import Column, Integer

# Local
from .models import User
from ..utils import helpers
```

### Type Hints

- Use type hints for all function parameters and return values
- Use the `typing` module for complex types
- For improved readability, consider using type aliases for complex types

Example:
```python
from typing import Dict, List, Optional, Tuple, Union

# Type alias
UserData = Dict[str, Union[str, int, List[str]]]

def process_user_data(user_id: int, data: UserData) -> Tuple[bool, Optional[str]]:
    """Process user data and return success status with optional error message."""
    # Implementation
    return True, None
```

## Project Structure

Standardized project structure for different types of Python applications:

### Library/Package

```
my_package/
├── pyproject.toml         # Project metadata and build configuration
├── setup.py               # (Optional) Setup script if not using pyproject.toml
├── README.md              # Project documentation
├── LICENSE                # License information
├── .gitignore             # Git ignore file
├── src/                   # Source code directory
│   └── my_package/        # Package directory
│       ├── __init__.py    # Package initialization
│       ├── module1.py     # Module file
│       └── subpackage/    # Subpackage directory
│           ├── __init__.py
│           └── module2.py
├── tests/                 # Test directory
│   ├── __init__.py
│   ├── test_module1.py
│   └── test_subpackage/
│       └── test_module2.py
└── docs/                  # Documentation directory
    └── index.md
```

### Web Application (Django/Flask)

```
my_webapp/
├── pyproject.toml         # Project metadata and build configuration
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore file
├── manage.py              # Django management script
├── app/                   # Application directory
│   ├── __init__.py
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL configuration
│   └── wsgi.py            # WSGI configuration
├── apps/                  # Django applications
│   ├── core/              # Core application
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   └── users/             # Users application
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       └── tests.py
├── static/                # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── templates/             # HTML templates
│   ├── base.html
│   └── pages/
└── docs/                  # Documentation directory
```

### Data Science Project

```
data_project/
├── pyproject.toml         # Project metadata and build configuration
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore file
├── data/                  # Data directory (often gitignored)
│   ├── raw/               # Raw data
│   ├── processed/         # Processed data
│   └── external/          # External data sources
├── notebooks/             # Jupyter notebooks
│   ├── exploratory/       # Exploratory analysis
│   └── final/             # Final analysis
├── src/                   # Source code
│   ├── __init__.py
│   ├── data/              # Data processing scripts
│   ├── features/          # Feature engineering scripts
│   ├── models/            # Model definition and training
│   └── visualization/     # Visualization scripts
├── tests/                 # Tests
│   ├── __init__.py
│   └── test_data.py
├── models/                # Saved models
└── reports/               # Generated reports
    └── figures/           # Generated figures
```

## Dependencies Management

### Tools

- Use `pip` with a `requirements.txt` file for simple projects
- Use `poetry` for complex projects with intricate dependency management
- Use `pyproject.toml` for project configuration when possible

### Best Practices

- Pin exact versions of dependencies for applications (`requests==2.28.1`)
- Use version ranges for libraries (`requests>=2.27.0,<2.29.0`)
- Separate development dependencies from production dependencies
- Include a `requirements-dev.txt` for development dependencies if using pip
- Document all dependencies with purpose and usage in comments

### Example Poetry Configuration

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "My awesome Python project"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.28.1"
pandas = "^1.5.0"
numpy = "^1.23.3"

[tool.poetry.group.dev.dependencies]
pytest = "^7.1.3"
black = "^22.8.0"
isort = "^5.10.1"
mypy = "^0.981"
flake8 = "^5.0.4"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
```

## Documentation

### Docstring Format

Use Google-style docstrings for all modules, classes, methods, and functions:

```python
def calculate_summary_statistics(
    data: List[float], include_outliers: bool = True
) -> Dict[str, float]:
    """Calculate summary statistics for a list of numeric values.
    
    This function computes basic statistical measures including mean,
    median, standard deviation, min, and max for the provided data.
    
    Args:
        data: A list of numeric values to analyze
        include_outliers: Whether to include outlier values in calculations.
            If False, values outside 3 standard deviations are excluded.
    
    Returns:
        A dictionary containing the summary statistics with the following keys:
            - mean: arithmetic mean
            - median: median value
            - std_dev: standard deviation
            - min: minimum value
            - max: maximum value
    
    Raises:
        ValueError: If the input data is empty or contains non-numeric values.
    
    Examples:
        >>> calculate_summary_statistics([1.0, 2.0, 3.0, 4.0, 5.0])
        {'mean': 3.0, 'median': 3.0, 'std_dev': 1.41, 'min': 1.0, 'max': 5.0}
    """
    # Implementation...
```

### Project Documentation

- Include a comprehensive README.md with:
  - Project description and purpose
  - Installation instructions
  - Usage examples
  - Configuration options
  - Development setup
  - Contribution guidelines
- Use MkDocs or Sphinx for generating documentation websites
- Include in-line comments for complex logic that isn't self-explanatory

## Testing

### Framework

- Use pytest as the primary testing framework
- Organize tests to mirror the structure of the application code
- Name test files with the prefix `test_` (e.g., `test_models.py`)
- Name test functions with the prefix `test_` (e.g., `test_user_authentication`)

### Coverage Requirements

- Aim for at least 80% code coverage for application code
- 90% coverage for critical paths and core functionality
- 100% coverage for utility functions and helpers

### Test Types

- **Unit Tests**: Test individual functions and methods in isolation
- **Integration Tests**: Test interactions between components
- **Functional Tests**: Test complete features from user perspective
- **Parametrized Tests**: Use pytest's parametrize for testing multiple inputs

### Example Test

```python
import pytest
from my_package.utils import validate_email

@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("invalid-email", False),
    ("user@example", False),
    ("user@.com", False),
    ("@example.com", False),
])
def test_validate_email(email, expected):
    """Test that email validation correctly identifies valid and invalid emails."""
    assert validate_email(email) == expected

def test_validate_email_with_empty_input():
    """Test that email validation raises ValueError for empty input."""
    with pytest.raises(ValueError) as excinfo:
        validate_email("")
    assert "Email cannot be empty" in str(excinfo.value)
```

## Error Handling

### Guidelines

- Be explicit about exceptions, avoid bare `except:` clauses
- Use specific built-in exceptions when appropriate
- Create custom exceptions for application-specific errors
- Include meaningful error messages in exceptions
- Log exceptions with appropriate context and stack traces

### Example

```python
import logging
from typing import Dict, Optional

class DatabaseConnectionError(Exception):
    """Raised when database connection fails."""
    pass

class UserNotFoundError(Exception):
    """Raised when requested user is not found."""
    pass

def get_user(user_id: int) -> Dict[str, any]:
    """Retrieve user data from database.
    
    Args:
        user_id: The ID of the user to retrieve
        
    Returns:
        User data dictionary
        
    Raises:
        UserNotFoundError: If the user doesn't exist
        DatabaseConnectionError: If database connection fails
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Database access logic
        connection = get_database_connection()
        user = connection.query(f"SELECT * FROM users WHERE id = {user_id}")
        
        if not user:
            logger.warning(f"User with ID {user_id} not found")
            raise UserNotFoundError(f"User with ID {user_id} does not exist")
            
        return user
        
    except ConnectionError as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise DatabaseConnectionError(f"Failed to connect to database: {str(e)}") from e
```

## Performance Considerations

### Optimization Guidelines

- Optimize for readability first, then performance when necessary
- Use appropriate data structures for the task (e.g., sets for membership testing)
- Prefer list comprehensions over loops for simple transformations
- Use generators for processing large datasets
- Take advantage of built-in functions and standard library

### Memory Management

- Be aware of memory usage for large data structures
- Use generators and iterators for processing large datasets
- Consider chunking large files during processing
- Avoid creating unnecessary copies of large data

### Performance Profiling

- Use the `time` module for basic timing
- Use `cProfile` for more detailed performance profiling
- Use `memory_profiler` to monitor memory usage
- Document performance benchmarks for critical operations

## Security Best Practices

### Data Handling

- Never store sensitive information (passwords, API keys) in code
- Use environment variables or secure vaults for sensitive configuration
- Sanitize all user input before processing
- Use parameterized queries for database operations

### Dependency Security

- Regularly scan dependencies for security vulnerabilities
- Use tools like `safety` or `bandit` in CI/CD pipelines
- Keep dependencies updated to latest secure versions

### Authentication

- Use established libraries for authentication (e.g., `authlib`, `python-jose`)
- Implement proper password hashing with `bcrypt` or `argon2`
- Use secure cookies with proper flags (httponly, secure, samesite)
- Implement proper session management

### Example Security Checks

```python
# BAD: SQL Injection vulnerability
query = f"SELECT * FROM users WHERE username = '{username}'"

# GOOD: Parameterized query
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))

# BAD: Command injection vulnerability
os.system(f"convert {filename} output.png")

# GOOD: Use subprocess with safe arguments
subprocess.run(["convert", filename, "output.png"], check=True)
```

## Packaging and Deployment

### Package Structure

- Follow the src-layout pattern for packages
- Include necessary package metadata in `pyproject.toml` or `setup.py`
- Create proper `__init__.py` files with appropriate imports
- Define `__all__` in `__init__.py` to control exported symbols

### Distribution

- Use Poetry or setuptools for building packages
- Generate wheel packages for distribution
- Publish to PyPI or private package repository for shared libraries
- Document installation and usage instructions

### Docker Deployment

- Use multi-stage builds for smaller images
- Create appropriate Dockerfiles for different environments
- Use non-root users in containers
- Pin specific base image versions

Example Dockerfile:
```dockerfile
FROM python:3.9-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.9-slim

WORKDIR /app

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser

# Copy wheels from builder stage
COPY --from=builder /app/wheels /app/wheels

# Install dependencies
RUN pip install --no-cache /app/wheels/*

# Copy application code
COPY src/ /app/src/

# Switch to non-root user
USER appuser

# Run application
CMD ["python", "-m", "src.main"]
```

## Environment Management

### Virtual Environments

- Always use virtual environments for Python projects
- Use `venv` for simple projects or `poetry` for complex ones
- Document environment setup instructions in README

### Environment Variables

- Use environment variables for configuration
- Use `.env` files for local development (never commit to version control)
- Provide a `.env.example` file with required variables (but no sensitive values)
- Use a library like `python-dotenv` or `pydantic` for environment variable loading

### Configuration Management

- Keep configuration separate from code
- Use a hierarchical approach for configuration (defaults, env vars, config files)
- Validate configuration at startup
- Use strong typing for configuration objects

Example with Pydantic:
```python
from pydantic import BaseSettings, Field, PostgresDsn, validator
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "MyApp"
    DEBUG: bool = False
    DATABASE_URL: PostgresDsn
    API_KEY: str
    MAX_CONNECTIONS: int = 10
    CACHE_TTL: int = Field(default=300, gt=0)
    
    @validator("API_KEY")
    def api_key_must_be_valid(cls, v):
        if len(v) < 32:
            raise ValueError("API key must be at least 32 characters")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Use settings
settings = Settings()
```

## IDE Configuration

### Visual Studio Code

Recommended extensions:
- Python (Microsoft)
- Pylance
- Python Docstring Generator
- Jupyter
- Python Test Explorer

Workspace settings (`settings.json`):
```json
{
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "88"],
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": ["--max-line-length", "88"],
    "python.linting.mypyEnabled": true,
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
}
```

### PyCharm

Recommended plugins:
- Python Security
- Requirements
- Mypy
- Black

Configuration:
- Enable Black as external tool for formatting
- Configure isort as external tool for import sorting
- Setup mypy for type checking
- Configure pytest as the default test runner 