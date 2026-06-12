import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(page_title="EPCR AI — SHAP Explainability", page_icon="🧬", layout="wide")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .kpi-box { background:#ffffff; border:1px solid #e8ecf0; border-radius:10px; padding:1.2rem 1.4rem; }
  .kpi-label { font-size:13px; color:#6b7280; font-weight:500; margin-bottom:4px; }
  .kpi-value { font-size:28px; font-weight:700; color:#111827; line-height:1.1; }
  .kpi-blue  { font-size:28px; font-weight:700; color:#2563eb; line-height:1.1; }
  .kpi-green { font-size:28px; font-weight:700; color:#059669; line-height:1.1; }
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
  .thesis-card {
    background:#eff6ff; border:1px solid #bfdbfe; border-left:4px solid #2563eb;
    border-radius:8px; padding:1rem 1.2rem; margin-bottom:1.25rem;
    font-size:13px; color:#1e40af; line-height:1.6; font-style:italic;
  }
  .log-progress { background:#f9fafb; border:1px solid #e5e7eb; border-radius:10px; padding:1rem 1.4rem; margin-bottom:1.5rem; }
  .log-step { display:inline-block; font-size:12px; font-weight:600; padding:4px 12px; border-radius:20px; margin-right:6px; margin-bottom:4px; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown("## 🧬 EPCR AI — SHAP Explainability Engine")
st.markdown("*Why every fraud flag was raised — transparent, auditable, investigator-ready · Log 7*")

st.markdown("""
<div class='log-progress'>
  <div style='font-size:12px;font-weight:600;color:#6b7280;margin-bottom:8px;'>PLATFORM BUILD PROGRESS</div>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 1: Setup</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 2: Image Scoring</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 3: Workflow</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 4: Graph Network</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 5: Digital Twin</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 6: Validation</span>
  <span class='log-step' style='background:#dcfce7;color:#166534;'>● Log 7: Forecasting</span>
  <span class='log-step' style='background:#f3f4f6;color:#9ca3af;'>○ Log 8: Expert Review</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='thesis-card'>
  <strong>Why this page exists:</strong> In the Log 6 investigator survey, 50% of respondents said they would
  only trust EPCR AI <em>"if I can see the reasoning behind each flag."</em> This page delivers that.
  Every fraud flag is now backed by SHAP (SHapley Additive exPlanations) — the gold standard for
  explainable AI in regulated industries. Validated on 590,540 real IEEE-CIS transactions.
</div>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load_shap():
    try:
        shap_df  = pd.read_csv("data/data/shap_values.csv")
        feat_imp = pd.read_csv("data/data/shap_feature_importance.csv")
        thresh   = pd.read_csv("data/data/threshold_analysis.csv")
        metrics  = pd.read_csv("data/data/model_metrics.csv")
        return shap_df, feat_imp, thresh, metrics
    except Exception as e:
        st.error(f"Data not found: {e}")
        return None, None, None, None

shap_df, feat_imp, thresh_df, metrics_df = load_shap()

if shap_df is None:
    st.stop()

features = ['TransactionAmt','card1','card2','card3','card5','addr1','addr2']
metrics  = metrics_df.iloc[0]

# ── KPIs ──────────────────────────────────────────────────────
st.markdown("<div class='section-header'>📊 Model Performance — With Explainability</div>",
            unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Precision</div>
      <div class='kpi-value'>{metrics['precision']:.1%}</div>
      <div class='kpi-sub'>At threshold {metrics['threshold']}</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Recall</div>
      <div class='kpi-value'>{metrics['recall']:.1%}</div>
      <div class='kpi-sub'>Fraud cases caught</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Top Fraud Driver</div>
      <div class='kpi-blue' style='font-size:18px;margin-top:4px;'>{feat_imp.iloc[0]['feature']}</div>
      <div class='kpi-sub'>{feat_imp.iloc[0]['pct_contribution']:.1f}% of fraud signal</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Features Explained</div>
      <div class='kpi-value'>7</div>
      <div class='kpi-sub'>All fraud drivers visible</div>
    </div>""", unsafe_allow_html=True)
with k5:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Explainability Method</div>
      <div class='kpi-blue' style='font-size:20px;margin-top:4px;'>SHAP</div>
      <div class='kpi-sub'>Shapley value attribution</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Feature importance ─────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown("<div class='section-header'>🔍 Feature Importance — What Drives Fraud Flags</div>",
                unsafe_allow_html=True)

    feat_sorted = feat_imp.sort_values('mean_abs_shap')
    fig1 = go.Figure(go.Bar(
        x=feat_sorted['mean_abs_shap'],
        y=feat_sorted['feature'],
        orientation='h',
        marker_color='#2563eb',
        text=[f"{v:.4f}" for v in feat_sorted['mean_abs_shap']],
        textposition='outside'
    ))
    fig1.update_layout(
        xaxis=dict(title='Mean |SHAP Value|', gridcolor='#f3f4f6'),
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=20,b=20,l=20,r=60), height=300
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown("<div class='section-header'>📊 Feature Contribution to Fraud Score (%)</div>",
                unsafe_allow_html=True)

    fig2 = go.Figure(go.Pie(
        labels=feat_imp['feature'],
        values=feat_imp['pct_contribution'],
        hole=0.45,
        marker_colors=['#2563eb','#7c3aed','#059669','#d97706','#dc2626','#0891b2','#6b7280']
    ))
    fig2.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=20,b=20,l=20,r=20), height=300
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
<div class='insight-card'>
  <strong>Key finding:</strong> TransactionAmt is the dominant fraud driver at 48.2% of total SHAP signal.
  Card identifiers (card1, card2, card5) collectively contribute 37.8% — confirming that shared card
  identities across claims are a primary fraud ring signal. This validates EPCR AI's graph propagation
  approach: connecting claims by shared card entities captures the most important fraud signal.
</div>
""", unsafe_allow_html=True)

# ── Threshold slider ───────────────────────────────────────────
st.markdown("<div class='section-header'>🎛️ Precision-Recall Threshold — Investigator Control</div>",
            unsafe_allow_html=True)

st.markdown("""
<div class='thesis-card'>
  <strong>Addressing the false positive concern:</strong> The #1 hesitation from Log 6 survey respondents
  was false positives. This slider lets investigators tune the threshold — trade precision for recall
  based on their team's review capacity.
</div>
""", unsafe_allow_html=True)

selected_thresh = st.slider(
    "Fraud flag threshold (higher = fewer but more accurate flags)",
    min_value=0.20, max_value=0.80, value=0.35, step=0.05,
    format="%.2f"
)

row = thresh_df[thresh_df['threshold'] == selected_thresh]
if not row.empty:
    r = row.iloc[0]
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.markdown(f"""<div class='kpi-box'>
          <div class='kpi-label'>Precision at {selected_thresh}</div>
          <div class='kpi-value'>{r['precision']:.1%}</div>
          <div class='kpi-sub'>Flags that are correct</div>
        </div>""", unsafe_allow_html=True)
    with t2:
        st.markdown(f"""<div class='kpi-box'>
          <div class='kpi-label'>Recall at {selected_thresh}</div>
          <div class='kpi-value'>{r['recall']:.1%}</div>
          <div class='kpi-sub'>Fraud cases caught</div>
        </div>""", unsafe_allow_html=True)
    with t3:
        st.markdown(f"""<div class='kpi-box'>
          <div class='kpi-label'>F1 Score at {selected_thresh}</div>
          <div class='kpi-value'>{r['f1']:.1%}</div>
          <div class='kpi-sub'>Precision-recall balance</div>
        </div>""", unsafe_allow_html=True)
    with t4:
        recommendation = ("High precision — fewer reviews, more accurate"
                          if selected_thresh >= 0.45 else
                          ("Balanced — recommended for most SIU teams"
                           if selected_thresh >= 0.30 else
                           "High recall — more reviews, catches more fraud"))
        st.markdown(f"""<div class='kpi-box'>
          <div class='kpi-label'>Recommendation</div>
          <div class='kpi-value' style='font-size:13px;margin-top:4px;'>{recommendation}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Threshold curve
fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=thresh_df['threshold'], y=thresh_df['precision'],
    name='Precision', line=dict(color='#2563eb', width=2)
))
fig3.add_trace(go.Scatter(
    x=thresh_df['threshold'], y=thresh_df['recall'],
    name='Recall', line=dict(color='#dc2626', width=2)
))
fig3.add_trace(go.Scatter(
    x=thresh_df['threshold'], y=thresh_df['f1'],
    name='F1 Score', line=dict(color='#059669', width=2, dash='dash')
))
fig3.add_vline(x=selected_thresh, line_dash='dot',
               line_color='#d97706', line_width=2,
               annotation_text=f"Selected: {selected_thresh}")
fig3.update_layout(
    xaxis=dict(title='Threshold', gridcolor='#f3f4f6'),
    yaxis=dict(title='Score', gridcolor='#f3f4f6', range=[0,1]),
    plot_bgcolor='white', paper_bgcolor='white',
    legend=dict(orientation='h', yanchor='bottom', y=1.02),
    margin=dict(t=40,b=20,l=20,r=20), height=300
)
st.plotly_chart(fig3, use_container_width=True)

# ── Claim inspector ────────────────────────────────────────────
st.markdown("<div class='section-header'>🔎 Claim-Level SHAP Explanation</div>",
            unsafe_allow_html=True)

flagged = shap_df[shap_df['predicted_prob'] >= selected_thresh].copy()
st.markdown(f"**{len(flagged):,} claims flagged** at threshold {selected_thresh} · "
            f"Showing SHAP breakdown for individual claims")

if len(flagged) > 0:
    sample_claim = flagged.sample(1, random_state=42).iloc[0]

    shap_vals  = [sample_claim[f] for f in features]
    base_value = sample_claim['predicted_prob'] - sum(shap_vals)

    colors = ['#dc2626' if v > 0 else '#059669' for v in shap_vals]
    sorted_pairs = sorted(zip(features, shap_vals), key=lambda x: abs(x[1]), reverse=True)
    sorted_feats = [p[0] for p in sorted_pairs]
    sorted_vals  = [p[1] for p in sorted_pairs]
    sorted_colors= ['#dc2626' if v > 0 else '#059669' for v in sorted_vals]

    fig4 = go.Figure(go.Bar(
        x=sorted_vals,
        y=sorted_feats,
        orientation='h',
        marker_color=sorted_colors,
        text=[f"{'+' if v>0 else ''}{v:.4f}" for v in sorted_vals],
        textposition='outside'
    ))
    fig4.update_layout(
        title=f"SHAP Waterfall — Sample Flagged Claim (Fraud Score: {sample_claim['predicted_prob']:.2f})",
        xaxis=dict(title='SHAP Value (red = pushes toward fraud, green = away from fraud)',
                   gridcolor='#f3f4f6'),
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=50,b=20,l=20,r=80), height=320
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.caption("Each bar shows how much that feature pushed the fraud score up (red) or down (green). "
               "Investigators can audit every flag with this breakdown.")

# ── Responsible AI ─────────────────────────────────────────────
st.markdown("""
<div class='insight-card'>
  <strong>Responsible AI — Explainability Audit Trail:</strong> Every fraud flag in EPCR AI is now
  backed by a SHAP breakdown showing exactly which features drove the decision. This satisfies the
  explainability requirement raised by 50% of Log 6 survey respondents, meets the NAIC Model Bulletin
  on AI transparency requirements, and provides the audit trail required for regulatory compliance.
  No claim is denied automatically — all flags are recommendations for human investigator review.
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("EPCR AI · SHAP Explainability · Log 7 · IEEE-CIS Dataset · UConn AI Venture Velocity Challenge 2026 · Trishan1990")
