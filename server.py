import _queue
from multiprocessing import Queue
from time import sleep
from flask import Flask, request, jsonify

app = Flask(__name__)
message_queue = {}


@app.route('/message', methods=['POST'])
def post():
    rq = request.json
    user_id = rq["user_id"]

    if user_id not in message_queue:
        message_queue[user_id] = Queue()
    message_queue[user_id].put(rq)
    return "OK"


@app.route('/long_poll', methods=['GET'])
def get():
    try:
        user_id = request.args.get("user_id")

        if user_id not in message_queue:
            message_queue[user_id] = Queue()

        tnum = 0
        while message_queue[user_id].empty():
            sleep(0.1)
            tnum += 1
            if tnum >= 50:
                return "NO"

        r = message_queue[user_id].get()
        return jsonify(r)

    except _queue.Empty as exec:
        print(str(exec))
        return jsonify({"error": "Timeout"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9090, threaded=True)
