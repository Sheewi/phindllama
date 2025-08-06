# src/integration/test_error_handling.py
"""Integration tests for error handling system."""
import unittest
from unittest.mock import Mock, patch
from pathlib import Path
from ..core.mcp_controller import MCPController
from ..utils.error_handler import ErrorHandler
from ..config.settings import Settings

class TestErrorHandling(unittest.TestCase):
    """Integration test suite for error handling system."""
    
    def setUp(self):
        self.settings = Settings().get_default_settings()
        self.error_handler = ErrorHandler(self.settings['error_handling'])
        self.controller = MCPController()
        
    def test_error_propagation(self):
        """Test error propagation through system components."""
        # Test MCP controller error handling
        with patch.object(self.error_handler, 'handle_error') as mock_handle:
            self.controller.initialize({'test_mode': True})
            
            # Simulate agent error
            error_data = {'type': 'agent_error', 'message': 'Test agent error'}
            result = self.error_handler.handle_error(error_data)
            
            mock_handle.assert_called_once()
            self.assertEqual(result['status'], 'handled')
            
    @patch('requests.post')
    def test_error_reporting(self, mock_post):
        """Test error reporting and revenue generation."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'reward': 0.1}
        mock_post.return_value = mock_response
        
        error_data = {'type': 'test', 'message': 'Test error'}
        result = self.error_handler.handle_error(error_data)
        
        self.assertEqual(result['revenue_generated']['amount'], 0.1)
        self.assertEqual(result['revenue_generated']['currency'], 'ETH')
