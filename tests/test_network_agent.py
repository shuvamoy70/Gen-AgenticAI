"""
Tests for the NetworkAgent class.
"""
import pytest
from unittest.mock import MagicMock, patch

from app.agents.network_agent import NetworkAgent
from app.models.model_manager import ModelManager
from app.tools.network_tools import NetworkTools

class TestNetworkAgent:
    """Test suite for the NetworkAgent class."""
    
    @pytest.fixture
    def mock_model_manager(self):
        """Create a mock ModelManager."""
        mock = MagicMock(spec=ModelManager)
        mock.generate_text.return_value = "This is a mock response."
        return mock
    
    @pytest.fixture
    def mock_network_tools(self):
        """Create a mock NetworkTools."""
        mock = MagicMock(spec=NetworkTools)
        # Set up return values for the mock methods
        mock.analyze_traffic.return_value = {"total_traffic": "500 Mbps", "unusual_patterns": False}
        mock.detect_anomalies.return_value = {"anomalies_detected": False, "anomalies": []}
        mock.check_health.return_value = {"overall_status": "healthy", "components": []}
        mock.diagnose_issue.return_value = {"possible_issues": []}
        mock.search_knowledge_base.return_value = {"results": []}
        mock.suggest_solutions.return_value = {"solutions": []}
        mock.classify_query.return_value = {"top_category": "general", "confidence": 0.8}
        return mock
    
    @pytest.fixture
    def agent(self, mock_model_manager, mock_network_tools):
        """Create a NetworkAgent with mock dependencies."""
        with patch('app.agents.network_agent.ModelManager', return_value=mock_model_manager):
            with patch('app.agents.network_agent.NetworkTools', return_value=mock_network_tools):
                return NetworkAgent(model_name="mock_model")
    
    def test_init(self, agent, mock_model_manager, mock_network_tools):
        """Test that the agent initializes correctly."""
        assert agent.model_manager == mock_model_manager
        assert agent.tools == mock_network_tools
        assert agent.memory == []
    
    def test_plan_troubleshooting(self, agent):
        """Test planning for troubleshooting queries."""
        plan = agent._plan("We have a problem with our network")
        assert "diagnose_issue" in plan
        assert "search_knowledge_base" in plan
        assert "suggest_solutions" in plan
    
    def test_plan_monitoring(self, agent):
        """Test planning for monitoring queries."""
        plan = agent._plan("Can you detect any anomalies in our network?")
        assert "analyze_network_traffic" in plan
        assert "detect_anomalies" in plan
    
    def test_plan_maintenance(self, agent):
        """Test planning for maintenance queries."""
        plan = agent._plan("What maintenance should we do to prevent issues?")
        assert "check_network_health" in plan
        assert "predict_failures" in plan
        assert "suggest_maintenance" in plan
    
    def test_execute_plan(self, agent, mock_network_tools):
        """Test executing a plan."""
        plan = ["analyze_network_traffic", "detect_anomalies"]
        results = agent._execute_plan(plan, "Check for anomalies")
        
        assert "steps_executed" in results
        assert results["steps_executed"] == plan
        assert "tools_output" in results
        assert "analyze_network_traffic" in results["tools_output"]
        assert "detect_anomalies" in results["tools_output"]
        
        # Verify that the tools were called
        mock_network_tools.analyze_traffic.assert_called_once()
        mock_network_tools.detect_anomalies.assert_called_once()
    
    def test_formulate_response(self, agent, mock_model_manager):
        """Test formulating a response."""
        plan_results = {
            "steps_executed": ["analyze_network_traffic", "detect_anomalies"],
            "tools_output": {
                "analyze_network_traffic": {"total_traffic": "500 Mbps"},
                "detect_anomalies": {"anomalies_detected": False, "recommendations": ["Keep monitoring"]}
            }
        }
        
        response = agent._formulate_response(plan_results, "Check for anomalies")
        
        assert "answer" in response
        assert "reasoning" in response
        assert "actions" in response
        assert response["answer"] == "This is a mock response."
        assert "analyze_network_traffic" in response["reasoning"]
        assert "detect_anomalies" in response["reasoning"]
        assert "Keep monitoring" in response["actions"]
        
        # Verify that the model was called
        mock_model_manager.generate_text.assert_called_once()
    
    def test_process_query(self, agent):
        """Test processing a full query."""
        response = agent.process_query("Check our network health")
        
        assert "answer" in response
        assert "reasoning" in response
        assert "actions" in response
        
        # Verify that the memory was updated
        assert len(agent.memory) == 2
        assert agent.memory[0]["role"] == "user"
        assert agent.memory[0]["content"] == "Check our network health"
        assert agent.memory[1]["role"] == "assistant"
        assert agent.memory[1]["content"] == response["answer"]
