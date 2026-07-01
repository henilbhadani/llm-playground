from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "We are hiring a python developer",
    "Looking for a software engineer who codes in python",
    "We need a chef for our restaurant"
]

embeddings = model.encode(sentences)

print(f"Embedding shape: {embeddings.shape}")
print(f"First embedding (first 5 numbers): {embeddings[0][:5]}")

sim_1_2 = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
sim_1_3 = cosine_similarity([embeddings[0]], [embeddings[2]])[0][0]

print(f"Similarity - Python dev vs Software engineer: {sim_1_2:.4f}")
print(f"Similarity - Python dev vs Chef: {sim_1_3:.4f}")