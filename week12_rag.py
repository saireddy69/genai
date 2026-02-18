from pypdf import PdfReader

# Path to your PDF
pdf_path = r"C:\Users\VenkataSaiChejarla\Downloads\file-example_PDF_1MB.pdf"

reader = PdfReader(pdf_path)

full_text = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        full_text += text + "\n"

# print("Total characters extracted:", len(full_text))
# print("\nFirst 500 characters:\n")
# print(full_text[:500])

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


chunks = chunk_text_with_overlap(full_text)

# print("Total chunks created:", len(chunks))
# print("\nPreview of first chunk:\n")
# print(chunks[0][:500])

import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create persistent client
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get collection
collection = client.get_or_create_collection(name="pdf_collection")

print("Chroma persistent collection ready.")

# Generate embeddings
chunk_embeddings = model.encode(chunks).tolist()

# Add to collection
collection.add(
    documents=chunks,
    embeddings=chunk_embeddings,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

print("Chunks stored in persistent Chroma DB.")

def retrieve_chunks(query, top_k=1):
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    return results["documents"][0], results["distances"][0]


query = "What is this document about?"

docs, distances = retrieve_chunks(query)

for doc, dist in zip(docs, distances):
    print(f"\nDistance: {dist:.4f}")
    # print(doc[:400])

import transformers
print(transformers.__version__)

# from transformers import pipeline
# pipeline("text2text-generation", model="google/flan-t5-base")

# Load local text generation model
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model_llm = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")


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

    outputs = model_llm.generate(
        **inputs,
        max_new_tokens=150
    )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return answer



if distances[0] > 1.2:
    print("No relevant information found in document.")
else:
    answer = generate_answer(query, docs)
    print(answer)
