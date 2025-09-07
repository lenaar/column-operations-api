"""
Tests for calculation service functions
"""
import pytest
from unittest.mock import patch, MagicMock
from services.calculation_service import sum_columns, calculate_formula
from api.schemas import SumColumnsRequest, FormulaRequest


class TestSumColumns:
    """Test sum_columns function"""
    
    @patch('services.calculation_service.get_all_data')
    def test_sum_columns_success(self, mock_get_all_data):
        """Test successful column sum"""
        # Mock data
        mock_data = {
            'data': [
                {'column_1': 10, 'column_2': 20, 'column_3': 30, 'column_4': 40, 'column_5': 50},
                {'column_1': 15, 'column_2': 25, 'column_3': 35, 'column_4': 45, 'column_5': 55},
                {'column_1': 20, 'column_2': 30, 'column_3': 40, 'column_4': 50, 'column_5': 60}
            ]
        }
        mock_get_all_data.return_value = mock_data
        
        request = SumColumnsRequest(
            the_first_col_name="column_1",
            my_second_colname="column_2"
        )
        
        result = sum_columns(request)
        expected = [30, 40, 50]  # 10+20, 15+25, 20+30
        assert result == expected
    
    @patch('services.calculation_service.get_all_data')
    def test_sum_different_columns(self, mock_get_all_data):
        """Test sum of different columns"""
        mock_data = {
            'data': [
                {'column_1': 5, 'column_2': 10, 'column_3': 15, 'column_4': 20, 'column_5': 25}
            ]
        }
        mock_get_all_data.return_value = mock_data
        
        request = SumColumnsRequest(
            the_first_col_name="column_1",
            my_second_colname="column_5"
        )
        
        result = sum_columns(request)
        expected = [30]  # 5 + 25
        assert result == expected


class TestCalculateFormula:
    """Test calculate_formula function"""
    
    @patch('services.calculation_service.get_all_data')
    def test_simple_addition(self, mock_get_all_data):
        """Test simple addition formula"""
        mock_data = {
            'data': [
                {'column_1': 10, 'column_2': 20, 'column_3': 30, 'column_4': 40, 'column_5': 50}
            ]
        }
        mock_get_all_data.return_value = mock_data
        
        request = FormulaRequest(myFormula="column_1 + column_2")
        result = calculate_formula(request)
        expected = [30]  # 10 + 20
        assert result == expected
    
    @patch('services.calculation_service.get_all_data')
    def test_complex_formula(self, mock_get_all_data):
        """Test complex formula with multiplication and addition"""
        mock_data = {
            'data': [
                {'column_1': 2, 'column_2': 3, 'column_3': 4, 'column_4': 5, 'column_5': 6}
            ]
        }
        mock_get_all_data.return_value = mock_data
        
        request = FormulaRequest(myFormula="column_1 + column_2 * column_3")
        result = calculate_formula(request)
        expected = [14]  # 2 + (3 * 4) = 2 + 12 = 14
        assert result == expected
    
    @patch('services.calculation_service.get_all_data')
    def test_formula_with_parentheses(self, mock_get_all_data):
        """Test formula with parentheses"""
        mock_data = {
            'data': [
                {'column_1': 2, 'column_2': 3, 'column_3': 4, 'column_4': 5, 'column_5': 6}
            ]
        }
        mock_get_all_data.return_value = mock_data
        
        request = FormulaRequest(myFormula="(column_1 + column_2) * column_3")
        result = calculate_formula(request)
        expected = [20]  # (2 + 3) * 4 = 5 * 4 = 20
        assert result == expected
    
    @patch('services.calculation_service.get_all_data')
    def test_multiple_rows(self, mock_get_all_data):
        """Test formula calculation for multiple rows"""
        mock_data = {
            'data': [
                {'column_1': 1, 'column_2': 2, 'column_3': 3, 'column_4': 4, 'column_5': 5},
                {'column_1': 6, 'column_2': 7, 'column_3': 8, 'column_4': 9, 'column_5': 10},
                {'column_1': 11, 'column_2': 12, 'column_3': 13, 'column_4': 14, 'column_5': 15}
            ]
        }
        mock_get_all_data.return_value = mock_data
        
        request = FormulaRequest(myFormula="column_1 + column_2")
        result = calculate_formula(request)
        expected = [3, 13, 23]  # 1+2, 6+7, 11+12
        assert result == expected
    
    @patch('services.calculation_service.get_all_data')
    def test_invalid_formula(self, mock_get_all_data):
        """Test invalid formula raises error"""
        mock_data = {
            'data': [
                {'column_1': 1, 'column_2': 2, 'column_3': 3, 'column_4': 4, 'column_5': 5}
            ]
        }
        mock_get_all_data.return_value = mock_data
        
        request = FormulaRequest(myFormula="column_1 + invalid_syntax")
        with pytest.raises(ValueError, match="Invalid formula"):
            calculate_formula(request)
