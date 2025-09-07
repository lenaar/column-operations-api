"""
Tests for data service functions
"""
import pytest
from unittest.mock import patch, MagicMock
from services.data_service import get_all_data


class TestGetAllData:
    """Test get_all_data function"""
    
    def _create_mock_row(self, row_id, **columns):
        """Helper to create mock database row"""
        mock_row = MagicMock()
        mock_row.id = row_id
        for col, value in columns.items():
            setattr(mock_row, col, value)
        return mock_row
    
    @patch('services.data_service.SessionLocal')
    def test_get_all_data_success(self, mock_session_local):
        """Test successful data retrieval"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        
        # Create test data more concisely
        mock_rows = [
            self._create_mock_row(1, column_1=10, column_2=20, column_3=30, column_4=40, column_5=50),
            self._create_mock_row(2, column_1=15, column_2=25, column_3=35, column_4=45, column_5=55)
        ]
        mock_session.query.return_value.all.return_value = mock_rows
        
        result = get_all_data()
        
        # Test the essentials
        assert result['count'] == 2
        assert len(result['data']) == 2
        assert result['data'][0]['id'] == 1
        assert result['data'][0]['column_1'] == 10
        assert result['data'][0]['column_2'] == 20
        assert result['data'][1]['id'] == 2
        assert result['data'][1]['column_1'] == 15
        assert result['data'][1]['column_2'] == 25
        assert result['data'][1]['column_3'] == 35
        assert result['data'][1]['column_4'] == 45
        assert result['data'][1]['column_5'] == 55
        mock_session.close.assert_called_once()
    
    @patch('services.data_service.SessionLocal')
    def test_get_all_data_empty(self, mock_session_local):
        """Test empty database"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query.return_value.all.return_value = []
        
        result = get_all_data()
        
        assert result['count'] == 0
        assert result['data'] == []
        mock_session.close.assert_called_once()
    
    @patch('services.data_service.SessionLocal')
    def test_session_closed_on_exception(self, mock_session_local):
        """Test session cleanup on error"""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        mock_session.query.side_effect = Exception("Database error")
        
        with pytest.raises(Exception):
            get_all_data()
        
        mock_session.close.assert_called_once()
