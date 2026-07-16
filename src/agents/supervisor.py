from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage, SystemMessage

from graph.state import EstadoAgente

from agents.financial_agent import financial_agent
from agents.sentiment_agent import sentiment_agent

from graph.router import router

def nodo_supervisor(state: EstadoAgente) -> dict:
    ultimo = state["messages"][-1].content
    print(f"[SUPERVISOR] Recibida consulta: {ultimo}")
    print(f"[SUPERVISOR] Derivando al agente correspondiente...")
    return {}

def nodo_sintetizar(state: EstadoAgente) -> dict:
    llm = ChatOpenAI(model="gpt-4o-mini")
    mensajes = [
        SystemMessage(content="""Eres un analista financiero senior.
        Con la información de los análisis anteriores, genera un informe 
        de due diligence estructurado con:
        - Resumen ejecutivo
        - Situación financiera
        - Sentimiento y reputación
        - Riesgos detectados
        - Conclusión"""),
    ] + state["messages"]  # añadimos todo el historial como contexto
    
    respuesta = llm.invoke(mensajes)
    return {"messages": [respuesta]}

builder = StateGraph(EstadoAgente)
builder.add_node("supervisor", nodo_supervisor)
builder.add_node("financial_agent", financial_agent)  # el grafo compilado como nodo
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