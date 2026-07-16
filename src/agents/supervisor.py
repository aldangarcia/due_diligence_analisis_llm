from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage

from graph.state import EstadoAgente

from agents.financial_agent import financial_agent
from agents.sentiment_agent import sentiment_agent

from graph.router import router

from output.report import InformeEmpresa

def nodo_supervisor(state: EstadoAgente) -> dict:
    ultimo = state["messages"][-1].content
    print(f"[SUPERVISOR] Recibida consulta: {ultimo}")
    print(f"[SUPERVISOR] Derivando al agente correspondiente...")
    return {}

def nodo_sintetizar(state: EstadoAgente) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(InformeEmpresa)
    mensajes = [
        SystemMessage(content="""Eres un analista financiero senior con experiencia de 15 años analizando empresas.
        Genera un informe de due diligence estructurado con todos los campos."""),
    ] + state["messages"]
    
    informe = llm.invoke(mensajes)
    return {
        "informe": informe,
        "messages": [AIMessage(content=str(informe))]
    }


builder = StateGraph(EstadoAgente)
builder.add_node("supervisor", nodo_supervisor)
builder.add_node("financial_agent", financial_agent)  
builder.add_node("sentiment_agent", sentiment_agent)
builder.add_node("sintetizar", nodo_sintetizar)

builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", router, {
    "financial_agent": "financial_agent",
    "sentiment_agent": "sentiment_agent",
})
builder.add_edge("financial_agent", "sintetizar")
builder.add_edge("sentiment_agent", "sintetizar")
builder.add_edge("sintetizar", END)

supervisor = builder.compile()