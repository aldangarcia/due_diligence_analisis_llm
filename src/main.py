from tools.sentiment import get_sentiment

result = get_sentiment.invoke({
    "symbol": "ITX.MC",
    "company_name": "Inditex",
    "consulta": "resultados financieros recientes"
})

print(result)