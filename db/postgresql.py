from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from config import DB_URI

# Initialize an async connection pool
# max_size = 10, allows 10 parallel connections
# autocommits = True, ensures checkpoints commit immediately without manual transaction management
def get_pool():
    if not DB_URI:
        raise ValueError("DATABASE URL is missing from enviroment variables")
    return AsyncConnectionPool(conninfo=DB_URI, max_size=10, kwargs={"autocommit":True})
