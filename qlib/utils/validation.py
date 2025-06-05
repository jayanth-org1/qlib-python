"""
Data validation utilities for Qlib
This module provides validation functions for data processing and configuration.
"""

from typing import Any, Dict, List, Union, Optional
import pandas as pd
import numpy as np

from qlib.utils.data import update_config, S_DROP, deepcopy_basic_type


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration dictionary using data utilities.
    
    Parameters
    ----------
    config : Dict[str, Any]
        Configuration dictionary to validate
        
    Returns
    -------
    bool
        True if configuration is valid
    """
    if not isinstance(config, dict):
        return False
    
    # Using function from data.py
    test_config = deepcopy_basic_type(config)
    
    # Check if config can be updated without errors
    try:
        updated = update_config(test_config, {"validation_test": "passed"})
        return "validation_test" in updated
    except Exception:
        return False


def sanitize_config(config: Dict[str, Any], remove_keys: List[str] = None) -> Dict[str, Any]:
    """
    Sanitize configuration by removing specified keys.
    
    Parameters
    ----------
    config : Dict[str, Any]
        Configuration to sanitize
    remove_keys : List[str], optional
        Keys to remove from configuration
        
    Returns
    -------
    Dict[str, Any]
        Sanitized configuration
    """
    if remove_keys is None:
        remove_keys = []
    
    # Using S_DROP from data.py and update_config function
    drop_config = {key: S_DROP for key in remove_keys}
    return update_config(config, drop_config)


def validate_dataframe(df: pd.DataFrame, required_columns: List[str] = None) -> Dict[str, Any]:
    """
    Validate a pandas DataFrame for data processing.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to validate
    required_columns : List[str], optional
        Required column names
        
    Returns
    -------
    Dict[str, Any]
        Validation results
    """
    if required_columns is None:
        required_columns = []
    
    validation_result = {
        "is_valid": True,
        "errors": [],
        "warnings": [],
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict()
    }
    
    # Check for required columns
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        validation_result["is_valid"] = False
        validation_result["errors"].append(f"Missing required columns: {missing_columns}")
    
    # Check for empty DataFrame
    if df.empty:
        validation_result["warnings"].append("DataFrame is empty")
    
    # Check for null values
    null_counts = df.isnull().sum()
    if null_counts.any():
        validation_result["warnings"].append(f"Null values found: {null_counts[null_counts > 0].to_dict()}")
    
    return validation_result


class ConfigValidator:
    """
    A class for validating and managing configurations.
    """
    
    def __init__(self, default_config: Dict[str, Any] = None):
        """
        Initialize the validator with a default configuration.
        
        Parameters
        ----------
        default_config : Dict[str, Any], optional
            Default configuration to use as base
        """
        self.default_config = default_config or {}
        self.validation_history = []
    
    def validate_and_merge(self, user_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate user configuration and merge with defaults.
        
        Parameters
        ----------
        user_config : Dict[str, Any]
            User-provided configuration
            
        Returns
        -------
        Dict[str, Any]
            Merged and validated configuration
        """
        # Using update_config from data.py
        merged_config = update_config(self.default_config, user_config)
        
        # Record validation
        validation_record = {
            "timestamp": pd.Timestamp.now(),
            "user_config": deepcopy_basic_type(user_config),
            "merged_config": deepcopy_basic_type(merged_config),
            "is_valid": validate_config(merged_config)
        }
        
        self.validation_history.append(validation_record)
        
        return merged_config
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of validation history.
        
        Returns
        -------
        Dict[str, Any]
            Validation summary
        """
        if not self.validation_history:
            return {"total_validations": 0, "success_rate": 0.0}
        
        successful_validations = sum(1 for record in self.validation_history if record["is_valid"])
        total_validations = len(self.validation_history)
        
        return {
            "total_validations": total_validations,
            "successful_validations": successful_validations,
            "success_rate": successful_validations / total_validations,
            "latest_validation": self.validation_history[-1]["timestamp"]
        } 