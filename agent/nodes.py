from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from agent.state import AgentState
from agent.tools import llm_with_tools
import time
from langchain_core.messages import SystemMessage, RemoveMessage
from groq import RateLimitError
from config import llm

def summarize(state):
    print("--- Summarizer is called ---")
    messages = state["messages"]
    existing_summary = state.get("summary", "")
    
    if len(messages) > 6:
        print("Memory Limit Exceeded: Pruning Old Messages")
        
        messages_to_sum = messages[:-2]
        
        prompt = SystemMessage(content= f"You are a helpful assistant and you give a 50 word summary of the following messages:\n {messages_to_sum}. You can also use the old summary {existing_summary}")
        answer = llm.invoke([prompt])
        new_summary = answer.content
        
        # delete old messages
        delete_messages = [RemoveMessage(id=m.id) for m in messages_to_sum if getattr(m,'id', None)]
        return {"summary": new_summary,
                "messages": delete_messages}
        
    else:
        default_summary = existing_summary if existing_summary else 'The conversation just started, there is no summary yet'
        return {"summary": default_summary}

def agent(state):
    for i in range(3):
        try:
            print("--- Call Agent ---")
            summary = state.get("summary", "The conversation just started, there is no summary yet")
            messages = list(state["messages"])
            
            # Connecting summary and latest messages
            input_messages = [SystemMessage(content = f"Ιστορικό συνομιλίας: {summary}")] + messages
            
            response = llm_with_tools.invoke(input_messages)
            return {"messages": [response]} 
        
        except RateLimitError as e:
            if i==2:
                print('GROQ API is out of reach close the app and enter again')
                raise e
            
            print("You have reached GROQ's free limit tokem/minute. Wait 20 seconds")
            time.sleep(20)


def create_workflow(tools, checkpointer=None):
    # Define a new graph
    workflow = StateGraph(AgentState)

    # Agent Nodes
    workflow.add_node("summarize", summarize)
    workflow.add_node("agent", agent)
    retrieve = ToolNode(tools=tools)
    workflow.add_node("retrieve", retrieve)

    # Agent Edges
    workflow.add_edge(START, "summarize")
    workflow.add_edge("summarize", "agent")
    workflow.add_conditional_edges("agent", tools_condition, {"tools":"retrieve",END:END})
    workflow.add_edge("retrieve", "agent")

    graph = workflow.compile(checkpointer=checkpointer)
    return graph