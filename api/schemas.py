"""
Pydantic models for API requests and responses
"""
from pydantic import BaseModel, create_model
from typing import List
from config.columns import get_columns_names

# Create DataRow model dynamically based on column configuration
def create_data_row_model():
    """Create DataRow model dynamically based on column configuration"""
    fields = {'id': (int, ...)}  # ID field is always required
    
    # Add data columns dynamically
    for column_name in get_columns_names():
        fields[column_name] = (int, ...)
    
    return create_model('DataRow', **fields)

# Create the model
DataRow = create_data_row_model()

class DataResponse(BaseModel):
    data: List[DataRow]
    count: int

class SumColumnsRequest(BaseModel):
    the_first_col_name: str
    my_second_colname: str

class SumColumnsResponse(BaseModel):
    result: List[int]

class FormulaRequest(BaseModel):
    myFormula: str

class FormulaResponse(BaseModel):
    result: List[int]