#!/usr/bin/env python
import os
import sys
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from pathlib import Path
import pytest

NOTEBOOKS_DIR = Path(__file__).parent.parent / "notebooks"

# Skip notebooks that require specific setup or take too long to execute in automated tests
SKIP_NOTEBOOKS = []

def get_notebooks():
    """Get all notebook paths except those in the skip list."""
    notebooks = []
    for nb_path in NOTEBOOKS_DIR.glob("**/*.ipynb"):
        if nb_path.name not in SKIP_NOTEBOOKS and not nb_path.name.startswith("."):
            notebooks.append(nb_path)
    return notebooks

@pytest.mark.parametrize("notebook_path", get_notebooks())
def test_notebook_runs_without_errors(notebook_path):
    """Test that a notebook runs without errors."""
    # Check if notebook exists
    if not notebook_path.exists():
        pytest.skip(f"Notebook {notebook_path} does not exist")
    
    print(f"Testing notebook: {notebook_path}")
    
    # Read the notebook
    with open(notebook_path, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    
    # Create executor
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    
    try:
        # Execute the notebook
        ep.preprocess(nb, {"metadata": {"path": notebook_path.parent}})
    except Exception as e:
        # Get the cell that caused the error
        for cell in nb.cells:
            if hasattr(cell, "outputs"):
                for output in cell.outputs:
                    if output.output_type == "error":
                        error_message = "\n".join(output.traceback)
                        pytest.fail(f"Error in notebook {notebook_path}: {error_message}")
        # If we couldn't find the error in the notebook, raise the original exception
        pytest.fail(f"Error in notebook {notebook_path}: {str(e)}")

if __name__ == "__main__":
    # This allows the script to be run directly
    notebooks = get_notebooks()
    for notebook in notebooks:
        try:
            test_notebook_runs_without_errors(notebook)
            print(f"✅ {notebook.name} passed")
        except Exception as e:
            print(f"❌ {notebook.name} failed: {str(e)}")
            sys.exit(1)
    print(f"All {len(notebooks)} notebooks executed successfully!")