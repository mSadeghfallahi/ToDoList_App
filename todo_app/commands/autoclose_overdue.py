"""Scheduled command to automatically close overdue tasks.

This module runs a background job every 15 minutes to find all tasks with
deadline < now() and status != DONE, and marks them as DONE.
"""
from __future__ import annotations

import schedule
import time
import logging
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from todo_app.db.session import SessionLocal
from todo_app.models.task import Task, TaskStatus


# Configure logging
logger = logging.getLogger(__name__)


def autoclose_overdue_tasks(db_session: Optional[Session] = None) -> int:
    """Find and close all overdue tasks.
    
    Queries for tasks where:
    - deadline < now (current UTC time)
    - status is not DONE
    
    Updates matching tasks to:
    - status = DONE
    - updated_at = now
    
    Args:
        db_session: Optional SQLAlchemy session. If None, creates a new one.
        
    Returns:
        Count of tasks that were auto-closed.
    """
    session = db_session or SessionLocal()
    
    try:
        now = datetime.now(timezone.utc)
        
        # Query for overdue, non-done tasks
        overdue_tasks = session.query(Task).filter(
            Task.deadline < now,
            Task.status != TaskStatus.DONE
        ).all()
        
        if not overdue_tasks:
            logger.debug(f"[{now.isoformat()}] No overdue tasks found.")
            return 0
        
        # Update all overdue tasks to DONE
        closed_count = 0
        for task in overdue_tasks:
            try:
                task.status = TaskStatus.DONE
                task.updated_at = now
                closed_count += 1
                logger.info(
                    f"Auto-closed task ID={task.id}, "
                    f"project_id={task.project_id}, deadline={task.deadline}"
                )
            except Exception as e:
                logger.error(f"Failed to close task ID={task.id}: {e}")
        
        # Commit all changes
        session.commit()
        
        logger.info(f"Successfully auto-closed {closed_count} overdue task(s).")
        return closed_count
        
    except Exception as e:
        session.rollback()
        logger.error(f"Error in autoclose_overdue_tasks: {e}", exc_info=True)
        return 0
        
    finally:
        if not db_session:  # Only close if we created the session
            session.close()


def schedule_autoclose_job() -> None:
    """Schedule the autoclose job to run every 15 minutes.
    
    This function configures the schedule and should be called once during
    application startup. The scheduled job runs within the Python process.
    
    Example:
        from todo_app.commands.autoclose_overdue import schedule_autoclose_job
        
        if __name__ == "__main__":
            schedule_autoclose_job()
            while True:
                schedule.run_pending()
                time.sleep(1)
    """
    schedule.every(15).minutes.do(autoclose_overdue_tasks)
    logger.info("Scheduled autoclose_overdue_tasks to run every 15 minutes.")


def run_scheduler() -> None:
    """Run the scheduler loop indefinitely.
    
    This is a blocking function that continuously runs pending scheduled jobs.
    Call this function in a separate thread or process if you want the scheduler
    to run alongside other application logic.
    
    Example:
        import threading
        from todo_app.commands.autoclose_overdue import run_scheduler
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
    """
    schedule_autoclose_job()
    
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
