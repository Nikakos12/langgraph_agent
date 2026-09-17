# 🤖 LangGraph Conversational RAG Agent

A stateful AI Agent architecture built with **LangGraph**, **PostgreSQL**, and **ChromaDB**. 

This project demonstrates a multi-node conversational graph featuring short-term memory summarization, domain-specific retrieval-augmented generation (RAG), and persistent database state checkpointing.

---

## 📌 Project Overview

The primary goal of this repository is to build an AI Agent architecture that bridges the gap between stateful LLM orchestration, vector databases, and production web services. 

### Key Architectural Features:
* **Stateful Graph Orchestration**: Built using `LangGraph` to manage multi-step reasoning, tool execution, and dynamic flow control.
* **Context Summarization & Memory Management**: Automatically summarizes past chat context to prevent LLM token limits from overflowing.
* **Domain-Specific RAG Tools**: Dual vector-search tools backed by local `ChromaDB` instances and `Ollama` embeddings (`nomic-embed-text`) querying specialized document corpuses.
* **Persistent Session Checkpointing**: Integrated with `PostgreSQL` via `psycopg-pool` to save state across multi-turn interactions.

---

## 🏗️ Repository Architecture & Project Structure

```text
.
├── app.py                  # Main entry point: initializes connection pools, checkpointers, & workflow
├── config.py               # Application configuration and environment variable management
├── db/
│   └── postgresql.py       # Asynchronous PostgreSQL connection pool initialization (psycopg-pool)
├── agent/                  # Core Agent Architecture & LangGraph Logic
│   ├── state.py            # Agent state schema definition (AgentState TypedDict)
│   ├── nodes.py            # Graph node implementations (Summarizer, Core Agent, Tool Execution)
│   ├── tools.py            # Custom RAG tools and vectorstore initialization
│   └── graph.py            # Workflow compilation and asynchronous interactive agent runtime
├── api/                    # [In Progress] Web API Layer
│   ├── router.py           # FastAPI routes exposing agent endpoints
│   └── schemas.py          # API request and response data models
├── Chroma_db/              # Local persistent vector database storage (Git-ignored)
├── music/                  # Source domain documents (e.g., Introduction to Music PDF)
└── archeology/             # Source domain documents (e.g., Archaeology Starter PDF)
```

## File & Folder Breakdown

### 📄 Core Engine
* **`app.py`**: The central orchestrator. Sets up platform event loop policies, opens the async PostgreSQL connection pool, initializes the graph checkpointer, compiles the workflow with tools, and executes the agent session.
* **`config.py`**: Handles environment variable loading and sets up runtime credentials (such as API keys and database links).

### 🧠 Agent Module (`/agent`)
* **`agent/state.py`**: Defines `AgentState`, tracking messages and running summary context across conversation cycles.
* **`agent/nodes.py`**: Houses the graph processing logic:
  * **`summarize`**: Trims older message history and uses LLM calls to build rolling conversation summaries.
  * **`agent`**: Invokes the primary LLM with system state and available tools.
* **`agent/tools.py`**: Builds domain-specific retriever tools (`music_retriever_tool`, `arch_retriever_tool`). Handles automatic PDF document loading, text splitting, and vector indexing into ChromaDB.
* **`agent/graph.py`**: Constructs the state graph, defines conditional edges for tool routing, applies recursion limits, and manages the async interactive CLI interface.

### 💾 Database & Storage (`/db`, `/Chroma_db`, `/music`, `/archeology`)
* **`db/postgresql.py`**: Configures the asynchronous connection pool (`AsyncConnectionPool`) for LangGraph's `AsyncPostgresSaver`, enabling persistent state checkpoints.
* **`music/` & `archeology/`**: Folders holding source PDF documents parsed into vector embeddings.
* **`Chroma_db/`**: Local storage directory housing the embedded vector datasets.

### 🌐 Web API Layer (`/api`) — *Next Phase*
* **`api/schemas.py`**: Defines input request payloads (e.g., `ChatRequest`, `SessionID`) and structured response formats.
* **`api/router.py`**: Exposes HTTP and WebSocket endpoints via FastAPI, allowing frontend applications to interact asynchronously with the LangGraph engine.

---

## 🛠️ Tech Stack & Dependencies

| Category | Technologies |
| :--- | :--- |
| **Agent Orchestration** | LangGraph, LangChain |
| **LLM Engine** | ChatGroq (`groq`) |
| **Embeddings & Vector Database** | Ollama (`nomic-embed-text`), ChromaDB |
| **Database & Persistence** | PostgreSQL, `psycopg-pool`, `AsyncPostgresSaver` |
| **Web Framework (Target)** | FastAPI |
| **Deployment (Target)** | Docker, AMD Cloud Infrastructure |

---

## 🛣️ Project Roadmap & Future Enhancements

- [x] **Phase 1: Agent & RAG Core**: Complete multi-node workflow, Chroma vector retrievers, and memory summarization.
- [x] **Phase 2: Persistence**: Integrate PostgreSQL state checkpointer with async connection pooling.
- [ ] **Phase 3: Validation Refactor**: Implement Pydantic for fail-fast configuration (`pydantic-settings`), structured tool inputs (`args_schema`), and LLM output parsing.
- [ ] **Phase 4: API Integration**: Build out `/api/schemas.py` and `/api/router.py` using FastAPI for RESTful and streaming chat interactions.
- [ ] **Phase 5: Cloud Deployment**: Containerize the service with Docker and deploy the full stack to AMD Cloud infrastructure.