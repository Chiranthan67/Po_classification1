from __future__ import annotations

import json
import logging
from functools import lru_cache
from typing import Any

from groq import Groq

from prompts import PROMPT_VERSION, build_system_prompt
from settings import load_settings
from taxonomy import TAXONOMY, validate_classification

logger = logging.getLogger(__name__)


def _get_streamlit_secret(key: str) -> str | None:
    """
    Optional Streamlit secret access. Keeps classifier usable outside Streamlit.
    """
    try:
        import streamlit as st  # local import to avoid hard dependency
    except Exception:
        return None
    try:
        return st.secrets.get(key)  # type: ignore[no-any-return]
    except Exception:
        return None


@lru_cache(maxsize=1)
def _get_client() -> Groq:
    settings = load_settings()
    api_key = settings.api_key or _get_streamlit_secret("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GROQ_API_KEY (env or Streamlit secrets).")
    return Groq(api_key=api_key, timeout=settings.timeout_s)


def _build_user_prompt(po_description: str, supplier: str) -> str:
    return f"""PO Description: {po_description}\nSupplier: {supplier}"""


def _safe_json_loads(raw: str) -> dict[str, Any] | None:
    try:
        return json.loads(raw)
    except Exception:
        return None


def _post_process(payload: dict[str, Any], po_description: str) -> dict[str, Any]:
    """
    Normalize the model response and validate it against the taxonomy.
    """
    l1 = payload.get("L1")
    l2 = payload.get("L2")
    l3 = payload.get("L3")
    safe_l1, safe_l2, safe_l3 = validate_classification(l1, l2, l3, TAXONOMY)
    payload["po_description"] = payload.get("po_description") or po_description
    payload["L1"] = safe_l1
    payload["L2"] = safe_l2
    payload["L3"] = safe_l3
    payload.setdefault("prompt_version", PROMPT_VERSION)
    return payload


def classify_po(po_description: str, Supplier: str = "Not provided") -> str:
    """
    Classify a PO description into L1/L2/L3 categories.
    Returns a JSON string for backward compatibility with the Streamlit app.
    """
    settings = load_settings()
    user_prompt = _build_user_prompt(po_description, Supplier)
    system_prompt = build_system_prompt(TAXONOMY)

    response = _get_client().chat.completions.create(
        model=settings.model,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    raw = response.choices[0].message.content
    payload = _safe_json_loads(raw)
    if payload is None:
        logger.warning("Model returned invalid JSON: %s", raw)
        payload = {
            "po_description": po_description,
            "L1": "Not sure",
            "L2": "Not sure",
            "L3": "Not sure",
            "error": "Invalid JSON from model",
        }
    normalized = _post_process(payload, po_description)
    return json.dumps(normalized, ensure_ascii=True)
