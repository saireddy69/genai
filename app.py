from fastapi import FastAPI, UploadFile, File
import uuid

app = FastAPI()

# ------------------------
# Global placeholders (lazy loaded)
# ------------------------

embedding_model = None
tokenizer = None
llm_model = None
collection = None


# ------------------------
# Lazy Model Loader
# ------------------------

def load_models():
    global embedding_model, tokenizer, llm_model, collection

    # Load embedding model + Chroma only once
    if embedding_model is None:
        from sentence_transformers import SentenceTransformer
        import chromadb

        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_or_create_collection(name="pdf_collection")

    # Load LLM only once
    if tokenizer is None:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

        tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
        llm_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")


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


def retrieve_chunks(query, top_k=1):
    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results["documents"][0], results["distances"][0]


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


# ------------------------
# Endpoints
# ------------------------

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    load_models()

    from pypdf import PdfReader

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
        ids=[str(uuid.uuid4()) for _ in range(len(chunks))]
    )

    return {"message": "PDF processed and stored successfully."}


@app.post("/ask")
async def ask_question(query: str):
    load_models()

    docs, distances = retrieve_chunks(query)

    if distances[0] > 1.2:
        return {"answer": "No relevant information found in document."}

    answer = generate_answer(query, docs)

    return {"answer": answer}


@app.get("/health")
def health():
    return {"status": "running"}
