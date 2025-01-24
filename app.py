from flask import Flask, request, jsonify,render_template
from tasks import process_all_urls  # Celery task
from redis_setup import *
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
STREAM_URLS_KEY=os.getenv('STREAM_URLS_KEY')
redis_client=get_redis_client()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add-url", methods=["POST"])
def add_url():
    """
    Endpoint to add a new URL to the Redis queue.
    """
    data = request.get_json()
    url = data.get("url")
    stream_name = data.get("stream_name")
    if url: 
        redis_client.hset(STREAM_URLS_KEY, stream_name, url)
        # redis_client.rpush(STREAM_URLS_KEY, url)
        return jsonify({"message": f"URL {url} added successfully!"}), 201
    return jsonify({"message": "URL is required!"}), 400

@app.route("/remove-url", methods=["POST"])
def remove_url():
    """
    Endpoint to remove a URL from the Redis queue.
    """
    data = request.get_json()
    url = data.get("url")
    if url:
        redis_client.lrem(STREAM_URLS_KEY, 0, url)
        return jsonify({"message": f"URL {url} removed successfully!"}), 200
    return jsonify({"message": "URL is required!"}), 400

@app.route("/start-processing", methods=["POST"])
def start_processing():
    """
    Start the Celery task to process URLs.
    """
    try:
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

        # BASE_OUTPUT_DIR = data.get("output_dir", "./screenshots")
        # LUKLA_CONSTANTS = data.get("lukla_constants", {})  # LUKLA_CONSTANTS can be dynamic too
        
        #args=[] to pass the dict as a pack and not open it
        process_all_urls.apply_async(args=[LUKLA_CONSTANTS])  # Trigger the task in Celery
        return jsonify({"message": "Started processing URLs!"}), 200
    except Exception as e:
        # Log the error and return a 500 response
        logger.error(f"Error in /start-processing: {e}")
        return jsonify({"message": "An internal error occurred!"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
