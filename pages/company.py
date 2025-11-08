# pages/company.py
import streamlit as st
from utils import build_substring_mask, matched_in, highlight_match, paginate, render_table_html

def render(COMPANY_DF, PINCODE_DF, company_manifest, pincode_manifest):
    st.markdown("<h3>🏢 Company Listing Search</h3>", unsafe_allow_html=True)
    if COMPANY_DF is None or COMPANY_DF.empty:
        st.warning("No company data loaded. Place company_listings*.xlsx or .csv in the app folder.")
        COMPANY_DF = COMPANY_DF if COMPANY_DF is not None else None
        # create an empty consistent DataFrame to avoid further crashes
        import pandas as pd
        COMPANY_DF = pd.DataFrame(columns=["COMPANY_NAME", "BANK_NAME", "COMPANY_CATEGORY"])

    # Search input and button
    q_col, btn_col = st.columns([4, 1])
    with q_col:
        st.text_input("Search (company or bank)", key="company_form_q", placeholder="Type and press Search")
    with btn_col:
        if st.button("🔍 Search", use_container_width=True):
            st.session_state.company_query = st.session_state.company_form_q
            st.session_state.company_page = 0

    # Bank filter safely
    banks = ["All"]
    if "BANK_NAME" in COMPANY_DF.columns:
        banks += sorted(COMPANY_DF["BANK_NAME"].dropna().astype(str).unique().tolist())
    st.selectbox("🏦 Bank", banks, index=banks.index(st.session_state.get("company_bank", "All")) if st.session_state.get("company_bank", "All") in banks else 0, key="company_bank", on_change=lambda: st.session_state.update({"company_page": 0}))

    q = st.session_state.get("company_query", "").strip()
    results = COMPANY_DF.copy()
    search_cols = [c for c in ["COMPANY_NAME", "BANK_NAME"] if c in results.columns]
    if not results.empty:
        mask = build_substring_mask(results, search_cols, q)
        results = results[mask]
        if st.session_state.company_bank != "All" and "BANK_NAME" in results.columns:
            results = results[results["BANK_NAME"].astype(str) == st.session_state.company_bank]

    st.markdown(f"**✅ Found {len(results):,} result(s)**", unsafe_allow_html=True)
    page_df, total, cur, pages = paginate(results, "company_page", "company_page_size")

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

    # Pagination controls
    col_prev, col_page, col_next = st.columns([1,1,1])
    with col_prev:
        if st.button("⬅ Prev", key="company_prev") and cur > 0:
            st.session_state.company_page = cur - 1
            st.experimental_rerun()
    with col_page:
        st.markdown(f"<div style='text-align:center; font-weight:700;'>Page {cur+1} / {pages}</div>", unsafe_allow_html=True)
    with col_next:
        if st.button("Next ➡", key="company_next") and cur < pages - 1:
            st.session_state.company_page = cur + 1
            st.experimental_rerun()
