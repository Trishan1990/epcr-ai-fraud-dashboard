import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="EPCR AI — Investigation Console", page_icon="🔎", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .kpi-box { background:#ffffff; border:1px solid #e8ecf0; border-radius:10px; padding:1.2rem 1.4rem; }
  .kpi-label { font-size:13px; color:#6b7280; font-weight:500; margin-bottom:4px; }
  .kpi-value { font-size:28px; font-weight:700; color:#111827; line-height:1.1; }
  .kpi-sub   { font-size:12px; color:#6b7280; margin-top:4px; }
  .kpi-high  { font-size:28px; font-weight:700; color:#dc2626; line-height:1.1; }
  .kpi-med   { font-size:28px; font-weight:700; color:#d97706; line-height:1.1; }
  .kpi-low   { font-size:28px; font-weight:700; color:#059669; line-height:1.1; }
  .section-header {
    font-size:15px; font-weight:600; color:#111827;
    margin:1.5rem 0 0.75rem 0; border-bottom:1px solid #f3f4f6; padding-bottom:6px;
  }
  .insight-card {
    background:#f0fdf4; border:1px solid #bbf7d0; border-left:4px solid #059669;
    border-radius:8px; padding:1rem 1.2rem; margin-bottom:0.75rem;
    font-size:13px; color:#111827; line-height:1.6;
  }
  .warning-card {
    background:#fffbeb; border:1px solid #fde68a; border-left:4px solid #d97706;
    border-radius:8px; padding:1rem 1.2rem; margin-bottom:0.75rem;
    font-size:13px; color:#111827; line-height:1.6;
  }
  .danger-card {
    background:#fef2f2; border:1px solid #fecaca; border-left:4px solid #dc2626;
    border-radius:8px; padding:1rem 1.2rem; margin-bottom:0.75rem;
    font-size:13px; color:#111827; line-height:1.6;
  }
  .thesis-card {
    background:#eff6ff; border:1px solid #bfdbfe; border-left:4px solid #2563eb;
    border-radius:8px; padding:1rem 1.2rem; margin-bottom:1.25rem;
    font-size:13px; color:#1e40af; line-height:1.6; font-style:italic;
  }
  .log-progress { background:#f9fafb; border:1px solid #e5e7eb; border-radius:10px; padding:1rem 1.4rem; margin-bottom:1.5rem; }
  .log-step { display:inline-block; font-size:12px; font-weight:600; padding:4px 12px; border-radius:20px; margin-right:6px; }
  .queue-row {
    display:flex; align-items:center; gap:12px;
    background:#ffffff; border:1px solid #e8ecf0; border-radius:8px;
    padding:12px 16px; margin-bottom:8px;
  }
  .badge {
    font-size:11px; font-weight:600; padding:3px 8px;
    border-radius:4px; white-space:nowrap;
  }
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
claims = pd.DataFrame({
    "claim_id":          ["CLM-1001","CLM-1002","CLM-1003","CLM-1004","CLM-1005",
                          "CLM-1006","CLM-1007","CLM-1008","CLM-1009","CLM-1010"],
    "policy_id":         ["POL-8912","POL-7741","POL-6654","POL-2399","POL-4811",
                          "POL-9123","POL-3345","POL-7022","POL-1855","POL-6488"],
    "claim_type":        ["Auto Damage"] * 10,
    "fraud_score":       [0.82, 0.31, 0.56, 0.76, 0.22, 0.68, 0.91, 0.44, 0.18, 0.73],
    "fraud_driver":      [
        "Metadata anomaly + texture artifacts",
        "No major anomaly",
        "Lighting inconsistency",
        "Duplicate image similarity",
        "No major anomaly",
        "Blur and edge inconsistency",
        "AI-generated damage pattern",
        "Missing EXIF metadata",
        "No major anomaly",
        "Repeated visual pattern"
    ],
    "estimated_savings": [4200, 0, 1200, 3800, 0, 2100, 5100, 900, 0, 3600],
})

def risk_info(score):
    if score >= 0.70: return "High",   "#dc2626", "#fef2f2", "Escalate to SIU"
    if score >= 0.40: return "Medium", "#d97706", "#fffbeb", "Manual Review"
    return               "Low",    "#059669", "#f0fdf4", "Auto-Process"

claims["risk_level"]   = claims["fraud_score"].apply(lambda s: risk_info(s)[0])
claims["action"]       = claims["fraud_score"].apply(lambda s: risk_info(s)[3])

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 🔎 EPCR AI — Investigation Console")
st.markdown("*Investigator triage queue · Prioritized by fraud risk · Log 3 capability*")

st.markdown("""
<div class='log-progress'>
  <div style='font-size:12px;font-weight:600;color:#6b7280;margin-bottom:8px;'>PLATFORM BUILD PROGRESS</div>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 1: Setup</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 2: Image Scoring</span>
  <span class='log-step' style='background:#dcfce7;color:#166534;'>● Log 3: Workflow</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 4: Graph Network</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 5: Digital Twin</span>
  <span class='log-step' style='background:#f3f4f6;color:#9ca3af;'>○ Log 6: Validation</span>
  <span class='log-step' style='background:#f3f4f6;color:#9ca3af;'>○ Log 7: Forecasting</span>
  <span class='log-step' style='background:#f3f4f6;color:#9ca3af;'>○ Log 8: Expert Review</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='thesis-card'>
  <strong>Log 3 Assumption:</strong> A prioritized investigator queue — ranked by fraud risk with
  explainable drivers — reduces time-to-investigation and ensures SIU teams focus on the highest
  value cases first. Our Log 6 survey found the investigator priority queue was the
  joint #1 most wanted feature (50% of respondents).
</div>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>📊 Queue Summary</div>", unsafe_allow_html=True)

high_risk   = claims[claims["risk_level"] == "High"]
med_risk    = claims[claims["risk_level"] == "Medium"]
low_risk    = claims[claims["risk_level"] == "Low"]
total_savings = claims["estimated_savings"].sum()

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Total Claims in Queue</div>
      <div class='kpi-value'>{len(claims)}</div>
      <div class='kpi-sub'>Awaiting investigator action</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>High Risk</div>
      <div class='kpi-high'>{len(high_risk)}</div>
      <div class='kpi-sub'>Escalate to SIU immediately</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Medium Risk</div>
      <div class='kpi-med'>{len(med_risk)}</div>
      <div class='kpi-sub'>Manual review required</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Low Risk</div>
      <div class='kpi-low'>{len(low_risk)}</div>
      <div class='kpi-sub'>Auto-process eligible</div>
    </div>""", unsafe_allow_html=True)
with k5:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Est. Fraud Savings</div>
      <div class='kpi-value'>${total_savings:,.0f}</div>
      <div class='kpi-sub'>If all High/Med flagged claims caught</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Filters ───────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🎛️ Filter Queue</div>", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)
with f1:
    risk_filter = st.multiselect("Risk Level", ["High", "Medium", "Low"],
                                  default=["High", "Medium", "Low"])
with f2:
    sort_by = st.selectbox("Sort By", ["Fraud Score (High → Low)",
                                        "Estimated Savings (High → Low)",
                                        "Claim ID"])
with f3:
    min_score = st.slider("Minimum Fraud Score", 0.0, 1.0, 0.0, 0.05)

filtered = claims[
    (claims["risk_level"].isin(risk_filter)) &
    (claims["fraud_score"] >= min_score)
].copy()

if sort_by == "Fraud Score (High → Low)":
    filtered = filtered.sort_values("fraud_score", ascending=False)
elif sort_by == "Estimated Savings (High → Low)":
    filtered = filtered.sort_values("estimated_savings", ascending=False)
else:
    filtered = filtered.sort_values("claim_id")

# ── Queue Table ───────────────────────────────────────────────────────────────
st.markdown(f"<div class='section-header'>📋 Triage Queue — {len(filtered)} claims</div>",
            unsafe_allow_html=True)

for _, row in filtered.iterrows():
    level, color, bg, action = risk_info(row["fraud_score"])
    bar_pct = int(row["fraud_score"] * 100)

    savings_str = f"${row['estimated_savings']:,}" if row["estimated_savings"] > 0 else "—"

    st.markdown(f"""
    <div style='background:#ffffff;border:1px solid #e8ecf0;border-radius:10px;
                padding:14px 18px;margin-bottom:8px;'>
      <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;'>
        <div style='display:flex;align-items:center;gap:12px;'>
          <span style='font-size:14px;font-weight:700;color:#111827;'>{row["claim_id"]}</span>
          <span style='font-size:12px;color:#6b7280;'>{row["policy_id"]}</span>
          <span style='font-size:11px;color:#6b7280;background:#f3f4f6;
                       padding:2px 8px;border-radius:4px;'>{row["claim_type"]}</span>
          <span class='badge' style='background:{bg};color:{color};'>{level} Risk</span>
        </div>
        <div style='display:flex;align-items:center;gap:16px;'>
          <span style='font-size:13px;font-weight:700;color:{color};'>{row["fraud_score"]:.2f}</span>
          <span style='font-size:12px;color:#059669;font-weight:500;'>{savings_str}</span>
          <span style='font-size:12px;font-weight:600;color:#2563eb;'>{action}</span>
        </div>
      </div>
      <div style='display:flex;align-items:center;gap:10px;'>
        <div style='flex:1;height:6px;background:#f3f4f6;border-radius:3px;overflow:hidden;'>
          <div style='width:{bar_pct}%;height:6px;background:{color};border-radius:3px;'></div>
        </div>
        <span style='font-size:11px;color:#6b7280;min-width:260px;'>{row["fraud_driver"]}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Risk Distribution Chart ───────────────────────────────────────────────────
st.markdown("<div class='section-header'>📊 Queue Risk Distribution</div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    fig1 = go.Figure(go.Bar(
        x=filtered["claim_id"],
        y=filtered["fraud_score"],
        marker_color=[risk_info(s)[1] for s in filtered["fraud_score"]],
        text=[f"{s:.2f}" for s in filtered["fraud_score"]],
        textposition="outside"
    ))
    fig1.update_layout(
        title="Fraud Score by Claim",
        yaxis=dict(range=[0, 1.15], gridcolor="#f3f4f6", title="Fraud Score"),
        xaxis=dict(title="Claim ID"),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=40, b=20, l=20, r=20), height=300
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    risk_counts = filtered["risk_level"].value_counts()
    fig2 = go.Figure(go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        hole=0.5,
        marker_colors=["#dc2626", "#d97706", "#059669"]
    ))
    fig2.update_layout(
        title="Claims by Risk Level",
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=40, b=20, l=20, r=20), height=300
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Investigator note ─────────────────────────────────────────────────────────
st.markdown("""
<div class='insight-card'>
  <strong>How to use this queue:</strong> Claims are ranked by fraud score. Start with High Risk —
  these should be escalated to SIU before end of day. Medium Risk claims require adjuster review
  before payment approval. Low Risk claims are eligible for straight-through processing.
  All actions are logged for compliance.
</div>
<div class='thesis-card' style='margin-top:0.5rem;'>
  <strong>Responsible AI:</strong> This queue is a <em>prioritization tool</em> — not an automated
  decision system. Every flag requires human investigator sign-off before any claim action is taken.
  Investigators can override any AI recommendation at any time.
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("EPCR AI · Investigation Console · Log 3 · UConn AI Venture Velocity Challenge 2026 · Created by Trishan1990")
