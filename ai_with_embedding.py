from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np
import pickle

# Embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embedding_dim = 384

# Map met documenten
folder = "heembouw_docs"

if not os.path.exists(folder):
    raise FileNotFoundError(f"De map '{folder}' bestaat niet. Maak deze map aan en voeg .txt bestanden toe.")

files = [f for f in os.listdir(folder) if f.endswith(".txt")]
if not files:
    raise FileNotFoundError(f"Geen .txt bestanden gevonden in '{folder}'.")

# FAISS index
index = faiss.IndexFlatL2(embedding_dim)
texts = []

for filename in files:
    with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
        content = f.read()
        vector = model.encode(content).astype("float32")
        index.add(np.array([vector]))
        texts.append(content)



# Map voor opslag FAISS-bestanden
output_folder = "faiss_data/"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(folder):
    if filename.endswith(".txt"):
        with open(os.path.join(folder, filename), "r", encoding="utf-8") as f:
            content = f.read()
            vector = model.encode(content).astype("float32")
            index.add(np.array([vector]))
            texts.append(content)

# Opslaan in aparte map
index_file = os.path.join(output_folder, "faiss_index.bin")
texts_file = os.path.join(output_folder, "faiss_texts.pkl")

with open(index_file, "wb") as f:
    pickle.dump(index, f)
with open(texts_file, "wb") as f:
    pickle.dump(texts, f)

print(f"FAISS index opgeslagen in map: {output_folder}")
