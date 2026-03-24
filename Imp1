from langgraph.graph import StateGraph

state ={
    "input" : "Ujwala"
}

def hello(state):
    state["output"] = "Hello " + state["input"]
    return state

graph = StateGraph(dict)
graph.add_node("chat",hello)
graph.set_entry_point("chat")
app = graph.compile()
result = app.invoke({"input" : "Ujwala"})
print(result)

