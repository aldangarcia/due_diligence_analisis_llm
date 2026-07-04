from langchain_core.tools import tool
import yfinance as yf
import pandas as pd

@tool
def get_financials(symbol:str) -> dict:
    """
    Gets the symbol that we want to analyze and returns the data we are interested at
    """
    ticker = yf.Ticker(symbol)

    return {
    "income_stmt": ticker.income_stmt,
    "balance_sheet": ticker.balance_sheet,
    "cashflow": ticker.cashflow
    }