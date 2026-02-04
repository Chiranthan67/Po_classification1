import json
import streamlit as st
from classifier import classify_po

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(page_title="PO Category Classifier", layout="centered")

# -----------------------------
# App title
# -----------------------------
st.title("📦 PO L1–L2–L3 Classifier")

# -----------------------------
# Inputs
# -----------------------------
po_description = st.text_area(
    "PO Description",
    height=120,
    placeholder="Example: Supply of stainless steel pipes for refinery maintenance"
)

supplier = st.text_input(
    "Supplier (optional)",
    placeholder="Example: ABC Industrial Supplies"
)

# -----------------------------
# Action
# -----------------------------
if st.button("Classify"):
    if not po_description.strip():
        st.warning("Please enter a PO description.")
    else:
        with st.spinner("Classifying..."):
            try:
                result = classify_po(po_description, supplier)
            except Exception as e:
                st.error("Classification failed.")
                st.text(str(e))
                st.stop()

        # -----------------------------
        # Output handling
        # -----------------------------
        try:
            parsed = json.loads(result)
            st.success("Classification successful ✅")
            st.json(parsed)
        except json.JSONDecodeError:
            st.error("Invalid model response (expected JSON).")
            st.text("Raw output:")
            st.text(result)
