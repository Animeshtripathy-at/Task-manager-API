from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from database import SessionLocal
import models
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_due_dates():
    logger.info(f"Checking for due dates at {datetime.now()}")
    db = SessionLocal()
    try:
        now = datetime.now()
        # Look for tasks due within the next 24 hours that are not DONE
        upcoming_deadline = now + timedelta(days=1)
        tasks = db.query(models.Task).filter(
            models.Task.due_date <= upcoming_deadline,
            models.Task.due_date >= now,
            models.Task.status != models.TaskStatus.DONE
        ).all()
        
        for task in tasks:
            # Simulated notification
            logger.info(f"REMINDER: Task '{task.title}' (ID {task.id}) is due at {task.due_date}. Please complete it soon!")
            
    except Exception as e:
        logger.error(f"Error checking due dates: {e}")
    finally:
        db.close()

def setup_scheduler():
    scheduler = BackgroundScheduler()
    # Check every 1 minute for demonstration purposes
    scheduler.add_job(
        check_due_dates,
        trigger=IntervalTrigger(minutes=1),
        id='check_due_dates_job',
        name='Check for upcoming task due dates',
        replace_existing=True
    )
    scheduler.start()
    logger.info("APScheduler started successfully.")
