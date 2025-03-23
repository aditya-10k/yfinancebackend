from flask import Flask
from app.routes.stock_routes import stockblueprint

app = Flask(__name__)

app.register_blueprint(stockblueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, port=5000)