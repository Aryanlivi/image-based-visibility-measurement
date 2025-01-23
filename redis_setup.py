import redis
from dotenv import load_dotenv
import os 
load_dotenv()
# Redis client for managing URLs
redis_client = redis.StrictRedis(host=os.getenv('redis_host'), port=os.getenv('redis_port'), decode_responses=True)
STREAM_URLS_KEY = os.getenv('STREAM_URLS_KEY')  # Key to store URLs in Redis

def get_redis_client():
    return redis_client