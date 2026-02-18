import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create Chroma client (in-memory for now)
client = chromadb.Client()

# Create a collection
# collection = client.create_collection(name="resume_collection")

# documents = [
#     "Experienced Python backend developer with FastAPI and PostgreSQL",
#     "Frontend developer skilled in React and JavaScript",
#     "Machine learning engineer with TensorFlow experience",
#     "DevOps engineer with Docker and Kubernetes expertise",
#     "Data analyst proficient in SQL and Power BI"
# ]

# Generate embeddings
# embeddings = model.encode(documents).tolist()

# client.delete_collection(name="resume_collection")
collection = client.create_collection(name="resume_collection")


# # Add to collection
# collection.add(
#     documents=documents,
#     embeddings=embeddings,
#     ids=[f"id_{i}" for i in range(len(documents))]
# )

# print("Documents added successfully.")

# query = "Python FastAPI backend engineer"

# query_embedding = model.encode([query]).tolist()

# results = collection.query(
#     query_embeddings=query_embedding,
#     n_results=3
# )

# print(results)

# for doc, distance in zip(results["documents"][0], results["distances"][0]):
#     print(f"{distance:.4f}  |  {doc}")

# documents = [
#     "Experienced Python backend developer with FastAPI and PostgreSQL",
#     "Frontend developer skilled in React and JavaScript",
#     "Machine learning engineer with TensorFlow experience",
#     "DevOps engineer with Docker and Kubernetes expertise",
#     "Data analyst proficient in SQL and Power BI"
# ]

# metadatas = [
#     {"role": "backend", "experience": 5},
#     {"role": "frontend", "experience": 3},
#     {"role": "ml", "experience": 4},
#     {"role": "devops", "experience": 6},
#     {"role": "data", "experience": 2}
# ]

# embeddings = model.encode(documents).tolist()

# collection.add(
#     documents=documents,
#     embeddings=embeddings,
#     metadatas=metadatas,
#     ids=[f"id_{i}" for i in range(len(documents))]
# )

# print("Documents with metadata added successfully.")


# query = "Looking for developer"

# query_embedding = model.encode([query]).tolist()

# results = collection.query(
#     query_embeddings=query_embedding,
#     n_results=5,
#     where={"role": "backend"}   # metadata filter
# )

# for doc, distance in zip(results["documents"][0], results["distances"][0]):
#     print(f"{distance:.4f}  |  {doc}")

# all_data = collection.get()

# for id_, doc, meta in zip(
#     all_data["ids"],
#     all_data["documents"],
#     all_data["metadatas"]
# ):
#     print(f"ID: {id_}")
#     print(f"Document: {doc}")
#     print(f"Metadata: {meta}")
#     print("-" * 50)


def chunk_text(text, chunk_size=100):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

# sample_text = """
# Retrieval Augmented Generation (RAG) is a technique that combines
# vector search with large language models. It allows the model to
# retrieve relevant documents before generating responses.
# Chunking helps improve retrieval accuracy by splitting large documents
# into smaller meaningful parts.
# """

# chunks = chunk_text(sample_text, chunk_size=100)

# for i, chunk in enumerate(chunks):
#     print(f"\nChunk {i+1}:\n{chunk}")

def chunk_text_with_overlap(text, chunk_size=100, overlap=30):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# chunks = chunk_text_with_overlap(sample_text, chunk_size=100, overlap=30)

# for i, chunk in enumerate(chunks):
#     print(f"\nChunk {i+1}:\n{chunk}")

long_text = """
Company Leave Policy:

Employees are entitled to 20 days of annual leave per year.
Maternity leave is granted for 6 months with full pay.
Paternity leave is granted for 15 days.
Sick leave requires medical documentation if exceeding 3 days.

Remote Work Policy:

Employees may work remotely up to 3 days per week.
Manager approval is required for extended remote work.
Work-from-home setup allowance is provided once per year.

Security Policy:

All employees must use two-factor authentication.
Passwords must be changed every 90 days.
Sharing login credentials is strictly prohibited.
"""

chunks = chunk_text_with_overlap(long_text, chunk_size=200, overlap=50)

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i}:\n{chunk}")

# client.delete_collection(name="policy_collection")
collection = client.create_collection(name="policy_collection")

chunk_embeddings = model.encode(chunks).tolist()

collection.add(
    documents=chunks,
    embeddings=chunk_embeddings,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

print("Chunks stored successfully.")

query = "How many months is maternity leave?"

query_embedding = model.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)

for doc, distance in zip(results["documents"][0], results["distances"][0]):
    print(f"\nDistance: {distance:.4f}")
    print(doc)
