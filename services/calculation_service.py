"""
Calculation service for column operations and formulas
"""
from api.schemas import SumColumnsRequest
from .data_service import get_all_data
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

