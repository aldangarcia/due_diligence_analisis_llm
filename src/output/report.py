from pydantic import BaseModel, Field
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

class RatiosFinancieros(BaseModel):
    gross_margin: Optional[str] = Field(default=None, description="margen bruto como porcentaje o 'No disponible'")
    net_margin: Optional[str] = Field(default=None, description="margen neto como porcentaje")
    ebitda_margin: Optional[str] = Field(default=None, description="margen EBITDA como porcentaje")
    debt_to_equity: Optional[str] = Field(default=None, description="ratio deuda sobre capital")
    debt_to_ebitda: Optional[str] = Field(default=None, description="ratio deuda sobre EBITDA")
    current_ratio: Optional[str] = Field(default=None, description="ratio de liquidez corriente o 'No disponible'")

class InformeEmpresa(BaseModel):
    empresa: str = Field(description="nombre de la empresa a analizar")
    ticker: str = Field(description="indice de la empresa a analizar")
    resumen_ejecutivo: str = Field(description="resumen ejecutivo del análisis")
    situacion_financiera: str = Field(description="situacion financiera actual de la empresa")
    sentimiento_reputacion: str = Field(description="sentimiento sobre la reputación de la empresa: negativo, positivo o neutro")
    riesgos_detectados: list[str] = Field(description="lista de los riesgos detectados para la empresa")
    conclusion: str = Field(description="conclusion del estado de la empresa para el due diligence")
    puntuacion: float = Field(description="puntuacion del 1 al 10 para la empresa")