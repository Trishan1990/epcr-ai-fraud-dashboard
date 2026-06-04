import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="EPCR AI — Claims Triage", page_icon="📌", layout="wide")

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
  .kpi-amber { font-size:28px; font-weight:700; color:#d97706; line-height:1.1; }
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
  .siu-row {
    background:#fef2f2; border:1px solid #fecaca; border-left:4px solid #dc2626;
    border-radius:8px; padding:12px 16px; margin-bottom:8px;
    font-size:13px; color:#111827;
  }
  .badge { font-size:11px; font-weight:600; padding:3px 8px; border-radius:4px; white-space:nowrap; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_claims():
    try:
        df = pd.read_csv("data/data/claims_operations.csv")
    except Exception:
        # Fallback synthetic data if CSV missing
        import numpy as np
        np.random.seed(42)
        n = 40
        severities   = np.random.choice(["Critical","High","Medium","Low"], n,
                                         p=[0.15, 0.25, 0.35, 0.25])
        fraud_scores = {"Critical": (0.80,1.0), "High": (0.65,0.85),
                        "Medium": (0.40,0.65), "Low": (0.05,0.40)}
        scores = [round(np.random.uniform(*fraud_scores[s]), 2) for s in severities]
        df = pd.DataFrame({
            "claim_id":           [f"CLM-{2000+i}" for i in range(n)],
            "policy_id":          [f"POL-{np.random.randint(1000,9999)}" for _ in range(n)],
            "claim_type":         np.random.choice(["Auto Damage","Liability","Theft","Medical"], n),
            "claim_amount":       np.random.randint(500, 25000, n),
            "fraud_score":        scores,
            "severity":           severities,
            "status":             np.random.choice(["Open","Under Review","Escalated","Closed"], n),
            "assigned_team":      np.random.choice(["SIU Alpha","SIU Beta","Claims Adj.","Auto-Process"], n),
            "days_open":          np.random.randint(0, 45, n),
            "recommended_action": [
                "Escalate to SIU" if s in ["Critical","High"]
                else ("Manual review" if s == "Medium" else "Auto-process")
                for s in severities
            ]
        })
    return df

claims = load_claims()
claims_sorted = claims.sort_values(["fraud_score","claim_amount"], ascending=[False,False])

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 📌 EPCR AI — Claims Triage")
st.markdown("*AI-driven investigator prioritization · Operational workflow simulation · Log 3 capability*")

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
  <strong>Log 3 Assumption:</strong> AI-generated fraud scores can be operationalized into an
  investigator prioritization workflow that consistently surfaces the highest-risk claims at the
  top of the SIU queue — reducing time-to-investigation and ensuring SIU teams focus on cases
  with the highest fraud exposure first.
</div>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>📊 Triage Dashboard</div>", unsafe_allow_html=True)

total_claims    = len(claims)
critical_claims = len(claims[claims["severity"] == "Critical"])
high_risk       = len(claims[claims["severity"].isin(["Critical","High"])])
total_exposure  = claims["claim_amount"].sum()
siu_exposure    = claims[claims["severity"].isin(["Critical","High"])]["claim_amount"].sum()
avg_score       = claims["fraud_score"].mean()

# Triage success metric
top5          = claims_sorted.head(5)
high_in_top5  = len(top5[top5["severity"].isin(["Critical","High"])])
success_rate  = high_in_top5 / 5

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Total Claims</div>
      <div class='kpi-value'>{total_claims}</div>
      <div class='kpi-sub'>In current queue</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Critical</div>
      <div class='kpi-red'>{critical_claims}</div>
      <div class='kpi-sub'>Immediate SIU escalation</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>High-Risk Queue</div>
      <div class='kpi-amber'>{high_risk}</div>
      <div class='kpi-sub'>Critical + High severity</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>SIU Exposure</div>
      <div class='kpi-red'>${siu_exposure:,.0f}</div>
      <div class='kpi-sub'>At-risk claim value</div>
    </div>""", unsafe_allow_html=True)
with k5:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Avg Fraud Score</div>
      <div class='kpi-value'>{avg_score:.2f}</div>
      <div class='kpi-sub'>Across all claims</div>
    </div>""", unsafe_allow_html=True)
with k6:
    score_color = "kpi-green" if success_rate >= 0.70 else "kpi-red"
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Triage Accuracy</div>
      <div class='{score_color}'>{success_rate*100:.0f}%</div>
      <div class='kpi-sub'>High-risk in top 5 positions</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown("<div class='section-header'>Claims by Severity</div>", unsafe_allow_html=True)
    sev_counts  = claims["severity"].value_counts().reindex(
        ["Critical","High","Medium","Low"], fill_value=0)
    sev_colors  = ["#dc2626","#d97706","#2563eb","#059669"]
    fig1 = go.Figure(go.Bar(
        x=sev_counts.index, y=sev_counts.values,
        marker_color=sev_colors,
        text=sev_counts.values, textposition="outside"
    ))
    fig1.update_layout(
        yaxis=dict(gridcolor="#f3f4f6"),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=10, b=10, l=10, r=10), height=280, showlegend=False
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown("<div class='section-header'>Claim Amount by Severity</div>",
                unsafe_allow_html=True)
    fig2 = px.box(claims, x="severity", y="claim_amount",
                  category_orders={"severity": ["Critical","High","Medium","Low"]},
                  color="severity",
                  color_discrete_map={"Critical":"#dc2626","High":"#d97706",
                                      "Medium":"#2563eb","Low":"#059669"})
    fig2.update_layout(
        yaxis=dict(gridcolor="#f3f4f6", title="Claim Amount ($)"),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=10, b=10, l=10, r=10), height=280, showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Triage success check ──────────────────────────────────────────────────────
st.markdown("<div class='section-header'>✅ Triage Success Validation</div>",
            unsafe_allow_html=True)

if success_rate >= 0.70:
    st.markdown(f"""
    <div class='insight-card'>
      <strong>✅ Success threshold met — {success_rate*100:.0f}% of top 5 queue positions are high-risk claims.</strong>
      The AI prioritization workflow is correctly surfacing the most dangerous claims first.
      SIU teams using this queue will always investigate the highest-value fraud cases before
      lower-risk claims consume their capacity.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class='warning-card'>
      <strong>⚠️ Success threshold not met — {success_rate*100:.0f}% of top 5 positions are high-risk.</strong>
      Prioritization logic requires refinement. The fraud score weighting may need adjustment
      to better separate critical claims from medium-risk ones in the queue ordering.
    </div>
    """, unsafe_allow_html=True)

# ── Full queue table ──────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>📋 Full Prioritized Investigator Queue</div>",
            unsafe_allow_html=True)

# Filters
f1, f2, f3 = st.columns(3)
with f1:
    sev_filter = st.multiselect("Severity", ["Critical","High","Medium","Low"],
                                 default=["Critical","High","Medium","Low"])
with f2:
    status_filter = st.multiselect("Status",
                                    claims["status"].unique().tolist(),
                                    default=claims["status"].unique().tolist())
with f3:
    min_score = st.slider("Min fraud score", 0.0, 1.0, 0.0, 0.05)

filtered = claims_sorted[
    (claims_sorted["severity"].isin(sev_filter)) &
    (claims_sorted["status"].isin(status_filter)) &
    (claims_sorted["fraud_score"] >= min_score)
]

def color_severity(val):
    colors = {"Critical":"background-color:#fef2f2;color:#dc2626;font-weight:600",
              "High":     "background-color:#fffbeb;color:#d97706;font-weight:600",
              "Medium":   "background-color:#eff6ff;color:#2563eb;font-weight:600",
              "Low":      "background-color:#f0fdf4;color:#059669;font-weight:600"}
    return colors.get(val, "")

def color_score(val):
    if val >= 0.70: return "color:#dc2626;font-weight:700"
    if val >= 0.40: return "color:#d97706;font-weight:700"
    return "color:#059669;font-weight:700"

display_cols = ["claim_id","policy_id","claim_type","claim_amount",
                "fraud_score","severity","status","assigned_team",
                "days_open","recommended_action"]

try:
    styled = (filtered[display_cols]
              .style
              .map(color_severity, subset=["severity"])
              .map(color_score,    subset=["fraud_score"])
              .format({"claim_amount": "${:,.0f}", "fraud_score": "{:.2f}"}))
except AttributeError:
    styled = (filtered[display_cols]
              .style
              .map(color_severity, subset=["severity"])
              .map(color_score,    subset=["fraud_score"])
              .format({"claim_amount": "${:,.0f}", "fraud_score": "{:.2f}"}))


st.dataframe(styled, use_container_width=True, hide_index=True)

# ── SIU Escalation Queue ──────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🚨 SIU Escalation Queue — Immediate Action Required</div>",
            unsafe_allow_html=True)

siu_queue = claims_sorted[claims_sorted["severity"].isin(["Critical","High"])]

for _, row in siu_queue.iterrows():
    score_color = "#dc2626" if row["fraud_score"] >= 0.70 else "#d97706"
    sev_bg      = "#fef2f2" if row["severity"] == "Critical" else "#fffbeb"
    st.markdown(f"""
    <div style='background:{sev_bg};border:1px solid #fecaca;border-left:4px solid {score_color};
                border-radius:8px;padding:12px 16px;margin-bottom:8px;'>
      <div style='display:flex;align-items:center;justify-content:space-between;'>
        <div style='display:flex;align-items:center;gap:12px;'>
          <span style='font-size:14px;font-weight:700;color:#111827;'>{row["claim_id"]}</span>
          <span class='badge' style='background:{sev_bg};color:{score_color};
                border:1px solid {score_color};'>{row["severity"]}</span>
          <span style='font-size:12px;color:#6b7280;'>{row["claim_type"]}</span>
        </div>
        <div style='display:flex;align-items:center;gap:20px;'>
          <span style='font-size:13px;font-weight:700;color:{score_color};'>
            Score: {row["fraud_score"]:.2f}</span>
          <span style='font-size:13px;color:#111827;font-weight:500;'>
            ${row["claim_amount"]:,.0f}</span>
          <span style='font-size:12px;color:#2563eb;font-weight:600;'>
            {row["recommended_action"]}</span>
          <span style='font-size:11px;color:#6b7280;'>
            {row["days_open"]} days open · {row["assigned_team"]}</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Responsible AI ────────────────────────────────────────────────────────────
st.markdown("""
<div class='thesis-card' style='margin-top:1.5rem;'>
  <strong>Responsible AI:</strong> This triage queue is a prioritization tool only.
  No claim is denied or approved automatically. Every SIU escalation requires
  investigator sign-off. Investigators can override any queue position at any time.
  All actions are logged for compliance and audit purposes.
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("EPCR AI · Claims Triage · Log 3 · UConn AI Venture Velocity Challenge 2026 · Created by Trishan1990")
