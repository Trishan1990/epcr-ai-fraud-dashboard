import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import cv2
import random

st.set_page_config(
    page_title="Image Validation",
    page_icon="🖼️",
    layout="wide"
)

st.title("Claim Image Validation")
st.caption("Upload a claim image and generate an AI fraud-risk score")

uploaded_file = st.file_uploader(
    "Upload vehicle damage image",
    type=["jpg", "jpeg", "png"]
)

def calculate_fake_fraud_score(image):
    arr = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

    edge_density = cv2.Canny(gray, 100, 200).mean() / 255
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    brightness = gray.mean() / 255

    texture_risk = min(edge_density * 2.5, 1)
    blur_risk = 1 - min(blur_score / 1000, 1)
    brightness_risk = abs(brightness - 0.5) * 1.4
    metadata_risk = random.uniform(0.15, 0.55)
    duplicate_risk = random.uniform(0.05, 0.45)

    fraud_score = (
        0.55 * blur_risk +
        0.20 * texture_risk +
        0.10 * brightness_risk +
        0.10 * metadata_risk +
        0.05 * duplicate_risk
    )

    if blur_risk > 0.7:
        fraud_score += 0.20

    if texture_risk > 0.3:
        fraud_score += 0.15

    fraud_score = min(fraud_score, 1.0)

    return {
        "fraud_score": float(np.clip(fraud_score, 0, 1)),
        "texture_risk": float(np.clip(texture_risk, 0, 1)),
        "blur_risk": float(np.clip(blur_risk, 0, 1)),
        "brightness_risk": float(np.clip(brightness_risk, 0, 1)),
        "metadata_risk": metadata_risk,
        "duplicate_risk": duplicate_risk,
        "edge_density": edge_density,
        "blur_score": blur_score,
    }

def create_heatmap(image):
    arr = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

    edges = cv2.Canny(gray, 80, 180)
    heatmap = cv2.applyColorMap(edges, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(
        arr,
        0.70,
        heatmap,
        0.30,
        0
    )

    return overlay

def risk_label(score):
    if score >= 0.70:
        return "High", "Escalate to SIU investigator"
    elif score >= 0.40:
        return "Medium", "Manual review recommended"
    return "Low", "Auto-process eligible"

if uploaded_file:
    image = Image.open(uploaded_file)
    results = calculate_fake_fraud_score(image)
    label, action = risk_label(results["fraud_score"])

    left, right = st.columns([1, 1])

    with left:
        st.subheader("Uploaded Claim Image")
        st.image(image, use_container_width=True)

        st.subheader("AI Suspicious Region Heatmap")
        overlay = create_heatmap(image)
        st.image(
            overlay,
            caption="AI-generated suspicious region visualization",
            use_container_width=True
        )

    with right:
        st.subheader("AI Fraud Score")

        st.metric(
            "Composite Fraud Score",
            f"{results['fraud_score']:.2f}"
        )

        st.metric(
            "Risk Level",
            label
        )

        st.info(
            f"Recommended Action: {action}"
        )

        st.write("### Fraud Drivers")

        driver_df = pd.DataFrame({
            "Signal": [
                "Texture Artifact Risk",
                "Blur / Manipulation Risk",
                "Lighting Risk",
                "Metadata Risk",
                "Duplicate Risk"
            ],
            "Score": [
                results["texture_risk"],
                results["blur_risk"],
                results["brightness_risk"],
                results["metadata_risk"],
                results["duplicate_risk"]
            ]
        })

        st.dataframe(
            driver_df,
            use_container_width=True
        )

    st.divider()

    st.subheader("Explainability Summary")

    if label == "High":
        st.error(
            "This image should be escalated. The model detected abnormal visual or metadata patterns."
        )
    elif label == "Medium":
        st.warning(
            "This image requires manual review before payment decision."
        )
    else:
        st.success(
            "This image appears low-risk based on current validation rules."
        )

else:
    st.info(
        "Upload a vehicle damage image to generate a fraud score."
    )