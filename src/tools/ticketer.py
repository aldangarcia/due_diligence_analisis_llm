from langchain_core.tools import tool
import yfinance as yf


@tool
def get_ticketer(name: str, exchange: str = None) -> str:
    """
    Searches for the stock ticker of a company given its name.
    Returns the ticker symbol to use with yfinance.
    """
    resultado = yf.Search(name)
    quotes = resultado.quotes

    if not quotes:
        return f"No ticker found for {name}"

    # probamos TODOS los tickers que devuelve yf.Search directamente
    # sin construir nada, usando los símbolos tal cual
    for q in quotes:
        symbol = q["symbol"]
        test = yf.Ticker(symbol).income_stmt
        if not test.empty:
            return symbol

    # si ninguno tiene datos, devolvemos el primero
    return quotes[0]["symbol"]