import yfinance as yf

ticker = yf.Ticker("ITX.MC")  # Inditex como ejemplo

print(ticker.balance_sheet.index.tolist())