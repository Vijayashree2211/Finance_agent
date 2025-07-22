from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from models.db import init_db 
from routes import stock, recommend

app = Flask(__name__)
CORS(app)
api = Api(app, title="Financial Agent API", version="1.0", doc="/docs")

init_db()
api.add_namespace(stock.ns, path="/stock")
api.add_namespace(recommend.ns, path="/recommend")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
