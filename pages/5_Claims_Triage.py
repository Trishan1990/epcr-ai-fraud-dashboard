import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Claims Triage",
    page_icon="📌",
    layout="wide"
)

st.title("AI Claims Triage & Investigator Prioritization")
st.caption("Operational workflow simulation for SIU escalation and claims review prioritization")

claims = pd.read_csv("data/data/claims_operations.csv")

# Sort high-risk claims first
claims_sorted = claims.sort_values(
    by=["fraud_score", "claim_amount"],
    ascending=[False, False]
)

total_claims = len(claims)
critical_claims = len(claims[claims["severity"] == "Critical"])
high_risk_claims = len(claims[claims["severity"].isin(["Critical", "High"])])
total_exposure = claims["claim_amount"].sum()
siu_exposure = claims[claims["severity"].isin(["Critical", "High"])]["claim_amount"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Claims", total_claims)
c2.metric("Critical Claims", critical_claims)
c3.metric("High-Risk Queue", high_risk_claims)
c4.metric("SIU Exposure", f"${siu_exposure:,.0f}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Claims by Severity")
    severity_counts = claims["severity"].value_counts().reset_index()
    severity_counts.columns = ["severity", "count"]

    fig = px.bar(
        severity_counts,
        x="severity",
        y="count",
        title="Severity Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Claim Amount by Severity")
    fig = px.box(
        claims,
        x="severity",
        y="claim_amount",
        title="Claim Amount Distribution by Severity"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Prioritized Investigator Queue")

st.dataframe(
    claims_sorted[
        [
            "claim_id",
            "policy_id",
            "claim_type",
            "claim_amount",
            "fraud_score",
            "severity",
            "status",
            "assigned_team",
            "days_open",
            "recommended_action"
        ]
    ],
    use_container_width=True
)

st.divider()

st.subheader("SIU Escalation Queue")

siu_queue = claims_sorted[claims_sorted["severity"].isin(["Critical", "High"])]

for _, row in siu_queue.iterrows():
    st.error(
        f"{row['claim_id']} | {row['severity']} | Fraud Score: {row['fraud_score']} | "
        f"Claim Amount: ${row['claim_amount']:,.0f} | Action: {row['recommended_action']}"
    )

st.divider()

st.subheader("Experiment Success Check")

top_5 = claims_sorted.head(5)
high_in_top_5 = len(top_5[top_5["severity"].isin(["Critical", "High"])])
success_rate = high_in_top_5 / 5

st.metric(
    "High-Risk Claims in Top 5 Queue Positions",
    f"{success_rate * 100:.0f}%"
)

if success_rate >= 0.70:
    st.success(
        "Success threshold met: more than 70% of top-priority queue positions are high-risk claims."
    )
else:
    st.warning(
        "Success threshold not met: prioritization logic requires refinement."
    )

st.info(
    "This simulation tests whether AI-generated fraud scores can be operationalized into an investigator prioritization workflow."
)
