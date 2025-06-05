"""
Module B - Part of circular dependency demonstration
This module imports from module A, which in turn imports from this module.
"""

import time
from datetime import datetime

from circular_dep_module_a import format_data, DataValidator

def process_data_with_time(data):
    """
    Process data with timestamp information.
    This function depends on module A, creating a circular dependency.
    """
    if not data:
        return None
    
    # Using function from module A
    formatted = format_data(data)
    timestamp = datetime.now().isoformat()
    
    return {
        "data": formatted,
        "timestamp": timestamp,
        "processed_at": time.time()
    }

def get_current_time_info():
    """Get current time information"""
    return {
        "current_time": datetime.now(),
        "unix_timestamp": time.time()
    }

class TimeProcessor:
    """A class that processes time-related data"""
    
    def __init__(self):
        self.validator = DataValidator()  # Using class from module A
    
    def process_with_validation(self, data):
        """Process data with validation"""
        if self.validator.validate(data):
            return process_data_with_time(data)
        return None 