import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

st.set_page_config(page_title="EPCR AI — Fraud Intelligence Lab", layout="wide")

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
  .reason-item {
    display:flex; gap:10px; align-items:flex-start;
    background:#ffffff; border:1px solid #e8ecf0; border-radius:8px;
    padding:10px 14px; margin-bottom:7px; font-size:13px; color:#374151;
  }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/fraud_network_claims.csv")
    df["claim_date"] = pd.to_datetime(df["claim_date"])
    return df

df = load_data()

# ── Graph risk logic ──────────────────────────────────────────────────────────
df["baseline_flag"] = df["base_fraud_score"] >= 70

repair_shop_counts = df["repair_shop"].value_counts()
phone_counts       = df["phone_last4"].value_counts()
image_counts       = df["image_hash"].value_counts()

def network_influence(row):
    score = 0
    if repair_shop_counts[row["repair_shop"]] >= 4: score += 20
    if phone_counts[row["phone_last4"]]        >= 2: score += 20
    if image_counts[row["image_hash"]]         >= 2: score += 25
    if row["metadata_status"] != "Present":          score += 10
    if row["policy_tenure_months"] <= 6:             score += 10
    if row["days_to_report"] <= 1:                   score += 5
    return score

df["network_influence_score"] = df.apply(network_influence, axis=1)
df["composite_fraud_score"]   = (df["base_fraud_score"] + df["network_influence_score"]).clip(upper=100)
df["graph_enhanced_flag"]     = df["composite_fraud_score"] >= 70
df["risk_upgrade"]            = df["graph_enhanced_flag"] & (~df["baseline_flag"])

def severity(score):
    if score >= 85: return "Critical"
    if score >= 70: return "High"
    if score >= 45: return "Medium"
    return "Low"

df["severity"] = df["composite_fraud_score"].apply(severity)

baseline_count     = int(df["baseline_flag"].sum())
graph_count        = int(df["graph_enhanced_flag"].sum())
upgraded_count     = int(df["risk_upgrade"].sum())
additional_exposure = int(df.loc[df["risk_upgrade"], "claim_amount"].sum())

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 🔬 EPCR AI — Fraud Intelligence Lab")
st.markdown("*Graph-based fraud propagation · Organized ring detection · Log 4 capability*")

st.markdown("""
<div class='log-progress'>
  <div style='font-size:12px;font-weight:600;color:#6b7280;margin-bottom:8px;'>PLATFORM BUILD PROGRESS</div>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 1: Setup</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 2: Image Scoring</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 3: Workflow</span>
  <span class='log-step' style='background:#dcfce7;color:#166534;'>● Log 4: Graph Network</span>
  <span class='log-step' style='background:#dbeafe;color:#1e40af;'>✓ Log 5: Digital Twin</span>
  <span class='log-step' style='background:#f3f4f6;color:#9ca3af;'>○ Log 6: Validation</span>
  <span class='log-step' style='background:#f3f4f6;color:#9ca3af;'>○ Log 7: Forecasting</span>
  <span class='log-step' style='background:#f3f4f6;color:#9ca3af;'>○ Log 8: Expert Review</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='thesis-card'>
  <strong>Log 4 Assumption:</strong> Connected claim entities reveal organized fraud risk that
  standalone claim-level fraud scores completely miss. By building a graph of shared repair shops,
  phone numbers, image hashes, and claimant identities, EPCR AI can surface hidden fraud rings
  before losses escalate — validated on the IEEE-CIS dataset at 87.6% precision in Log 5.
</div>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>📊 Graph Detection Results</div>", unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Claims Analyzed</div>
      <div class='kpi-value'>{len(df)}</div>
      <div class='kpi-sub'>In fraud network graph</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Baseline High-Risk</div>
      <div class='kpi-value'>{baseline_count}</div>
      <div class='kpi-sub'>Standalone score ≥ 70</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Graph-Enhanced High-Risk</div>
      <div class='kpi-blue'>{graph_count}</div>
      <div class='kpi-sub'>After network propagation</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Hidden Claims Surfaced</div>
      <div class='kpi-red'>{upgraded_count}</div>
      <div class='kpi-sub'>Missed by baseline scoring</div>
    </div>""", unsafe_allow_html=True)
with k5:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Additional SIU Exposure</div>
      <div class='kpi-red'>${additional_exposure:,.0f}</div>
      <div class='kpi-sub'>At-risk if undetected</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Baseline vs Graph chart ───────────────────────────────────────────────────
st.markdown("<div class='section-header'>📊 Baseline vs Graph-Enhanced Detection</div>",
            unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    fig1 = go.Figure(go.Bar(
        x=["Standalone Score", "EPCR AI Graph"],
        y=[baseline_count, graph_count],
        marker_color=["#cbd5e1", "#2563eb"],
        text=[baseline_count, graph_count],
        textposition="outside"
    ))
    fig1.update_layout(
        title="High-Risk Claims Detected",
        yaxis=dict(gridcolor="#f3f4f6"),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=40, b=20, l=20, r=20), height=280, showlegend=False
    )
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    sev_counts  = df["severity"].value_counts().reindex(
        ["Critical","High","Medium","Low"], fill_value=0)
    fig2 = go.Figure(go.Pie(
        labels=sev_counts.index, values=sev_counts.values, hole=0.5,
        marker_colors=["#dc2626","#d97706","#2563eb","#059669"]
    ))
    fig2.update_layout(
        title="Claims by Severity (Graph-Enhanced)",
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(t=40, b=20, l=20, r=20), height=280
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown(f"""
<div class='insight-card'>
  <strong>Key finding:</strong> Graph propagation surfaced <strong>{upgraded_count} hidden claims</strong>
  worth <strong>${additional_exposure:,.0f}</strong> in exposure that standalone scoring missed entirely.
  These claims were not high-risk individually — they became suspicious only when shared entities
  (repair shops, phone numbers, image hashes) were analyzed as a connected network.
  This is the core value proposition of EPCR AI over Verisk and ISO ClaimSearch.
</div>
""", unsafe_allow_html=True)

# ── Network graph ─────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🕸️ Entity Relationship Graph</div>",
            unsafe_allow_html=True)

st.markdown("""
<div class='thesis-card'>
  Each node is a claim or shared entity (repair shop, phone, image hash, vehicle, claimant).
  Each edge is a connection. Nodes with many connections are potential fraud-enabling hubs.
  The counterfactual analysis below shows what happens when these hubs are removed.
</div>
""", unsafe_allow_html=True)

@st.cache_data
def build_graph(data):
    G = nx.Graph()
    for _, row in data.iterrows():
        claim_node = row["claim_id"]
        G.add_node(claim_node, node_type="Claim")
        entity_nodes = [
            ("Repair Shop", row["repair_shop"]),
            ("Phone",       f"Phone-{row['phone_last4']}"),
            ("Image",       row["image_hash"]),
            ("Vehicle",     f"{row['vehicle_year']} {row['vehicle_make']} {row['vehicle_model']}"),
            ("Claimant",    row["claimant_id"]),
        ]
        for entity_type, entity_value in entity_nodes:
            G.add_node(entity_value, node_type=entity_type)
            G.add_edge(claim_node, entity_value)
    return G

G   = build_graph(df)
pos = nx.spring_layout(G, seed=42, k=0.45)

edge_x, edge_y = [], []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

node_x, node_y, node_text, node_size, node_color = [], [], [], [], []
type_colors = {"Claim":"#2563eb","Repair Shop":"#dc2626","Phone":"#d97706",
               "Image":"#059669","Vehicle":"#7c3aed","Claimant":"#0891b2"}

for node in G.nodes():
    x, y   = pos[node]
    degree = G.degree(node)
    ntype  = G.nodes[node].get("node_type","Claim")
    node_x.append(x); node_y.append(y)
    node_text.append(f"{node}<br>Type: {ntype}<br>Connections: {degree}")
    node_size.append(10 + degree * 4)
    node_color.append(type_colors.get(ntype, "#6b7280"))

fig_graph = go.Figure(data=[
    go.Scatter(x=edge_x, y=edge_y,
               line=dict(width=0.8, color="#e5e7eb"),
               hoverinfo="none", mode="lines"),
    go.Scatter(x=node_x, y=node_y,
               mode="markers",
               text=[str(n)[:18] for n in G.nodes()],
               hovertext=node_text, hoverinfo="text",
               marker=dict(size=node_size, color=node_color,
                           line=dict(width=1, color="#ffffff")))
])
fig_graph.update_layout(
    showlegend=False, height=650,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis=dict(showgrid=False, zeroline=False, visible=False),
    yaxis=dict(showgrid=False, zeroline=False, visible=False),
    plot_bgcolor="white", paper_bgcolor="white"
)
st.plotly_chart(fig_graph, use_container_width=True)

# Color legend
st.markdown("""
<div style='display:flex;gap:16px;flex-wrap:wrap;font-size:12px;margin-top:-8px;margin-bottom:1rem;'>
  <span style='color:#2563eb;font-weight:500;'>● Claim</span>
  <span style='color:#dc2626;font-weight:500;'>● Repair Shop</span>
  <span style='color:#d97706;font-weight:500;'>● Phone</span>
  <span style='color:#059669;font-weight:500;'>● Image Hash</span>
  <span style='color:#7c3aed;font-weight:500;'>● Vehicle</span>
  <span style='color:#0891b2;font-weight:500;'>● Claimant</span>
</div>
""", unsafe_allow_html=True)

# ── Centrality ────────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🧠 Network Centrality — Fraud Hub Detection</div>",
            unsafe_allow_html=True)

centrality    = nx.degree_centrality(G)
centrality_df = pd.DataFrame({
    "Entity":            list(centrality.keys()),
    "Centrality Score":  [round(v, 4) for v in centrality.values()],
    "Connections":       [G.degree(n) for n in centrality.keys()]
}).sort_values("Centrality Score", ascending=False).head(15)

st.dataframe(centrality_df, use_container_width=True, hide_index=True)

top_entity = centrality_df.iloc[0]["Entity"]
top_conns  = centrality_df.iloc[0]["Connections"]

st.markdown(f"""
<div class='danger-card'>
  <strong>🚨 Highest-influence entity: {top_entity}</strong> with {top_conns} connections.
  This entity may be acting as a fraud-enabling hub in the claim network.
  Targeted SIU investigation of this entity could disrupt multiple connected claims simultaneously.
</div>
""", unsafe_allow_html=True)

# ── Suspicious clusters ───────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🚨 Suspicious Fraud Rings / Claim Clusters</div>",
            unsafe_allow_html=True)

cluster_rows = []
for entity_col in ["repair_shop", "phone_last4", "image_hash"]:
    for entity, group in df.groupby(entity_col):
        if len(group) >= 2:
            cluster_rows.append({
                "Shared Entity Type":   entity_col.replace("_"," ").title(),
                "Shared Entity":        entity,
                "Connected Claims":     len(group),
                "Avg Base Score":       round(group["base_fraud_score"].mean(), 1),
                "Avg Composite Score":  round(group["composite_fraud_score"].mean(), 1),
                "Claim Exposure ($)":   int(group["claim_amount"].sum()),
                "Claim IDs":            ", ".join(group["claim_id"].tolist())
            })

if cluster_rows:
    clusters_df = pd.DataFrame(cluster_rows).sort_values(
        ["Connected Claims","Claim Exposure ($)"], ascending=False)
    st.dataframe(clusters_df, use_container_width=True, hide_index=True)
else:
    st.markdown("<div class='insight-card'>No suspicious clusters detected.</div>",
                unsafe_allow_html=True)

# ── Claims upgraded ───────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>⬆️ Claims Upgraded by Graph Propagation</div>",
            unsafe_allow_html=True)

upgraded_df = df[df["risk_upgrade"]].copy()
if not upgraded_df.empty:
    st.markdown(f"""
    <div class='warning-card'>
      <strong>{len(upgraded_df)} claims were below the risk threshold on standalone scoring
      but crossed it after graph propagation.</strong>
      These are exactly the organized fraud cases that Verisk and ISO ClaimSearch miss.
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(
        upgraded_df[["claim_id","loss_city","repair_shop","claim_amount",
                     "base_fraud_score","network_influence_score",
                     "composite_fraud_score","severity","metadata_status","image_hash"]]
        .sort_values("composite_fraud_score", ascending=False),
        use_container_width=True, hide_index=True
    )
else:
    st.markdown("<div class='insight-card'>No claims upgraded in this dataset.</div>",
                unsafe_allow_html=True)

# ── Explainable reasoning ─────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🔎 Explainable Fraud Reasoning — Claim Inspector</div>",
            unsafe_allow_html=True)

selected_claim = st.selectbox("Select a claim to inspect", df["claim_id"].tolist(),
                               label_visibility="collapsed")
claim = df[df["claim_id"] == selected_claim].iloc[0]

reasons = []
if repair_shop_counts[claim["repair_shop"]] >= 4:
    reasons.append(("🏭 Repair Shop", f"Appears in {repair_shop_counts[claim['repair_shop']]} claims — potential fraud hub"))
if phone_counts[claim["phone_last4"]] >= 2:
    reasons.append(("📞 Phone Number", f"Last 4 digits reused across {phone_counts[claim['phone_last4']]} claims"))
if image_counts[claim["image_hash"]] >= 2:
    reasons.append(("🖼️ Image Hash", f"Duplicate image found in {image_counts[claim['image_hash']]} claims"))
if claim["metadata_status"] != "Present":
    reasons.append(("📋 Metadata", "Image EXIF metadata missing — possible re-export or manipulation"))
if claim["policy_tenure_months"] <= 6:
    reasons.append(("📅 Policy Tenure", f"Only {claim['policy_tenure_months']} months old — short-tenure risk"))
if claim["days_to_report"] <= 1:
    reasons.append(("⚡ Report Speed", "Claim reported within 1 day — unusually fast"))

score_color = "#dc2626" if claim["composite_fraud_score"] >= 70 else ("#d97706" if claim["composite_fraud_score"] >= 45 else "#059669")

r1, r2, r3 = st.columns(3)
with r1:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Base Fraud Score</div>
      <div class='kpi-value'>{int(claim["base_fraud_score"])}</div>
      <div class='kpi-sub'>Standalone score</div>
    </div>""", unsafe_allow_html=True)
with r2:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Network Influence</div>
      <div class='kpi-blue'>+{int(claim["network_influence_score"])}</div>
      <div class='kpi-sub'>Added by graph propagation</div>
    </div>""", unsafe_allow_html=True)
with r3:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Composite Fraud Score</div>
      <div style='font-size:28px;font-weight:700;color:{score_color};line-height:1.1;'>
        {int(claim["composite_fraud_score"])}</div>
      <div class='kpi-sub'>Final risk assessment</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("**Escalation Reason Codes:**")

if reasons:
    for icon_label, desc in reasons:
        st.markdown(f"""
        <div class='reason-item'>
          <span style='font-weight:600;min-width:140px;'>{icon_label}</span>
          <span>{desc}</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("<div class='insight-card'>No major network-based fraud signals detected for this claim.</div>",
                unsafe_allow_html=True)

# ── Counterfactual ────────────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🧬 Counterfactual Network Analysis</div>",
            unsafe_allow_html=True)

st.markdown("""
<div class='thesis-card'>
  <strong>Research question:</strong> What happens to the fraud network if the most influential
  entity is removed? This experiment identifies fraud-enabling hubs whose removal would cause
  maximum network fragmentation — helping SIU teams prioritize which entities to investigate first.
</div>
""", unsafe_allow_html=True)

original_nodes = G.number_of_nodes()
original_edges = G.number_of_edges()

G_cf = G.copy()
if top_entity in G_cf:
    G_cf.remove_node(top_entity)

remaining_nodes = G_cf.number_of_nodes()
remaining_edges = G_cf.number_of_edges()
edge_reduction  = original_edges - remaining_edges

cf1, cf2, cf3, cf4 = st.columns(4)
with cf1:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Entity Removed</div>
      <div class='kpi-value' style='font-size:16px;margin-top:4px;'>{str(top_entity)[:20]}</div>
      <div class='kpi-sub'>Highest centrality node</div>
    </div>""", unsafe_allow_html=True)
with cf2:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Original Network Links</div>
      <div class='kpi-value'>{original_edges}</div>
      <div class='kpi-sub'>Before removal</div>
    </div>""", unsafe_allow_html=True)
with cf3:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Remaining Links</div>
      <div class='kpi-value'>{remaining_edges}</div>
      <div class='kpi-sub'>After removal</div>
    </div>""", unsafe_allow_html=True)
with cf4:
    st.markdown(f"""<div class='kpi-box'>
      <div class='kpi-label'>Links Disrupted</div>
      <div class='kpi-red'>{edge_reduction}</div>
      <div class='kpi-sub'>Network fragmentation</div>
    </div>""", unsafe_allow_html=True)

st.markdown(f"""
<div class='insight-card'>
  <strong>Counterfactual result:</strong> Removing <strong>{top_entity}</strong> disrupted
  <strong>{edge_reduction} network connections</strong> — fragmenting the fraud ring.
  This suggests targeted SIU investigation of this single entity could neutralize multiple
  connected claims simultaneously, making it the highest-ROI investigation target in this network.
</div>
""", unsafe_allow_html=True)

# ── Experiment conclusion ─────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🧪 Log 4 — Experiment Conclusion</div>",
            unsafe_allow_html=True)

lift_pct = round((graph_count - baseline_count) / max(baseline_count, 1) * 100, 1)

st.markdown(f"""
<div class='danger-card'>
  <strong>Finding:</strong> Standalone fraud scoring detected <strong>{baseline_count}</strong>
  high-risk claims. Graph-enhanced propagation detected <strong>{graph_count}</strong> —
  a <strong>+{lift_pct}% lift</strong> by surfacing {upgraded_count} hidden claims worth
  ${additional_exposure:,.0f} in exposure.
</div>
<div class='insight-card'>
  <strong>Interpretation:</strong> Fraud risk does not always appear at the individual claim level.
  It emerges through shared entities — repair shops, reused images, phone numbers, and
  short-tenure policies — that connect otherwise unrelated claims into organized fraud rings.
</div>
<div class='thesis-card'>
  <strong>Venture implication:</strong> EPCR AI is not an image fraud tool. It is an
  <strong>early-warning fraud intelligence platform</strong> for organized insurance fraud —
  validated on 590,540 real transactions (Log 5) at 87.6% precision, with a +25.6% recall
  improvement over standalone scoring. Log 6 asks: do investigators prefer this intelligence
  over what they currently use?
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("EPCR AI · Fraud Intelligence Lab · Log 4 · UConn AI Venture Velocity Challenge 2026 · Created by Trishan1990")
