"""Scheduled command to automatically close overdue tasks.

This module provides the job that runs every 15 minutes to find all tasks with
deadline < now() and status != DONE, and marks them as DONE.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

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
    # Defer importing SessionLocal to avoid importing DB engine at module import time
    session = db_session
    created_session = False
    if session is None:
        from todo_app.db.session import SessionLocal

        session = SessionLocal()
        created_session = True
    
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
        if created_session and session is not None:
            session.close()


def schedule_autoclose_job() -> None:
    """Schedule the autoclose job to run every 15 minutes.
    
    This function configures the schedule and should be called once during
    application startup. The scheduled job runs within the Python process.
    
    Example:
        from todo_app.commands.autoclose_overdue import schedule_autoclose_job
        from todo_app.commands.scheduler import run_scheduler
        
        schedule_autoclose_job()
        run_scheduler()
    """
    from todo_app.commands.scheduler import schedule_autoclose_job as schedule_job
    schedule_job(autoclose_overdue_tasks)


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Schedule and run the autoclose job
    from todo_app.commands.scheduler import run_scheduler
    schedule_autoclose_job()
    run_scheduler()
