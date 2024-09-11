# syntax=docker/dockerfile:1

FROM python:3.12.5-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

VOLUME /app

CMD ["python3", "app.py", "--port=5000", "--host=0.0.0.0", "--chatfile='chat_messages.json'"]
