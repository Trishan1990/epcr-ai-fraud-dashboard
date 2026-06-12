import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(page_title="EPCR AI — Forecasting Engine", page_icon="📡", layout="wide")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .kpi-box { background:#ffffff; border:1px solid #e8ecf0; border-radius:10px; padding:1.2rem 1.4rem; }
  .kpi-label { font-size:13px; color:#6b7280; font-weight:500; margin-bottom:4px; }
  .kpi-value { font-size:28px; font-weight:700; color:#111827; line-height:1.1; }
  .kpi-red   { font-size:28px; font-weight:700; color:#dc2626; line-height:1.1; }
  .kpi-green { font-size:28px; font-weight:700; color:#059669; line-height:1.1; }
  .kpi-blue  { font-size:28px; font-weight:700; color:#2563eb; line-height:1.1; }
  .kpi-amber { font-size:28px; font-weight:700; color:#d97706; line-height:1.1; }
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
  .log-step { display:inline-block; font-size:12px; font-weight:600; padding:4px 12px; border-radius:20px; margin-right:6px; margin-bottom:4px; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown("## 📡 EPCR AI — Fraud Forecasting Engine")
st.markdown("*Predicting which claims will escalate into fraud rings — before losses occur · Log 7*")

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
  <strong>Log 7 Assumption:</strong> Current fraud networks contain signals that predict future escalation.
  By combining standalone fraud scores with network propagation through shared entities, EPCR AI can
  identify claims that appear low-risk individually but are connected to high-risk fraud networks —
  surfacing future fraud rings before losses escalate.
</div>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load_forecast():
    try:
        forecast = pd.read_csv("data/data/forecast_scores.csv")
        metrics  = pd.read_csv("data/data/model_metrics.csv")
        return forecast, metrics
    except Exception as e:
        st.error(f"Data not found: {e}")
        return None, None

forecast_df, metrics_df = load_forecast()
if forecast_df is None:
    st.stop()

metrics = metrics_df.iloc[0]

# ── KPIs ──────────────────────────────────────────────────────
st.markdown("<div class='section-header'>📊 Forecasting Results — 5,000 Transaction Sample</div>",
            unsafe_allow_html=True)

critical = len(forecast_df[forecast_df['risk_level'] == 'Critical'])
high     = len(forecast_df[forecast_df['risk_level'] == 'High'])
medium   = len(forecast_df[forecast_df['risk_level'] == 'Medium'])
near_miss= int(forecast_df['near_miss'].sum())
avg_network = forecast_df['network_risk_score'].mean()
uplift = len(forecast_df[
    (forecast_df['network_risk_score'] > forecast_df['fraud_prob'] + 0.05)
])

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Critical Risk</div>
      <div class='kpi-red'>{critical}</div>
      <div class='kpi-sub'>Network score ≥ 0.85</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>High Risk</div>
      <div class='kpi-amber'>{high}</div>
      <div class='kpi-sub'>Network score ≥ 0.70</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Medium Risk</div>
      <div class='kpi-blue'>{medium}</div>
      <div class='kpi-sub'>Network score ≥ 0.45</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Near-Miss Claims</div>
      <div class='kpi-amber'>{near_miss:,}</div>
      <div class='kpi-sub'>Low standalone, high network</div>
    </div>""", unsafe_allow_html=True)
with k5:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Network Uplift</div>
      <div class='kpi-green'>{uplift:,}</div>
      <div class='kpi-sub'>Claims elevated by graph signal</div>
    </div>""", unsafe_allow_html=True)
with k6:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Avg Network Score</div>
      <div class='kpi-value'>{avg_network:.3f}</div>
      <div class='kpi-sub'>Across all sampled claims</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown("<div class='section-header'>Risk Level Distribution</div>",
                unsafe_allow_html=True)
    risk_counts = forecast_df['risk_level'].value_counts().reindex(
        ['Critical','High','Medium','Low'], fill_value=0)
    fig1 = go.Figure(go.Bar(
        x=risk_counts.index, y=risk_counts.values,
        marker_color=['#dc2626','#d97706','#2563eb','#059669'],
        text=risk_counts.values, textposition='outside'
    ))
    fig1.update_layout(
        yaxis=dict(gridcolor='#f3f4f6'),
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=20,b=20,l=20,r=20), height=280, showlegend=False
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown("<div class='section-header'>Standalone Score vs Network Risk Score</div>",
                unsafe_allow_html=True)
    sample = forecast_df.sample(min(500, len(forecast_df)), random_state=42)
    color_map = {'Critical':'#dc2626','High':'#d97706','Medium':'#2563eb','Low':'#059669'}
    fig2 = go.Figure()
    for level, color in color_map.items():
        mask = sample['risk_level'] == level
        if mask.sum() > 0:
            fig2.add_trace(go.Scatter(
                x=sample[mask]['fraud_prob'],
                y=sample[mask]['network_risk_score'],
                mode='markers',
                name=level,
                marker=dict(color=color, size=4, opacity=0.6)
            ))
    fig2.add_shape(type='line', x0=0, y0=0, x1=1, y1=1,
                   line=dict(dash='dash', color='#9ca3af', width=1))
    fig2.update_layout(
        xaxis=dict(title='Standalone Fraud Score', gridcolor='#f3f4f6', range=[0,1]),
        yaxis=dict(title='Network Risk Score', gridcolor='#f3f4f6', range=[0,1]),
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=20,b=20,l=20,r=20), height=280,
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
<div class='insight-card'>
  <strong>Reading the scatter plot:</strong> Points above the diagonal line are claims where the
  network risk score is higher than the standalone fraud score. These are claims that appear
  lower-risk individually but are connected to high-risk fraud networks — exactly the organized
  fraud rings that Verisk and ISO ClaimSearch miss.
</div>
""", unsafe_allow_html=True)

# ── Near-miss panel ────────────────────────────────────────────
st.markdown("<div class='section-header'>⚠️ Near-Miss Claims — Hidden Fraud Ring Connections</div>",
            unsafe_allow_html=True)

st.markdown("""
<div class='warning-card'>
  <strong>What are near-miss claims?</strong> These are claims that scored below the standalone
  fraud threshold but have elevated network risk scores due to connections with confirmed fraud
  entities. They represent the early warning signal of an emerging fraud ring.
  A claims adjuster at Metro Hartford specifically requested this feature in Log 6 feedback.
</div>
""", unsafe_allow_html=True)

near_miss_df = forecast_df[forecast_df['near_miss'] == 1].copy()
near_miss_df = near_miss_df.sort_values('network_risk_score', ascending=False)

if len(near_miss_df) > 0:
    st.markdown(f"**{len(near_miss_df):,} near-miss claims detected** in this sample — "
                f"low standalone score but elevated network risk")

    display = near_miss_df.head(20).copy()
    display['fraud_prob']         = display['fraud_prob'].round(3)
    display['network_risk_score'] = display['network_risk_score'].round(3)
    display['Network Uplift']     = (display['network_risk_score'] -
                                      display['fraud_prob']).round(3)
    display = display.rename(columns={
        'TransactionAmt':     'Amount ($)',
        'card1':              'Card ID',
        'isFraud':            'Actual Fraud',
        'fraud_prob':         'Standalone Score',
        'network_risk_score': 'Network Score',
        'risk_level':         'Risk Level'
    })[['Amount ($)','Card ID','Actual Fraud','Standalone Score',
        'Network Score','Network Uplift','Risk Level']]

    st.dataframe(display, use_container_width=True, hide_index=True)
else:
    st.info("No near-miss claims in current sample.")

# ── Forecast distribution ──────────────────────────────────────
st.markdown("<div class='section-header'>📈 Network Risk Score Distribution</div>",
            unsafe_allow_html=True)

fig3 = go.Figure()
fig3.add_trace(go.Histogram(
    x=forecast_df['fraud_prob'], name='Standalone Score',
    nbinsx=50, marker_color='#cbd5e1', opacity=0.7
))
fig3.add_trace(go.Histogram(
    x=forecast_df['network_risk_score'], name='Network Risk Score',
    nbinsx=50, marker_color='#2563eb', opacity=0.7
))
fig3.update_layout(
    barmode='overlay',
    xaxis=dict(title='Risk Score', gridcolor='#f3f4f6'),
    yaxis=dict(title='Count', gridcolor='#f3f4f6'),
    plot_bgcolor='white', paper_bgcolor='white',
    legend=dict(orientation='h', yanchor='bottom', y=1.02),
    margin=dict(t=40,b=20,l=20,r=20), height=280
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
<div class='insight-card'>
  <strong>What this shows:</strong> The network risk score distribution (blue) has a heavier
  tail than the standalone score (grey) — meaning the graph propagation elevates more claims
  into higher-risk buckets by detecting their connections to fraud rings. This is the forecasting
  signal: claims that appear clean in isolation but dangerous in context.
</div>
""", unsafe_allow_html=True)

# ── What Log 8 asks ────────────────────────────────────────────
st.markdown("<div class='section-header'>➡️ What Log 8 Asks</div>", unsafe_allow_html=True)
st.markdown("""
<div class='thesis-card'>
  Log 7 proved EPCR AI can predict future fraud escalation through network signals and explain
  every decision with SHAP attribution. <strong>Log 8 asks: is this methodology credible
  and deployable by a real insurer?</strong> Named expert reviewers, a responsible AI
  assessment, NAIC compliance documentation, and a 90-day pilot structure will close
  the final gap before June 20.
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("EPCR AI · Fraud Forecasting Engine · Log 7 · IEEE-CIS Dataset · UConn AI Venture Velocity Challenge 2026 · Trishan1990")
