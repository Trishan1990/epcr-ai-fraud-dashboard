
import streamlit as st

st.set_page_config(page_title="Enterprise ROI", page_icon="💰", layout="wide")

st.title("Enterprise ROI Dashboard")
st.caption("Business value of AI-powered claims fraud detection")

claims_per_year = st.number_input("Annual claims volume", value=100000)
avg_claim_value = st.number_input("Average claim payout ($)", value=3500)
fraud_rate = st.slider("Estimated fraud rate (%)", 1, 20, 8)
detection_lift = st.slider("AI detection improvement (%)", 5, 60, 25)
manual_review_reduction = st.slider("Manual review reduction (%)", 5, 60, 35)

fraud_loss = claims_per_year * avg_claim_value * (fraud_rate / 100)
savings = fraud_loss * (detection_lift / 100)
operational_savings = claims_per_year * 18 * (manual_review_reduction / 100)
total_value = savings + operational_savings

c1, c2, c3 = st.columns(3)
c1.metric("Estimated Annual Fraud Exposure", f"${fraud_loss:,.0f}")
c2.metric("Fraud Savings from AI", f"${savings:,.0f}")
c3.metric("Total Annual Value", f"${total_value:,.0f}")

st.subheader("Suggested SaaS Pricing")
st.write("""
- Starter: $5,000/month for small carriers
- Growth: $15,000/month for regional carriers
- Enterprise: Custom pricing + API volume charges
""")
