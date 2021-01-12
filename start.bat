call .\env\Scripts\activate

pip install -r requirements.txt
set FLASK_APP=main.py
set FLASK_DEBUG=1
set FLASK_ENV=development

flask run
