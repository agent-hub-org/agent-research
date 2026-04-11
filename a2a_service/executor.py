import logging

from agent_sdk.a2a.executor import StreamingAgentExecutor
from agents.agent import run_query, stream_for_a2a

logger = logging.getLogger("agent_research.a2a_executor")

class ResearchAgentExecutor(StreamingAgentExecutor):
    """A2A executor that streams research agent responses chunk-by-chunk."""
    def __init__(self):
        super().__init__(run_query_fn=run_query, stream_fn=stream_for_a2a)
