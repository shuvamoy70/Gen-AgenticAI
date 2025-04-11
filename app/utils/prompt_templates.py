"""
Prompt Templates Module

This module provides templates for prompts used with language models.
"""
from typing import Dict, List, Any, Optional

class PromptTemplates:
    """
    A collection of prompt templates for various tasks.
    
    These templates are used to format inputs for language models
    in a consistent and effective way.
    """
    
    @staticmethod
    def network_diagnosis(symptoms: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a prompt for network issue diagnosis.
        
        Args:
            symptoms: Description of the network symptoms
            context: Optional additional context
            
        Returns:
            Formatted prompt string
        """
        context_str = ""
        if context:
            context_str = "\nAdditional context:\n"
            for key, value in context.items():
                context_str += f"- {key}: {value}\n"
        
        return f"""You are an expert network diagnostician. Based on the following symptoms, diagnose the most likely network issues.

Symptoms:
{symptoms}
{context_str}
Provide a detailed analysis of the potential causes and recommended solutions. Format your response as:

Diagnosis:
[Your diagnosis here]

Potential Causes:
- [Cause 1]
- [Cause 2]
...

Recommended Solutions:
1. [Solution 1]
2. [Solution 2]
...

Severity: [Low/Medium/High/Critical]
"""

    @staticmethod
    def network_planning(requirements: str, constraints: Optional[str] = None) -> str:
        """
        Create a prompt for network planning.
        
        Args:
            requirements: Network requirements
            constraints: Optional constraints
            
        Returns:
            Formatted prompt string
        """
        constraints_str = f"\nConstraints:\n{constraints}" if constraints else ""
        
        return f"""You are an expert network architect. Design a network solution based on the following requirements.

Requirements:
{requirements}
{constraints_str}

Provide a detailed network design including:

Architecture Overview:
[Overview description]

Components:
- [Component 1]: [Description]
- [Component 2]: [Description]
...

Network Topology:
[Topology description]

Security Considerations:
- [Security measure 1]
- [Security measure 2]
...

Implementation Steps:
1. [Step 1]
2. [Step 2]
...

Estimated Costs and Resources:
[Cost and resource estimates]
"""

    @staticmethod
    def anomaly_detection(network_data: str, historical_context: Optional[str] = None) -> str:
        """
        Create a prompt for network anomaly detection.
        
        Args:
            network_data: Current network data
            historical_context: Optional historical context
            
        Returns:
            Formatted prompt string
        """
        historical_str = f"\nHistorical Context:\n{historical_context}" if historical_context else ""
        
        return f"""You are an expert in network security and anomaly detection. Analyze the following network data to identify any anomalies or security concerns.

Current Network Data:
{network_data}
{historical_str}

Identify any anomalies, potential security threats, or unusual patterns in the data. Format your response as:

Anomalies Detected:
- [Anomaly 1]: [Description and significance]
- [Anomaly 2]: [Description and significance]
...

Risk Assessment:
[Overall risk assessment]

Recommended Actions:
1. [Action 1]
2. [Action 2]
...

Monitoring Recommendations:
- [Recommendation 1]
- [Recommendation 2]
...
"""

    @staticmethod
    def network_optimization(current_state: str, goals: str) -> str:
        """
        Create a prompt for network optimization.
        
        Args:
            current_state: Description of current network state
            goals: Optimization goals
            
        Returns:
            Formatted prompt string
        """
        return f"""You are an expert network optimization specialist. Recommend optimizations based on the current network state and goals.

Current Network State:
{current_state}

Optimization Goals:
{goals}

Provide detailed optimization recommendations. Format your response as:

Performance Analysis:
[Analysis of current performance bottlenecks]

Optimization Recommendations:
1. [Recommendation 1]: [Description and expected impact]
2. [Recommendation 2]: [Description and expected impact]
...

Implementation Priority:
- High Priority: [List high priority optimizations]
- Medium Priority: [List medium priority optimizations]
- Low Priority: [List low priority optimizations]

Expected Outcomes:
[Description of expected improvements after implementation]

Monitoring Metrics:
- [Metric 1]: [Description and target values]
- [Metric 2]: [Description and target values]
...
"""

    @staticmethod
    def network_troubleshooting(issue_description: str, steps_taken: Optional[str] = None) -> str:
        """
        Create a prompt for network troubleshooting.
        
        Args:
            issue_description: Description of the network issue
            steps_taken: Optional steps already taken
            
        Returns:
            Formatted prompt string
        """
        steps_str = f"\nSteps Already Taken:\n{steps_taken}" if steps_taken else ""
        
        return f"""You are an expert network troubleshooter. Provide a systematic approach to troubleshoot and resolve the following network issue.

Issue Description:
{issue_description}
{steps_str}

Provide a systematic troubleshooting approach. Format your response as:

Initial Assessment:
[Your assessment of the issue]

Troubleshooting Steps:
1. [Step 1]: [Purpose and expected outcome]
2. [Step 2]: [Purpose and expected outcome]
...

Potential Root Causes:
- [Cause 1]: [Explanation]
- [Cause 2]: [Explanation]
...

Resolution Recommendations:
1. [Recommendation 1]
2. [Recommendation 2]
...

Prevention Measures:
- [Measure 1]: [How it prevents recurrence]
- [Measure 2]: [How it prevents recurrence]
...
"""
