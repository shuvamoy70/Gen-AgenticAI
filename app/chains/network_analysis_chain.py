"""
Network Analysis Chain Module

This module defines a multi-step chain for analyzing network issues,
similar to LangChain's sequential chains.
"""
from typing import Dict, List, Any, Optional

from app.models.model_manager import ModelManager
from app.tools.network_tools import NetworkTools
from app.utils.logger import get_logger

logger = get_logger(__name__)

class NetworkAnalysisChain:
    """
    A multi-step chain for analyzing network issues.
    
    This chain follows these steps:
    1. Classify the query to determine the type of network issue
    2. Gather relevant data using appropriate tools
    3. Analyze the data to identify potential causes
    4. Generate recommendations based on the analysis
    """
    
    def __init__(self, model_manager: ModelManager):
        """
        Initialize the NetworkAnalysisChain.
        
        Args:
            model_manager: The ModelManager instance to use for text processing
        """
        self.model_manager = model_manager
        self.tools = NetworkTools()
        logger.info("NetworkAnalysisChain initialized")
    
    def run(self, query: str) -> Dict[str, Any]:
        """
        Run the full analysis chain on a user query.
        
        Args:
            query: The user's query about a network issue
            
        Returns:
            The results of the analysis chain
        """
        logger.info(f"Running network analysis chain for query: {query}")
        
        # Step 1: Classify the query
        classification = self.tools.classify_query(query)
        top_category = classification["top_category"]
        logger.debug(f"Query classified as: {top_category}")
        
        # Step 2: Gather relevant data based on the category
        data = self._gather_data(query, top_category)
        logger.debug(f"Gathered data for {top_category}")
        
        # Step 3: Analyze the data
        analysis = self._analyze_data(query, data, top_category)
        logger.debug("Data analysis completed")
        
        # Step 4: Generate recommendations
        recommendations = self._generate_recommendations(query, analysis, top_category)
        logger.debug("Recommendations generated")
        
        # Combine all results
        return {
            "query": query,
            "classification": classification,
            "data": data,
            "analysis": analysis,
            "recommendations": recommendations
        }
    
    def _gather_data(self, query: str, category: str) -> Dict[str, Any]:
        """
        Gather relevant data based on the query category.
        
        Args:
            query: The user's query
            category: The category of the query
            
        Returns:
            The gathered data
        """
        data = {}
        
        if category == "troubleshooting":
            data["diagnosis"] = self.tools.diagnose_issue(query)
            data["knowledge_base"] = self.tools.search_knowledge_base(query)
        
        elif category == "monitoring":
            data["traffic"] = self.tools.analyze_traffic()
            data["anomalies"] = self.tools.detect_anomalies()
        
        elif category == "maintenance":
            data["health"] = self.tools.check_health()
            data["predictions"] = self.tools.predict_failures()
        
        elif category == "configuration":
            # For configuration queries, we might need different tools
            # For now, just use the knowledge base
            data["knowledge_base"] = self.tools.search_knowledge_base(query)
        
        else:  # general or unknown category
            # Gather a bit of everything
            data["traffic"] = self.tools.analyze_traffic()
            data["health"] = self.tools.check_health()
            data["knowledge_base"] = self.tools.search_knowledge_base(query)
        
        return data
    
    def _analyze_data(self, query: str, data: Dict[str, Any], category: str) -> Dict[str, Any]:
        """
        Analyze the gathered data to identify potential causes.
        
        Args:
            query: The user's query
            data: The gathered data
            category: The category of the query
            
        Returns:
            The analysis results
        """
        analysis = {
            "summary": "",
            "potential_causes": [],
            "severity": "unknown"
        }
        
        # In a real implementation, this would use the model to analyze the data
        # For now, we'll use a simple rule-based approach
        
        if category == "troubleshooting":
            if "diagnosis" in data:
                diagnosis = data["diagnosis"]
                possible_issues = diagnosis.get("possible_issues", [])
                
                if possible_issues:
                    # Extract potential causes from the knowledge base
                    top_issue = possible_issues[0]["issue"]
                    for entry in data.get("knowledge_base", {}).get("results", []):
                        if entry["issue"] == top_issue:
                            analysis["potential_causes"] = entry.get("causes", [])
                            break
                    
                    # Set severity based on confidence
                    confidence = possible_issues[0].get("confidence", 0)
                    if confidence > 0.8:
                        analysis["severity"] = "high"
                    elif confidence > 0.5:
                        analysis["severity"] = "medium"
                    else:
                        analysis["severity"] = "low"
                    
                    # Generate summary
                    analysis["summary"] = f"The issue appears to be related to {top_issue} with {confidence:.0%} confidence."
        
        elif category == "monitoring":
            if "anomalies" in data and data["anomalies"].get("anomalies_detected"):
                anomalies = data["anomalies"].get("anomalies", [])
                
                if anomalies:
                    # Extract potential causes based on anomaly types
                    for anomaly in anomalies:
                        if anomaly["type"] == "traffic spike":
                            analysis["potential_causes"].append("Possible DDoS attack or traffic surge")
                        elif anomaly["type"] == "new connection pattern":
                            analysis["potential_causes"].append("Potential unauthorized access attempt")
                    
                    # Set severity based on anomaly severity
                    severities = [a.get("severity") for a in anomalies]
                    if "high" in severities:
                        analysis["severity"] = "high"
                    elif "medium" in severities:
                        analysis["severity"] = "medium"
                    else:
                        analysis["severity"] = "low"
                    
                    # Generate summary
                    analysis["summary"] = f"Detected {len(anomalies)} anomalies in network traffic that require attention."
            else:
                analysis["summary"] = "No significant anomalies detected in network traffic."
                analysis["severity"] = "low"
        
        elif category == "maintenance":
            if "health" in data:
                components = data["health"].get("components", [])
                warning_components = [c for c in components if c.get("status") == "warning"]
                
                if warning_components:
                    # Extract potential causes based on component warnings
                    for component in warning_components:
                        analysis["potential_causes"].append(f"{component['name']} showing warning signs")
                    
                    # Set severity
                    analysis["severity"] = "medium"
                    
                    # Generate summary
                    analysis["summary"] = f"{len(warning_components)} out of {len(components)} components showing warning status."
                else:
                    analysis["summary"] = "All network components appear to be healthy."
                    analysis["severity"] = "low"
        
        else:  # general or configuration
            analysis["summary"] = "General network status appears normal with no critical issues detected."
            analysis["severity"] = "low"
        
        return analysis
    
    def _generate_recommendations(self, query: str, analysis: Dict[str, Any], category: str) -> List[str]:
        """
        Generate recommendations based on the analysis.
        
        Args:
            query: The user's query
            analysis: The analysis results
            category: The category of the query
            
        Returns:
            A list of recommendations
        """
        recommendations = []
        
        # Add recommendations based on severity
        severity = analysis.get("severity", "unknown")
        
        if severity == "high":
            recommendations.append("Immediate attention required to address the identified issues")
        elif severity == "medium":
            recommendations.append("Schedule maintenance within the next 24-48 hours")
        elif severity == "low":
            recommendations.append("Monitor the situation as part of regular maintenance")
        
        # Add specific recommendations based on category and potential causes
        potential_causes = analysis.get("potential_causes", [])
        
        if category == "troubleshooting":
            if "latency" in query.lower() or any("latency" in cause.lower() for cause in potential_causes):
                recommendations.extend([
                    "Check for bandwidth-intensive applications",
                    "Implement QoS (Quality of Service) policies",
                    "Optimize routing tables"
                ])
            elif "packet loss" in query.lower() or any("packet loss" in cause.lower() for cause in potential_causes):
                recommendations.extend([
                    "Check physical connections",
                    "Replace faulty hardware",
                    "Reduce network congestion"
                ])
        
        elif category == "monitoring":
            if any("DDoS" in cause for cause in potential_causes):
                recommendations.extend([
                    "Implement rate limiting",
                    "Configure firewall rules to block attack sources",
                    "Consider a DDoS protection service"
                ])
            elif any("unauthorized" in cause.lower() for cause in potential_causes):
                recommendations.extend([
                    "Review access control lists",
                    "Check for compromised credentials",
                    "Enable additional logging for suspicious activities"
                ])
        
        elif category == "maintenance":
            recommendations.extend([
                "Perform regular firmware updates on all network devices",
                "Schedule comprehensive network testing during off-hours",
                "Document all maintenance activities and outcomes"
            ])
        
        # Ensure we have at least some recommendations
        if not recommendations:
            recommendations = [
                "Conduct a thorough network assessment",
                "Review network documentation and configurations",
                "Consider consulting with a network specialist for further analysis"
            ]
        
        return recommendations
