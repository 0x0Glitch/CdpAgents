import json
import os
import sys
import time
import subprocess
import threading
from decimal import Decimal
from queue import Queue
from typing import Any, Dict, List, Optional, Union

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Dual Chain Agent API",
    description="API for routing instructions to Base or Optimism blockchain agents",
    version="1.0.0",
)

# Constants for blockchain identifiers
BASE_CHAIN_ID = "84532"  # Base Sepolia
OPTIMISM_CHAIN_ID = "11155420"  # Optimism Sepolia

# Agent scripts paths - fix the typo in the Base agent file name
BASE_AGENT_SCRIPT = "AiAgen1.py"  # Base agent script
OPTIMISM_AGENT_SCRIPT = "AiAgent2.py"  # Optimism agent script

# Stores running processes for each agent
agent_processes = {
    BASE_CHAIN_ID: None,
    OPTIMISM_CHAIN_ID: None,
}

# Queues for communication with each agent
agent_input_queues = {
    BASE_CHAIN_ID: Queue(),
    OPTIMISM_CHAIN_ID: Queue(),
}

# Queues for receiving output from agents
agent_output_queues = {
    BASE_CHAIN_ID: Queue(),
    OPTIMISM_CHAIN_ID: Queue(),
}

# Thread locks
agent_locks = {
    BASE_CHAIN_ID: threading.Lock(),
    OPTIMISM_CHAIN_ID: threading.Lock(),
}

# Task storage
tasks = {}
task_counter = 0
task_lock = threading.Lock()

class Instruction(BaseModel):
    """Model for receiving instructions via API."""
    instruction: str
    chain_id: Optional[str] = None  # If not specified, we'll try to determine it
    timeout: Optional[int] = 60     # Timeout in seconds

class TaskResponse(BaseModel):
    """Model for task creation response."""
    task_id: str
    status: str
    chain_id: str
    instruction: str

class TaskResult(BaseModel):
    """Model for task result response."""
    task_id: str
    status: str
    chain_id: str
    instruction: str
    result: Optional[str] = None
    error: Optional[str] = None

def chain_identifier_from_instruction(instruction: str) -> str:
    """
    Try to determine if the instruction is for Base or Optimism.
    
    Simple keyword matching for now, can be expanded to be more intelligent.
    Returns the chain_id or None if can't determine.
    """
    instruction_lower = instruction.lower()
    
    # Check for explicit blockchain mentions
    if any(term in instruction_lower for term in ["base", "base sepolia", "base-sepolia"]):
        return BASE_CHAIN_ID
    
    if any(term in instruction_lower for term in ["optimism", "optimism sepolia", "op", "optimism-sepolia"]):
        return OPTIMISM_CHAIN_ID
        
    # More intelligent parsing could be added
    
    # Default to Base if we can't determine
    return None

def start_agent_if_needed(chain_id: str):
    """Start the agent process if it's not already running."""
    with agent_locks[chain_id]:
        if agent_processes[chain_id] is None or agent_processes[chain_id].poll() is not None:
            # Determine which script to use
            script = BASE_AGENT_SCRIPT if chain_id == BASE_CHAIN_ID else OPTIMISM_AGENT_SCRIPT
            chain_name = "Base" if chain_id == BASE_CHAIN_ID else "Optimism"
            
            print(f"Starting {chain_name} agent using script: {script}")
            
            # Start the process
            process = subprocess.Popen(
                ["python", script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
            )
            
            agent_processes[chain_id] = process
            
            # Start threads to handle I/O with the process
            threading.Thread(
                target=process_output_thread,
                args=(chain_id, process),
                daemon=True
            ).start()
            
            threading.Thread(
                target=process_input_thread,
                args=(chain_id, process),
                daemon=True
            ).start()
            
            print(f"Started agent for chain {chain_id} ({chain_name})")
            
            # Give the process a moment to initialize
            time.sleep(2)
            
            return True
    
    return False

def process_output_thread(chain_id: str, process: subprocess.Popen):
    """Thread to read output from the agent process and put it in the output queue."""
    chain_name = "Base" if chain_id == BASE_CHAIN_ID else "Optimism"
    
    try:
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"[{chain_name}] {line.strip()}")
                agent_output_queues[chain_id].put(line.strip())
    except Exception as e:
        print(f"Error reading output from {chain_name} agent: {str(e)}")
    finally:
        print(f"{chain_name} agent output thread ended")

def process_input_thread(chain_id: str, process: subprocess.Popen):
    """Thread to send input from the input queue to the agent process."""
    chain_name = "Base" if chain_id == BASE_CHAIN_ID else "Optimism"
    
    try:
        while process.poll() is None:
            try:
                instruction = agent_input_queues[chain_id].get(timeout=1)
                process.stdin.write(instruction + "\n")
                process.stdin.flush()
                print(f"Sent to {chain_name} agent: {instruction}")
            except Exception:
                # No input yet
                pass
    except Exception as e:
        print(f"Error sending input to {chain_name} agent: {str(e)}")
    finally:
        print(f"{chain_name} agent input thread ended")

def execute_instruction(chain_id: str, instruction: str, timeout: int = 60) -> str:
    """
    Execute the given instruction on the specified chain's agent.
    
    Args:
        chain_id: The chain ID to use
        instruction: The instruction to send to the agent
        timeout: Maximum time to wait for a response
        
    Returns:
        The response from the agent
    """
    start_agent_if_needed(chain_id)
    
    # Send the instruction to the agent
    agent_input_queues[chain_id].put(instruction)
    
    # Collect output until we have a complete response
    start_time = time.time()
    result = []
    
    # Detect markers for when the agent has finished processing
    response_complete = False
    
    while not response_complete and (time.time() - start_time < timeout):
        try:
            line = agent_output_queues[chain_id].get(timeout=1)
            result.append(line)
            
            # Check for completion markers
            if "-------------------" in line or ">>>" in line:
                response_complete = True
        except Exception:
            # No output yet
            time.sleep(0.1)
    
    if not response_complete:
        return "Timeout waiting for agent response"
    
    return "\n".join(result)

def process_instruction_task(task_id: str, chain_id: str, instruction: str, timeout: int):
    """Background task to process an instruction and update the task result."""
    try:
        # Execute the instruction on the appropriate agent
        result = execute_instruction(chain_id, instruction, timeout)
        
        # Update the task status
        with task_lock:
            tasks[task_id]["status"] = "completed"
            tasks[task_id]["result"] = result
    except Exception as e:
        # Handle any errors
        with task_lock:
            tasks[task_id]["status"] = "failed"
            tasks[task_id]["error"] = str(e)

@app.get("/")
async def root():
    """Root endpoint, just to check if the API is running."""
    return {
        "message": "Dual Chain Agent API is running",
        "info": "Use Base agent (AiAgen1.py) for Base Sepolia and Optimism agent (AiAgent2.py) for Optimism Sepolia"
    }

@app.post("/instruction", response_model=TaskResponse)
async def submit_instruction(instruction_data: Instruction, background_tasks: BackgroundTasks):
    """
    Submit an instruction to be processed by the appropriate agent.
    
    If chain_id is not specified, we'll try to determine which chain to use.
    """
    global task_counter
    
    # Parse the instruction
    instruction_text = instruction_data.instruction
    
    # Determine which chain to use if not specified
    chain_id = instruction_data.chain_id
    if not chain_id:
        chain_id = chain_identifier_from_instruction(instruction_text)
        if not chain_id:
            chain_id = BASE_CHAIN_ID  # Default to Base
    
    # Validate the chain ID
    if chain_id not in [BASE_CHAIN_ID, OPTIMISM_CHAIN_ID]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid chain_id: {chain_id}. Must be {BASE_CHAIN_ID} (Base) or {OPTIMISM_CHAIN_ID} (Optimism)."
        )
    
    # Create a task ID
    with task_lock:
        task_counter += 1
        task_id = f"task-{task_counter}"
        
        # Initialize the task
        tasks[task_id] = {
            "task_id": task_id,
            "status": "pending",
            "chain_id": chain_id,
            "instruction": instruction_text,
            "result": None,
            "error": None,
            "created_at": time.time()
        }
    
    # Start the task in the background
    background_tasks.add_task(
        process_instruction_task, 
        task_id, 
        chain_id, 
        instruction_text,
        instruction_data.timeout or 60
    )
    
    # Return the task info
    return TaskResponse(
        task_id=task_id,
        status="pending",
        chain_id=chain_id,
        instruction=instruction_text
    )

@app.get("/task/{task_id}", response_model=TaskResult)
async def get_task_result(task_id: str):
    """Get the result of a previously submitted task."""
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {task_id}"
        )
    
    task = tasks[task_id]
    
    return TaskResult(
        task_id=task_id,
        status=task["status"],
        chain_id=task["chain_id"],
        instruction=task["instruction"],
        result=task["result"],
        error=task["error"]
    )

@app.get("/tasks", response_model=List[TaskResult])
async def get_all_tasks():
    """Get all tasks."""
    return [
        TaskResult(
            task_id=task_id,
            status=task["status"],
            chain_id=task["chain_id"],
            instruction=task["instruction"],
            result=task["result"],
            error=task["error"]
        )
        for task_id, task in tasks.items()
    ]

def shutdown_agents():
    """Shutdown all agent processes."""
    for chain_id, process in agent_processes.items():
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            
            print(f"Shutdown agent for chain {chain_id}")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    shutdown_agents()

def main():
    """Start the FastAPI server."""
    try:
        # Check if the agent scripts exist
        for script in [BASE_AGENT_SCRIPT, OPTIMISM_AGENT_SCRIPT]:
            if not os.path.exists(script):
                print(f"Error: Agent script {script} not found!")
                sys.exit(1)
        
        print(f"Using Base agent script: {BASE_AGENT_SCRIPT}")
        print(f"Using Optimism agent script: {OPTIMISM_AGENT_SCRIPT}")
        
        # Start the Uvicorn server
        uvicorn.run(
            "dual_agent_api:app",
            host="0.0.0.0",
            port=8000,
            reload=False
        )
    except KeyboardInterrupt:
        print("Shutting down...")
        shutdown_agents()
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        shutdown_agents()

if __name__ == "__main__":
    main() 