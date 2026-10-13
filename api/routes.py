from fastapi import APIRouter, HTTPException, Request
from langchain_core.messages import HumanMessage
from api.schemas import ChatRequest, ChatResponse
from agent.graph import run_agent

router = APIRouter()


@router.post('/chat', response_model=ChatResponse)
async def chat(request_data:ChatRequest, request: Request):
    
    graph = request.app.state.graph
    
    if graph is None:
        raise HTTPException(
            status_code=503,
            detail = 'Agent is not initialized'
        )
        
    response = await run_agent(
        graph=graph,
        message = request_data.message,
        thread_id=request_data.thread_id
    )
    
    return ChatResponse(response=response)