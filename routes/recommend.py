from flask_restx import Namespace, Resource, fields
from flask import request
from utils.suggest import get_top_stocks, get_mutual_fund_suggestions, suggest_travel_by_budget, suggest_savings, dynamic_allocation

ns = Namespace("recommend", description="Smart investment suggestions")

req_model = ns.model("RecommendRequest", {
    "age": fields.String(required=True, description="Age group or numeric age"),
    "goal": fields.String(required=True, description="Financial goal"),
    "expenses": fields.Raw(required=True, description="Dictionary of expense categories and amounts"),
})

def parse_age(age_input):
    try:
        if "-" in age_input:
            age_num = int(age_input.split("-")[0])
        else:
            age_num = int(age_input)
        return age_num
    except Exception:
        return None

@ns.route("/portfolio")
class RecommendPortfolio(Resource):
    @ns.expect(req_model)
    def post(self):
        data = request.json
        age = data.get("age")
        goal = data.get("goal")
        expenses = data.get("expenses", {})

        age_num = parse_age(age)
        if age_num is None:
            return {"error": "Invalid age provided."}, 400

        allocation = dynamic_allocation(age_num, goal)

        stocks = get_top_stocks()
        mutual_funds = get_mutual_fund_suggestions()

        travel_suggestions = []
        if "travel" in expenses:
            try:
                travel_budget = float(expenses.get("travel", 0))
                travel_suggestions = suggest_travel_by_budget(travel_budget)
            except Exception:
                travel_suggestions = []

        savings_tips = suggest_savings(expenses)

        return {
            "age": age_num,
            "goal": goal,
            "asset_allocation": allocation,
            "stock_suggestions": stocks,
            "mutual_fund_suggestions": mutual_funds,
            "travel_suggestions": travel_suggestions,
            "savings_tips": savings_tips
        }
