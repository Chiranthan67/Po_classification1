import json
import streamlit as st

# Page configuration
st.set_page_config(page_title="PO Category Classifier", layout="centered")

# App title
st.title("📦 PO L1–L2–L3 Classifier")

# Inputs
po_description = st.text_area("PO Description", height=120)
supplier = st.text_input("Supplier (optional)")

# Action
if st.button("Classify"):
    if not po_description.strip():
        st.warning("Please enter a PO description.")
    else:
        with st.spinner("Classifying..."):
            result = classify_po(po_description, supplier)

        try:
            st.json(json.loads(result))
        except Exception:
            st.error("Invalid model response")
            st.text(result)
