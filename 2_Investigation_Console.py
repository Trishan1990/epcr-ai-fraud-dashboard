
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Investigation Console", page_icon="🕵️", layout="wide")

st.title("AI Fraud Investigation Console")
st.caption("Prioritize claims for investigator review")

claims = pd.read_csv("data/sample_claims.csv")

risk_filter = st.multiselect(
    "Filter by risk level",
    options=sorted(claims["risk_level"].unique()),
    default=sorted(claims["risk_level"].unique())
)

filtered = claims[claims["risk_level"].isin(risk_filter)]

st.dataframe(
    filtered[["claim_id", "policy_id", "claim_type", "fraud_score", "risk_level", "fraud_driver", "recommended_action"]],
    use_container_width=True
)

st.subheader("Top 5 Highest-Risk Claims")
st.dataframe(
    claims.sort_values("fraud_score", ascending=False).head(5),
    use_container_width=True
)
