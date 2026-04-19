from fastapi import FastAPI,UploadFile, File
from fastapi.responses import JSONResponse
from graph import run_agent
from retriever import ingest_pdf, clear_collection
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup (before yield) ---
    print("🟢 App starting...")

    yield  # App runs here

    # --- Shutdown (after yield) ---
    print("🔴 App shutting down... clearing vector DB.")
    clear_collection()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "Only PDF files allowed"})

    content = await file.read()

    num_chunks = ingest_pdf(content)
    return {"message": f"PDF ingested into {num_chunks} chunks"}

@app.post("/chat")
async def chat(query: str):
    answer = await run_agent(query)
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=True)
