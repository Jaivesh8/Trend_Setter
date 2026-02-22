import os
import json
from typing import List, Optional, TypedDict
from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

from app.transcript.query_pipeline import query_reels
from dotenv import load_dotenv
load_dotenv()

# ── Pydantic output schema (unchanged) ───────────────────────────────────────
class IdeaStructure(BaseModel):
    concept: str; hook: str; structure: List[str]
    emotion: str; why_it_works: str

class OptimizationVariant(BaseModel):
    change: str; add: str; result: str

class OptimizationSuggestion(BaseModel):
    second_idea_emotional_variant: OptimizationVariant

class BestFitRecommendation(BaseModel):
    best_idea_index: int; reason: str

class AnalysisBlock(BaseModel):
    performance_drivers: List[str]; engagement_triggers: List[str]

class StrategistOutput(BaseModel):
    analysis: AnalysisBlock
    patterns: List[str]
    ideas: List[IdeaStructure]
    best_fit_recommendation: BestFitRecommendation
    optimization_suggestion: OptimizationSuggestion


# ── LangGraph state ───────────────────────────────────────────────────────────
class AgentState(TypedDict):
    query: str
    chat_history: List
    documents: List[Document]
    answer: Optional[StrategistOutput]
    sources: List[dict]


# ── LLM ──────────────────────────────────────────────────────────────────────
_base_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.85, max_tokens=2048)
llm = _base_llm.with_structured_output(StrategistOutput, method="json_mode")


# ── System prompt (unchanged) ─────────────────────────────────────────────────
# system_prompt = """
# You are an expert social media performance analyst and viral content strategist specializing in Instagram Reels.
# [... keep your full system prompt here ...]

# Retrieved Reels:
# {context}
# """
system_prompt = """
You are an expert social media performance analyst and viral content strategist specializing in Instagram Reels.

Analyze the retrieved reels and return a JSON response. IMPORTANT: Every field marked as a list MUST be a JSON array, even if it contains only one item.

Your response must be valid JSON with exactly these fields:
- "analysis": {{"performance_drivers": ["string1", "string2"], "engagement_triggers": ["string1", "string2"]}}
- "patterns": ["string1", "string2"]
- "ideas": [{{"concept": "string", "hook": "string", "structure": ["step1", "step2", "step3"], "emotion": "string", "why_it_works": "string"}}]
- "best_fit_recommendation": {{"best_idea_index": 0, "reason": "string"}}
- "optimization_suggestion": {{"second_idea_emotional_variant": {{"change": "string", "add": "string", "result": "string"}}}}

Retrieved Reels:
{{context}}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])


# ── Graph nodes ───────────────────────────────────────────────────────────────
def retrieve(state: AgentState) -> AgentState:
    """Node 1: fetch relevant reels"""
    results = query_reels(state["query"], top_k=8, text_weight=0.6)
    docs = []
    sources = []
    for r in results:
        meta = r["metadata"]
        reel = r.get("reel", {})
        docs.append(Document(
            page_content=f"Caption: {meta.get('caption','')}\nTranscript: {reel.get('transcript','')}".strip(),
            metadata={
                "id": r["id"], "owner": meta.get("owner", ""),
                "likes": meta.get("likes", 0), "duration": meta.get("duration", 0),
                "rrf_score": r.get("rrf_score", 0), "url": meta.get("video_url", ""),
            }
        ))
        sources.append(docs[-1].metadata)
    return {**state, "documents": docs, "sources": sources}


def generate(state: AgentState) -> AgentState:
    """Node 2: run LLM with retrieved context"""
    context = "\n\n".join(d.page_content for d in state["documents"])
    response = llm.invoke(prompt.format_messages(
        context=context,
        chat_history=state["chat_history"],
        input=state["query"]
    ))
    return {**state, "answer": response}


def update_history(state: AgentState) -> AgentState:
    """Node 3: persist chat turn"""
    history = list(state["chat_history"])
    history.append(HumanMessage(content=state["query"]))
    answer_str = (
        state["answer"].model_dump_json(indent=2)
        if isinstance(state["answer"], StrategistOutput)
        else str(state["answer"])
    )
    history.append(AIMessage(content=answer_str))
    return {**state, "chat_history": history}


# ── Build graph ───────────────────────────────────────────────────────────────
workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)
workflow.add_node("update_history", update_history)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", "update_history")
workflow.add_edge("update_history", END)

graph = workflow.compile()

# ── Shared chat history across turns ─────────────────────────────────────────
_chat_history: List = []

def conversational_rag(query: str) -> dict:
    global _chat_history
    result = graph.invoke({
        "query": query,
        "chat_history": _chat_history,
        "documents": [],
        "answer": None,
        "sources": []
    })
    _chat_history = result["chat_history"]
    return {"answer": result["answer"], "context": result["documents"], "sources": result["sources"]}