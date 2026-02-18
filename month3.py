from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "I love backend development",
    "I enjoy building APIs",
    "The sky is blue"
]

embeddings = model.encode(sentences)

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

print("Sentence 1 vs 2:", cosine_similarity(embeddings[0], embeddings[1]))
print("Sentence 1 vs 3:", cosine_similarity(embeddings[0], embeddings[2]))

documents = [
    "Experienced Python backend developer with FastAPI and PostgreSQL",
    "Frontend developer skilled in React and JavaScript",
    "Machine learning engineer with TensorFlow experience",
    "DevOps engineer with Docker and Kubernetes expertise",
    "Data analyst proficient in SQL and Power BI"
]

doc_embeddings = model.encode(documents)

def semantic_search(query, documents, doc_embeddings):
    query_embedding = model.encode([query])[0]
    
    scores = []
    
    for i, doc_embedding in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_embedding)
        scores.append((documents[i], score))
    
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

results = semantic_search(
    "Python FastAPI backend engineer",
    documents,
    doc_embeddings
)


for doc, score in results:
    print(f"{score:.4f}  |  {doc}")


print(len(embeddings[0]))
print(len(embeddings[1]))
print(len(embeddings[2]))
