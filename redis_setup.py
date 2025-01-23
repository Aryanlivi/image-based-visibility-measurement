import redis

redis_client =redis.StrictRedis(host='localhost', port=6379, db=0)

def add_url_to_queue(url):
    redis_client.rpush('url_queue', url)
    print(redis_client)
    

add_url_to_queue("https://www.youtube.com/watch?v=X5-X5AeJbAE")  