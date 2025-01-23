import time
from datetime import datetime,timedelta
from src.ImageHandler import ImageHandler
from src.YoutubeHandler import YoutubeHandler
from src.Utils import get_current_datetime
import logging
import redis
from celery_config import celery_app
from dotenv import load_dotenv 
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Redis client for managing URLs
redis_client = redis.StrictRedis(host=os.getenv('redis_host'), port=os.getenv('redis_port'), decode_responses=True)
STREAM_URLS_KEY = os.getenv('STREAM_URLS_KEY')  # Key to store URLs in Redis



def wait_for_next_10_minute_interval():
    current_time =get_current_datetime()

    # Calculate how many minutes past the last 10-minute mark
    minutes_past = current_time.minute % 10

    # Calculate the next 10-minute interval, ensuring seconds are set to 00
    if minutes_past == 0:
        next_interval = current_time.replace(second=0, microsecond=0)  # Already at the correct 10-minute mark
    else:
        # Adjust the time to the next 10-minute interval and set seconds and microseconds to 00
        next_interval = (current_time + timedelta(minutes=(10 - minutes_past))).replace(second=0, microsecond=0)

    # Wait until the next 10-minute mark
    wait_time = ((next_interval - current_time).total_seconds())+20
    logger.info(f"Waiting for {wait_time} seconds to reach the next 10-minute interval... i.e {next_interval}")
    time.sleep(wait_time)

@celery_app.task
def process_all_urls():
    """
    Celery task to process all URLs from Redis and take screenshots every 10 minutes.
    """
    try:
        while True:
            # Wait for the next 10-minute interval to always start capturing from the 10 min interval gap
            wait_for_next_10_minute_interval()

            # Get all URLs from Redis
            urls = redis_client.lrange(STREAM_URLS_KEY, 0, -1)
            
            
            if not urls:
                logger.info("No URLs to process. Waiting for the next interval...")
                continue

            # Process each URL
            for url in urls:
                try:
                    logger.info(f"Processing URL: {url}")
                    yt_handler = YoutubeHandler(url, BASE_OUTPUT_DIR)            
                    img_path, capture_time = yt_handler.capture_screenshot()

                    img_handler = ImageHandler(img_path)
                    maker_note = img_handler.create_encoded_maker_note(
                        device_id=LUKLA_CONSTANTS["device_id"],
                        devicecode=LUKLA_CONSTANTS["devicecode"],
                        album_code=LUKLA_CONSTANTS["album_code"],
                        latitude=LUKLA_CONSTANTS["latitude"],
                        longitude=LUKLA_CONSTANTS["longitude"],
                        altitude=LUKLA_CONSTANTS["altitude"],
                        imageowner=LUKLA_CONSTANTS["imageowner"],
                        datetime_taken=capture_time,
                    )

                    # Add metadata and upload to FTP
                    file_name = img_handler.add_metadata_and_save(
                        maker_note,
                        firstangle=LUKLA_CONSTANTS["firstAngle"],
                        lastangle=LUKLA_CONSTANTS["lastAngle"],
                    )
                    img_handler.upload_to_ftp(file_to_upload=file_name)

                    logger.info(f"Successfully processed URL: {url}")
                except Exception as e:
                    logger.error(f"Error processing URL {url}: {e}")

    except Exception as e:
        logger.error(f"Critical error in processing task: {e}")