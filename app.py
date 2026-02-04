import json
import logging
from datetime import datetime

import streamlit as st

from classifier import classify_po
from settings import load_settings

logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="PO Category Classifier", layout="wide")

st.markdown(
    """
    <style>
    :root {
      --bg: #f7f4ef;
      --ink: #1b1b1b;
      --accent: #e06c00;
      --panel: #ffffff;
      --muted: #6b6b6b;
      --border: #e7e0d6;
    }
    .stApp { background: var(--bg); color: var(--ink); }
    .hero {
      padding: 20px 22px;
      border: 1px solid var(--border);
      border-radius: 14px;
      background: linear-gradient(135deg, #fff7ec 0%, #ffffff 60%);
      margin-bottom: 16px;
    }
    .hero h1 { font-size: 32px; margin: 0; }
    .hero p { margin: 6px 0 0; color: var(--muted); }
    .card {
      border: 1px solid var(--border);
      border-radius: 12px;
      background: var(--panel);
      padding: 16px;
      box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .pill {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 999px;
      background: #f1e7da;
      color: #6a4a2b;
      font-size: 12px;
      margin-right: 6px;
      margin-bottom: 6px;
    }
    .label { color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; }
    .value { font-size: 18px; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>PO L1–L2–L3 Classifier</h1>
      <p>Fast, structured categorization of purchase order descriptions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

examples = [
    ("DocuSign subscription", "DocuSign Inc", "DocuSign eSignature Enterprise Pro Subscription"),
    ("Office cleaning", "XYZ Facility Services", "Cleaning services for office premises - March"),
    ("Flight ticket", "Indigo Airlines", "Flight ticket for business travel"),
    ("Health insurance", "ABC Insurance", "Payment for employee health insurance premium"),
]

if "po_description" not in st.session_state:
    st.session_state.po_description = ""
if "supplier" not in st.session_state:
    st.session_state.supplier = ""
if "history" not in st.session_state:
    st.session_state.history = []

left, right = st.columns([1.2, 1])

with left:
    st.markdown("### Input")
    example_label = st.selectbox(
        "Quick example",
        ["None"] + [e[0] for e in examples],
        index=0,
    )
    if example_label != "None":
        for label, supplier, text in examples:
            if label == example_label:
                st.session_state.po_description = text
                st.session_state.supplier = supplier
                break

    po_description = st.text_area(
        "PO Description",
        height=140,
        key="po_description",
        placeholder="e.g., Annual subscription for cloud security monitoring",
    )
    supplier = st.text_input("Supplier (optional)", key="supplier")

    col_a, col_b = st.columns([1, 1])
    with col_a:
        classify_clicked = st.button("Classify", use_container_width=True)
    with col_b:
        if st.button("Clear", use_container_width=True):
            st.session_state.po_description = ""
            st.session_state.supplier = ""

    with st.expander("Advanced"):
        settings = load_settings()
        st.caption("Configuration sourced from environment variables when present.")
        st.code(
            {
                "model": settings.model,
                "temperature": settings.temperature,
                "max_tokens": settings.max_tokens,
                "timeout_s": settings.timeout_s,
            }
        )

with right:
    st.markdown("### Result")
    result_container = st.container()

    if classify_clicked:
        if not po_description.strip():
            st.warning("Please enter a PO Description.")
        else:
            with st.spinner("Classifying..."):
                raw_result = classify_po(po_description, supplier)
            try:
                parsed = json.loads(raw_result)
            except Exception:
                parsed = {"error": "Invalid model response", "raw": raw_result}

            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
            st.session_state.history.insert(0, {"timestamp": timestamp, "result": parsed})

            with result_container:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                if "error" in parsed:
                    st.error(parsed["error"])
                    st.code(parsed.get("raw", ""))
                else:
                    st.markdown('<div class="label">Primary</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="value">{parsed.get("L1","Not sure")}</div>', unsafe_allow_html=True)
                    st.markdown(" ")
                    st.markdown('<div class="label">Secondary</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="value">{parsed.get("L2","Not sure")}</div>', unsafe_allow_html=True)
                    st.markdown(" ")
                    st.markdown('<div class="label">Tertiary</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="value">{parsed.get("L3","Not sure")}</div>', unsafe_allow_html=True)
                    confidence = parsed.get("confidence", "Not sure")
                    st.markdown(" ")
                    st.markdown(f'<span class="pill">Confidence: {confidence}</span>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Recent Runs")
    if st.session_state.history:
        for item in st.session_state.history[:5]:
            result = item["result"]
            st.markdown(
                f'<div class="card"><div class="label">{item["timestamp"]}</div>'
                f'<div class="value">{result.get("L1","Not sure")} / '
                f'{result.get("L2","Not sure")} / {result.get("L3","Not sure")}</div>'
                f'<div style="color:#6b6b6b;font-size:12px;margin-top:6px;">'
                f'{result.get("po_description","")}</div></div>',
                unsafe_allow_html=True,
            )
    else:
        st.caption("No runs yet.")
