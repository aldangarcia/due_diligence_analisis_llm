from agents.supervisor import supervisor
from output.saver import guardar_informe
from output.report import InformeEmpresa
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# 1) ejecuta el supervisor normalmente sin campo informe
resultado = supervisor.invoke({
    "messages": [HumanMessage(content="Analiza Inditex completamente")],
})

# 2) coge todos los mensajes y genera el informe estructurado aquí
llm = ChatOpenAI(model="gpt-4o-mini").with_structured_output(InformeEmpresa)
informe = llm.invoke([
    SystemMessage(content="""Eres un analista financiero senior.
    Con la información de los análisis anteriores, genera un informe 
    de due diligence estructurado con todos los campos requeridos.
    La puntuación es del 1 al 10 donde 10 es excelente."""),
] + resultado["messages"])

# 3) guarda los archivos
guardar_informe(informe)

# 4) muestra el resultado
print(f"\nEmpresa: {informe.empresa}")
print(f"Puntuación: {informe.puntuacion}/10")
print(f"Riesgos: {informe.riesgos_detectados}")

