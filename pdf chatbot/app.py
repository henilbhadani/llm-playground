import os
import streamlit as st
from rag_pipeline import load_pdf, chunk_text, store_in_chromadb, query_collection, ask_gemini
import tempfile
import re

st.title("PDF Chatbot")
st.write("Upload a PDF and ask questions about it.")

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

def safe_collection_name(name):
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    name = name[:63].strip('_-')
    return name or "pdf_chunks"

if uploaded_file:
    @st.cache_resource
    def setup_pipeline(file_name, file_bytes):
        tmp_path=None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name
            text = load_pdf(tmp_path)
            chunks = chunk_text(text)
            collection = store_in_chromadb(chunks,collection_name=safe_collection_name(file_name))
            return collection
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    try:
        collection = setup_pipeline(uploaded_file.name, uploaded_file.getvalue())
    except Exception as e:
        st.error(f"Failed to process PDF: {str(e)}")
        st.stop()

    question = st.text_input("Ask a question about your PDF:")

    if question:
        with st.spinner("Searching..."):
            relevant_chunks = query_collection(collection, question)
            answer = ask_gemini(question, relevant_chunks)
        st.write("**Answer:**", answer)