from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from document_processor import read_file_content, create_embeddings, store_embeddings

app = FastAPI()

class DocumentInput(BaseModel):
    file_path: str

@app.post("/api/documents/process")
async def process_document(input: DocumentInput):
    file_path = input.file_path
    try:
        content = read_file_content(file_path)
        embeddings = create_embeddings(content)
        metadata = {"file_path": file_path}
        asset_id = store_embeddings(embeddings, metadata)
        return {"asset_id": asset_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))