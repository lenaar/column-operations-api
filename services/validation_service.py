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

def extract_column_names_from_formula(formula: str) -> list:
    """Extract column names from formula by splitting on operators"""
    # Split formula by mathematical operators and parentheses
    # Split on operators: +, -, *, /, (, )
    tokens = re.split(r'[+\-*/()\s]+', formula)
    # Filter out empty strings and keep only column names
    return [token for token in tokens if token and token.startswith('column_')]

def validate_formula_characters(formula: str) -> bool:
    """Validate formula characters"""
    allowed_chars = set('column_12345+-*/() ')
    invalid_chars = set(formula) - allowed_chars
    if invalid_chars:
        raise ValueError(f"Formula contains invalid characters: {', '.join(invalid_chars)}")
    return True

def validate_formula_columns(formula: str) -> bool:
    """Validate that all column names in formula are valid"""
    # Extract column names from formula by splitting on operators
    formula_columns = extract_column_names_from_formula(formula)

    if not formula_columns:
        raise ValueError(f"Formula must contain at least one column.")
    
    # Check if all columns in formula are valid using the existing function
    for column_name in formula_columns:
        validate_column_name(column_name)

    return True

def validate_formula(request: FormulaRequest) -> bool:
    """Validate formula syntax and column references"""
    valid_columns = get_data_columns()
    
    formula = request.myFormula.strip()
    
    if not formula:
        raise ValueError("Formula cannot be empty")
    
    # Validate formula columns
    validate_formula_columns(formula)
    
    # Validate formula characters
    validate_formula_characters(formula)
    
    # Check for balanced parentheses
    if formula.count('(') != formula.count(')'):
        raise ValueError("Unbalanced parentheses in formula")
    
    
    return True

