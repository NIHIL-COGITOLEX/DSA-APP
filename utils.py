# utils.py
from typing import Any, Iterable, List
import pandas as pd
import re
import streamlit as st
import math

def set_default(k, v):
    if k not in st.session_state:
        st.session_state[k] = v

def rerun():
    try:
        st.rerun()
    except Exception:
        try:
            st.experimental_rerun()
        except Exception:
            pass

def normalize_headers(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.copy()
    df.columns = [str(c).strip().upper().replace(" ", "_") for c in df.columns]
    return df

def highlight_match(text: Any, query: str) -> str:
    s = "" if pd.isna(text) else str(text)
    q = (query or "").strip()
    if not q:
        return s
    return re.sub(re.escape(q), lambda m: f"<mark style='background:rgba(230,115,172,0.18);padding:0 4px;border-radius:4px;color:#fff'>{m.group(0)}</mark>", s, flags=re.IGNORECASE)

def matched_in(row: pd.Series, q: str, cols: Iterable[str]) -> List[str]:
    ql = (q or "").strip().lower()
    if not ql:
        return []
    hits = []
    for c in cols:
        if c in row and ql in ("" if pd.isna(row[c]) else str(row[c]).lower()):
            hits.append(c)
    return hits

def build_substring_mask(df: pd.DataFrame, cols: Iterable[str], q: str) -> pd.Series:
    if not q:
        return pd.Series(True, index=df.index)
    ql = str(q).lower()
    mask = pd.Series(False, index=df.index)
    for c in cols:
        if c in df.columns:
            mask |= df[c].astype(str).str.lower().str.contains(ql, regex=False, na=False)
    return mask

def paginate(df: pd.DataFrame, page_key: str, size_key: str):
    total = len(df)
    page_size = max(1, int(st.session_state.get(size_key, 20)))
    pages = max(1, math.ceil(total / page_size))
    st.session_state[page_key] = min(st.session_state.get(page_key, 0), pages - 1)
    cur = st.session_state[page_key]
    start, end = cur * page_size, cur * page_size + page_size
    return df.iloc[start:end], total, cur, pages

def render_table_html(df: pd.DataFrame, hidden=None) -> str:
    if hidden is None:
        hidden = {"ROW_KEY", "MATCHED_IN", "A_BRANCH_PINCODE"}
    visible_cols = [c for c in df.columns if c not in hidden]
    if not visible_cols:
        return "<div class='card'><div class='kicker'>No visible columns</div></div>"
    html = df[visible_cols].to_html(index=False, classes="full-width-table", escape=False)
    return f"<div class='table-wrap'>{html}</div>"
