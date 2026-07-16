from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage

from graph.state import EstadoAgente
from tools.ticketer import get_ticketer
from tools.financials import get_financials
from tools.metrics import get_ratios

tools = [get_ticketer, get_financials, get_ratios]
tools_disponibles = {t.name: t for t in tools}

llm = ChatOpenAI(model="gpt-4o-mini")
llm_con_tools = llm.bind_tools(tools)

def nodo_llm(state: EstadoAgente) -> dict:
    respuesta = llm_con_tools.invoke(state["messages"])
    return {"messages": [respuesta]}

def nodo_tools(state: EstadoAgente) -> dict:
    ultimo_mensaje = state["messages"][-1]
    resultados = []
    for llamada in ultimo_mensaje.tool_calls:
        print(f"Tool llamada: {llamada['name']} con args: {llamada['args']}")  # <- añade esto
        funcion = tools_disponibles[llamada["name"]]
        salida = funcion.invoke(llamada["args"])
        print(f"Resultado: {salida}")  # <- y esto
        resultados.append(ToolMessage(content=str(salida), tool_call_id=llamada["id"]))
    return {"messages": resultados}

def hay_que_usar_tools(state: EstadoAgente) -> str:
    if len(state["messages"]) > 10:
        print(f"Limite alcanzado ({len(state['messages'])} mensajes), forzando salida")
        return "terminar"
    ultimo = state["messages"][-1]
    return "usar_tools" if getattr(ultimo, "tool_calls", None) else "terminar"

builder = StateGraph(EstadoAgente)
builder.add_node("llm", nodo_llm)
builder.add_node("tools", nodo_tools)
builder.add_edge(START, "llm")
builder.add_conditional_edges(
    "llm",
    hay_que_usar_tools,
    {"usar_tools": "tools", "terminar": END}
)
builder.add_edge("tools", "llm")

financial_agent = builder.compile()
