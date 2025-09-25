# Agents in this Repository

## Overview

This repository demonstrates building agents using LangGraph, focusing on an email assistant that can:
- Triage incoming emails
- Draft appropriate responses
- Execute actions (calendar scheduling, etc.)
- Incorporate human feedback
- Learn from past interactions

## Environment Setup

**Recommended: Using uv (faster and more reliable)**

```bash
# Install uv if you haven't already
pip install uv

# Install the package with development dependencies
uv sync --extra dev
```

**Alternative: Using pip**

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Ensure you have a recent version of pip (required for editable installs with pyproject.toml)
python3 -m pip install --upgrade pip

# Install the package in editable mode
pip install -e .
```

The package is installed as `interrupt_workshop` with import name `email_assistant`, allowing you to import from anywhere with `from email_assistant import ...`

## Agent Implementations

### Scripts 

The repository contains several implementations with increasing complexity in `src/email_assistant`:

1. **LangGraph 101** (`langgraph_101.py`)
   - Basics of LangGraph 

2. **Basic Email Assistant** (`email_assistant.py`)
   - Core email triage and response functionality

3. **Human-in-the-Loop** (`email_assistant_hitl.py`) 
   - Adds ability for humans to review and approve actions

4. **Memory-Enabled HITL** (`email_assistant_hitl_memory.py`)
   - Adds persistent memory to learn from feedback

5. **Gmail Integration** (`email_assistant_hitl_memory_gmail.py`)
   - Connects to Gmail API for real email processing

### Notebooks

Each aspect of the agent is explained in dedicated notebooks:
- `notebooks/langgraph_101.ipynb` - LangGraph basics
- `notebooks/agent.ipynb` - Basic agent implementation
- `notebooks/evaluation.ipynb` - Agent evaluation
- `notebooks/hitl.ipynb` - Human-in-the-loop functionality
- `notebooks/memory.ipynb` - Adding memory capabilities

## Running Tests

### Testing Scripts

Test to ensure all implementations work:

```bash
# Test all implementations
python tests/run_all_tests.py --all
```

(Note: This will leave out the Gmail implementation `email_assistant_hitl_memory_gmail` from testing.)

### Testing Notebooks

Test all notebooks to ensure they run without errors:

```bash
# Run all notebook tests directly
python tests/test_notebooks.py
```

