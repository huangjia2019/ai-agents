#!/usr/bin/env python

import pytest
import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

def pytest_addoption(parser):
    """Add command-line options to pytest."""
    parser.addoption(
        "--agent-module", 
        action="store", 
        default="email_assistant_hitl_memory",
        help="Specify which email assistant module to test"
    )

@pytest.fixture(scope="session")
def agent_module_name(request):
    """Return the agent module name from command line."""
    return request.config.getoption("--agent-module")