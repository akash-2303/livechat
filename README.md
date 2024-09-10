# livechat

Video ID to test:   NayY-ppAQUc
Can add port number as argument and also textfile name

python3 app.py --port portnumber --chatfile filename

Steps to run on local: 
1. create virtual environment - `python3 -m venv venv`
2. install dependencies in requiremetns.txt  - `pip install requirements.txt`
3. install sqlite database - `brew install sqlite`
4. setup sqlite database for the application - `python3 init_db.py`

After this the application should have access to the sqlite database file.