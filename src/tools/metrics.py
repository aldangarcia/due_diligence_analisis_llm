import yfinance as yf
from langchain_core.tools import tool

@tool
def get_ratios(symbol: str) -> dict:
    """
    Calcula los principales ratios financieros de una empresa dado su ticker.
    Devuelve márgenes, ratios de endeudamiento y liquidez.
    """
    ticker = yf.Ticker(symbol)
    
    income = ticker.income_stmt
    balance = ticker.balance_sheet

    # debug temporal: ver qué ticker está llegando y si tiene datos
    print(f"Ticker recibido: {symbol}")
    print(f"Columnas income_stmt: {income.columns.tolist()}")

    if income.empty or len(income.columns) == 0:
        return {"error": f"No se encontraron datos financieros para el ticker {symbol}"}

    revenue = income.loc["Total Revenue", income.columns[0]]
    gross_profit = income.loc["Gross Profit", income.columns[0]]
    net_income = income.loc["Net Income", income.columns[0]]
    ebitda = income.loc["EBITDA", income.columns[0]]
    total_debt = balance.loc["Total Debt", balance.columns[0]]
    equity = balance.loc["Common Stock Equity", balance.columns[0]]
    current_assets = balance.loc["Current Assets", balance.columns[0]]
    current_liabilities = balance.loc["Current Liabilities", balance.columns[0]]

    gross_margin = gross_profit / revenue
    net_margin = net_income / revenue
    ebitda_margin = ebitda / revenue
    debt_to_equity = total_debt / equity
    debt_to_ebitda = total_debt / ebitda
    current_ratio = current_assets / current_liabilities

    return {
        "gross_margin": gross_margin,
        "net_margin": net_margin,
        "ebitda_margin": ebitda_margin,
        "debt_to_equity":debt_to_equity,
        "debt_to_ebitda": debt_to_ebitda,
        "current_ratio": current_ratio
    }