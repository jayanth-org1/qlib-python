
from dep_module_b import process_data_with_time

def validate_input_data(data):

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