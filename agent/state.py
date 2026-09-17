# ---------------------> Langgraph imports
from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

# --------------------> Create Agent Class
class AgentState(TypedDict):
    # the add_messages function describes how the new messages are processed
    # Default is to replace the new message the old one, but with add_messages the new messages is appended
    messages: Annotated[Sequence[BaseMessage], add_messages]
    summary: str
