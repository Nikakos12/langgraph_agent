# 🤖 LangGraph Conversational RAG Agent

A stateful conversational AI agent built with **LangGraph, Groq, ChromaDB, Ollama Embeddings, PostgreSQL, and FastAPI**.

The project demonstrates graph-based agent orchestration, domain-specific Retrieval-Augmented Generation (RAG), conversation summarization, persistent conversation state, and a REST API for interacting with the agent through Postman.

The application currently supports two execution modes:

- **Terminal mode:** interact with the agent directly through the command line.
- **API mode:** send HTTP requests to the FastAPI `/chat` endpoint using Postman.

**Project status:** In progress.

---

## 📌 Project Overview

The goal of this project is to explore how stateful LLM applications can combine agent orchestration, document retrieval, conversation memory, database persistence, and API integration.

The agent uses LangGraph to manage its workflow, Groq to run the language model, and domain-specific retrieval tools to access information from PDF documents.

### Key Features

- **Stateful graph orchestration:** Uses LangGraph nodes and conditional edges to manage the agent workflow and tool execution.
- **Conversation summarization:** Summarizes older conversation history when the message history exceeds a configured threshold.
- **Domain-specific RAG:** Uses ChromaDB vector stores and Ollama's `nomic-embed-text` embedding model to retrieve relevant information from PDF documents.
- **Tool calling:** Allows the LLM to request the appropriate retrieval tool when external document context is needed.
- **Persistent state checkpointing:** Uses PostgreSQL and LangGraph's `AsyncPostgresSaver` to persist graph state associated with conversation thread IDs.
- **Asynchronous execution:** Uses asynchronous graph invocation and PostgreSQL connection pooling.
- **REST API:** Exposes the agent through a FastAPI endpoint that can be tested using Postman.

---

## 🏗️ Architecture and Project Structure

```text
.
├── app.py                  # Terminal application entry point
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration, environment variables, and LLM setup
├── agent/
│   ├── __init__.py
│   ├── state.py             # AgentState definition
│   ├── nodes.py             # Summarization and agent nodes
│   ├── tools.py             # PDF loading, vector stores, and RAG tools
│   └── graph.py             # Graph construction and runtime functions
├── api/
│   ├── __init__.py
│   ├── routes.py            # FastAPI /chat endpoint
│   └── schemas.py           # API request and response models
├── db/
│   ├── __init__.py
│   └── postgresql.py        # Asynchronous PostgreSQL connection pool
├── music/                   # Source PDF documents for music retrieval
├── archeology/              # Source PDF documents for archaeology retrieval
├── Chroma_db/               # Persistent local vector stores (Git-ignored)
├── .env                     # Local environment variables (not committed)
├── .gitignore
└── README.md
```

---

## 🧠 Core Components

### Agent Module (`agent/`)

- **`state.py`:** Defines the graph state, including the conversation messages and summary.
- **`nodes.py`:** Implements the summarization node and the main agent node. The agent invokes the LLM and handles rate-limit retries.
- **`tools.py`:** Loads PDF documents, splits them into chunks, creates or loads ChromaDB vector stores, and exposes the music and archaeology retrievers as tools.
- **`graph.py`:** Defines the LangGraph workflow, including conditional routing between the agent and the retrieval tools.

### Database (`db/`)

- **`postgresql.py`:** Creates an asynchronous PostgreSQL connection pool used by LangGraph's PostgreSQL checkpointer.
- **PostgreSQL checkpointing:** Persists graph state so that conversations can continue across invocations associated with the same thread ID.

### Configuration (`config.py`)

Loads environment variables, defines file paths, and configures the Groq-hosted language model.

### API (`api/` and `main.py`)

- **`main.py`:** Creates the FastAPI application and initializes resources through its lifespan handler.
- **`api/routes.py`:** Exposes the `POST /chat` endpoint.
- **`api/schemas.py`:** Defines the request and response models used by the API.

---

## 🔄 Agent Workflow

The graph follows this general workflow:

1. A user submits a message through the terminal or API.
2. The application invokes the compiled LangGraph workflow with the message and a thread ID.
3. The summarization node manages older conversation history when the configured threshold is exceeded.
4. The agent node sends the conversation context to the Groq-hosted LLM.
5. The LLM either returns a response directly or requests a retrieval tool.
6. If a tool is requested, LangGraph routes execution to the tool node.
7. The selected retriever searches the relevant ChromaDB vector store and returns document chunks.
8. The graph returns to the agent node, allowing the LLM to use the retrieved context.
9. The final response is returned to the terminal or through the API response model.

The graph uses a configured recursion limit to constrain workflow execution.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Agent orchestration | LangGraph, LangChain |
| Language model | Groq via `ChatGroq` |
| Embeddings | Ollama, `nomic-embed-text` |
| Vector database | ChromaDB |
| Document processing | PDFMinerLoader, RecursiveCharacterTextSplitter |
| State persistence | PostgreSQL, `AsyncPostgresSaver` |
| Connection pooling | `psycopg_pool` |
| API framework | FastAPI |
| API testing | Postman |
| Language | Python |

---

## ⚙️ Prerequisites

Before running the application, make sure you have:

- Python installed.
- PostgreSQL running and a database available.
- A Groq API key.
- Ollama installed and running locally.
- The `nomic-embed-text` embedding model available in Ollama.
- The source PDF documents required by the retrieval tools.

Pull the embedding model if you have not already:

```bash
ollama pull nomic-embed-text
```

Install the project's Python dependencies using your dependency file, if provided:

```bash
pip install -r requirements.txt
```

If the repository does not yet contain a `requirements.txt`, create one from the project's actual dependencies before following this installation step.

---

## 🔐 Environment Configuration

Create a `.env` file in the location expected by your configuration module.

Example:

```dotenv
GROQ_API_KEY=your_groq_api_key
DB_URI=postgresql://username:password@localhost:5432/your_database
```

Use the variable names expected by your actual `config.py` and PostgreSQL connection module.

Do not commit `.env` files, API keys, passwords, or other credentials to GitHub.

---

## ▶️ Running the Application

The project supports two separate ways to interact with the agent.

### 1. Terminal Execution

Run the terminal entry point:

```bash
python app.py
```

The application initializes the PostgreSQL connection pool, sets up the checkpointer, creates the tools, compiles the graph, and starts an interactive terminal session.

Enter a message when prompted. The agent processes the message through LangGraph and prints its response in the terminal.

Use this mode to experiment with conversations, retrieval, summarization, and graph behavior without an HTTP client.

### 2. API Execution Through Postman

The API version runs the agent behind FastAPI. Instead of entering messages in the terminal, you send HTTP requests through Postman.

**Step 1 — Start the FastAPI server**

From the directory containing `main.py`, run:

```bash
uvicorn main:app --reload
```

If `main.py` is inside a subdirectory, change to that directory first. For example, if it is inside `app/`:

```bash
cd app
uvicorn main:app --reload
```

The application lifespan handler initializes the PostgreSQL connection pool, checkpointer, tools, and compiled graph during startup.

**Step 2 — Open Postman**

Create a new HTTP request with the following settings:

- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/chat`
- **Body:** `raw` → `JSON`
- **Header:** `Content-Type: application/json`

**Step 3 — Send a message**

Example request body:

```json
{
  "message": "What does the music document explain?",
  "thread_id": "postman-session-1"
}
```

Replace the message with any question relevant to the available documents.

**Step 4 — Inspect the response**

The endpoint returns a JSON response in the following format:

```json
{
  "response": "The generated answer from the agent..."
}
```

The response content depends on the user's message and the information available to the agent.

**Step 5 — Continue the conversation**

Send another request using the same `thread_id` to continue the associated conversation, provided checkpointing is configured correctly.

Use a different `thread_id` to represent a separate conversation.

The API is currently intended for local development and testing. Authentication and additional production security controls remain future improvements.

---

## 💾 Retrieval and Vector Storage

The project maintains separate vector stores for the supported document domains.

When a required vector store is missing or empty, the application:

1. Loads the relevant PDF document.
2. Splits the document into smaller text chunks.
3. Generates embeddings using Ollama's `nomic-embed-text` model.
4. Stores the embedded chunks in ChromaDB.

When an existing vector store is available, the application attempts to load it instead of rebuilding the index.

The retrieval tools return relevant document content to the agent, which can use that information to generate a context-aware response.

---

## 🗺️ Development Roadmap

- [x] **Agent and RAG core:** LangGraph workflow, conditional tool routing, PDF retrieval, and conversation summarization.
- [x] **Persistent state:** PostgreSQL checkpointer and asynchronous connection pooling.
- [x] **Terminal interface:** Interactive command-line execution.
- [x] **REST API integration:** FastAPI endpoint for agent interaction through Postman.
- [ ] **Validation improvements:** Strengthen request validation, configuration validation, tool input schemas, and structured output handling.
- [ ] **Testing and reliability:** Add automated tests for graph execution, retrieval, session isolation, and API error handling.
- [ ] **Security improvements:** Add appropriate authentication, authorization, input limits, and production-safe error handling.
- [ ] **Deployment:** Containerize the application and configure a suitable deployment environment.

---

## ⚠️ Current Limitations

- The API is designed for local development and is not yet production-hardened.
- Authentication and authorization are not yet implemented.
- Retrieval quality depends on the source documents, chunking strategy, embeddings, and retriever configuration.
- The project has not yet been presented as a fully tested production deployment.
- Generated vector stores and external services must be configured correctly for the application to run.

---

## 🎯 Project Goals

This project is a practical exploration of building conversational AI systems with stateful orchestration, retrieval-augmented generation, tool calling, persistent memory, and API integration.

It is intended to evolve toward a more robust AI application through improved validation, testing, security, and deployment practices.