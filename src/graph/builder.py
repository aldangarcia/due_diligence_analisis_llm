from langgraph.graph import StateGraph, START, END
from graph.state import EstadoAgente
from graph.router import router
from agents.financial_agent import financial_agent
from agents.sentiment_agent import sentiment_agent

def build_graph():
    builder = StateGraph(EstadoAgente)
    builder.add_node("financial_agent", financial_agent)
    builder.add_node("sentiment_agent", sentiment_agent)
    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges("supervisor", router, {...})
    return builder.compile()