from langgraph.graph import StateGraph
from agent.llm import groq_llm
from agent.retriever import retriever
from typing import Optional,TypedDict

class AgentState(TypedDict):
    query: str
    context: Optional[str]
    answer: Optional[str]

def retrieve_node(state: AgentState):
    docs = retriever.get_relevant_documents(state["query"])
    state["context"] = "\n".join([d.page_content for d in docs])
    print("Context Chunks :\n")
    for doc in docs:
        print(doc)
    return state

def llm_node(state: AgentState):
    prompt = f"""
You are an assistant that follows the ReAct reasoning pattern.

Use the following context to answer the user’s question.
If the answer cannot be found in the context, say "I don’t know based on the provided context."

---
Context:
{state['context']}
---
Question:
{state['query']}
---
Instructions:
- First, think about the question and the context (Reason).
- Then, provide the final answer strictly based on the context (Act).
- Do not use any outside knowledge.
- If unsure, say you don't know.

Final Answer:
"""

    response = groq_llm.invoke(prompt)
    state["answer"] = response
    return state


# Build workflow
graph = StateGraph(AgentState)
graph.add_node("retrieve", retrieve_node)
graph.add_node("llm", llm_node)
graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "llm")
graph.set_finish_point("llm")

workflow = graph.compile()

# Async runner for FastAPI
async def run_agent(query: str) -> str:
    state: AgentState = {"query": query}
    final_state = workflow.invoke(state)
    return final_state["answer"]

