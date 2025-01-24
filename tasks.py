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
from redis_setup import *
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
def process_all_urls(LUKLA_CONSTANTS):
    """
    Celery task to process all URLs from Redis and take screenshots every 10 minutes.
    """
    try:
        while True:
            # Wait for the next 10-minute interval to always start capturing from the 10 min interval gap
            # wait_for_next_10_minute_interval()
            redis_client = get_redis_client()

            # Get all stream names and URLs from the Redis hash
            streams = redis_client.hgetall(os.getenv('STREAM_URLS_KEY'))  # Retrieve all key-value pairs from the hash
            logger.info(streams)
            if not streams:
                logger.info("No streams to process. Waiting for the next interval...")
                continue


            # Process each stream
            for stream_name, url in streams.items():
                try:
                    logger.info(f"Processing URL: {url}")
                    BASE_OUTPUT_DIR = f"./screenshots/"+stream_name
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
                    # img_handler.upload_to_ftp(file_to_upload=file_name)
                    logger.info(f"BASE:{BASE_OUTPUT_DIR}")
                    logger.info(f"Successfully processed URL: {url}")
                except Exception as e:
                    logger.error(f"Error processing URL {url}: {e}")
            time.sleep(60*2)#wait 10 min
    except Exception as e:
        logger.error(f"Critical error in processing task: {e}")    