from flask import Flask, request, jsonify
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import requests

app = Flask(__name__)

# Load embedding & FAISS
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "faiss_db",
    embedding,
    allow_dangerous_deserialization=True
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

def ask_llama(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=120)
    return r.json()["response"]

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")

    docs = db.similarity_search(question, k=4)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
Kamu adalah asisten AI kecantikan dan kesehatan kuku.
Jawab dengan bahasa Indonesia yang jelas, ringkas, dan edukatif.

KONTEKS:
{context}

PERTANYAAN:
{question}

JAWABAN:
"""

    answer = ask_llama(prompt)

    return jsonify({
        "question": question,
        "answer": answer,
        "sources": [d.metadata["source"] for d in docs]
    })

if __name__ == "__main__":
    app.run(debug=True)
