from flask import Flask, render_template, request, Response, jsonify
import pytchat
from multiprocessing import Process, Event
import time
import os
import argparse


#Initializing flask and handling command line arguments
parser = argparse.ArgumentParser(description="Run a Flask app for YouTube live chat fetching.")
parser.add_argument('--chatfile', type=str, default='chat_messages.txt',
                    help='Filename to store chat messages.')
parser.add_argument('--port', type=int, default=5000,
                    help='Port on which to run the Flask app.')
args = parser.parse_args()

app = Flask(__name__)

# Use the provided filename or the default 'chat_messages.txt'
CHAT_FILE = args.chatfile
stop_event = Event()
fetch_process = None  # Initialize globally

def fetch_chat_messages(video_id):
    chat = pytchat.create(video_id=video_id)
    with open(CHAT_FILE, 'w', encoding='utf-8') as file:
        while chat.is_alive() and not stop_event.is_set():
            for c in chat.get().sync_items():
                try:
                    file.write(f"{c.datetime} [{c.author.name}] - {c.message}\n")
                except Exception as e:
                    print(f"Failed to write message due to: {e}")
                file.flush()
            time.sleep(1)

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
            if os.path.exists(CHAT_FILE):
                os.remove(CHAT_FILE)
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

# if __name__ == '__main__':
#     app.run(debug=True, threaded=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=args.port, threaded=True)
