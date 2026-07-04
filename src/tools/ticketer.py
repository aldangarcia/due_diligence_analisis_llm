from langchain_core.tools import tool
import financedatabase as fd

@tool
def get_ticketer(name:str, currency:str = None, market:str = None) -> str:
    """
    This function gets the name of the company and returns the symbol for yfinance
    """
    equities = fd.Equities()

    result = equities.search(
        name=name,
        currency=currency,
        market=market
    )

    if result.empty:
        return "No se encontró ninguna empresa con ese nombre"
    
    return result.index[0]

