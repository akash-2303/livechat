import sqlite3
from flask import jsonify

# Function to establish a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')  # 'database.db' is the SQLite file
    conn.row_factory = sqlite3.Row  # Allows us to get dictionary-like access to row data
    return conn


def push_comment_to_db(comment):
    try:
        etag = comment['etag']
        author = comment['author']
        text = comment['text']
        likes = comment.get('likes', 0)  # Default to 0 likes if not provided

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO comments (etag, author, text, likes)
            VALUES (?, ?, ?, ?)
        ''', (etag, author, text, likes))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return e
    
def bulk_comment_to_db(comments):
    for comment in comments:
        push_comment_to_db(comment)