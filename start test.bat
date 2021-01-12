call .\env\Scripts\activate

pip install -r requirements.txt
set FLASK_APP=main.py

flask test
cmd /k
