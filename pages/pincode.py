# pages/pincode.py
import streamlit as st
from utils import build_substring_mask, matched_in, highlight_match, paginate, render_table_html
import pandas as pd

def render(COMPANY_DF, PINCODE_DF, company_manifest, pincode_manifest):
    st.markdown("<h3>📮 Pincode Availability Checker</h3>", unsafe_allow_html=True)
    if PINCODE_DF is None or PINCODE_DF.empty:
        st.warning("No pincode data loaded. Place pincode_listings*.xlsx or .csv in the app folder.")
        PINCODE_DF = pd.DataFrame(columns=["PINCODE", "LOCATION", "BANK_NAME", "STATE"])

    q_col, btn_col = st.columns([4,1])
    with q_col:
        st.text_input("Search (pincode or location)", key="pincode_form_q", placeholder="Type and press Search")
    with btn_col:
        if st.button("🔍 Search", use_container_width=True):
            st.session_state.pincode_query = st.session_state.pincode_form_q
            st.session_state.pincode_page = 0

    banks = ["All"]
    if "BANK_NAME" in PINCODE_DF.columns:
        banks += sorted(PINCODE_DF["BANK_NAME"].dropna().astype(str).unique().tolist())
    st.selectbox("🏦 Bank", banks, index=banks.index(st.session_state.get("pincode_bank", "All")) if st.session_state.get("pincode_bank", "All") in banks else 0, key="pincode_bank", on_change=lambda: st.session_state.update({"pincode_page": 0}))

    q = st.session_state.get("pincode_query", "").strip()
    results = PINCODE_DF.copy()
    search_cols = [c for c in ["PINCODE", "LOCATION"] if c in results.columns]
    if not results.empty:
        mask = build_substring_mask(results, search_cols, q)
        results = results[mask]
        if st.session_state.pincode_bank != "All" and "BANK_NAME" in results.columns:
            results = results[results["BANK_NAME"].astype(str) == st.session_state.pincode_bank]

    st.markdown(f"**✅ Found {len(results):,} result(s)**", unsafe_allow_html=True)
    page_df, total, cur, pages = paginate(results, "pincode_page", "pincode_page_size")

    if q and not page_df.empty:
        display_page = page_df.copy()
        display_page["MATCHED_IN"] = display_page.apply(lambda r: ", ".join(matched_in(r, q, search_cols)) or "-", axis=1)
        for c in search_cols:
            display_page[c] = display_page[c].apply(lambda x: highlight_match(x, q))
        st.markdown(render_table_html(display_page), unsafe_allow_html=True)
    elif not q and not page_df.empty:
        st.markdown(render_table_html(page_df), unsafe_allow_html=True)
    else:
        st.info("No matching results. Try another query.")

    # pagination
    col_prev, col_page, col_next = st.columns([1,1,1])
    with col_prev:
        if st.button("⬅ Prev", key="pincode_prev") and cur > 0:
            st.session_state.pincode_page = cur - 1
            st.experimental_rerun()
    with col_page:
        st.markdown(f"<div style='text-align:center; font-weight:700;'>Page {cur+1} / {pages}</div>", unsafe_allow_html=True)
    with col_next:
        if st.button("Next ➡", key="pincode_next") and cur < pages - 1:
            st.session_state.pincode_page = cur + 1
            st.experimental_rerun()
