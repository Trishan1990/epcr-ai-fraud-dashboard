import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="EPCR AI Claims Fraud Command Center",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

h1 {
    color: #0f172a;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("🚗 EPCR AI — Claims Fraud Command Center")
st.caption("AI-powered claim image validation, fraud scoring, and investigator triage")

claims = pd.read_csv("data/sample_claims.csv")

# ---------- KPI SECTION ----------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Claims Processed", len(claims))

with c2:
    st.metric(
        "High-Risk Claims",
        len(claims[claims["risk_level"] == "High"])
    )

with c3:
    st.metric(
        "Avg Fraud Score",
        round(claims["fraud_score"].mean(), 2)
    )

with c4:
    st.metric(
        "Estimated Fraud Savings",
        "$" + format(claims["estimated_savings"].sum(), ",")
    )

st.divider()

# ---------- CHARTS ----------
left, right = st.columns(2)

with left:
    fig = px.histogram(
        claims,
        x="fraud_score",
        nbins=10,
        title="Fraud Risk Distribution"
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    risk_counts = claims["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["risk_level", "count"]

    fig = px.pie(
        risk_counts,
        values="count",
        names="risk_level",
        title="Claims by Risk Level",
        hole=0.45
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------- TRIAGE TABLE ----------
st.subheader("📋 Recent Claim Triage Queue")

styled = claims.style.background_gradient(
    subset=["fraud_score"],
    cmap="Reds"
)

st.dataframe(
    styled,
    use_container_width=True
)