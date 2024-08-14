# Document based Chat Service

This project is a chat service that allows users to start chat threads, post messages, and retrieve chat history based on a document. It supports `.pdf`, `.txt` and `.docx` and uses a vector database for storing and querying chat data.

## Setup Instructions

1. **Clone the repository**:
    ```sh
    git clone https://github.com/b9aurav/momentum-sh-backend.git
    cd chat-service
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the root directory and add the following:
    ```env
    COHERE_API_KEY=your_cohere_api_key
    ```

5. **Run the application**:
    ```sh
    uvicorn main:app --reload
    ```

## API Documentation

### 1. Process Document

**Endpoint**: `/api/documents/process`

**Method**: `POST`

**Request**:
```json
{
    "file_path": "string"
}
```

**Response**
```json
{
    "asset_id": "string"
}
```

### 2. Start Chat Service

**Endpoint**: `/api/chat/start`

**Method**: `POST`

**Request**:
```json
{
    "asset_id": "string"
}
```

**Response**
```json
{
    "chat_thread_id": "string"
}
```

### 3. Send Message

**Endpoint**: `/api/chat/message`

**Method**: `POST`

**Request**:
```json
{
    "chat_thread_id": "string",
    "user_message": "string"
}
```

**Response**
```json
{
    "agent_response": "string"
}
```

### 4. Get Chat History

**Endpoint**: `/api/chat/history`

**Method**: `GET`

**Request**:
```json
{
    "chat_thread_id": "string"
}
```

**Response**
```json
{
    "History"
}
```

### 5. Response Streaming for Real-time interaction

**URL**: `ws://127.0.0.1:8000/ws/chat/<chat_thread_id>`

## Potential Improvements

* Implement comprehensive error handling for all API endpoints to provide meaningful error messages and status codes.
* Add authentication and authorization mechanisms to secure the API endpoints.
* Write unit and integration tests to ensure the reliability and correctness of the codebase.
* Develop a user-friendly web interface for interacting with the chat service.