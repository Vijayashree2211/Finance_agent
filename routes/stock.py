from flask_restx import Namespace, Resource, fields
from flask import request
import yfinance as yf

ns = Namespace("stock", description="Stock operations")

stock_model = ns.model("StockRequest", {
    "ticker": fields.String(required=True)
})

@ns.route("/analyze")
class StockAnalysis(Resource):
    @ns.expect(stock_model)
    def post(self):
        data = request.json
        ticker = data["ticker"]
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo", interval="1d")

        if hist.empty:
            return {"error": "No data found."}, 404

        stats = hist["Close"].describe().to_dict()
        return {"ticker": ticker, "summary": stats}
