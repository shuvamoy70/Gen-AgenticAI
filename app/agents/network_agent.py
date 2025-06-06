"""
Network Agent Module

This module defines the NetworkAgent class, which is responsible for processing
network-related queries and taking appropriate actions.
"""
import json
from typing import Dict, List, Any

from app.models.model_manager import ModelManager
from app.tools.network_tools import NetworkTools
from app.chains.network_analysis_chain import NetworkAnalysisChain
from app.utils.logger import get_logger
from app.utils.config import get_setting

logger = get_logger(__name__)

class NetworkAgent:
    """
    An agentic AI assistant specialized in network management and troubleshooting.

    This agent uses a combination of NLP models and specialized tools to:
    1. Understand user queries about network issues
    2. Plan a sequence of steps to address the query
    3. Execute relevant tools and gather information
    4. Formulate a comprehensive response
    """

    def __init__(self, model_name: str = None):
        """
        Initialize the NetworkAgent with specified models and tools.

        Args:
            model_name: The name of the Hugging Face model to use. If None, uses the default from config.
        """
        # Get agent settings from config
        agent_config = get_setting('agent', {})
        models_config = get_setting('models', {})

        # Use provided model_name or get default from config
        if model_name is None:
            default_model = "HuggingFace/distilbert-base-uncased"
            if models_config and 'default' in models_config:
                default_model = models_config['default']
            model_name = default_model

        # Initialize components
        self.model_manager = ModelManager(model_name)
        self.tools = NetworkTools()
        self.analysis_chain = NetworkAnalysisChain(self.model_manager)

        # Set up memory with configured limit
        self.memory = []  # Simple memory to store conversation history
        self.memory_limit = 10
        if agent_config and 'memory_limit' in agent_config:
            self.memory_limit = agent_config['memory_limit']

        # Log initialization
        logger.info(f"NetworkAgent initialized with model: {model_name}")

    def _plan(self, query: str) -> List[str]:
        """
        Generate a plan of actions based on the user query.

        Args:
            query: The user's input query

        Returns:
            A list of action steps to address the query
        """
        # In a real implementation, this would use the model to generate a plan
        # For now, we'll use a simple rule-based approach

        query_lower = query.lower()

        # Get agent settings from config
        agent_config = get_setting('agent', {})
        use_advanced_chain = False
        if agent_config and 'use_advanced_chain' in agent_config:
            use_advanced_chain = agent_config['use_advanced_chain']

        # Check if the query is complex enough to use the analysis chain
        is_complex = len(query.split()) > 10 or '?' in query

        # Use the analysis chain for complex queries if enabled
        if use_advanced_chain and is_complex:
            logger.info("Using NetworkAnalysisChain for complex query")
            return ["use_analysis_chain"]

        # Otherwise use the simple rule-based approach
        if "anomaly" in query_lower or "unusual" in query_lower:
            return ["analyze_network_traffic", "detect_anomalies", "generate_report"]
        elif "maintenance" in query_lower or "prevent" in query_lower:
            return ["check_network_health", "predict_failures", "suggest_maintenance"]
        elif "troubleshoot" in query_lower or "problem" in query_lower or "issue" in query_lower:
            return ["diagnose_issue", "search_knowledge_base", "suggest_solutions"]
        else:
            return ["classify_query", "search_knowledge_base", "generate_response"]

    def _execute_plan(self, plan: List[str], query: str) -> Dict[str, Any]:
        """
        Execute the generated plan by calling appropriate tools.

        Args:
            plan: List of action steps to execute
            query: The original user query

        Returns:
            Results from executing the plan
        """
        results = {
            "steps_executed": plan,
            "tools_output": {}
        }

        for step in plan:
            # Special case for the analysis chain
            if step == "use_analysis_chain":
                # Run the full analysis chain
                chain_results = self.analysis_chain.run(query)

                # Store the chain results in the tools_output
                results["chain_output"] = chain_results

                # Also store individual components for compatibility
                if "classification" in chain_results:
                    results["tools_output"]["classify_query"] = chain_results["classification"]
                if "data" in chain_results:
                    for data_key, data_value in chain_results["data"].items():
                        results["tools_output"][data_key] = data_value
                if "recommendations" in chain_results:
                    results["tools_output"]["recommendations"] = {
                        "timestamp": chain_results.get("timestamp", ""),
                        "recommendations": chain_results["recommendations"]
                    }
            # Map steps to tool functions
            elif step == "analyze_network_traffic":
                results["tools_output"][step] = self.tools.analyze_traffic()
            elif step == "detect_anomalies":
                results["tools_output"][step] = self.tools.detect_anomalies()
            elif step == "check_network_health":
                results["tools_output"][step] = self.tools.check_health()
            elif step == "predict_failures":
                results["tools_output"][step] = self.tools.predict_failures()
            elif step == "diagnose_issue":
                results["tools_output"][step] = self.tools.diagnose_issue(query)
            elif step == "search_knowledge_base":
                results["tools_output"][step] = self.tools.search_knowledge_base(query)
            elif step == "suggest_solutions":
                results["tools_output"][step] = self.tools.suggest_solutions(query)
            elif step == "generate_report":
                results["tools_output"][step] = self.tools.generate_report()
            elif step == "suggest_maintenance":
                results["tools_output"][step] = self.tools.suggest_maintenance()
            elif step == "classify_query":
                results["tools_output"][step] = self.tools.classify_query(query)
            elif step == "generate_response":
                # This will be handled in the process_query method
                pass

        return results

    def _formulate_response(self, plan_results: Dict[str, Any], query: str) -> Dict[str, Any]:
        """
        Formulate a comprehensive response based on the plan execution results.

        Args:
            plan_results: Results from executing the plan
            query: The original user query

        Returns:
            A structured response including answer, reasoning, and actions
        """
        # In a real implementation, this would use the model to generate a coherent response
        # based on the results of the executed plan

        # Check if we used the analysis chain
        if "chain_output" in plan_results:
            # Use the analysis chain results directly
            chain_output = plan_results["chain_output"]

            # Extract the analysis summary
            analysis = chain_output.get("analysis", {})
            summary = analysis.get("summary", "Analysis not available")

            # Generate a response using the model with the analysis
            context = json.dumps(chain_output)
            response_text = self.model_manager.generate_text(
                prompt=f"Query: {query}\nAnalysis: {summary}\nContext: {context}\nProvide a detailed and helpful response."
            )

            # Use the recommendations from the chain
            actions = chain_output.get("recommendations", [])

            # Add reasoning from the analysis
            reasoning = f"I analyzed your query using our network analysis chain. {summary}"
            if "potential_causes" in analysis:
                causes = analysis["potential_causes"]
                if causes:
                    reasoning += f" Potential causes include: {', '.join(causes)}"
        else:
            # Extract relevant information from plan results
            tools_output = plan_results["tools_output"]
            steps = plan_results["steps_executed"]

            # Generate a response using the model
            context = json.dumps(tools_output)
            response_text = self.model_manager.generate_text(
                prompt=f"Query: {query}\nContext: {context}\nProvide a helpful response."
            )

            # Extract recommended actions
            actions = []
            for _, output in tools_output.items():  # Use _ for unused variable
                if "recommendations" in output:
                    actions.extend(output["recommendations"])

            # Generate reasoning based on the steps executed
            reasoning = f"I analyzed your query by following these steps: {', '.join(steps)}"

        return {
            "answer": response_text,
            "reasoning": reasoning,
            "actions": actions if actions else ["No specific actions recommended at this time."]
        }

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query through the full agent pipeline.

        Args:
            query: The user's input query

        Returns:
            A structured response to the query
        """
        logger.info(f"Processing query: {query}")

        # Add query to memory and respect memory limit
        self.memory.append({"role": "user", "content": query})

        # Trim memory if it exceeds the limit
        if len(self.memory) > self.memory_limit * 2:  # *2 because each exchange has user and assistant messages
            # Keep only the most recent exchanges
            self.memory = self.memory[-(self.memory_limit * 2):]

        # 1. Generate a plan
        plan = self._plan(query)
        logger.debug(f"Generated plan: {plan}")

        # 2. Execute the plan
        plan_results = self._execute_plan(plan, query)
        logger.debug(f"Plan execution results: {plan_results}")

        # 3. Formulate a response
        response = self._formulate_response(plan_results, query)
        logger.info(f"Generated response for query")

        # Add response to memory
        self.memory.append({"role": "assistant", "content": response["answer"]})

        return response
