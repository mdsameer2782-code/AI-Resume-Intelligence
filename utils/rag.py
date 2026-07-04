from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import os

VECTOR_DB = "vector_store"


def create_vector_store(text, embeddings):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    docs = splitter.create_documents([text])

    db = FAISS.from_documents(docs, embeddings)

    if not os.path.exists(VECTOR_DB):
        os.makedirs(VECTOR_DB)

    db.save_local(VECTOR_DB)

    return db


def load_vector_store(embeddings):
    return FAISS.load_local(
        VECTOR_DB,
        embeddings,
        allow_dangerous_deserialization=True
    )


def search_resume(query, embeddings, k=3):
    db = load_vector_store(embeddings)

    docs = db.similarity_search(query, k=k)

    return "\n\n".join([doc.page_content for doc in docs])