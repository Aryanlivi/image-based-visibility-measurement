import time
from datetime import datetime,timedelta
from src.ImageHandler import ImageHandler
from src.YoutubeHandler import YoutubeHandler
from src.Utils import get_current_datetime
import logging

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
def process_all_urls():
    # wait_for_next_10_minute_interval()
    
    # # URL of the YouTube live stream
    STREAM_URL = "https://www.youtube.com/watch?v=X5-X5AeJbAE"

    # # Base output directory
    BASE_OUTPUT_DIR = "./screenshots"
    
    # -----FOR LUKLA----------
    LUKLA_CONSTANTS = {
        "device_id": 0,  # pick a random id
        "devicecode": "yt_1",
        "album_code": "album1",
        "latitude": 27.687162,
        "longitude": 86.732396,
        "altitude": 2800,
        "imageowner": "aryan",
        "firstAngle": 350,
        "lastAngle":0,
    }

    
    
    while True:
        yt_handler=YoutubeHandler(STREAM_URL,BASE_OUTPUT_DIR)
        img_handler=ImageHandler(img_path)
        maker_note=img_handler.create_encoded_maker_note(
            device_id=LUKLA_CONSTANTS["device_id"],
            devicecode=LUKLA_CONSTANTS["devicecode"],      
            album_code=LUKLA_CONSTANTS["album_code"],
            latitude=LUKLA_CONSTANTS["latitude"],
            longitude=LUKLA_CONSTANTS["longitude"],
            altitude=LUKLA_CONSTANTS["altitude"],
            imageowner=LUKLA_CONSTANTS["imageowner"],
            datetime_taken=capture_time,      
        )
        file_name=img_handler.add_metadata_and_save(maker_note,firstangle=LUKLA_CONSTANTS['firstAngle'],lastangle=LUKLA_CONSTANTS['lastAngle'])
        img_handler.upload_to_ftp(file_to_upload=file_name)
        # Wait for 10 minutes before capturing the next screenshot
        time.sleep(300)  # 5 minutes
        
if __name__ == "__main__":
    process_all_urls()
