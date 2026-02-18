from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import chromadb
import torch
import uuid

app = FastAPI()

# ------------------------
# Load Models (Global)
# ------------------------

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
llm_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="pdf_collection")


# ------------------------
# Utility Functions
# ------------------------

def chunk_text_with_overlap(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def generate_answer(query, retrieved_docs):
    context = "\n\n".join(retrieved_docs)
    context = context[:1500]

    prompt = f"""
    Answer the question based only on the context below.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

    outputs = llm_model.generate(
        **inputs,
        max_new_tokens=150
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return answer


def retrieve_chunks(query, top_k=1):
    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results["documents"][0], results["distances"][0]

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    reader = PdfReader(file.file)

    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    chunks = chunk_text_with_overlap(full_text)

    chunk_embeddings = embedding_model.encode(chunks).tolist()

    collection.add(
        documents=chunks,
        embeddings=chunk_embeddings,
        # ids=[f"chunk_{i}" for i in range(len(chunks))]
        ids=[str(uuid.uuid4()) for _ in range(len(chunks))]

    )

    return {"message": "PDF processed and stored successfully."}

@app.post("/ask")
async def ask_question(query: str):
    docs, distances = retrieve_chunks(query)

    if distances[0] > 1.2:
        return {"answer": "No relevant information found in document."}

    answer = generate_answer(query, docs)

    return {"answer": answer}

@app.get("/health")
def health():
    return {"status": "running"}
