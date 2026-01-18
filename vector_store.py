import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

with open("data/raw/kuku_dataset.json", encoding="utf-8") as f:
    docs = json.load(f)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

texts, metadatas = [], []

for d in docs:
    for c in splitter.split_text(d["content"]):
        texts.append(c)
        metadatas.append({"source": d["url"]})

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_texts(texts, embedding, metadatas=metadatas)
db.save_local("faiss_db")

print("✅ Vector store berhasil dibuat")
