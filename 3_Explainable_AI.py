
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Explainable AI", page_icon="🧠", layout="wide")

st.title("Explainable AI")
st.caption("Why the model flagged a claim")

feature_importance = pd.DataFrame({
    "Feature": [
        "Texture Artifact Score",
        "Metadata Anomaly",
        "Duplicate Similarity",
        "Blur / Edge Inconsistency",
        "Lighting Inconsistency",
        "Claim Amount",
        "Prior Claim Frequency"
    ],
    "Importance": [0.24, 0.19, 0.17, 0.14, 0.11, 0.08, 0.07]
})

fig = px.bar(feature_importance, x="Importance", y="Feature", orientation="h", title="Fraud Model Feature Importance")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Example Explanation")
st.write("""
Claim CLM-1007 was flagged as high-risk because:
- The uploaded image had abnormal texture artifacts.
- EXIF metadata was missing.
- A visually similar image appeared in another claim.
- Damage pattern severity did not match the reported collision description.
""")
