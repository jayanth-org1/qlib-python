"""
Module A - Part of circular dependency demonstration
This module imports from module B, which in turn imports from this module.
"""

from circular_dep_module_b import process_data_with_time

def validate_input_data(data):
    """
    Validate input data using time processing utilities.
    This function depends on module B, creating a circular dependency.
    """
    if not data:
        return False
    
    # Using function from module B
    processed = process_data_with_time(data)
    return processed is not None

def format_data(data):
    """Format data for processing"""
    return f"formatted_{data}"

class DataValidator:
    """A class that validates data"""
    
    def __init__(self):
        self.validation_count = 0
    
    def validate(self, data):
        """Validate data and increment counter"""
        self.validation_count += 1
        return validate_input_data(data) 