from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_huggingface import HuggingFacePipeline 
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline 
import torch 

# Hugging face model
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0" 
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, device_map="auto")

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=128, temperature=0.7)
llm = HuggingFacePipeline(pipeline=pipe)


class AgentState(TypedDict):
    question: str
    answer: str

#Node
def call_agent(state: AgentState):
    print("Agent is thinking")
    response = llm.invoke(f"Question: {state['question']}\nAnswer:")
    return {"answer": response} 

workflow = StateGraph(AgentState)

workflow.add_node("agent", call_agent)

workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

app = workflow.compile()

question = "Explain recursion simply."
result = app.invoke({"question": question})
print(f"RESPONSE: {result['answer']}")
