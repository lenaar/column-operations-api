"""
Centralized column configuration for the database model.
Single source of truth for all column-related constants.
"""
from typing import List

# Column configuration - Single source of truth
COLUMN_NAMES: List[str] = ['column_1', 'column_2', 'column_3', 'column_4', 'column_5']
COLUMN_COUNT: int = len(COLUMN_NAMES)

# All columns including ID
ALL_COLUMN_NAMES: List[str] = ['id'] + COLUMN_NAMES

def get_data_columns() -> List[str]:
    """Get data column names (excluding id)"""
    return COLUMN_NAMES.copy()

def get_columns_names() -> List[str]:
    """Get data column names (excluding id) - alias for get_data_columns"""
    return get_data_columns()

def is_valid_column(column_name: str) -> bool:
    """Check if column name is valid"""
    return column_name in COLUMN_NAMES
