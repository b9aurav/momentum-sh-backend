from models import ChatThread
from langchain_cohere import ChatCohere
import dotenv
from langchain.chains.question_answering import load_qa_chain
from document_processor import get_document_from_db
from langchain_core.documents import Document

dotenv.load_dotenv()
llm = ChatCohere(model='command-medium-nightly', cohere_api_key=dotenv.get_key(dotenv_path='.env', key_to_get='COHERE_API_KEY'))

chat_threads = {}

def start_chat_service(asset_id: str) -> str:
    chat_thread = ChatThread(asset_id)
    chat_threads[chat_thread.thread_id] = chat_thread
    return chat_thread.thread_id

def post_message_service(chat_thread_id: str, user_message: str) -> str:
    chat_thread = chat_threads.get(chat_thread_id)
    if not chat_thread:
        raise ValueError("Chat thread not found")
    
    agent_response = query_langchain(chat_thread.asset_id, user_message)
    chat_thread.messages.append({"user_message": user_message, "agent_response": agent_response})
    
    return agent_response

def get_chat_history_service(chat_thread_id: str):
    chat_thread = chat_threads.get(chat_thread_id)
    if not chat_thread:
        raise ValueError("Chat thread not found")
    
    return chat_thread.messages

def query_langchain(asset_id: str, user_message: str) -> str:
    result = get_document_from_db(asset_id)
    doc = Document(
        page_content=result['documents'][0],
        metadata=result['metadatas'][0],
        id=result['ids'][0]
    )
    print(f"Document: {doc}")
    chain = load_qa_chain(llm, chain_type="stuff")
    answer = chain.run(input_documents=[doc], question=user_message)
    return answer