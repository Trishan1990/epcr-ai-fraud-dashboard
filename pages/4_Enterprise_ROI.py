import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="EPCR AI — Enterprise ROI", page_icon="💰", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .kpi-box { background:#ffffff; border:1px solid #e8ecf0; border-radius:10px; padding:1.2rem 1.4rem; }
  .kpi-label { font-size:13px; color:#6b7280; font-weight:500; margin-bottom:4px; }
  .kpi-value { font-size:28px; font-weight:700; color:#111827; line-height:1.1; }
  .kpi-green { font-size:28px; font-weight:700; color:#059669; line-height:1.1; }
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
    font-size:13px; color:#1e40af; line-height:1.6; font-style:italic;
  }
  .warning-card {
    background:#fffbeb; border:1px solid #fde68a; border-left:4px solid #d97706;
    border-radius:8px; padding:1rem 1.2rem; margin-bottom:0.75rem;
    font-size:13px; color:#111827; line-height:1.6;
  }
  .log-progress { background:#f9fafb; border:1px solid #e5e7eb; border-radius:10px; padding:1rem 1.4rem; margin-bottom:1.5rem; }
  .log-step { display:inline-block; font-size:12px; font-weight:600; padding:4px 12px; border-radius:20px; margin-right:6px; }
  .pricing-card {
    background:#ffffff; border:1px solid #e8ecf0; border-radius:12px;
    padding:1.5rem; text-align:center; height:100%;
  }
  .pricing-card.featured { border:2px solid #2563eb; background:#eff6ff; }
  .pricing-tier { font-size:14px; font-weight:700; color:#6b7280; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:8px; }
  .pricing-price { font-size:32px; font-weight:700; color:#111827; margin-bottom:4px; }
  .pricing-sub { font-size:12px; color:#6b7280; margin-bottom:16px; }
  .pricing-feature { font-size:13px; color:#374151; margin-bottom:6px; text-align:left; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 💰 EPCR AI — Enterprise ROI Calculator")
st.markdown("*Business case for AI-powered fraud detection · Market sizing and pricing*")

st.markdown("""
<div class='log-progress'>
  <div style='font-size:12px;font-weight:600;color:#6b7280;margin-bottom:8px;'>PLATFORM BUILD PROGRESS</div>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 1: Setup</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 2: Image Scoring</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 3: Workflow</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 4: Graph Network</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 5: Digital Twin</span>
  <span class='log-step' style='background:#f3f4f6;color:#9ca3af;'>○ Log 6: Validation</span>
  <span class='log-step' style='background:#f3f4f6;color:#9ca3af;'>○ Log 7: Forecasting</span>
  <span class='log-step' style='background:#f3f4f6;color:#9ca3af;'>○ Log 8: Expert Review</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='thesis-card'>
  <strong>Market context:</strong> Insurance fraud costs U.S. insurers approximately
  <strong>$308 billion per year</strong> (Coalition Against Insurance Fraud, 2025).
  A mid-size P&C insurer processing 50,000 claims/year with an 8% fraud rate has
  <strong>$14M in annual fraud exposure</strong>. EPCR AI's graph model — validated at
  87.6% precision on 590,540 real transactions — captures fraud rings that standalone
  scoring completely misses.
</div>
""", unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🎛️ Configure Your Insurer Profile</div>",
            unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    claims_per_year       = st.number_input("Annual claims volume", value=100000, step=5000)
    avg_claim_value       = st.number_input("Average claim payout ($)", value=3500, step=100)
    fraud_rate            = st.slider("Estimated fraud rate (%)", 1, 20, 8)
with col2:
    detection_lift        = st.slider("EPCR AI detection improvement (%)", 5, 60, 25,
                                       help="Based on Log 5: +25.6% recall improvement on IEEE-CIS dataset")
    manual_review_reduction = st.slider("Manual review time reduction (%)", 5, 60, 35)
    cost_per_review       = st.number_input("Cost per manual review ($)", value=18, step=1)

# ── Calculations ──────────────────────────────────────────────────────────────
fraud_loss           = claims_per_year * avg_claim_value * (fraud_rate / 100)
fraud_savings        = fraud_loss * (detection_lift / 100)
operational_savings  = claims_per_year * cost_per_review * (manual_review_reduction / 100)
total_value          = fraud_savings + operational_savings
roi_multiple         = total_value / max((claims_per_year * 1.50), 1)  # vs $1.50/claim pricing
payback_months       = max((claims_per_year * 1.50 * 12) / max(total_value, 1), 0.1)

# ── KPI Row ───────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>📊 Your ROI Estimate</div>", unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Annual Fraud Exposure</div>
      <div class='kpi-value'>${fraud_loss/1e6:.1f}M</div>
      <div class='kpi-sub'>{fraud_rate}% of {claims_per_year:,} claims</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Fraud Savings from AI</div>
      <div class='kpi-green'>${fraud_savings/1e6:.1f}M</div>
      <div class='kpi-sub'>+{detection_lift}% detection improvement</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Operational Savings</div>
      <div class='kpi-green'>${operational_savings:,.0f}</div>
      <div class='kpi-sub'>{manual_review_reduction}% fewer manual reviews</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Total Annual Value</div>
      <div class='kpi-green'>${total_value/1e6:.2f}M</div>
      <div class='kpi-sub'>Fraud + operational combined</div>
    </div>""", unsafe_allow_html=True)
with k5:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Payback Period</div>
      <div class='kpi-blue'>{payback_months:.1f} mo</div>
      <div class='kpi-sub'>At $1.50/claim pricing</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown("<div class='section-header'>Value Breakdown</div>", unsafe_allow_html=True)
    fig1 = go.Figure(go.Bar(
        x=["Fraud Detection Savings", "Operational Savings"],
        y=[fraud_savings, operational_savings],
        marker_color=["#2563eb", "#059669"],
        text=[f"${fraud_savings:,.0f}", f"${operational_savings:,.0f}"],
        textposition="outside"
    ))
    fig1.update_layout(
        yaxis=dict(gridcolor="#f3f4f6", title="USD ($)"),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=20, b=20, l=20, r=20), height=280,
        showlegend=False
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.markdown("<div class='section-header'>Fraud Exposure vs AI Recovery</div>",
                unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name="Unrecovered Fraud",
                          x=["Without EPCR AI", "With EPCR AI"],
                          y=[fraud_loss, fraud_loss - fraud_savings],
                          marker_color="#fecaca"))
    fig2.add_trace(go.Bar(name="Recovered by AI",
                          x=["Without EPCR AI", "With EPCR AI"],
                          y=[0, fraud_savings],
                          marker_color="#059669"))
    fig2.update_layout(
        barmode="stack",
        yaxis=dict(gridcolor="#f3f4f6", title="USD ($)"),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=20, b=20, l=20, r=20), height=280,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Pricing ───────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>💳 EPCR AI — SaaS Pricing</div>",
            unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.markdown("""
    <div class='pricing-card'>
      <div class='pricing-tier'>Starter</div>
      <div class='pricing-price'>$5K</div>
      <div class='pricing-sub'>/month · up to 5,000 claims</div>
      <div class='pricing-feature'>✅ Image validation</div>
      <div class='pricing-feature'>✅ Fraud scoring</div>
      <div class='pricing-feature'>✅ Investigator queue</div>
      <div class='pricing-feature'>❌ Graph network</div>
      <div class='pricing-feature'>❌ Forecasting</div>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown("""
    <div class='pricing-card featured'>
      <div class='pricing-tier' style='color:#2563eb;'>Growth ★ Most Popular</div>
      <div class='pricing-price'>$15K</div>
      <div class='pricing-sub'>/month · up to 25,000 claims</div>
      <div class='pricing-feature'>✅ Image validation</div>
      <div class='pricing-feature'>✅ Fraud scoring</div>
      <div class='pricing-feature'>✅ Investigator queue</div>
      <div class='pricing-feature'>✅ Graph network detection</div>
      <div class='pricing-feature'>❌ Forecasting</div>
    </div>
    """, unsafe_allow_html=True)

with p3:
    st.markdown("""
    <div class='pricing-card'>
      <div class='pricing-tier'>Enterprise</div>
      <div class='pricing-price'>$1.50</div>
      <div class='pricing-sub'>/claim · unlimited volume</div>
      <div class='pricing-feature'>✅ Full platform access</div>
      <div class='pricing-feature'>✅ Graph network detection</div>
      <div class='pricing-feature'>✅ Risk forecasting</div>
      <div class='pricing-feature'>✅ SHAP explainability</div>
      <div class='pricing-feature'>✅ SLA + dedicated support</div>
    </div>
    """, unsafe_allow_html=True)

with p4:
    st.markdown("""
    <div class='pricing-card'>
      <div class='pricing-tier'>Pilot</div>
      <div class='pricing-price'>Free</div>
      <div class='pricing-sub'>90-day read-only deployment</div>
      <div class='pricing-feature'>✅ Full platform access</div>
      <div class='pricing-feature'>✅ SIU feedback loop</div>
      <div class='pricing-feature'>✅ ROI measurement</div>
      <div class='pricing-feature'>✅ No commitment required</div>
      <div class='pricing-feature' style='color:#2563eb;'>→ Contact for pilot access</div>
    </div>
    """, unsafe_allow_html=True)

# ── Competitive context ───────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🏆 Why Not Just Use Verisk or ISO ClaimSearch?</div>",
            unsafe_allow_html=True)

st.markdown("""
<div class='warning-card'>
  <strong>The gap existing tools leave:</strong> Verisk and ISO ClaimSearch score individual claims.
  They cannot detect organized fraud rings — multiple claims connected through shared repair shops,
  phone numbers, or image hashes. Our Log 5 results showed standalone scoring catches only 922
  fraud cases out of 20,592 actual fraud transactions (4.5%). EPCR AI's graph model caught 7,840
  (38%) — an 8.5× improvement — by tracing the network behind the claim.
</div>
<div class='insight-card'>
  <strong>EPCR AI is not a replacement for Verisk.</strong> It is a graph intelligence layer
  that sits on top of existing scoring tools and surfaces the organized fraud rings they miss.
  This means zero rip-and-replace cost for insurers — EPCR AI plugs in via API alongside
  whatever scoring system is already in place.
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("EPCR AI · Enterprise ROI · UConn AI Venture Velocity Challenge 2026 · Created by Trishan1990")
