"""Scheduler for managing background jobs.

This module provides the scheduler loop that runs pending scheduled tasks
at their configured intervals.
"""
from __future__ import annotations

import schedule
import time
import logging


# Configure logging
logger = logging.getLogger(__name__)


def schedule_autoclose_job(job_func) -> None:
    """Schedule a job to run every 15 minutes.
    
    Args:
        job_func: Callable function to execute on schedule
    """
    schedule.every(15).minutes.do(job_func)
    logger.info(f"Scheduled {job_func.__name__} to run every 15 minutes.")


def run_scheduler() -> None:
    """Run the scheduler loop indefinitely.
    
    This is a blocking function that continuously runs pending scheduled jobs.
    Call this function in a separate thread or process if you want the scheduler
    to run alongside other application logic.
    
    Example:
        import threading
        from todo_app.commands.scheduler import run_scheduler
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
    """
    logger.info("Starting scheduler loop...")
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Check for pending jobs every second
    except KeyboardInterrupt:
        logger.info("Scheduler interrupted.")
    except Exception as e:
        logger.error(f"Scheduler error: {e}", exc_info=True)


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Run the scheduler
    run_scheduler()
