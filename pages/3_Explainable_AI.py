import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="EPCR AI — Explainable AI", page_icon="🧠", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .kpi-box { background:#ffffff; border:1px solid #e8ecf0; border-radius:10px; padding:1.2rem 1.4rem; }
  .kpi-label { font-size:13px; color:#6b7280; font-weight:500; margin-bottom:4px; }
  .kpi-value { font-size:28px; font-weight:700; color:#111827; line-height:1.1; }
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
  .claim-card { background:#ffffff; border:1px solid #e8ecf0; border-radius:10px; padding:1.2rem 1.4rem; margin-bottom:1rem; }
  .driver-row { display:flex; align-items:center; gap:12px; margin-bottom:8px; }
  .driver-label { font-size:13px; color:#374151; width:200px; flex-shrink:0; }
  .driver-bar-wrap { flex:1; height:8px; background:#f3f4f6; border-radius:4px; overflow:hidden; }
  .driver-score { font-size:13px; font-weight:600; min-width:36px; text-align:right; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 🧠 EPCR AI — Explainable AI")
st.markdown("*Why the AI flagged each claim — every decision explained · Log 3 capability*")

st.markdown("""
<div class='log-progress'>
  <div style='font-size:12px;font-weight:600;color:#6b7280;margin-bottom:8px;'>PLATFORM BUILD PROGRESS</div>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 1: Setup</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 2: Image Scoring</span>
  <span class='log-step' style='background:#dcfce7;color:#166534;'>● Log 3: Explainability</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 4: Graph Network</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 5: Digital Twin</span>
  <span class='log-step' style='background:#f3f4f6;color:#9ca3af;'>○ Log 6: Validation</span>
  <span class='log-step' style='background:#f3f4f6;color:#9ca3af;'>○ Log 7: Forecasting</span>
  <span class='log-step' style='background:#f3f4f6;color:#9ca3af;'>○ Log 8: Expert Review</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='thesis-card'>
  <strong>Why explainability matters:</strong> In our Log 6 survey, 50% of insurance professionals said
  they would only trust an AI fraud system <em>"if I can see the reasoning behind each flag."</em>
  This page delivers exactly that — every fraud score is broken down into auditable, human-readable signals.
</div>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>📊 Model Explainability Overview</div>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown("""<div class='kpi-box'>
      <div class='kpi-label'>Top Fraud Driver</div>
      <div class='kpi-value' style='font-size:18px;'>Texture Artifact</div>
      <div class='kpi-sub'>24% of total fraud score weight</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown("""<div class='kpi-box'>
      <div class='kpi-label'>Features Tracked</div>
      <div class='kpi-value'>7</div>
      <div class='kpi-sub'>Visual + metadata + behavioral</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown("""<div class='kpi-box'>
      <div class='kpi-label'>Explainability Method</div>
      <div class='kpi-value' style='font-size:18px;'>SHAP</div>
      <div class='kpi-sub'>Shapley value attribution · Log 7</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown("""<div class='kpi-box'>
      <div class='kpi-label'>Human Override</div>
      <div class='kpi-value' style='font-size:18px;'>Always On</div>
      <div class='kpi-sub'>AI flags only — no auto-denial</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Feature Importance Chart ──────────────────────────────────────────────────
st.markdown("<div class='section-header'>📊 Fraud Model — Feature Importance</div>", unsafe_allow_html=True)

feature_importance = pd.DataFrame({
    "Feature":    ["Texture Artifact Score", "Metadata Anomaly", "Duplicate Similarity",
                   "Blur / Edge Inconsistency", "Lighting Inconsistency",
                   "Claim Amount", "Prior Claim Frequency"],
    "Importance": [0.24, 0.19, 0.17, 0.14, 0.11, 0.08, 0.07],
    "Category":   ["Visual", "Metadata", "Visual", "Visual", "Visual", "Behavioral", "Behavioral"]
})
feature_importance = feature_importance.sort_values("Importance")

color_map = {"Visual": "#2563eb", "Metadata": "#d97706", "Behavioral": "#059669"}
colors    = [color_map[c] for c in feature_importance["Category"]]

fig = go.Figure(go.Bar(
    x=feature_importance["Importance"],
    y=feature_importance["Feature"],
    orientation="h",
    marker_color=colors,
    text=[f"{v:.0%}" for v in feature_importance["Importance"]],
    textposition="outside"
))
fig.update_layout(
    xaxis=dict(tickformat=".0%", gridcolor="#f3f4f6", range=[0, 0.32]),
    yaxis=dict(gridcolor="#f3f4f6"),
    plot_bgcolor="white", paper_bgcolor="white",
    margin=dict(t=20, b=20, l=20, r=60),
    height=320,
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

# Legend
st.markdown("""
<div style='display:flex;gap:16px;margin-top:-8px;margin-bottom:1rem;font-size:12px;'>
  <span style='color:#2563eb;font-weight:500;'>■ Visual signal</span>
  <span style='color:#d97706;font-weight:500;'>■ Metadata signal</span>
  <span style='color:#059669;font-weight:500;'>■ Behavioral signal</span>
</div>
""", unsafe_allow_html=True)

# ── Claim Selector ────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🔍 Claim-Level Explanation</div>", unsafe_allow_html=True)

claims = {
    "CLM-20481 · High Risk · 0.91": {
        "score": 0.91, "level": "High", "color": "#dc2626",
        "drivers": [
            ("Texture Artifact Score",    0.88, "Abnormal edge patterns detected — consistent with AI-generated damage"),
            ("Metadata Anomaly",          0.82, "EXIF metadata missing entirely — file appears re-exported"),
            ("Duplicate Similarity",      0.74, "Visually similar image found in CLM-18834"),
            ("Blur / Edge Inconsistency", 0.61, "Selective blur inconsistent with collision physics"),
            ("Lighting Inconsistency",    0.45, "Light source direction conflicts with reported time of incident"),
            ("Claim Amount",              0.30, "Slightly above median for reported damage type"),
            ("Prior Claim Frequency",     0.22, "2 prior claims in 18 months — within acceptable range"),
        ],
        "summary": "This claim was flagged High Risk. Three critical signals — texture artifacts, missing metadata, and a duplicate image match — indicate a high probability of staged damage or image manipulation. Recommend immediate SIU escalation."
    },
    "CLM-20489 · Medium Risk · 0.58": {
        "score": 0.58, "level": "Medium", "color": "#d97706",
        "drivers": [
            ("Texture Artifact Score",    0.41, "Minor edge anomalies — possibly due to image compression"),
            ("Metadata Anomaly",          0.55, "Timestamp inconsistency in EXIF data"),
            ("Duplicate Similarity",      0.18, "No duplicate match found"),
            ("Blur / Edge Inconsistency", 0.62, "Some blur inconsistency around damage zone"),
            ("Lighting Inconsistency",    0.38, "Lighting broadly consistent with reported conditions"),
            ("Claim Amount",              0.25, "Within normal range for claim type"),
            ("Prior Claim Frequency",     0.10, "No prior claims on this policy"),
        ],
        "summary": "This claim was flagged Medium Risk. Blur inconsistency and a metadata timestamp anomaly warrant manual adjuster review before payment. No definitive manipulation detected — human judgment required."
    },
    "CLM-20495 · Low Risk · 0.21": {
        "score": 0.21, "level": "Low", "color": "#059669",
        "drivers": [
            ("Texture Artifact Score",    0.15, "No significant texture artifacts"),
            ("Metadata Anomaly",          0.12, "Complete EXIF metadata present and consistent"),
            ("Duplicate Similarity",      0.08, "No duplicate match found"),
            ("Blur / Edge Inconsistency", 0.19, "Blur consistent with natural camera shake"),
            ("Lighting Inconsistency",    0.22, "Lighting consistent with reported time and location"),
            ("Claim Amount",              0.18, "Below median for damage type"),
            ("Prior Claim Frequency",     0.05, "No prior claims"),
        ],
        "summary": "This claim passed all AI validation checks. No significant fraud signals detected across visual, metadata, or behavioral dimensions. Eligible for straight-through processing."
    }
}

selected = st.selectbox("Select a claim to explain", list(claims.keys()),
                        label_visibility="collapsed")
claim = claims[selected]

# Claim summary card
level_card = "danger-card" if claim["level"] == "High" else ("warning-card" if claim["level"] == "Medium" else "insight-card")
dot = "🔴" if claim["level"] == "High" else ("🟡" if claim["level"] == "Medium" else "🟢")

st.markdown(f"""
<div class='{level_card}'>
  <strong>{dot} {claim['level']} Risk — Fraud Score: {claim['score']:.2f}</strong><br>
  {claim['summary']}
</div>
""", unsafe_allow_html=True)

# Driver breakdown
st.markdown("<div class='section-header'>Signal Breakdown</div>", unsafe_allow_html=True)

for name, score, desc in claim["drivers"]:
    bar_color = "#dc2626" if score >= 0.7 else ("#d97706" if score >= 0.4 else "#059669")
    st.markdown(f"""
    <div style='background:#ffffff;border:1px solid #e8ecf0;border-radius:8px;
                padding:12px 14px;margin-bottom:8px;'>
      <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;'>
        <span style='font-size:13px;font-weight:500;color:#111827;'>{name}</span>
        <span style='font-size:13px;font-weight:700;color:{bar_color};'>{score:.2f}</span>
      </div>
      <div style='background:#f3f4f6;border-radius:4px;height:7px;overflow:hidden;margin-bottom:5px;'>
        <div style='width:{score*100:.0f}%;height:7px;background:{bar_color};border-radius:4px;'></div>
      </div>
      <div style='font-size:11px;color:#6b7280;'>{desc}</div>
    </div>
    """, unsafe_allow_html=True)

# SHAP waterfall teaser
st.markdown("""
<div class='thesis-card' style='margin-top:1rem;'>
  <strong>Coming in Log 7:</strong> Full SHAP waterfall charts will show exactly how much each feature
  pushes the fraud score up or down for every individual claim — the gold standard for explainable AI
  in regulated industries. 50% of our surveyed investigators said explainability is their #1 requirement
  before trusting an AI fraud tool.
</div>
""", unsafe_allow_html=True)

# Responsible AI
st.markdown("""
<div class='insight-card'>
  <strong>Responsible AI:</strong> Every explanation shown here is auditable and logged.
  No claim is denied automatically. All High and Medium flags require investigator sign-off.
  This design directly addresses the false positive concern raised by 83% of our Log 6 survey respondents.
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("EPCR AI · Explainable AI · Log 3 · UConn AI Venture Velocity Challenge 2026 · Created by Trishan1990")
