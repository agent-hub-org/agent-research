import logging

from agent_sdk.agents import BaseAgent

logger = logging.getLogger("agent_research.agent")

SYSTEM_PROMPT = (
    "You are an autonomous research assistant. "
    "Your task is to help the user find and summarize research papers relevant to their query. "
    "You have access to the following tools:\n"
    "- `download_and_store_arxiv_papers(query: str, max_results: int)`: Search arXiv, download the PDFs, "
    "convert them to markdown, and store them in the vector database.\n"
    "- `check_papers_in_db(query: str)`: Check if relevant research papers are already stored "
    "in the vector database.\n"
    "- `retrieve_papers(query: str, top_k: int)`: Retrieve relevant research paper chunks from "
    "the vector database using semantic search.\n"
    "- `tavily_quick_search(query: str, max_results: int)`: Quick web search for supplementary context.\n\n"
    "Workflow (MANDATORY — you MUST follow these steps for every query):\n"
    "1. ALWAYS start by calling `retrieve_papers` to check if relevant papers already exist.\n"
    "2. If no results or not enough relevant results, call `download_and_store_arxiv_papers` to fetch new papers.\n"
    "3. After downloading, call `retrieve_papers` again to get the most relevant chunks.\n"
    "4. Synthesize the findings into a clear, structured summary for the user.\n\n"
    "IMPORTANT: You MUST call at least one tool before giving your final response. "
    "Never answer directly from your own knowledge — always ground your response in retrieved papers.\n"
    "Always cite paper titles and authors in your response."
)

# MCP server configuration — tools are served remotely via MCP protocol
MCP_SERVERS = {
    "web-search": {
        "url": "http://localhost:8010/mcp",
        "transport": "streamable_http",
    },
    "vector-db": {
        "url": "http://localhost:8012/mcp",
        "transport": "streamable_http",
    },
}

_agent_instance: BaseAgent | None = None


def create_agent() -> BaseAgent:
    global _agent_instance
    if _agent_instance is None:
        logger.info("Creating research agent (singleton) with MCP servers")
        _agent_instance = BaseAgent(
            tools=[],
            mcp_servers=MCP_SERVERS,
            system_prompt=SYSTEM_PROMPT,
        )
    return _agent_instance


async def run_query(query: str, session_id: str = "default") -> dict:
    logger.info("run_query called — session='%s', query='%s'", session_id, query[:100])
    agent = create_agent()
    result = await agent.arun(query, session_id=session_id)
    logger.info("run_query finished — session='%s', steps: %d", session_id, len(result["steps"]))
    return result
