# This file is your FastAPI application's entry point. Its job is to start the server's application, 
# initialize your LangGraph agent and its database connection, make the graph available to API requests, 
# and clean up when the application shuts down.

from agent.graph import run_agent
from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from agent.nodes import create_workflow
from agent.tools import get_tools
from api.routes import router
from db.postgresql import get_pool

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with get_pool() as pool:
        checkpointer = AsyncPostgresSaver(pool)
        await checkpointer.setup()
        
        tools = get_tools()
        app.state.graph = create_workflow(
            tools=tools,
            checkpointer=checkpointer
        )
        
        yield 
        
        app.state.graph = None

app = FastAPI(lifespan=lifespan)
app.include_router(router)