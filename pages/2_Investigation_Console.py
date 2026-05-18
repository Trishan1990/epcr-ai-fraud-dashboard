import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Investigation Console",
    page_icon="🕵️",
    layout="wide"
)

st.title("AI Fraud Investigation Console")
st.caption("Prioritize suspicious claims for investigator review")

claims = pd.DataFrame({
    "Claim ID": ["CLM-20481", "CLM-19321", "CLM-55122", "CLM-88412"],
    "Policy ID": ["POL-88321", "POL-99211", "POL-77411", "POL-11342"],
    "Fraud Score": [0.91, 0.76, 0.52, 0.22],
    "Risk Level": ["High", "High", "Medium", "Low"],
    "Status": [
        "Escalated",
        "Under Review",
        "Manual Validation",
        "Approved"
    ]
})

st.dataframe(
    claims,
    use_container_width=True
)

st.subheader("High-Risk Claims")

high_risk = claims[claims["Risk Level"] == "High"]

for _, row in high_risk.iterrows():

    st.error(
        f"{row['Claim ID']} | Fraud Score: {row['Fraud Score']}"
    )
