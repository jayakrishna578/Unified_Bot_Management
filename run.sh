python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

streamlit run main.py &
python bot.py &
python database.py &
python stock_data_retrieval_bot.py &
python query_bot.py &
