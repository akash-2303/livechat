# livechat

Video ID to test:   NayY-ppAQUc
Can add port number as argument and also textfile name

python3 app.py --port portnumber --chatfile filename

Steps to run on local: 
1. create virtual environment - `python3 -m venv venv`
2. install dependencies in requiremetns.txt  - `pip install requirements.txt`
3. install sqlite database - `brew install sqlite`
4. setup sqlite database for the application - `python3 init_db.py`
5. test the connection by uncommenting the function in `app.py` and running curl 

    ```bash
    curl -X POST http://localhost:4000/add_comment \
        -H "Content-Type: application/json" \
        -d '{
        "etag": "abc123",
        "author": "John Doe",
        "text": "This is a sample comment.",
        "likes": 10
        }'
    ```

    After this the application should have access to the sqlite database file.