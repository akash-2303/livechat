from flask import Flask, render_template, request, Response, jsonify
import pytchat
from multiprocessing import Process, Event
import time
import os

app = Flask(__name__)

# File to store chat messages
CHAT_FILE = 'chat_messages.txt'
stop_event = Event()
fetch_process = None  # Initialize globally


def fetch_chat_messages(video_id):
    chat = pytchat.create(video_id=video_id)
    with open(CHAT_FILE, 'w', encoding='utf-8') as file:  # Ensure file is opened with utf-8 encoding
        while chat.is_alive() and not stop_event.is_set():
            for c in chat.get().sync_items():
                try:
                    # Attempt to write the message to the file
                    file.write(f"{c.datetime} [{c.author.name}] - {c.message}\n")
                except UnicodeEncodeError:
                    # Handle the case where a message cannot be encoded into the file's encoding
                    # Optionally replace problematic characters or log the error
                    safe_message = c.message.encode('ascii', errors='ignore').decode('ascii')
                    file.write(f"{c.datetime} [{c.author.name}] - {safe_message}\n")
                file.flush()  # Ensure data is written to disk
            time.sleep(1)  # Brief sleep to avoid overwhelming the API



@app.route('/', methods=['GET', 'POST'])
def index():
    global fetch_process  # Declare fetch_process as global to modify it

    if request.method == 'POST':
        video_id = request.form.get('video_id')
        if video_id:
            # Stop any existing chat fetching process
            if fetch_process and fetch_process.is_alive():
                stop_event.set()
                fetch_process.join()

            stop_event.clear()
            # Clear previous chat messages
            if os.path.exists(CHAT_FILE):
                os.remove(CHAT_FILE)

            # Start a new process to fetch chat messages
            fetch_process = Process(target=fetch_chat_messages, args=(video_id,))
            fetch_process.start()

    return render_template('index.html')


@app.route('/events')
def stream():
    def generate():
        with open(CHAT_FILE, 'r', encoding='utf-8') as file:
            file.seek(0, os.SEEK_END)  # Start reading from the end of the file
            while not stop_event.is_set():
                line = file.readline()
                if line:
                    yield f"data: {line.strip()}\n\n"
                else:
                    time.sleep(1)  # Sleep if no new line is available
    return Response(generate(), mimetype='text/event-stream')


# @app.route('/events')
# def stream():
#     def generate():
#         with open(CHAT_FILE, 'r') as file:
#             while True:
#                 line = file.readline()
#                 if line:
#                     yield f"data: {line.strip()}\n\n"
#                 else:
#                     time.sleep(1)  # Sleep briefly to avoid tight loop

#     return Response(generate(), mimetype='text/event-stream')


@app.route('/stop', methods=['POST'])
def stop_chat():
    global fetch_process  # Declare fetch_process as global to modify it
    stop_event.set()
    if fetch_process and fetch_process.is_alive():
        fetch_process.join()
    return jsonify(message='Stopped fetching chat messages'), 200


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
