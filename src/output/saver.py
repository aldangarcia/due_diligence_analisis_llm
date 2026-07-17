import json 
import os 
from datetime import datetime

from output.report import InformeEmpresa

def guardar_informe(informe:InformeEmpresa):
    os.makedirs("results", exist_ok=True)

    nombre = f"{informe.empresa.replace(' ', '_').lower()}_{datetime.today().strftime('%Y-%m-%d')}"

    with open(f"results/{nombre}.json", "w", encoding="utf-8") as f:
        json.dump(informe.model_dump(), f, ensure_ascii=False, indent=2)

    md = f"""# Informe de Due Diligence — {informe.empresa}

**Ticker:** {informe.ticker}  
**Fecha:** {datetime.today().strftime('%d/%m/%Y')}  
**Puntuación:** {informe.puntuacion}/10

---

## Resumen Ejecutivo
{informe.resumen_ejecutivo}

---

## Situación Financiera
{informe.situacion_financiera}

---

## Ratios Financieros Clave

| Ratio | Valor | Interpretación |
|-------|-------|----------------|
| Margen Bruto | {informe.ratios.get('gross_margin', 'N/A')} | > 40% es saludable |
| Margen Neto | {informe.ratios.get('net_margin', 'N/A')} | > 10% es bueno |
| Margen EBITDA | {informe.ratios.get('ebitda_margin', 'N/A')} | > 15% es saludable |
| Deuda/Equity | {informe.ratios.get('debt_to_equity', 'N/A')} | < 1 es conservador |
| Deuda/EBITDA | {informe.ratios.get('debt_to_ebitda', 'N/A')} | < 3 es saludable |
| Current Ratio | {informe.ratios.get('current_ratio', 'N/A')} | > 1.5 es bueno |

---

## Sentimiento y Reputación
{informe.sentimiento_reputacion}

---

## Riesgos Detectados
{chr(10).join(f"- {r}" for r in informe.riesgos_detectados)}

---

## Conclusión
{informe.conclusion}

---
*Informe generado automáticamente por el agente de due diligence.*  
*Fuentes: yfinance, Tavily, NewsAPI*
"""

    with open(f"results/{nombre}.md", "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Informe guardado en results/{nombre}.json y results/{nombre}.md")
