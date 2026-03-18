# agent-research

Research paper agent that uses MCP servers for tools and exposes itself via both a REST API and an A2A protocol server.

## What It Does

- Autonomous research assistant for finding and summarizing academic papers
- Searches arXiv, downloads PDFs, converts to markdown, stores in vector DB
- Semantic search over stored papers
- Mandatory workflow: `retrieve_papers` → download if needed → retrieve again → synthesize
- Always cites paper titles and authors

## Architecture

- **Tools** served remotely via 2 MCP servers (web-search:8010, vector-db:8012)
- **Agent** built on agent-sdk (`BaseAgent` with LangGraph)
- **LLM Provider:** Groq (llama-3.3-70b-versatile)
- **A2A server** mounted at `/a2a` for agent-to-agent communication
- **REST API** for direct usage
- **MongoDB** for conversation persistence

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/ask` | Send a research query |
| GET | `/history/{session_id}` | Retrieve conversation history |
| GET | `/health` | Health check |
| — | `/a2a` | A2A protocol endpoint (used by marketplace) |

## A2A Agent Card

- **Skills:** paper-search, literature-review
- **URL:** `http://localhost:9002`

## Structure

```
agent-research/
├── app.py              # FastAPI + A2A server (port 8081)
├── pyproject.toml
├── agents/
│   └── agent.py        # Research agent with MCP config
├── a2a/
│   ├── agent_card.py   # A2A Agent Card definition
│   ├── executor.py     # ResearchAgentExecutor
│   └── server.py       # A2A Starlette app builder
├── database/
│   └── mongo.py        # MongoDB conversation storage
└── agent-sdk/          # Shared agent framework (submodule)
```

## Prerequisites

MCP tool servers must be running on ports 8010 and 8012.

## Running

```bash
infisical run -- uvicorn app:app --host 0.0.0.0 --port 8081
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key |
| `MONGO_URI` | MongoDB connection string |

## Dependencies

`agent-sdk`, `langchain`, `langgraph`, `motor`, `fastapi`, `uvicorn`, `a2a-sdk`, `langchain-mcp-adapters`
