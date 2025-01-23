from celery import Celery
from dotenv import load_dotenv
import os
load_dotenv()

host=os.getenv('redis_host')
port=os.getenv('redis_port')
# Configure Celery to use Redis as the broker
celery_app = Celery(
    'tasks',
    broker=f'redis://{host}:{port}/0',  # Redis URL
    # backend=f'redis://{host}:{port}/0'  # For result storage (optional)
)



# Set Celery configuration
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)