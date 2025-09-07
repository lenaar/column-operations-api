"""
Calculation service for column operations and formulas
"""
from api.schemas import SumColumnsRequest, FormulaRequest
from .data_service import get_all_data
from config.columns import get_columns_names
from typing import List

def sum_columns(request: SumColumnsRequest) -> List[int]:
    """Add two columns row by row"""
    data_response = get_all_data()
    result = []
    
    for row_data in data_response['data']:
        # Get column values from formatted data
        col1_value = row_data[request.the_first_col_name]
        col2_value = row_data[request.my_second_colname]
        result.append(col1_value + col2_value)
    
    return result

def calculate_formula(request: FormulaRequest) -> List[int]:
    """Calculate formula for each row"""
    data_response = get_all_data()
    result = []
    
    for row_data in data_response['data']:
        # Create a safe evaluation context with column values
        context = {}
        for column_name in get_columns_names():
            context[column_name] = row_data[column_name]
        
        # Evaluate the formula safely
        try:
            value = eval(request.myFormula, {"__builtins__": {}}, context)
            result.append(int(value))
        except Exception as e:
            raise ValueError(f"Invalid formula: {e}")
    
    return result