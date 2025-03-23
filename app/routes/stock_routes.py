from flask import jsonify , Blueprint

from app.services.stock_service import(
    stockinfo, stockdividend , stockfinancials ,stocknews
)

stockblueprint  =Blueprint('stock',__name__)

@stockblueprint.route('/stock/<symbol>' ,methods =['GET'])
def getstockinfo(symbol):
    return jsonify(stockinfo(symbol))

@stockblueprint.route('/stock/<symbol>/dividend' ,methods =['GET'])
def getstockdividend(symbol):
    return jsonify(stockdividend(symbol))

@stockblueprint.route('/stock/<symbol>/financials' ,methods =['GET'])
def getstockfinancials(symbol):
    return jsonify(stockfinancials(symbol))

@stockblueprint.route('/stock/<symbol>/news/' , methods = ['GET'])
def getstocknews(symbol):
    return jsonify(stocknews(symbol))
