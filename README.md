# Network AI Assistant

An agentic AI solution for network management and troubleshooting using Hugging Face models.

## Overview

The Network AI Assistant is a professional-grade application that uses agentic AI to help network administrators and engineers with various network management tasks:

- **Network Anomaly Detection**: Identify unusual patterns in network traffic
- **Predictive Maintenance**: Forecast potential network issues before they occur
- **Automated Troubleshooting**: Diagnose and suggest solutions for common network problems

The application is built with a modular architecture that follows industry best practices for GenAI and agentic AI systems.

## Project Structure

```
genai-agent/
│
├── app/                        # Core application logic
│   ├── agents/                 # All agent logic (planning, memory, tools)
│   ├── models/                 # Model wrappers (HuggingFace)
│   ├── tools/                  # Tool functions (network analysis, diagnostics)
│   ├── chains/                 # Multi-step chain logic
│   └── utils/                  # Helper functions (logging, prompts, etc.)
│
├── config/                     # Config files
│   └── settings.yaml           # Application settings
│
├── data/                       # Local data
│   └── knowledge_base.json     # Network troubleshooting knowledge base
│
├── tests/                      # Unit and integration tests
│
├── notebooks/                  # Exploration and prototyping
│
├── requirements.txt            # Python dependencies
└── main.py                     # Entry point
```

## Features

- **Agentic Architecture**: Uses a planning-based agent that can reason about network issues and take appropriate actions
- **Hugging Face Integration**: Leverages free models from Hugging Face for natural language understanding and generation
- **Modular Design**: Clean separation of concerns with specialized modules for agents, models, tools, and utilities
- **Streamlit Interface**: Professional and intuitive user interface built with Streamlit
- **Extensible Framework**: Easy to add new capabilities, tools, and models

## Application Flow

The following flowchart illustrates the execution flow of the Network AI Assistant:

```
[User] → Streamlit Interface (main.py)
   │
   ▼
[main.py] → Initialize NetworkAgent
   │
   ├──► Initialize ModelManager
   │      │
   │      └──► Check for Transformers library
   │           └──► Load model if available, otherwise use mock
   │
   └──► Initialize NetworkTools
          └──► Load knowledge base

   │
   ▼
[User submits query]
   │
   ▼
[main.py] → Call agent.process_query(user_input)
   │
   ▼
[NetworkAgent.process_query]
   │
   ├──► Add query to memory
   │
   ├──► Call _plan(query) to generate plan
   │      │
   │      └──► Analyze query keywords
   │           └──► Return appropriate tool sequence
   │
   ├──► Call _execute_plan(plan, query)
   │      │
   │      └──► For each step in plan:
   │           │
   │           ├──► Map step to NetworkTools method
   │           │     │
   │           │     ├──► analyze_traffic()
   │           │     ├──► detect_anomalies()
   │           │     ├──► check_health()
   │           │     ├──► diagnose_issue(query)
   │           │     ├──► search_knowledge_base(query)
   │           │     └──► etc.
   │           │
   │           └──► Collect results from each tool
   │
   ├──► Call _formulate_response(plan_results, query)
   │      │
   │      ├──► Extract tool outputs
   │      │
   │      ├──► Call model_manager.generate_text()
   │      │     │
   │      │     └──► Generate response text using model or mock
   │      │
   │      ├──► Extract recommendations from tool outputs
   │      │
   │      └──► Return structured response
   │
   └──► Add response to memory

   │
   ▼
[main.py] → Display response in Streamlit UI
   │
   ├──► Display answer
   ├──► Display reasoning (in expandable section)
   └──► Display recommended actions
```

This flowchart shows how the application processes user queries through the agent's planning, execution, and response formulation phases.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd genai-agent
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

Start the Streamlit application:
```
streamlit run main.py
```

If you're in a directory with multiple Python files, use the full path:
```
streamlit run /path/to/genai-agent/main.py
```

The application will be available at http://localhost:8501

## Usage Examples

### Network Troubleshooting

Ask the agent about network issues:
```
"We're experiencing high latency on our east coast servers. What could be causing this and how can we fix it?"
```

### Network Monitoring

Request information about current network status:
```
"Can you analyze our current network traffic and identify any anomalies?"
```

### Predictive Maintenance

Get recommendations for preventive maintenance:
```
"What maintenance tasks should we prioritize for our network infrastructure this month?"
```

## Extending the Application

### Adding New Tools

1. Create a new tool function in `app/tools/`
2. Register the tool in the appropriate agent class
3. Update the agent's planning logic to use the new tool

### Using Different Models

1. Update the model name in `config/settings.yaml`
2. The ModelManager will handle loading the new model

## License

[MIT License](LICENSE)

## Acknowledgments

- Hugging Face for providing free, open-source models
- Streamlit for the excellent web application framework
