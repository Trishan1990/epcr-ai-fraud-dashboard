import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="EPCR AI — Claims Fraud Command Center",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .kpi-box { background:#ffffff; border:1px solid #e8ecf0; border-radius:10px; padding:1.2rem 1.4rem; }
  .kpi-label { font-size:13px; color:#6b7280; font-weight:500; margin-bottom:4px; }
  .kpi-value { font-size:28px; font-weight:700; color:#111827; line-height:1.1; }
  .kpi-green { font-size:28px; font-weight:700; color:#059669; line-height:1.1; }
  .kpi-red   { font-size:28px; font-weight:700; color:#dc2626; line-height:1.1; }
  .kpi-blue  { font-size:28px; font-weight:700; color:#2563eb; line-height:1.1; }
  .kpi-sub   { font-size:12px; color:#6b7280; margin-top:4px; }

  .section-header {
    font-size:15px; font-weight:600; color:#111827;
    margin:1.5rem 0 0.75rem 0; border-bottom:1px solid #f3f4f6; padding-bottom:6px;
  }
  .insight-card {
    background:#f0fdf4; border:1px solid #bbf7d0; border-left:4px solid #059669;
    border-radius:8px; padding:1rem 1.2rem; margin-bottom:0.75rem;
    font-size:13px; color:#111827; line-height:1.6;
  }
  .thesis-card {
    background:#eff6ff; border:1px solid #bfdbfe; border-left:4px solid #2563eb;
    border-radius:8px; padding:1rem 1.2rem; margin-bottom:1.25rem;
    font-size:13px; color:#1e40af; line-height:1.6;
  }
  .warning-card {
    background:#fffbeb; border:1px solid #fde68a; border-left:4px solid #d97706;
    border-radius:8px; padding:1rem 1.2rem; margin-bottom:0.75rem;
    font-size:13px; color:#111827; line-height:1.6;
  }
  .hero-badge {
    display:inline-block; font-size:12px; font-weight:600;
    padding:4px 12px; border-radius:20px; margin-right:8px; margin-bottom:8px;
  }
  .log-progress { background:#f9fafb; border:1px solid #e5e7eb; border-radius:10px; padding:1rem 1.4rem; margin-bottom:1.5rem; }
  .log-step { display:inline-block; font-size:12px; font-weight:600; padding:4px 12px; border-radius:20px; margin-right:6px; margin-bottom:4px; }
  .nav-card {
    background:#ffffff; border:1px solid #e8ecf0; border-radius:10px;
    padding:1rem 1.2rem; height:100%; cursor:pointer;
    transition: border-color 0.2s;
  }
  .nav-card:hover { border-color:#2563eb; }
  .nav-title { font-size:14px; font-weight:600; color:#111827; margin-bottom:4px; }
  .nav-desc  { font-size:12px; color:#6b7280; line-height:1.5; }
  .nav-log   { font-size:11px; font-weight:600; color:#2563eb; margin-top:6px; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_claims():
    try:
        return pd.read_csv("data/sample_claims.csv")
    except Exception:
        import numpy as np
        np.random.seed(42)
        n = 10
        scores = np.random.uniform(0.1, 0.95, n).round(2)
        return pd.DataFrame({
            "claim_id":          [f"CLM-100{i}" for i in range(n)],
            "fraud_score":       scores,
            "risk_level":        ["High" if s >= 0.7 else ("Medium" if s >= 0.4 else "Low") for s in scores],
            "estimated_savings": [int(s * 6000) if s >= 0.4 else 0 for s in scores],
            "claim_type":        ["Auto Damage"] * n,
            "recommended_action":["Escalate to SIU" if s >= 0.7 else ("Manual Review" if s >= 0.4 else "Auto-Process") for s in scores]
        })

claims = load_claims()

# ── Hero header ───────────────────────────────────────────────────────────────
col_title, col_badge = st.columns([3, 1])

with col_title:
    st.markdown("## 🚗 EPCR AI — Claims Fraud Command Center")
    st.markdown("*AI-powered fraud intelligence platform for insurance investigators*")

    st.markdown("""
    <div style='margin-top:8px;'>
      <span class='hero-badge' style='background:#dcfce7;color:#166534;'>🏆 InsurTech NY Winner — $2,500 Grand Prize</span>
      <span class='hero-badge' style='background:#dbeafe;color:#1e40af;'>590,540 Real Transactions Validated</span>
      <span class='hero-badge' style='background:#faeeda;color:#633806;'>87.6% Precision</span>
      <span class='hero-badge' style='background:#f3f4f6;color:#374151;'>University of Connecticut</span>
      <span class='hero-badge' style='background:#fce7f3;color:#9d174d;'>📰 UConn Today Press Coverage</span>
    </div>
    """, unsafe_allow_html=True)

with col_badge:
    st.markdown("""
    <div style='background:#eff6ff;border:1px solid #bfdbfe;border-radius:10px;
                padding:1rem;text-align:center;margin-top:8px;'>
      <div style='font-size:11px;font-weight:600;color:#6b7280;margin-bottom:4px;'>VENTURE STATUS</div>
      <div style='font-size:16px;font-weight:700;color:#2563eb;'>🚀 In Development</div>
      <div style='font-size:11px;color:#6b7280;margin-top:4px;'>Log 7 of 8 complete</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Mission statement ─────────────────────────────────────────────────────────
st.markdown("""
<div class='thesis-card'>
  <strong>EPCR AI</strong> is an insurance fraud intelligence platform that catches organized fraud rings
  that claim-level scoring alone misses. By building a graph of shared repair shops, phone numbers,
  image hashes, and claimant identities across claims, EPCR AI surfaces hidden fraud networks —
  validated at <strong>87.6% precision on 590,540 real IEEE-CIS transactions</strong> with a
  <strong>+25.6% recall improvement</strong> over standalone fraud scoring.
  Built for SIU investigators. Designed to plug in alongside Verisk and ISO ClaimSearch, not replace them.
  Recognized by <strong>Renee Hamlen, CMO of Principal Financial Group</strong> and covered by
  <strong>UConn Today</strong> (April 2, 2026).
</div>
""", unsafe_allow_html=True)

# ── Platform progress ─────────────────────────────────────────────────────────
st.markdown("""
<div class='log-progress'>
  <div style='font-size:12px;font-weight:600;color:#6b7280;margin-bottom:8px;'>PLATFORM BUILD PROGRESS — 7 of 8 LOGS COMPLETE</div>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 1: Setup</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 2: Image Scoring</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 3: Workflow</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 4: Graph Network</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 5: Digital Twin</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 6: Validation</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 7: Forecasting</span>
  <span class='log-step' style='background:#dcfce7;color:#166534;'>● Log 8: Expert Review</span>
</div>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>📊 Live Platform Metrics</div>", unsafe_allow_html=True)

high_risk      = len(claims[claims["risk_level"] == "High"])
avg_score      = round(claims["fraud_score"].mean(), 2)
total_savings  = claims["estimated_savings"].sum()
total_claims   = len(claims)

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Claims Processed</div>
      <div class='kpi-value'>{total_claims}</div>
      <div class='kpi-sub'>In demo dataset</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>High-Risk Claims</div>
      <div class='kpi-red'>{high_risk}</div>
      <div class='kpi-sub'>Flagged for SIU review</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Avg Fraud Score</div>
      <div class='kpi-value'>{avg_score}</div>
      <div class='kpi-sub'>0 = clean · 1 = high risk</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Est. Fraud Savings</div>
      <div class='kpi-green'>${total_savings:,}</div>
      <div class='kpi-sub'>From flagged claims</div>
    </div>""", unsafe_allow_html=True)
with k5:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Real Data Precision</div>
      <div class='kpi-blue'>87.6%</div>
      <div class='kpi-sub'>590,540 IEEE-CIS transactions</div>
    </div>""", unsafe_allow_html=True)
with k6:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Recall Improvement</div>
      <div class='kpi-blue'>+25.6%</div>
      <div class='kpi-sub'>vs standalone fraud score</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown("<div class='section-header'>Fraud Risk Distribution</div>",
                unsafe_allow_html=True)
    fig1 = go.Figure(go.Histogram(
        x=claims["fraud_score"], nbinsx=10,
        marker_color="#2563eb", opacity=0.85
    ))
    fig1.update_layout(
        xaxis=dict(title="Fraud Score", gridcolor="#f3f4f6"),
        yaxis=dict(title="Count",       gridcolor="#f3f4f6"),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=10, b=20, l=20, r=20), height=280
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown("<div class='section-header'>Claims by Risk Level</div>",
                unsafe_allow_html=True)
    risk_counts = claims["risk_level"].value_counts()
    fig2 = go.Figure(go.Pie(
        labels=risk_counts.index, values=risk_counts.values, hole=0.5,
        marker_colors=["#dc2626","#d97706","#059669"]
    ))
    fig2.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=10, b=10, l=20, r=20), height=280
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Triage queue ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>📋 Recent Claim Triage Queue</div>",
            unsafe_allow_html=True)

claims_display = claims.sort_values("fraud_score", ascending=False).copy()

for _, row in claims_display.iterrows():
    score   = row["fraud_score"]
    level   = row["risk_level"]
    color   = "#dc2626" if level == "High" else ("#d97706" if level == "Medium" else "#059669")
    bg      = "#fef2f2" if level == "High" else ("#fffbeb" if level == "Medium" else "#f0fdf4")
    action  = row.get("recommended_action", "—")
    savings = row.get("estimated_savings", 0)
    savings_str = f"${savings:,}" if savings > 0 else "—"

    st.markdown(f"""
    <div style='background:#ffffff;border:1px solid #e8ecf0;border-radius:8px;
                padding:12px 16px;margin-bottom:6px;display:flex;
                align-items:center;justify-content:space-between;'>
      <div style='display:flex;align-items:center;gap:12px;'>
        <span style='font-size:14px;font-weight:700;color:#111827;'>{row["claim_id"]}</span>
        <span style='font-size:11px;font-weight:600;padding:2px 8px;border-radius:4px;
                     background:{bg};color:{color};'>{level} Risk</span>
        <span style='font-size:12px;color:#6b7280;'>{row.get("claim_type","Auto Damage")}</span>
      </div>
      <div style='display:flex;align-items:center;gap:20px;'>
        <div style='width:120px;'>
          <div style='display:flex;justify-content:space-between;margin-bottom:3px;'>
            <span style='font-size:11px;color:#6b7280;'>Fraud Score</span>
            <span style='font-size:11px;font-weight:700;color:{color};'>{score:.2f}</span>
          </div>
          <div style='height:5px;background:#f3f4f6;border-radius:3px;overflow:hidden;'>
            <div style='width:{int(score*100)}%;height:5px;background:{color};border-radius:3px;'></div>
          </div>
        </div>
        <span style='font-size:12px;color:#059669;font-weight:500;min-width:60px;'>{savings_str}</span>
        <span style='font-size:12px;color:#2563eb;font-weight:600;min-width:160px;'>{action}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Platform navigation ───────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🗺️ Platform Navigation</div>", unsafe_allow_html=True)
st.markdown("<p style='font-size:13px;color:#6b7280;margin-bottom:12px;'>Explore each capability in the sidebar or click below to understand what each page proves.</p>", unsafe_allow_html=True)

n1, n2, n3 = st.columns(3)
with n1:
    st.markdown("""<div class='nav-card'>
      <div class='nav-title'>🖼️ Image Validation</div>
      <div class='nav-desc'>Upload a claim photo. AI detects texture artifacts, blur manipulation, lighting inconsistencies and missing metadata.</div>
      <div class='nav-log'>Log 2 · Assumption: AI detects visual fraud signals faster than manual review</div>
    </div>""", unsafe_allow_html=True)
with n2:
    st.markdown("""<div class='nav-card'>
      <div class='nav-title'>🔎 Investigation Console</div>
      <div class='nav-desc'>Prioritized SIU queue ranked by fraud score. Filters, risk breakdown, and recommended actions per claim.</div>
      <div class='nav-log'>Log 3 · Assumption: AI prioritization surfaces highest-value cases first</div>
    </div>""", unsafe_allow_html=True)
with n3:
    st.markdown("""<div class='nav-card'>
      <div class='nav-title'>🧠 Explainable AI</div>
      <div class='nav-desc'>Every fraud flag explained. Feature importance, per-claim signal breakdown, and SHAP explainability.</div>
      <div class='nav-log'>Log 3 · Validates: 50% of investigators require explainability before trusting AI</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
n4, n5, n6 = st.columns(3)
with n4:
    st.markdown("""<div class='nav-card'>
      <div class='nav-title'>🔬 Fraud Intelligence Lab</div>
      <div class='nav-desc'>Graph-based fraud ring detection. Entity relationship network, centrality analysis, and counterfactual simulation.</div>
      <div class='nav-log'>Log 4 · Core differentiator vs Verisk and ISO ClaimSearch</div>
    </div>""", unsafe_allow_html=True)
with n5:
    st.markdown("""<div class='nav-card'>
      <div class='nav-title'>📊 Digital Twin</div>
      <div class='nav-desc'>Real validation on 590,540 IEEE-CIS transactions. 87.6% precision, +25.6% recall vs standalone scoring.</div>
      <div class='nav-log'>Log 5 · First real-data benchmark — synthetic data objection eliminated</div>
    </div>""", unsafe_allow_html=True)
with n6:
    st.markdown("""<div class='nav-card'>
      <div class='nav-title'>💰 Enterprise ROI</div>
      <div class='nav-desc'>Calculate fraud savings for any insurer profile. Pricing tiers, competitive comparison, and pilot program details.</div>
      <div class='nav-log'>Business case · $308B market · $1.50/claim API pricing</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
n7, n8, n9 = st.columns(3)
with n7:
    st.markdown("""<div class='nav-card'>
      <div class='nav-title'>🧬 SHAP Explainability</div>
      <div class='nav-desc'>Every fraud flag explained with SHAP attribution. Feature importance, threshold slider, and per-claim waterfall charts.</div>
      <div class='nav-log'>Log 7 · Validated: 50% of investigators require explainability before adoption</div>
    </div>""", unsafe_allow_html=True)
with n8:
    st.markdown("""<div class='nav-card'>
      <div class='nav-title'>📡 Forecasting Engine</div>
      <div class='nav-desc'>Network risk scores predict which claims will escalate. Near-miss panel surfaces hidden fraud ring connections before losses occur.</div>
      <div class='nav-log'>Log 7 · Graph topology predicts future fraud escalation</div>
    </div>""", unsafe_allow_html=True)
with n9:
    st.markdown("""<div class='nav-card'>
      <div class='nav-title'>🔐 Expert Review</div>
      <div class='nav-desc'>Named industry reviewers, responsible AI assessment, NAIC compliance documentation, and 90-day pilot structure.</div>
      <div class='nav-log'>Log 8 · Coming June 20 — final deployment readiness review</div>
    </div>""", unsafe_allow_html=True)

# ── Competitive + responsible AI ──────────────────────────────────────────────
st.markdown("<div class='section-header'>🏆 Why EPCR AI</div>", unsafe_allow_html=True)

r1, r2 = st.columns(2)
with r1:
    st.markdown("""
    <div class='warning-card'>
      <strong>The gap existing tools leave:</strong> Verisk and ISO ClaimSearch score individual
      claims. They cannot detect organized fraud rings. EPCR AI's graph model caught
      <strong>8.5× more fraud cases</strong> on the same dataset by tracing connections
      between claims — not just scoring them in isolation.
    </div>
    """, unsafe_allow_html=True)
with r2:
    st.markdown("""
    <div class='insight-card'>
      <strong>Responsible AI by design:</strong> EPCR AI never automatically denies a claim.
      Every flag is a recommendation for human review. All High and Medium risk cases require
      investigator sign-off. SHAP explainability shows the reasoning behind every decision.
      Validated by insurance professionals including a VP of Data & Governance and
      Metro Hartford claims adjuster in Log 6.
    </div>
    """, unsafe_allow_html=True)

# ── External validation ───────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🌟 External Validation</div>", unsafe_allow_html=True)

v1, v2, v3 = st.columns(3)
with v1:
    st.markdown("""
    <div class='insight-card'>
      <strong>🏆 InsurTech NY — $2,500 Grand Prize</strong><br>
      Won the InsurTech NY student case competition sponsored by Principal Financial Group.
      Covered by UConn Today (April 2, 2026).<br><br>
      <a href='https://today.uconn.edu/2026/04/uconn-grad-students-win-insurtech-ny-challenge-by-offering-practical-solutions-to-insurance-provider-woes/' target='_blank' style='color:#059669;font-weight:600;'>Read the article →</a>
    </div>
    """, unsafe_allow_html=True)
with v2:
    st.markdown("""
    <div class='insight-card'>
      <strong>🔬 Kaggle — Verified Real Data</strong><br>
      Graph propagation model validated on 590,540 real IEEE-CIS transactions.
      Public notebook under trishanguddu — independently verifiable by anyone.<br><br>
      <a href='https://www.kaggle.com/code/trishanguddu/epcr-ai-log-5-fraud-digital-twin' target='_blank' style='color:#059669;font-weight:600;'>View notebook →</a>
    </div>
    """, unsafe_allow_html=True)
with v3:
    st.markdown("""
    <div class='insight-card'>
      <strong>📋 Investigator Survey — 6 Responses</strong><br>
      100% of respondents prefer graph intelligence over standalone scoring.
      Includes VP Data & Governance and Metro Hartford Claims Adjuster.<br><br>
      <a href='https://docs.google.com/forms/d/e/1FAIpQLSda7mb0JO_GahZfwBSCJ5qNe4GmBQmRqKFPrJp84vCqRkG28Q/viewform' target='_blank' style='color:#059669;font-weight:600;'>Take the survey →</a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("EPCR AI · Claims Fraud Command Center · InsurTech NY Winner · UConn AI Venture Velocity Challenge 2026 · Created by Trishan1990")
