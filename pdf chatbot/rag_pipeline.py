import fitz
import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

# Step 1: Load PDF
def load_pdf(path):
    doc = fitz.open(path)
    text=""
    for page in doc:
        text += page.get_text()
    return text

# Step 2: Chunk the text
def chunk_text(text, chunk_size=500, overlap=50):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks=[]
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentences) <= chunk_size:
            current_chunk += sentence + " "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk += sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# Step 3 & 4: Embed chunks and store in ChromaDB
def store_in_chromadb(chunks):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks).tolist()

    client = chromadb.Client()
    collection = client.create_collection("pdf_chunks")

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    return collection

# Step 5: Query ChromaDB
def query_collection(collection, question, n_results=3):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embeddings = model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=query_embeddings,
        n_results=n_results
    )
    return results['documents'][0]

# Step 6: Ask Gemini using retrieved chunks
def ask_gemini(question, relevant_chunks):
    labeled_chunks = [f"[Chunk {i+1}: {chunk}]" for i,chunk in enumerate(relevant_chunks) ]
    context= "\n\n".join(labeled_chunks)

    prompt= f"""Answer the question using ONLY the context below.
            Cite which chunk number(s) you used, like [Chunk 1].
            If the answer is not in the context, say "I don't know based on the document."

            Context: {context}

            Question: {question}

            Answer:"""

    model= genai.GenerativeModel('gemini-2.5-flash')
    response= model.generate_content(prompt)
    return response.text

# Main pipeline
if __name__ == "__main__":
    pdf_path = "tiny-shakespeare.pdf"

    print("Loading PDF...")
    text = load_pdf(pdf_path)

    print("Chunking text...")
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks")

    print("Embedding and storing in ChromaDB...")
    collection = store_in_chromadb(chunks)

    question = "What does Menenius say about the belly?"

    print(f"\nquestion: {question}")
    print("Searching for relevant chunks...")
    relevant_chunks = query_collection(collection, question)

    print("Asking GEMINI...")
    answer = ask_gemini(question, relevant_chunks)

    print(f"\nAnswer: {answer}")