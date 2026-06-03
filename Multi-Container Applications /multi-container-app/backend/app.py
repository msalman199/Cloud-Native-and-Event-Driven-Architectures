from flask import Flask, jsonify, request
import redis
import os

app = Flask(__name__)

# TODO: Configure Redis connection
# Hint: Use environment variable REDIS_HOST
redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=6379,
    decode_responses=True
)

@app.route('/api/visits', methods=['GET'])
def get_visits():
    # TODO: Increment visit counter in Redis
    # TODO: Return JSON response with visit count
    pass

@app.route('/api/message', methods=['POST'])
def set_message():
    # TODO: Get message from request JSON
    # TODO: Store message in Redis with key 'message'
    # TODO: Return success response
    pass

@app.route('/api/message', methods=['GET'])
def get_message():
    # TODO: Retrieve message from Redis
    # TODO: Return message in JSON format
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
