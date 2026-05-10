from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

#Hugging face model
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="auto")

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=128, temperature=0.7)
llm = HuggingFacePipeline(pipeline=pipe)

#Nodes and Edges
class AgentState(TypedDict):
    question: str
    category: str
    answer: str

def classify(state: AgentState):
    question = state["question"].lower()
    if any(word in question for word in ["python", "java", "code", "recursion", "programming"]):
        category = "programming"
    elif any(word in question for word in ["machine learning", "ai", "overfitting", "ml", "neural"]):
        category = "ml"
    else:
        category = "general"
    print(f"DEBUG: Classified as [{category.upper()}]")
    return {"category": category}

def programming_expert(state: AgentState):
    print("Programming Expert is responding...")
    response = llm.invoke(f"Question: {state['question']}\nAnswer:")
    return {"answer": response}

def ml_expert(state: AgentState):
    print("ML Expert is responding...")
    response = llm.invoke(f"Question: {state['question']}\nAnswer:")
    return {"answer": response}

def general_expert(state: AgentState):
    print("General Expert is responding...")
    response = llm.invoke(f"Question: {state['question']}\nAnswer:")
    return {"answer": response}

def router(state: AgentState):
    return state["category"]

#Connection 
workflow = StateGraph(AgentState)
workflow.add_node("classifier", classify)
workflow.add_node("programming", programming_expert)
workflow.add_node("ml", ml_expert)
workflow.add_node("general", general_expert)
workflow.set_entry_point("classifier")
workflow.add_conditional_edges("classifier", router, {"programming": "programming", "ml": "ml", "general": "general"})
workflow.add_edge("programming", END)
workflow.add_edge("ml", END)
workflow.add_edge("general", END)
app = workflow.compile()

question = "What is recursion in Python?" # For eg
result = app.invoke({"question": question})
print("\n" + "="*30)
print("RESPONSE:")
print(result["answer"])
