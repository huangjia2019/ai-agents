#!/usr/bin/env python
import os
import subprocess
import sys
import argparse
from pathlib import Path

def main():
    # LangSmith suite / project name
    langsmith_project = "E-mail Tool Calling and Response Evaluation"

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run tests for email assistant implementations")
    parser.add_argument("--rich-output", action="store_true", help="[DEPRECATED] LangSmith output is now enabled by default")
    parser.add_argument("--experiment-name", help="Name for the LangSmith experiment")
    parser.add_argument("--implementation", help="Run tests for a specific implementation")
    parser.add_argument("--all", action="store_true", help="Run tests for all implementations")
    args = parser.parse_args()
    
    # Base pytest options
    base_pytest_options = ["-v", "--disable-warnings", "--langsmith-output"]
    # The --langsmith-output flag is now enabled by default for all test runs
    # The --rich-output flag is kept for backward compatibility
    
    # Define available implementations
    # Note: email_assistant_hitl and email_assistant_hitl_memory are not included because:
    # 1. They include the Question tool, which is not included in our evaluation dataset ground truth
    # 2. The hardcoded resume_command = Command(resume=[{"type": "accept", "args": ""}]) in test_response.py
    #    is invalid when the Question tool is encountered, causing the test to loop indefinitely
    # These implementations would need updated test datasets and handling logic to be testable
    implementations = [
        "email_assistant",
    ]
    
    # Determine which implementations to test
    if args.implementation:
        if args.implementation in implementations:
            implementations_to_test = [args.implementation]
        else:
            print(f"Error: Unknown implementation '{args.implementation}'")
            print(f"Available implementations: {', '.join(implementations)}")
            return 1
    elif args.all:
        implementations_to_test = implementations
    else:
        # Default to testing all implementations
        implementations_to_test = implementations
    
    # Run tests for each implementation
    for implementation in implementations_to_test:
        print(f"\nRunning tests for {implementation}...")
        
        # Set up LangSmith environment for this implementation
        os.environ["LANGSMITH_PROJECT"] = langsmith_project
        os.environ["LANGSMITH_TEST_SUITE"] = langsmith_project
        
        # Ensure tracing is enabled
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        
        # Create a fresh copy of the pytest options for this run
        pytest_options = base_pytest_options.copy()
        
        # Add the module parameter for this specific implementation
        module_param = f"--agent-module={implementation}"
        pytest_options.append(module_param)
        
        # Determine which test files to run based on implementation
        test_files = ["test_response.py"]  # All implementations run response tests
                    
        # Run each test file
        print(f"   Project: {langsmith_project}")
        print(f"\nℹ️ Test results for {implementation} are being logged to LangSmith")
        for test_file in test_files:
            print(f"\nRunning {test_file} for {implementation}...")
            experiment_name = f"Test: {test_file.split('/')[-1]} | Agent: {implementation}"
            print(f"   Experiment: {experiment_name}")
            os.environ["LANGSMITH_EXPERIMENT"] = experiment_name
            
            # Run pytest from the tests directory
            cmd = ["python", "-m", "pytest", test_file] + pytest_options
            
            # Change to the script's directory to ensure correct imports
            script_dir = Path(__file__).parent
            cwd = os.getcwd()
            os.chdir(script_dir)
            result = subprocess.run(cmd, capture_output=True, text=True)
            os.chdir(cwd)  # Restore original working directory
            
            # Print test output
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
                
if __name__ == "__main__":
    sys.exit(main() or 0)