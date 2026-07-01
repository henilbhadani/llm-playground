import streamlit as st
from rag_pipeline import load_pdf, chunk_text, store_in_chromadb, query_collection, ask_gemini

st.title("PDF Chatbot")
st.write("Ask questions about your PDF document.")

@st.cache_resource
def setup_pipeline():
    text = load_pdf("tiny-shakespeare.pdf")
    chunks = chunk_text(text)
    collection = store_in_chromadb(chunks)
    return collection

collection = setup_pipeline()

question = st.text_input("Ask a question:")

if question:
    with st.spinner("Searching..."):
        relevant_chunks = query_collection(collection, question)
        answer = ask_gemini(question, relevant_chunks)
    st.write("**Answer:**", answer)