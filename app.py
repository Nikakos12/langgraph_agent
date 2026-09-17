import asyncio
import sys

# correction psycopg for windows
if sys.platform == 'win32':
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except AttributeError:
        pass

from agent.nodes import create_workflow
from agent.tools import get_tools 
from agent.graph import compiled_graph
from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from config import DB_URI
from db.postgresql import get_pool
# this is the config section

async def main():
    if not DB_URI:
        raise ValueError("DATABASE URL is missing from the enviroment variables")
    
    # Open Async connection to PostgreSQL
    async with get_pool() as pool:
        # initialise checkpointer
        checkpointer = AsyncPostgresSaver(pool)
        
        # Creation of tables in the DB (if they do not exist)
        await checkpointer.setup()
        

        tools = get_tools()
        ag_graph = create_workflow(tools= tools, checkpointer=checkpointer)
        
        await compiled_graph(graph = ag_graph, thread_id = 'test-user-1')

if __name__ == '__main__':
    asyncio.run(main=main())