# src/integration/test_system_integration.py
"""Integration tests for system components."""
import unittest
from unittest.mock import Mock, patch
from pathlib import Path
from ..core.mcp_controller import MCPController
from ..utils.error_handler import ErrorHandler
from ..utils.scaling_manager import ScalingManager
from ..config.settings import Settings

class TestSystemIntegration(unittest.TestCase):
    """Integration test suite for system components."""
    
    def setUp(self):
        self.settings = Settings().get_default_settings()
        self.error_handler = ErrorHandler(self.settings['error_handling'])
        self.scaling_manager = ScalingManager(self.settings['scaling'])
        self.controller = MCPController()
        
    def test_system_startup_sequence(self):
        """Test complete system startup sequence."""
        # Test MCP controller initialization
        self.assertTrue(self.controller.initialize(self.settings))
        
        # Test agent creation and deployment
        agent_id = self.controller.create_agent('trading', {})
        self.assertIsNotNone(agent_id)
        
        # Test error handling integration
        error_data = {'type': 'test', 'message': 'Test error'}
        result = self.error_handler.handle_error(error_data)
        self.assertEqual(result['status'], 'handled')
        
        # Test scaling evaluation
        metrics = self.scaling_manager.evaluate_scaling({})
        self.assertIn('scaling_decision', metrics)
        
    @patch('requests.post')
    def test_web_integration(self, mock_post):
        """Test web integration components."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'success'}
        mock_post.return_value = mock_response
        
        # Test error reporting
        error_data = {'type': 'test', 'message': 'Test error'}
        result = self.error_handler.handle_error(error_data)
        self.assertEqual(result['status'], 'handled')
        
        # Test scaling evaluation with web metrics
        metrics = self.scaling_manager.evaluate_scaling({
            'web_traffic': 1000,
            'revenue': 100.0
        })
        self.assertIn('revenue_projection', metrics)
