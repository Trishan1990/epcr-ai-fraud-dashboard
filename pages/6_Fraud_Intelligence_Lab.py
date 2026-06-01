import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

st.set_page_config(page_title="Fraud Intelligence Lab", layout="wide")

st.title("🔬 Fraud Intelligence Lab")
st.subheader("Graph-Based Fraud Propagation Modeling for Early Insurance Fraud Detection")

st.markdown("""
This experiment tests whether connected claim entities can reveal organized fraud risk
that may be missed by standalone claim-level fraud scores.
""")

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("data/fraud_network_claims.csv")
df["claim_date"] = pd.to_datetime(df["claim_date"])

# -----------------------------
# Baseline logic
# -----------------------------
df["baseline_flag"] = df["base_fraud_score"] >= 70

# -----------------------------
# Network risk signals
# -----------------------------
repair_shop_counts = df["repair_shop"].value_counts()
phone_counts = df["phone_last4"].value_counts()
image_counts = df["image_hash"].value_counts()

def network_influence(row):
    score = 0

    if repair_shop_counts[row["repair_shop"]] >= 4:
        score += 20

    if phone_counts[row["phone_last4"]] >= 2:
        score += 20

    if image_counts[row["image_hash"]] >= 2:
        score += 25

    if row["metadata_status"] != "Present":
        score += 10

    if row["policy_tenure_months"] <= 6:
        score += 10

    if row["days_to_report"] <= 1:
        score += 5

    return score

df["network_influence_score"] = df.apply(network_influence, axis=1)
df["composite_fraud_score"] = (
    df["base_fraud_score"] + df["network_influence_score"]
).clip(upper=100)

df["graph_enhanced_flag"] = df["composite_fraud_score"] >= 70
df["risk_upgrade"] = df["graph_enhanced_flag"] & (~df["baseline_flag"])

def severity(score):
    if score >= 85:
        return "Critical"
    elif score >= 70:
        return "High"
    elif score >= 45:
        return "Medium"
    else:
        return "Low"

df["severity"] = df["composite_fraud_score"].apply(severity)

# -----------------------------
# KPI section
# -----------------------------
baseline_count = int(df["baseline_flag"].sum())
graph_count = int(df["graph_enhanced_flag"].sum())
upgraded_count = int(df["risk_upgrade"].sum())
additional_exposure = int(df.loc[df["risk_upgrade"], "claim_amount"].sum())

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Claims Analyzed", len(df))
col2.metric("Baseline High-Risk", baseline_count)
col3.metric("Graph-Enhanced High-Risk", graph_count)
col4.metric("Hidden Claims Surfaced", upgraded_count)
col5.metric("Additional SIU Exposure", f"${additional_exposure:,.0f}")

st.divider()

# -----------------------------
# Research comparison
# -----------------------------
st.header("📊 Baseline vs Graph-Enhanced Detection")

comparison = pd.DataFrame({
    "Model": ["Standalone Fraud Score", "Graph-Enhanced Fraud Propagation"],
    "High-Risk Claims Detected": [baseline_count, graph_count],
    "Detection Lift": [0, graph_count - baseline_count]
})

st.bar_chart(
    comparison.set_index("Model")["High-Risk Claims Detected"]
)

st.markdown("""
**Research Interpretation:**  
The graph-enhanced approach identifies claims that were not high-risk individually,
but became suspicious after shared entities such as repair shops, phone numbers,
image hashes, and metadata anomalies were analyzed.
""")

st.divider()

# -----------------------------
# Build network graph
# -----------------------------
st.header("🕸️ Entity Relationship Graph")

G = nx.Graph()

for _, row in df.iterrows():
    claim_node = row["claim_id"]

    G.add_node(claim_node, node_type="Claim")

    entity_nodes = [
    ("Repair Shop", row["repair_shop"]),
    ("Phone", f"Phone-{row['phone_last4']}"),
    ("Image", row["image_hash"]),
    ("Vehicle", f"{row['vehicle_year']} {row['vehicle_make']} {row['vehicle_model']}"),
    ("Claimant", row["claimant_id"]),
]

    for entity_type, entity_value in entity_nodes:
        G.add_node(entity_value, node_type=entity_type)
        G.add_edge(claim_node, entity_value)

pos = nx.spring_layout(G, seed=42, k=0.45)

edge_x = []
edge_y = []

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=1),
    hoverinfo="none",
    mode="lines"
)

node_x = []
node_y = []
node_text = []
node_size = []

for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

    degree = G.degree(node)
    node_text.append(f"{node}<br>Connections: {degree}")
    node_size.append(10 + degree * 4)

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers+text",
    text=[str(n)[:18] for n in G.nodes()],
    textposition="top center",
    hovertext=node_text,
    hoverinfo="text",
    marker=dict(
        size=node_size,
        line=dict(width=1)
    )
)

fig = go.Figure(data=[edge_trace, node_trace])

fig.update_layout(
    title="Claim-Entity Network: Claims, Repair Shops, Phones, Images, Vehicles, and Claimants",
    showlegend=False,
    height=700,
    margin=dict(l=20, r=20, t=50, b=20),
    xaxis=dict(showgrid=False, zeroline=False, visible=False),
    yaxis=dict(showgrid=False, zeroline=False, visible=False)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------
# Centrality research
# -----------------------------
st.header("🧠 Network Centrality Analysis")

centrality = nx.degree_centrality(G)

centrality_df = pd.DataFrame({
    "entity": list(centrality.keys()),
    "centrality_score": list(centrality.values()),
    "connections": [G.degree(n) for n in centrality.keys()]
}).sort_values("centrality_score", ascending=False)

st.dataframe(centrality_df.head(15), use_container_width=True)

top_entity = centrality_df.iloc[0]["entity"]

st.success(
    f"Highest influence entity identified: {top_entity}. "
    "This entity may represent a fraud-enabling node in the claim network."
)

st.divider()

# -----------------------------
# Suspicious clusters
# -----------------------------
st.header("🚨 Suspicious Fraud Rings / Claim Clusters")

cluster_rows = []

for entity_col in ["repair_shop", "phone_last4", "image_hash"]:
    grouped = df.groupby(entity_col)

    for entity, group in grouped:
        if len(group) >= 2:
            cluster_rows.append({
                "shared_entity_type": entity_col,
                "shared_entity": entity,
                "connected_claims": len(group),
                "avg_base_score": round(group["base_fraud_score"].mean(), 1),
                "avg_composite_score": round(group["composite_fraud_score"].mean(), 1),
                "claim_exposure": int(group["claim_amount"].sum()),
                "claims": ", ".join(group["claim_id"].tolist())
            })

clusters_df = pd.DataFrame(cluster_rows)

if not clusters_df.empty:
    clusters_df = clusters_df.sort_values(
        ["connected_claims", "claim_exposure"],
        ascending=False
    )
    st.dataframe(clusters_df, use_container_width=True)
else:
    st.info("No suspicious clusters detected.")

st.divider()

# -----------------------------
# Claims upgraded by graph risk
# -----------------------------
st.header("⬆️ Claims Upgraded by Graph Propagation")

upgraded_df = df[df["risk_upgrade"]].copy()

if not upgraded_df.empty:
    st.dataframe(
        upgraded_df[
            [
                "claim_id",
                "loss_city",
                "repair_shop",
                "claim_amount",
                "base_fraud_score",
                "network_influence_score",
                "composite_fraud_score",
                "severity",
                "metadata_status",
                "image_hash"
            ]
        ].sort_values("composite_fraud_score", ascending=False),
        use_container_width=True
    )
else:
    st.info("No claims were upgraded by graph propagation.")

st.divider()

# -----------------------------
# Explainable AI reasoning
# -----------------------------
st.header("🔎 Explainable Fraud Reasoning")

selected_claim = st.selectbox(
    "Select a claim to inspect",
    df["claim_id"].tolist()
)

claim = df[df["claim_id"] == selected_claim].iloc[0]

reasons = []

if repair_shop_counts[claim["repair_shop"]] >= 4:
    reasons.append(f"Repair shop appears in {repair_shop_counts[claim['repair_shop']]} claims")

if phone_counts[claim["phone_last4"]] >= 2:
    reasons.append(f"Phone last4 appears in {phone_counts[claim['phone_last4']]} claims")

if image_counts[claim["image_hash"]] >= 2:
    reasons.append(f"Image hash reused in {image_counts[claim['image_hash']]} claims")

if claim["metadata_status"] != "Present":
    reasons.append("Image metadata / EXIF is missing")

if claim["policy_tenure_months"] <= 6:
    reasons.append("Policy tenure is very short")

if claim["days_to_report"] <= 1:
    reasons.append("Claim was reported unusually quickly")

colA, colB, colC = st.columns(3)

colA.metric("Base Fraud Score", int(claim["base_fraud_score"]))
colB.metric("Network Influence", int(claim["network_influence_score"]))
colC.metric("Composite Fraud Score", int(claim["composite_fraud_score"]))

st.write("### Escalation Reason Codes")

if reasons:
    for reason in reasons:
        st.write(f"- {reason}")
else:
    st.write("- No major network-based fraud signals detected.")

st.divider()

# -----------------------------
# Final research conclusion
# -----------------------------
st.header("🧪 Experiment Learning")

st.markdown(f"""
**Finding:**  
Standalone fraud scoring detected **{baseline_count}** high-risk claims.  
Graph-enhanced fraud propagation detected **{graph_count}** high-risk claims.

The model surfaced **{upgraded_count} hidden claims** that were not high-risk individually
but became suspicious after connected claim entities were analyzed.

**Interpretation:**  
Fraud risk may not always appear at the individual claim level.  
It can emerge through shared entities such as repair shops, reused images,
phone numbers, and short-tenure policies.

**Venture Implication:**  
EPCR can evolve from an image-fraud detection dashboard into an early-warning
fraud intelligence platform for organized insurance fraud.
""")
