from flask import Flask, render_template, request, Response, jsonify
import pytchat
from multiprocessing import Process, Event
import time
import os
import json
import argparse
import db_utils
parser = argparse.ArgumentParser(description="Run a Flask app for YouTube live chat fetching.")
parser.add_argument('--chatfile', type=str, default='chat_messages.json', help='Filename to store chat messages in JSON format.')
parser.add_argument('--port', type=int, default=5000, help='Port on which to run the Flask app.')
args = parser.parse_args()

app = Flask(__name__)
CHAT_FILE = args.chatfile
stop_event = Event()
fetch_process = None  # Initialize globally

# Function to fetch chat messages
def fetch_chat_messages(video_id):
    chat = pytchat.create(video_id=video_id)
    while chat.is_alive() and not stop_event.is_set():
        for c in chat.get().sync_items():
            message = {
                "timestamp": c.datetime,
                "author": c.author.name,
                "message": c.message
            }
            try:
                save_message_to_json(message, CHAT_FILE)
            except Exception as e:
                print(f"Failed to write message due to: {e}")
            time.sleep(1)

# Function to save messages to JSON
def save_message_to_json(message, filename):
    try:
        # Attempt to load existing data
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(message)
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    global fetch_process
    if request.method == 'POST':
        video_id = request.form.get('video_id')
        if video_id:
            if fetch_process and fetch_process.is_alive():
                stop_event.set()
                fetch_process.join()
            stop_event.clear()
            fetch_process = Process(target=fetch_chat_messages, args=(video_id,))
            fetch_process.start()
    return render_template('index.html')

@app.route('/events')
def stream():
    def generate():
        with open(CHAT_FILE, 'r', encoding='utf-8') as file:
            file.seek(0, os.SEEK_END)
            while not stop_event.is_set():
                line = file.readline()
                if line:
                    yield f"data: {line.strip()}\n\n"
                else:
                    time.sleep(1)
    return Response(generate(), mimetype='text/event-stream')

@app.route('/stop', methods=['POST'])
def stop_chat():
    global fetch_process
    stop_event.set()
    if fetch_process and fetch_process.is_alive():
        fetch_process.join()
    return jsonify(message='Stopped fetching chat messages')

# test method to check database connection.
# @app.route('/add_comment', methods=['POST'])
# def add_comment():
#     try:
#         data = request.get_json()
#         db_utils.push_comment_to_db(data)

#         return jsonify({"message": "Comment added successfully!"}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, threaded=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=args.port, threaded=True)
