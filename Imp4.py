from langgraph.graph import StateGraph,END

state = {"input":"num",
         f"count" : 0,
        "output": "num"}

def process(state):
    state["count"] += 1
    state["output"] = state["output"] + " Good"
    return state

def decision(state):
    if state["count"] < 20:
        state["next"] = "loop"
    else:
        state["next"] = "end"
    return state


def route(state):
    return state["next"]


graph = StateGraph(dict)
graph.add_node("decision",decision)
graph.add_node("process",process)

graph.set_entry_point("process")
graph.add_edge("process", "decision")
graph.add_conditional_edges(
    "decision",
     route,
    {
        "loop": "process",
        "end": END
    }
)

app = graph.compile()

result = app.invoke({
    "input": "hello",
    "count": 0,
    "output": ""
})

print(result["output"])


