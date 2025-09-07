"""
Tests for validation service functions
"""
import pytest
from services.validation_service import (
    validate_column_name,
    validate_column_names,
    validate_formula_columns,
    validate_formula_characters,
    validate_formula,
    extract_column_names_from_formula
)
from api.schemas import SumColumnsRequest, FormulaRequest


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


class TestExtractColumnNamesFromFormula:
    """Test extract_column_names_from_formula function"""
    
    def test_simple_formula(self):
        """Test simple formula extraction"""
        result = extract_column_names_from_formula("column_1 + column_2")
        assert result == ["column_1", "column_2"]
    
    def test_complex_formula(self):
        """Test complex formula extraction"""
        result = extract_column_names_from_formula("(column_1 + column_2) * column_3 - column_4")
        assert result == ["column_1", "column_2", "column_3", "column_4"]
    
    def test_formula_with_numbers(self):
        """Test formula with numbers"""
        result = extract_column_names_from_formula("column_1 * 2 + column_2")
        assert result == ["column_1", "column_2"]
    
    def test_no_columns(self):
        """Test formula with no columns"""
        result = extract_column_names_from_formula("1 + 2 * 3")
        assert result == []


class TestValidateFormulaColumns:
    """Test validate_formula_columns function"""
    
    def test_valid_formula_columns(self):
        """Test valid formula columns"""
        assert validate_formula_columns("column_1 + column_2") is True
        assert validate_formula_columns("(column_1 + column_2) * column_3") is True
        assert validate_formula_columns("(column_1      + column_2   ) *   column_3") is True

    
    def test_invalid_formula_columns(self):
        """Test invalid formula columns"""
        with pytest.raises(ValueError, match="Invalid column name: 'column_11'"):
            validate_formula_columns("column_1 + column_11")

    def test_spaces_in_formula_columns(self):
        """Test spaces in formula columns"""
        with pytest.raises(ValueError, match="Formula must contain at least one column."):
            validate_formula_columns("   +   +   ")
    
    def test_no_columns_in_formula(self):
        """Test formula with no columns"""
        with pytest.raises(ValueError, match="Formula must contain at least one column"):
            validate_formula_columns("1 + 2 * 3")


class TestValidateFormulaCharacters:
    """Test validate_formula_characters function"""
    
    def test_valid_characters(self):
        """Test valid formula characters"""
        assert validate_formula_characters("column_1 + column_2") is True
        assert validate_formula_characters("(column_1 + column_2) * column_3") is True
    
    def test_invalid_characters(self):
        """Test invalid formula characters"""
        with pytest.raises(ValueError, match="Formula contains invalid characters: @"):
            validate_formula_characters("column_1 @ column_2")
        

class TestValidateFormula:
    """Test validate_formula function"""
    
    def test_valid_formula(self):
        """Test valid formula"""
        request = FormulaRequest(myFormula="column_1 + column_2 * column_3")
        assert validate_formula(request) is True
    
    def test_empty_formula(self):
        """Test empty formula"""
        request = FormulaRequest(myFormula="")
        with pytest.raises(ValueError, match="Formula cannot be empty"):
            validate_formula(request)
    
    def test_formula_with_invalid_columns(self):
        """Test formula with invalid columns"""
        request = FormulaRequest(myFormula="column_1 + column_11")
        with pytest.raises(ValueError, match="Invalid column name: 'column_11'"):
            validate_formula(request)
    
    def test_formula_with_invalid_characters(self):
        """Test formula with invalid characters"""
        request = FormulaRequest(myFormula="column_1 @ column_2")
        with pytest.raises(ValueError, match="Formula contains invalid characters: @"):
            validate_formula(request)
    
    def test_unbalanced_parentheses(self):
        """Test formula with unbalanced parentheses"""
        request = FormulaRequest(myFormula="(column_1 + column_2")
        with pytest.raises(ValueError, match="Unbalanced parentheses in formula"):
            validate_formula(request)
