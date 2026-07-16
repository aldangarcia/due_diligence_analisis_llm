from agents.supervisor import supervisor
from langchain_core.messages import HumanMessage

resultado = supervisor.invoke({
    "messages": [HumanMessage(content="Analiza Inditex completamente")]
})

print(resultado["messages"][-1].content)