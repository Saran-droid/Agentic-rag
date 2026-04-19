from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import chromadb
from io import BytesIO
from PyPDF2 import PdfReader
import os
from dotenv import load_dotenv

load_dotenv()

model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
embeddings = HuggingFaceEmbeddings(model_name=model_name)

chroma_db_path = os.getenv("CHROMA_DB_PATH", "chroma_db")
chroma_client = chromadb.PersistentClient(path=chroma_db_path)

collection_name = os.getenv("CHROMA_COLLECTION_NAME", "rag_docs")
collection = chroma_client.get_or_create_collection(
    name=collection_name,
    metadata={"hnsw:space": "cosine"}
)


chroma = Chroma(
    client=chroma_client,
    collection_name=collection_name,
    embedding_function=embeddings
)

retriever = chroma.as_retriever(search_type="similarity", search_kwargs={"k": 3})


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


def ingest_pdf(file_bytes: bytes) -> int:
    pdf = PdfReader(BytesIO(file_bytes))
    texts = [page.extract_text() for page in pdf.pages]
    chunks = text_splitter.split_text("\n".join(texts))
    documents = [Document(page_content=chunk) for chunk in chunks]
    chroma.add_documents(documents)
    return len(chunks)

def clear_collection():
    """Remove all documents by dropping and recreating the collection."""
    global collection
    chroma_client.delete_collection(collection_name)