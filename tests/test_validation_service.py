"""
Tests for validation service functions
"""
import pytest
from services.validation_service import (
    validate_column_name,
    validate_column_names,
)
from api.schemas import SumColumnsRequest


class TestValidateColumnName:
    """Test validate_column_name function"""
    
    def test_valid_column_name(self):
        """Test valid column names"""
        assert validate_column_name("column_1") is True
        assert validate_column_name("column_2") is True
        assert validate_column_name("column_5") is True
    
    def test_invalid_column_name(self):
        """Test invalid column names"""
        with pytest.raises(ValueError, match="Invalid column name: 'column_11'"):
            validate_column_name("column_11")
        
        with pytest.raises(ValueError, match="Invalid column name: 'invalid_col'"):
            validate_column_name("invalid_col")
    
    def test_empty_column_name(self):
        """Test empty column name"""
        with pytest.raises(ValueError, match="Column name cannot be empty"):
            validate_column_name("")
        
        with pytest.raises(ValueError, match="Column name cannot be empty"):
            validate_column_name("   ")


class TestValidateColumnNames:
    """Test validate_column_names function"""
    
    def test_valid_column_names(self):
        """Test valid column name pairs"""
        request = SumColumnsRequest(
            the_first_col_name="column_1",
            my_second_colname="column_2"
        )
        assert validate_column_names(request) is True
    
    def test_invalid_first_column(self):
        """Test invalid first column"""
        request = SumColumnsRequest(
            the_first_col_name="column_11",
            my_second_colname="column_2"
        )
        with pytest.raises(ValueError, match="Invalid column name: 'column_11'"):
            validate_column_names(request)
    
    def test_invalid_second_column(self):
        """Test invalid second column"""
        request = SumColumnsRequest(
            the_first_col_name="column_1",
            my_second_colname="column_21"
        )
        with pytest.raises(ValueError, match="Invalid column name: 'column_21'"):
            validate_column_names(request)

