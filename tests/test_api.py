import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from pc_advisor.api import app
import os

os.environ["OPENAI_API_KEY"] = "test-key"

client = TestClient(app)

class TestAPI:


    @patch('pc_advisor.dataset.DatabaseLoader')
    def test_get_parts_database_error(self, mock_loader_class):
        mock_loader = Mock()
        mock_loader_class.return_value = mock_loader
        mock_loader.get_all.side_effect = Exception('DB Error')
        
        response = client.get('/parts/gpuu')
        
        assert response.status_code == 200
        data = response.json()
        assert 'error' in data
        assert data['error'] == 'Invalid category'

    @patch('pc_advisor.dataset.mysql.connector.connect')
    @patch('pc_advisor.dataset.DatabaseLoader')
    @patch('pc_advisor.api.run_compatibility_check')
    def test_compatibility_endpoint(self, mock_run_compat, mock_loader_class, mock_connect):
        mock_run_compat.return_value = []
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        mock_loader = Mock()
        mock_loader_class.return_value = mock_loader
        mock_loader.search.return_value = []  # Mock empty search results
        
        payload = {
            "selected": {
                "CPU": "Intel i5",
                "Motherboard": "Test Board",
                "_use_case": "Gaming",
                "Budget": "$1000",
                "Mode": "Full PC build"
            }
        }
        
        response = client.post('/compatibility', json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert 'compat_issues' in data


    @patch('pc_advisor.dataset.mysql.connector.connect')
    @patch('pc_advisor.dataset.DatabaseLoader')
    @patch('pc_advisor.api.run_compatibility_check')
    @patch('pc_advisor.api.get_recommendations')
    def test_run_endpoint(self, mock_get_rec, mock_run_compat, mock_loader_class, mock_connect):
        mock_run_compat.return_value = []
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        
        mock_loader = Mock()
        mock_loader_class.return_value = mock_loader
        mock_loader.search.return_value = []
        mock_get_rec.return_value = "Test AI response"
        
        payload = {
            "selected": {
                "CPU": "Intel i5",
                "_use_case": "Gaming",
                "Budget": "$1000",
                "Mode": "Full PC build"
            }
        }
        
        response = client.post('/run', json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert 'compat_issues' in data
        assert 'ai_output' in data