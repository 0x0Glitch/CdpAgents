#!/usr/bin/env python3
"""
Dual Chain Agent API Client

This script provides a simple command-line interface to interact with the
Dual Chain Agent API server. It allows submitting instructions and checking
results without having to make HTTP requests manually.
"""

import argparse
import json
import time
import sys
from typing import Dict, Any, Optional

import requests

# API base URL
API_BASE_URL = "http://localhost:8000"

def submit_instruction(instruction: str, chain_id: Optional[str] = None, timeout: int = 60) -> Dict[str, Any]:
    """
    Submit an instruction to the API.
    
    Args:
        instruction: The instruction text
        chain_id: Optional chain ID (84532 for Base, 11155420 for Optimism)
        timeout: Timeout in seconds for the instruction to complete
        
    Returns:
        The API response as a dictionary
    """
    payload = {
        "instruction": instruction,
        "timeout": timeout
    }
    
    if chain_id:
        payload["chain_id"] = chain_id
    
    response = requests.post(f"{API_BASE_URL}/instruction", json=payload)
    
    if response.status_code != 200:
        print(f"Error submitting instruction: {response.text}")
        sys.exit(1)
    
    return response.json()

def get_task_result(task_id: str) -> Dict[str, Any]:
    """
    Get the result of a task.
    
    Args:
        task_id: The task ID to check
        
    Returns:
        The task result as a dictionary
    """
    response = requests.get(f"{API_BASE_URL}/task/{task_id}")
    
    if response.status_code != 200:
        print(f"Error getting task result: {response.text}")
        sys.exit(1)
    
    return response.json()

def wait_for_task_completion(task_id: str, polling_interval: int = 1, max_wait_time: int = 300) -> Dict[str, Any]:
    """
    Wait for a task to complete and return the result.
    
    Args:
        task_id: The task ID to wait for
        polling_interval: How often to check in seconds
        max_wait_time: Maximum time to wait in seconds
        
    Returns:
        The final task result
    """
    start_time = time.time()
    
    while True:
        result = get_task_result(task_id)
        
        if result["status"] in ["completed", "failed"]:
            return result
        
        if time.time() - start_time > max_wait_time:
            print(f"Timeout waiting for task {task_id} to complete after {max_wait_time} seconds")
            sys.exit(1)
        
        print(f"Task {task_id} is still {result['status']}... waiting {polling_interval}s")
        time.sleep(polling_interval)

def get_all_tasks() -> Dict[str, Any]:
    """
    Get all tasks.
    
    Returns:
        A list of all tasks
    """
    response = requests.get(f"{API_BASE_URL}/tasks")
    
    if response.status_code != 200:
        print(f"Error getting tasks: {response.text}")
        sys.exit(1)
    
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="Client for the Dual Chain Agent API")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Submit instruction command
    submit_parser = subparsers.add_parser("submit", help="Submit an instruction")
    submit_parser.add_argument("instruction", help="The instruction to submit")
    submit_parser.add_argument("--chain", "--chain-id", dest="chain_id", 
                              help="Chain ID (84532 for Base, 11155420 for Optimism)")
    submit_parser.add_argument("--timeout", type=int, default=60,
                              help="Timeout in seconds for the instruction")
    submit_parser.add_argument("--wait", action="store_true", 
                              help="Wait for the result instead of just returning the task ID")
    
    # Get task result command
    get_parser = subparsers.add_parser("get", help="Get a task result")
    get_parser.add_argument("task_id", help="The task ID to check")
    
    # List all tasks command
    subparsers.add_parser("list", help="List all tasks")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "submit":
        task = submit_instruction(args.instruction, args.chain_id, args.timeout)
        print(f"Submitted task: {task['task_id']}")
        
        if args.wait:
            print("Waiting for result...")
            result = wait_for_task_completion(task["task_id"])
            
            if result["status"] == "completed":
                print("\n=== RESULT ===")
                print(result["result"])
            else:
                print(f"\nTask failed: {result['error']}")
        else:
            print(f"To check result: python {sys.argv[0]} get {task['task_id']}")
    
    elif args.command == "get":
        result = get_task_result(args.task_id)
        
        print(f"Task ID: {result['task_id']}")
        print(f"Status: {result['status']}")
        print(f"Chain ID: {result['chain_id']}")
        print(f"Instruction: {result['instruction']}")
        
        if result["status"] == "completed":
            print("\n=== RESULT ===")
            print(result["result"])
        elif result["status"] == "failed":
            print(f"\nError: {result['error']}")
    
    elif args.command == "list":
        tasks = get_all_tasks()
        
        if not tasks:
            print("No tasks found")
            return
        
        print(f"Found {len(tasks)} tasks:")
        for task in tasks:
            print(f"- {task['task_id']}: {task['status']} (Chain: {task['chain_id']})")
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 