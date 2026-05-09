import pytest
import os
os.environ["OPENAI_API_KEY"] = "test-key"
from unittest.mock import Mock, patch
from pc_advisor.dataset import DatabaseLoader, PartMatch

class TestDatabaseLoader:

    @patch('pc_advisor.dataset.mysql.connector.connect')
    def test_init(self, mock_connect):
        mock_conn = Mock()
        mock_connect.return_value = mock_conn
        
        loader = DatabaseLoader()
        
        mock_connect.assert_called_once()
        assert loader.conn == mock_conn

    @patch('pc_advisor.dataset.mysql.connector.connect')
    def test_search_with_query(self, mock_connect):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'name': 'Test CPU', 'price': 299.99, 'id': 1, 'core_count': 8}
        ]
        mock_connect.return_value = mock_conn
        
        loader = DatabaseLoader()
        results = loader.search('cpus', 'test')
        
        assert len(results) == 1
        assert results[0].name == 'Test CPU'
        assert results[0].price == 299.99
        assert results[0].data == {'name': 'Test CPU', 'price': 299.99, 'id': 1, 'core_count': 8}
        
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        expected_sql = """
            SELECT *
            FROM `cpus`
            WHERE LOWER(name) LIKE %s
            LIMIT %s
        """
        assert call_args[0] == expected_sql
        assert call_args[1] == ('%test%', 5)

    @patch('pc_advisor.dataset.mysql.connector.connect')
    def test_search_no_query(self, mock_connect):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        loader = DatabaseLoader()
        results = loader.search('cpus', '')
        
        assert results == []
        mock_cursor.execute.assert_not_called()

    @patch('pc_advisor.dataset.mysql.connector.connect')
    def test_top(self, mock_connect):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'name': 'Top Item', 'price': None, 'id': 3}
        ]
        mock_connect.return_value = mock_conn
        
        loader = DatabaseLoader()
        results = loader.top('cases')
        
        assert len(results) == 1
        assert results[0].name == 'Top Item'
        assert results[0].price is None
        
        mock_cursor.execute.assert_called_once_with('SELECT * FROM `cases` LIMIT %s', (5,))

    @patch('pc_advisor.dataset.mysql.connector.connect')
    def test_get_all(self, mock_connect):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'name': 'Item 1', 'price': 100.0},
            {'name': 'Item 2', 'price': 200.0}
        ]
        mock_connect.return_value = mock_conn
        
        loader = DatabaseLoader()
        results = loader.get_all('monitors')
        
        assert len(results) == 2
        assert results[0]['name'] == 'Item 1'
        assert results[1]['price'] == 200.0
        
        mock_cursor.execute.assert_called_once_with('SELECT * FROM `monitors`')