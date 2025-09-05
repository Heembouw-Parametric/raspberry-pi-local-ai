from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np
import pickle

# Embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embedding_dim = 384

# FAISS index
index = faiss.IndexFlatL2(embedding_dim)
texts = []

# Map met documenten
folder = "heembouw_docs/"
for filename in os.listdir(folder):
    if filename.endswith(".txt"):
        with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
            content = f.read()
            vector = model.encode(content).astype("float32")
            index.add(np.array([vector]))
            texts.append(content)

# Opslaan
with open("faiss_index.bin", "wb") as f:
    pickle.dump(index, f)
with open("faiss_texts.pkl", "wb") as f:
    pickle.dump(texts, f)

print("FAISS index voor Heembouw-data is klaar!")
