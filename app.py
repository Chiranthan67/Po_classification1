import json
import logging

import streamlit as st

from classifier import classify_po
from settings import load_settings

logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="PO Category Classifier", layout="centered")

st.title("PO L1-L2-L3 Classifier")
po_description =  st.text_area("PO Description",height=120)
supplier = st.text_input("Supplier( optional )")
if st.button("Classify"):
    if not po_description.strip():
        st.warning("Please enter a PO Description")
    else:
        with st.spinner("Classifying...."):
            result = classify_po(po_description, supplier)
        try:
            st.json(json.loads(result))
        except Exception:
            st.error("Invalid model response")
            st.text(result)

with st.expander("Settings", expanded=False):
    settings = load_settings()
    st.caption("These values are sourced from environment variables when present.")
    st.code(
        {
            "model": settings.model,
            "temperature": settings.temperature,
            "max_tokens": settings.max_tokens,
            "timeout_s": settings.timeout_s,
        }
    )
