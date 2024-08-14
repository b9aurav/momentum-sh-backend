from langchain_cohere import ChatCohere
import dotenv
from langchain.chains.question_answering import load_qa_chain
from document_processor import get_document_from_db
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import uuid

dotenv.load_dotenv()
llm = ChatCohere(model='command-medium-nightly', cohere_api_key=dotenv.get_key(dotenv_path='.env', key_to_get='COHERE_API_KEY'))

persist_directory = "data"
embedder = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedder)

async def start_chat_service(asset_id: str) -> str:
    chat_thread_id = str(uuid.uuid4())
    vectordb.add_documents(documents=[Document(page_content="", metadata={"asset_id": asset_id}, id=chat_thread_id)])
    return chat_thread_id
    
async def post_message_service(chat_thread_id: str, user_message: str) -> str:
    results = vectordb.get(ids=[chat_thread_id])
    if not results:
        raise ValueError("Chat thread not found")
    
    asset_id = results['metadatas'][0]['asset_id']
    agent_response = await query_langchain(asset_id, user_message)
    
    updated_content = results['documents'][0] + f"\nUser: {user_message}\nAgent: {agent_response}"
    metadata = results['metadatas'][0]
    
    vectordb.update_documents(documents=[Document(page_content=updated_content, metadata=metadata)], ids=[chat_thread_id])
    
    return agent_response

async def get_chat_history_service(chat_thread_id: str):
    results = vectordb.get(ids=[chat_thread_id])
    if not results:
        raise ValueError("Chat thread not found")
    
    return results['documents'][0]

async def query_langchain(asset_id: str, user_message: str) -> str:
    result = get_document_from_db(asset_id)
    doc = Document(
        page_content=result['documents'][0],
        metadata=result['metadatas'][0],
        id=result['ids'][0]
    )
    chain = load_qa_chain(llm, chain_type="stuff")
    answer = chain.run(input_documents=[doc], question=user_message)
    return answer