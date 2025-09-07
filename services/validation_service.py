"""
Validation service for input validation
"""
import re
from api.schemas import SumColumnsRequest, FormulaRequest
from config.columns import get_data_columns, is_valid_column

def validate_column_name(column_name_raw: str) -> bool:
    """Validate that column name exists in the database"""
    valid_columns = get_data_columns()
    column_name = column_name_raw.strip()
    if not column_name:
        raise ValueError(f"Column name cannot be empty")
    
    if not is_valid_column(column_name):
        raise ValueError(
            f"Invalid column name: '{column_name}'. "
            f"Valid columns are: {', '.join(valid_columns)}"
        )
    return True

def validate_column_names(request: SumColumnsRequest) -> bool:
    """Validate that column names exist in the database"""

    validate_column_name(request.the_first_col_name)
    validate_column_name(request.my_second_colname)
    
    return True
