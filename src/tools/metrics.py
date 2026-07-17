import yfinance as yf
from langchain_core.tools import tool
def safe_get(df, fila):
    """Intenta obtener una fila del DataFrame, devuelve None si no existe."""
    try:
        return df.loc[fila, df.columns[0]]
    except KeyError:
        return None

@tool
def get_ratios(symbol: str) -> dict:
    """
    Calcula los principales ratios financieros de una empresa dado su ticker.
    Devuelve márgenes, ratios de endeudamiento y liquidez.
    """
    ticker = yf.Ticker(symbol)
    income = ticker.income_stmt
    balance = ticker.balance_sheet

    print(f"Ticker recibido: {symbol}")
    print(f"Columnas income_stmt: {income.columns.tolist()}")

    if income.empty or len(income.columns) == 0:
        return {"error": f"No se encontraron datos financieros para el ticker {symbol}"}

    revenue = safe_get(income, "Total Revenue")
    gross_profit = safe_get(income, "Gross Profit")
    net_income = safe_get(income, "Net Income")
    ebitda = safe_get(income, "EBITDA")
    total_debt = safe_get(balance, "Total Debt")
    equity = safe_get(balance, "Common Stock Equity")
    current_assets = safe_get(balance, "Current Assets")
    current_liabilities = safe_get(balance, "Current Liabilities")

    ratios = {}

    # solo calculamos si tenemos los datos necesarios
    if gross_profit and revenue:
        ratios["gross_margin"] = gross_profit / revenue
    else:
        ratios["gross_margin"] = "No disponible (sector financiero)"

    if net_income and revenue:
        ratios["net_margin"] = net_income / revenue

    if ebitda and revenue:
        ratios["ebitda_margin"] = ebitda / revenue

    if total_debt and equity:
        ratios["debt_to_equity"] = total_debt / equity

    if total_debt and ebitda:
        ratios["debt_to_ebitda"] = total_debt / ebitda

    if current_assets and current_liabilities:
        ratios["current_ratio"] = current_assets / current_liabilities
    else:
        ratios["current_ratio"] = "No disponible (sector financiero)"

    return ratios