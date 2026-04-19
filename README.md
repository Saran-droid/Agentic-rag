# Agentic RAG Chatbot

An intelligent chatbot that uses Retrieval-Augmented Generation (RAG) to answer questions based on uploaded PDF documents. Built with LangChain, LangGraph, ChromaDB, and Groq's LLM.

## Features

- 📄 Upload and process PDF documents
- 🔍 Semantic search using vector embeddings
- 🤖 ReAct reasoning pattern for intelligent responses
- 💬 Interactive chat interface
- 🗄️ Persistent vector storage with ChromaDB

## Architecture

- **Frontend**: Streamlit web interface
- **Backend**: FastAPI server
- **Vector DB**: ChromaDB with HuggingFace embeddings
- **LLM**: Groq (Llama 4 Maverick)
- **Orchestration**: LangGraph for agentic workflows

## Prerequisites

- Python 3.11 or higher
- Groq API key ([Get one here](https://console.groq.com/))

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd agentic-rag
```

2. Install dependencies using `uv` (recommended) or `pip`:
```bash
# Using uv
uv sync

# Or using pip
pip install -e .
```

3. Create a `.env` file from the example:
```bash
cp .env.example .env
```

4. Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_actual_api_key_here
```

## Usage

### Start the Backend Server

```bash
# Using uv
uv run python agent/main.py

# Or using python directly
python agent/main.py
```

The backend will start on `http://localhost:8000`

### Start the Frontend

In a separate terminal:

```bash
# Using uv
uv run streamlit run app.py

# Or using streamlit directly
streamlit run app.py
```

The frontend will open in your browser at `http://localhost:8501`

### Using the Application

1. Upload a PDF document using the sidebar
2. Wait for the document to be processed
3. Ask questions about the document in the chat interface
4. The system will retrieve relevant context and generate answers

## Configuration

All configuration is managed through environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | Required |
| `BACKEND_URL` | Backend API URL | `http://localhost:8000` |
| `BACKEND_HOST` | Backend host | `0.0.0.0` |
| `BACKEND_PORT` | Backend port | `8000` |
| `EMBEDDING_MODEL` | HuggingFace embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| `LLM_MODEL` | Groq LLM model | `meta-llama/llama-4-maverick-17b-128e-instruct` |
| `CHROMA_DB_PATH` | ChromaDB storage path | `chroma_db` |
| `CHROMA_COLLECTION_NAME` | Collection name | `rag_docs` |

## Project Structure

```
.
├── agent/
│   ├── chroma_db/          # Vector database storage (gitignored)
│   ├── __init__.py
│   ├── graph.py            # LangGraph workflow definition
│   ├── llm.py              # Groq LLM wrapper
│   ├── main.py             # FastAPI backend server
│   └── retriever.py        # Document ingestion & retrieval
├── app.py                  # Streamlit frontend
├── pyproject.toml          # Project dependencies
├── .env.example            # Environment variables template
├── .gitignore
└── README.md
```

## API Endpoints

### `GET /`
Health check endpoint

### `POST /upload_pdf`
Upload a PDF document for processing
- **Body**: Multipart form data with PDF file
- **Response**: Number of chunks created

### `POST /chat`
Query the chatbot
- **Query Parameter**: `query` (string)
- **Response**: Generated answer

## How It Works

1. **Document Ingestion**: PDFs are split into chunks, embedded using sentence-transformers, and stored in ChromaDB
2. **Retrieval**: User queries are embedded and matched against stored chunks using cosine similarity
3. **Generation**: Top 3 relevant chunks are passed to the LLM with a ReAct prompt
4. **Response**: The LLM reasons about the context and generates an answer

## Development

The project uses `uv` for dependency management. To add new dependencies:

```bash
uv add <package-name>
```

## License

MIT License

Copyright (c) 2026 Saran

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
