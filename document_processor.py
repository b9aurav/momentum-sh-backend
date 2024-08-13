import os
import uuid
from PyPDF2 import PdfReader
import docx
from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.create_collection("documents")

def read_file_content(file_path):
    print(f"Reading file: {file_path}")
    if not os.path.exists(file_path):
        raise FileNotFoundError("File does not exist.")
    
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                print('File content:', content)
                return content
        except Exception as e:
            print(f"Error reading .txt file: {e}")
            raise e
    elif ext == ".pdf":
        try:
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                content = ""
                for page in reader.pages:
                    page_content = page.extract_text()
                    print(f"Page content: {page_content}")
                    content += page_content
                return content
        except Exception as e:
            print(f"Error reading .pdf file: {e}")
            raise e
    elif ext == ".docx":
        try:
            print(f"Attempting to read .docx file: {file_path}")
            doc = docx.Document(file_path)
            fullText = []
            for para in doc.paragraphs:
                fullText.append(para.text)
            content = '\n'.join(fullText)
            print('File content:', content)
            return content
        except Exception as e:
            print(f"Error reading .docx file: {e}")
            raise e
    else:
        raise ValueError("Unsupported file type")

def create_embeddings(content):
    return model.encode(content)

def store_embeddings(embeddings, metadata):
    asset_id = str(uuid.uuid4())
    embeddings_list = embeddings.tolist() if hasattr(embeddings, 'tolist') else embeddings
    collection.add(embeddings=[embeddings_list], metadatas=[metadata], ids=[asset_id])
    return asset_id

def get_stored_embeddings(asset_id):
    result = collection.get(ids=[asset_id])
    return result