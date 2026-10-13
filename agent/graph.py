from langchain_core.messages import HumanMessage
from langgraph.errors import GraphRecursionError
import asyncio

async def compiled_graph(graph, thread_id: str):
    # Define or generate thread_id outside the loop for the current session
    thread_id = 'test-user-1' # str(uuid.uuid4())
    
    # create the config dictionary containing thread_id
    config = {
        "configurable": {
            "thread_id": thread_id
        },
        "recursion_limit": 6,
    }
    
    if thread_id:
        print('Thread ID has been initiated')
    
    while True:
        try:
            query = await asyncio.to_thread(input, "You:\n")
            
            if not query.strip():
                continue
            if query.strip().lower() in ["exit", "quit"]:
                print('Exiting agent...')
                break
            print(query)

            output_state = await graph.ainvoke({'messages': [HumanMessage(content = query)]}, 
                                        config = config)
            
            final_response = output_state['messages'][-1]
            print(f"\n\n Outout state is: \n{output_state}")
            print(f"\nThe output state type is {type(output_state)}")

            print(f"Bot:\n {final_response.content}")
        except GraphRecursionError:
            print("\n [SystemWarning] The query required too many steps. Please break down your requests in to smaller steps.")
        except Exception as e:
            print(f'\n[Error] {e}')
            
            
async def run_agent(graph, message:str, thread_id:str):
        
        # create the config dictionary containing thread_id
        config = {
            "configurable": {
                "thread_id": thread_id
            },
            "recursion_limit": 6,
        }
        
        output_state = await graph.ainvoke({'messages': [HumanMessage(content = message)]}, 
                                                config = config)
        
        final_response = output_state["messages"][-1]
        
        return final_response.content