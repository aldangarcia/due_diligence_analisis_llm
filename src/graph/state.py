from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import add_messages
from output.report import InformeEmpresa


class EstadoAgente(TypedDict):
    messages : Annotated[list, add_messages]
    informe: Optional[InformeEmpresa]

