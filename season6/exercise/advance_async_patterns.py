import asyncio
import random
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ResourceManager:
    """Simulates a resource that needs proper cleanup"""
    
    def __init__(self, name: str):
        self.name = name
        logger.info(f"Resource '{name}' initialized")
    
    async def cleanup(self):
        """Simulate cleanup of resources"""
        logger.info(f"Cleaning up resource '{self.name}'...")
        await asyncio.sleep(0.2)  # Simulate cleanup time
        logger.info(f"Resource '{self.name}' cleaned up successfully")

async def task_with_resource(task_id: int, duration: float) -> Dict[str, Any]:
    """
    Task that simulates work and manages resources that need cleanup
    
    Args:
        task_id: Identifier for this task
        duration: How long the task should take to complete
        
    Returns:
        Dict containing task results
    """
    resource = ResourceManager(f"Task-{task_id}-Resource")
    
    try:
        logger.info(f"Task {task_id} started, will take {duration:.2f}s")
        
        # Simulate work being done
        start_time = asyncio.get_event_loop().time()
        await asyncio.sleep(duration)
        elapsed = asyncio.get_event_loop().time() - start_time
        
        result = {
            "task_id": task_id,
            "status": "completed",
            "duration": elapsed,
            "result_value": random.randint(1, 100)
        }
        logger.info(f"Task {task_id} completed successfully in {elapsed:.2f}s")
        return result
        
    except asyncio.CancelledError:
        # This is raised when the task is cancelled (e.g., due to timeout)
        elapsed = asyncio.get_event_loop().time() - start_time
        logger.warning(f"Task {task_id} was cancelled after {elapsed:.2f}s")
        # Re-raise to properly propagate cancellation
        raise
    
    finally:
        await resource.cleanup()

async def execute_task_with_timeout(task_id: int, duration: float, timeout: float) -> Dict[str, Any]:
    """
    Execute a task with a timeout
    
    Args:
        task_id: Identifier for this task
        duration: How long the task should take
        timeout: Maximum time allowed for the task
        
    Returns:
        Dict with task results or timeout information
    """
    try:
        # Wait for the task with a timeout
        return await asyncio.wait_for(
            task_with_resource(task_id, duration), 
            timeout=timeout
        )
    
    except asyncio.TimeoutError:
        logger.warning(f"Task {task_id} timed out after {timeout}s")
        return {
            "task_id": task_id,
            "status": "timeout",
            "timeout": timeout
        }
    
    except Exception as e:
        logger.error(f"Task {task_id} failed with error: {str(e)}")
        return {
            "task_id": task_id,
            "status": "error",
            "error": str(e)
        }

async def main():
    """
    Main function that launches multiple tasks with different timeouts
    and collects their results
    """
    # Define tasks with their durations and timeouts
    # (task_id, duration, timeout)
    task_configs = [
        (1, 1.5, 2.0),    # Will complete successfully (finishes before timeout)
        (2, 3.0, 1.0),    # Will timeout (takes longer than allowed)
        (3, 0.5, 2.0),    # Will complete successfully (quick task)
        (4, 2.5, 2.0),    # Will timeout (slightly exceeds timeout)
        (5, 1.8, 2.0)     # Will complete successfully (just within timeout)
    ]
    
    logger.info("Starting task execution with timeouts")
    
    # Launch all tasks concurrently
    tasks = [
        execute_task_with_timeout(task_id, duration, timeout)
        for task_id, duration, timeout in task_configs
    ]
    
    # Wait for all tasks to complete and collect results
    results = await asyncio.gather(*tasks)
    
    # Process and display results
    completed = [r for r in results if r["status"] == "completed"]
    timeouts = [r for r in results if r["status"] == "timeout"]
    errors = [r for r in results if r["status"] == "error"]
    
    logger.info(f"Task execution summary:")
    logger.info(f"  - Completed: {len(completed)}/{len(results)}")
    logger.info(f"  - Timeouts: {len(timeouts)}/{len(results)}")
    logger.info(f"  - Errors: {len(errors)}/{len(results)}")
    
    logger.info("Detailed results:")
    for result in results:
        if result["status"] == "completed":
            logger.info(f"  ✅ Task {result['task_id']} completed in {result['duration']:.2f}s with value {result['result_value']}")
        elif result["status"] == "timeout":
            logger.info(f"  ⏱️ Task {result['task_id']} timed out after {result['timeout']}s")
        else:
            logger.info(f"  ❌ Task {result['task_id']} failed with error: {result['error']}")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())