1) Setup
python -m venv venv
venv\Scripts\activate

2) Requirments
pip install -r requirements.txt

3) Run the server
uvicorn main:app --reload

4) Run the test
python testing.py