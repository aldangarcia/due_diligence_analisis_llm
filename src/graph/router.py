from graph.state import EstadoAgente
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.types import Send
from dotenv import load_dotenv
load_dotenv()

def router(state: EstadoAgente):
    llm = ChatOpenAI(model="gpt-4o-mini")
    decision = llm.invoke([SystemMessage(content="""Decides qué agente usar según la pregunta del usuario.
        Responde SOLO con una de estas palabras exactas:
        - financial_agent
        - sentiment_agent
        - ambos"""),
        state["messages"][-1]
    ])

    resultado = decision.content.strip()

    if resultado == "ambos":
        return [
            Send("financial_agent", state),
            Send("sentiment_agent", state)
        ]
    elif resultado == "financial_agent":
        return "financial_agent"
    else:
        return "sentiment_agent"