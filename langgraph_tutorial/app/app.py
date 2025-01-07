import os
from typing import Dict, TypedDict, List
from dotenv import load_dotenv
from langchain.schema import BaseMessage
from langgraph.graph import StateGraph,END
from langchain_groq import ChatGroq 
load_dotenv()

llm = ChatGroq(
        groq_api_key=os.environ.get("GROQ_API_KEY"),
        model_name="llama-3.1-70b-versatile",
        temperature=0.1,
        model_kwargs={"top_p": 0.5, "seed": 1337}
    )

class State(TypedDict):
    messages: List[BaseMessage]
    next_step: str
    
workflow = StateGraph(State)

def greet(state:State):
    state["messages"].append({"role": "assistant", "content": "Hello! What's your name?"})
    state["next_step"] = "get_name"
    return state

def get_name(state: State) -> State:
    name = state["messages"][-1]["content"]
    state["messages"].append({"role": "assistant", "content": f"Nice to meet you, {name}! How can I assist you today?"})
    state["next_step"] = "end"
    return state

workflow.add_node("greet", greet)
workflow.add_node("get_name", get_name)

workflow.set_entry_point("greet")
workflow.add_edge("greet", "get_name")
workflow.add_edge("get_name", END)
app = workflow.compile()
initial_state = {"messages": [],"next_step":""}
# Run the graph
for event in app.stream(initial_state):
    for output in event.values():
        if "messages" in output:
            for message in output["messages"]:
                if message["role"] == "assistant":
                    print(f"Assistant: {message['content']}")
                elif message["role"] == "human":
                    print(f"Human: {message['content']}")
    
    # Check if 'next_step' exists
    if "next_step" in output and output["next_step"] == "get_name":
        user_input = input("Your response: ")
        output["messages"].append({"role": "human", "content": user_input})

print("Conversation ended.")