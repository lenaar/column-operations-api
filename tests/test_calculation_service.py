"""
Tests for calculation service functions
"""
import pytest
from unittest.mock import patch, MagicMock
from services.calculation_service import sum_columns
from api.schemas import SumColumnsRequest


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


