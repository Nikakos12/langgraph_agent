from pydantic import Field, BaseModel
import json 

class ChatRequest(BaseModel):
    message: str = Field(
        description="The message/query sent to the agent"
    )
    thread_id: str = Field(description="The id of the user")

class ChatResponse(BaseModel):
    response: str = Field(description="The agent's response")