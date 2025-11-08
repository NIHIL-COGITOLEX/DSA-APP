# pages/dashboard.py
import streamlit as st
from utils import render_table_html

def render(COMPANY_DF, PINCODE_DF, company_manifest, pincode_manifest):
    st.markdown("<h3>📊 Dashboard Overview</h3>", unsafe_allow_html=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1,1])
    total_companies = len(COMPANY_DF) if COMPANY_DF is not None else 0
    total_pincodes = len(PINCODE_DF) if PINCODE_DF is not None else 0

    with c1:
        st.markdown(f"<div class='card'><div class='kicker'>🏢 Total Companies</div><div style='font-size:22px;font-weight:800'>{total_companies:,}</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card'><div class='kicker'>📮 Total Pincodes</div><div style='font-size:22px;font-weight:800'>{total_pincodes:,}</div></div>", unsafe_allow_html=True)
