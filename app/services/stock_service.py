import yfinance as yf
from flask import jsonify
import json

def stockinfo(symbol):
    try:
        stock = yf.Ticker(symbol)
        stockinfos = dict(stock.info)
        return stockinfos
    except Exception as e:
        return {'Error': str(e)}

def stockdividend(symbol):
    try:
        stock = yf.Ticker(symbol)
        stockinfos = stock.dividends.to_json(orient="index") 
        return json.loads(stockinfos)  
    except Exception as e:
        return {'Error': str(e)}
    
def stockfinancials(symbol):
    try:
        stock = yf.Ticker(symbol)
        stockinfos = stock.financials.to_json(orient='index')
        return json.loads(stockinfos)
    except Exception as e:
        return {'Error': str(e)}

def stocknews(symbol):
    try:
        news = yf.Search(symbol, news_count=10).news
        return news
    except Exception as e:
        return {'Error': str(e)}