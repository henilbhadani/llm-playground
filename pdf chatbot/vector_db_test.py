import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "We are hiring a Python developer",
    "Looking for a software engineer who codes in Python",
    "We need a chef for our restaurant"
]

embeddings = model.encode(sentences).tolist()

client = chromadb.Client()

collection = client.create_collection("job_posts")

collection.add(
    documents = sentences,
    embeddings = embeddings,
    ids = ["id1","id2","id3"]
)

query = "I need a backend developer"
query_embedding = model.encode([query]).tolist()

results = collection.query(
    query_embeddings=query_embedding,
    n_results=2
)

print("Query:", query)
print("Most similar documents:", results['documents'])