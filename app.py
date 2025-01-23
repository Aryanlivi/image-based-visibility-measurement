from flask import Flask, request, jsonify,render_template
from tasks import process_all_urls  # Celery task
from redis_setup import *
app = Flask(__name__)

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
    if url: 
        redis_client.rpush(STREAM_URLS_KEY, url)
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
    data = request.get_json()
    stream_name = data.get("stream_name")
    
    BASE_OUTPUT_DIR = f"./screenshots/{stream_name}"
    print(BASE_OUTPUT_DIR)
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
    process_all_urls.apply_async(args=[BASE_OUTPUT_DIR, LUKLA_CONSTANTS])  # Trigger the task in Celery
    return jsonify({"message": "Started processing URLs!"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
