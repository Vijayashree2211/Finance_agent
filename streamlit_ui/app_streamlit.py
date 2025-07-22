import streamlit as st
import requests
import plotly.express as px

st.title("📈 Smart Financial Advisor")

# Age input
age_input = st.text_input("Enter your age (e.g. 28 or 26-35)", value="26-35", key="age_input")
goal = st.selectbox("What is your financial goal?", ["Wealth Growth", "Stable Income", "Retirement", "Tax Saving"], key="goal_input")

st.write("### Enter your expenses (monthly or daily)")

expenses = {}
num_expenses = st.number_input("How many expense categories?", min_value=1, max_value=20, value=3, step=1)

for i in range(num_expenses):
    category = st.text_input(f"Category {i+1}:", key=f"category_{i}")
    amount = st.number_input(f"Amount spent on {category}:", min_value=0.0, step=100.0, key=f"amount_{i}")
    if category and amount > 0:
        expenses[category.lower()] = amount

if st.button("Get Portfolio Advice"):
    with st.spinner("Generating recommendation..."):
        payload = {
            "age": age_input,
            "goal": goal,
            "expenses": expenses
        }

        try:
            res = requests.post("http://localhost:8000/recommend/portfolio", json=payload)
            res.raise_for_status()
            data = res.json()

            st.subheader("📊 Recommended Asset Allocation")
            fig = px.pie(
                values=list(data["asset_allocation"].values()),
                names=list(data["asset_allocation"].keys()),
                hole=0.3
            )
            st.plotly_chart(fig)

            st.subheader("💡 Stock Suggestions")
            for stock in data.get("stock_suggestions", []):
                st.markdown(f"- {stock}")

            st.subheader("💼 Mutual Fund Suggestions")
            html_list = "<ol>"
            for mf in data.get("mutual_fund_suggestions", []):
             html_list += f"<li>{mf}</li>"
            html_list += "</ol>"
            st.markdown(html_list, unsafe_allow_html=True)
            
            if data.get("travel_suggestions"):
                st.subheader("🌍 Suggested Travel Spots")
                for idx, place in enumerate(data["travel_suggestions"], 1):
                    st.markdown(f" **{idx}. {place}**")

            if data.get("savings_tips"):
                st.subheader("💡 Savings Tips")
                for tip in data["savings_tips"]:
                    st.markdown(f"- {tip}")

        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")
