import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

tickers = ['ADX','MSFT','IBM','XELA','HNST','NCR','AAPL','CNK','NFLX','SI']
def get_latest_closing_price(symbol):
    stock = {}
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="2d")
        change =  ((data['Close'][1]-data['Close'][0])/data['Close'][1])*100
        stock['symbol'] = symbol
        stock['price'] = format(data['Close'][0], ".2f")
        stock['change'] =  str(format(change, ".2f"))
        stock['name'] = ticker.info['shortName']
        stock['changeInPrice'] = format(data['Close'][1]-data['Close'][0],'.2f')
        return stock
    except Exception as e:
        print(e)

def get_stocks():
    stocks = []
    for ticker in tickers:
        stocks.append(get_latest_closing_price(ticker))
    return stocks

