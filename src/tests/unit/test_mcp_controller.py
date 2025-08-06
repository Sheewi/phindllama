# src/tests/unit/test_mcp_controller.py
"""Unit tests for MCP controller."""
import unittest
from unittest.mock import Mock, patch
from ..core.mcp_controller import MCPController
from ..utils.error_handler import ErrorHandler

class TestMCPController(unittest.TestCase):
    """Test suite for MCPController."""
    
    def setUp(self):
        self.error_handler = ErrorHandler({})
        self.controller = MCPController()
        
    def test_agent_creation(self):
        """Test agent creation functionality."""
        agent_id = self.controller.create_agent('trading', {})
        self.assertIsNotNone(agent_id)
        self.assertIn(agent_id, self.controller.active_agents)
        
    @patch('requests.post')
    def test_web_error_reporting(self, mock_post):
        """Test web-based error reporting."""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'reward': 0.1}
        
        error_data = {'type': 'test', 'message': 'Test error'}
        result = self.error_handler.handle_error(error_data)
        
        self.assertEqual(result['revenue_generated']['amount'], 0.1)
        self.assertEqual(result['revenue_generated']['currency'], 'ETH')
