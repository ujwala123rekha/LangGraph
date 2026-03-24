from langgraph.graph import StateGraph

state = {"input": "user "}

def decision_node(state):
    if "math" in state["input"].lower():
        state["next"] = "math"
    else:
       state["next"] = "chat"
    return state

def math_node(state):
    state["output"] = " Doing Mathematical operation"
    return state

def chat_node(state):
    state["output"] = "Chat application"
    return state

def route(state):
    return state["next"]

graph = StateGraph(dict)

graph.add_node("decision", decision_node)
graph.add_node("math_node", math_node)
graph.add_node("chat_node", chat_node)

graph.set_entry_point("decision")

graph.add_conditional_edges(
    "decision",
    route,
    {
        "math": "math_node",
        "chat": "chat_node"
    }
)


app = graph.compile()
while True:
    user = input("Say whats on your mind").lower()
    if user.lower() =="exit":
        print("Have a good day")
        break
    else:
     result = app.invoke({"input":user})
    print(result["output"])
