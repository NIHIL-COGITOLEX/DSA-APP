# pages/about.py
import streamlit as st
def render(COMPANY_DF, PINCODE_DF, company_manifest, pincode_manifest):
    st.markdown("<h3>🪶 About Cogito Lex</h3>", unsafe_allow_html=True)
    st.markdown("<div class='card'><p>Cogito Lex — mobile-first lookup app. Contact: cogitolex.nihil@gmail.com</p></div>", unsafe_allow_html=True)
