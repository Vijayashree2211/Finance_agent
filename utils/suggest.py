import yfinance as yf
import requests, os
from dotenv import load_dotenv
load_dotenv()
def get_top_stocks():
    stock_list = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "JPM", "V", "JNJ"]
    performance = []

    for symbol in stock_list:
        try:
            data = yf.Ticker(symbol).history(period="1mo")
            if not data.empty:
                growth = ((data["Close"].iloc[-1] - data["Close"].iloc[0]) / data["Close"].iloc[0]) * 100

                performance.append((symbol, round(growth, 2)))
        except:
            continue

    performance.sort(key=lambda x: x[1], reverse=True)
    return [f"{s[0]}: {s[1]}%" for s in performance[:5]]

def get_mutual_fund_suggestions():
    API_KEY = os.getenv("PERPLEXITY_API_KEY")
    URL = "https://api.perplexity.ai/chat/completions"

    if not API_KEY:
        return ["Missing API key. Set PERPLEXITY_API_KEY environment variable."]

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar",  # or sonar-medium-chat / sonar-pro-chat depending on access
        "messages": [
            {"role": "system", "content": "You are a financial assistant."},
            {"role": "user", "content": "Suggest the top 5 mutual funds in India based on recent performance and CAGR."}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }

    try:
        response = requests.post(URL, headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]

        # Clean and split reply into lines
        suggestions = [line.strip() for line in reply.split("\n") if line.strip()]
        return suggestions

    except requests.exceptions.HTTPError as e:
        return [f"API Error: {e.response.status_code} - {e.response.text}"]
    except Exception as e:
        return [f"Unexpected error: {str(e)}"]



def suggest_travel_by_budget(budget_inr):
    API_KEY = os.getenv("PERPLEXITY_API_KEY")
    URL = "https://api.perplexity.ai/chat/completions"

    if not API_KEY:
        return ["Missing API key. Set PERPLEXITY_API_KEY environment variable."]

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar",  # or sonar-medium-chat / sonar-pro-chat
        "messages": [
            {"role": "system", "content": "You are a helpful travel assistant."},
            {"role": "user", "content": f"Suggest travel destinations in India within ₹{budget_inr} budget."}
        ],
        "max_tokens": 200,
        "temperature": 0.7
    }

    try:
        response = requests.post(URL, headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]

        # Clean each suggestion (remove numbering if present)
        suggestions = []
        for line in reply.split("\n"):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith("-")):
                line = line.lstrip("1234567890.-) ")
                suggestions.append(line)
            elif line:
                suggestions.append(line)
        return suggestions

    except requests.exceptions.HTTPError as e:
        return [f"API Error: {e.response.status_code} - {e.response.text}"]
    except Exception as e:
        return [f"Unexpected error: {str(e)}"]


def suggest_savings(expenses):
    total = sum(expenses.values())
    non_essentials = sum(v for k, v in expenses.items() if k.lower() not in ['medicine', 'grocery', 'academic'])
    
    suggestions = []
    if non_essentials > 0.4 * total:
        suggestions.append("💡 Consider cutting down non-essential expenses.")
    if total > 50000:
        suggestions.append("💰 Start a SIP or Recurring Deposit (RD) to lock in monthly savings.")
    else:
        suggestions.append("📱 Track daily spending using apps like Walnut or Moneyview.")
    if "medicine" not in expenses:
        suggestions.append("⚕️ It's good to keep a monthly buffer for health expenses.")
    return suggestions

def dynamic_allocation(age_num, goal):
    """
    Return asset allocation dict based on age and financial goal.
    Allocation percentages always sum to 100.
    """

    # Base allocations by age
    if age_num <= 25:
        base_alloc = {
            "Stocks": 60,
            "Mutual Funds": 20,
            "Gold": 5,
            "Real Estate": 10,
            "Bonds": 5
        }
    elif age_num <= 35:
        base_alloc = {
            "Stocks": 50,
            "Mutual Funds": 25,
            "Gold": 5,
            "Real Estate": 15,
            "Bonds": 5
        }
    elif age_num <= 50:
        base_alloc = {
            "Stocks": 35,
            "Mutual Funds": 30,
            "Gold": 10,
            "Real Estate": 20,
            "Bonds": 5
        }
    else:
        base_alloc = {
            "Stocks": 20,
            "Mutual Funds": 25,
            "Gold": 15,
            "Real Estate": 20,
            "Bonds": 20
        }

    # Adjust based on goal
    goal = goal.lower()
    if "wealth" in goal or "growth" in goal:
        base_alloc["Stocks"] += 10
        base_alloc["Bonds"] -= 5
        base_alloc["Mutual Funds"] += 5
    elif "stable" in goal or "income" in goal:
        base_alloc["Bonds"] += 10
        base_alloc["Stocks"] -= 10
    elif "retirement" in goal:
        base_alloc["Bonds"] += 15
        base_alloc["Stocks"] -= 15
    elif "tax" in goal:
        base_alloc["Mutual Funds"] += 10
        base_alloc["Stocks"] -= 5

    # Normalize to sum 100 (just in case)
    total = sum(base_alloc.values())
    normalized_alloc = {k: round(v * 100 / total) for k, v in base_alloc.items()}

    return normalized_alloc
