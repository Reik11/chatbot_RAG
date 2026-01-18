cara nge run 

git clone https://github.com/Reik11/chatbot_RAG.git

cd chatbbot_RAG

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python scraper/scrape_id.py

python vector_store.py

VERSI ollama 3.2:3b

https://ollama.com/download

ollama pull llama3.2

ollama run llama3.2

python app.py
