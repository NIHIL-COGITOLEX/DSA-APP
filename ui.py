# ui.py
import streamlit as st

GLOBAL_CSS = r"""
<style>
:root{ --rose-soft:#E673AC; --beige:#f3e8d8; --muted:#bfae97; }
body { background: linear-gradient(180deg,#0f0b12,#1a100c); color:var(--beige); font-family:Inter, sans-serif; }
.container { max-width:1080px; margin:8px auto; padding:12px; }
.card { background: rgba(255,255,255,0.02); border-radius:12px; padding:12px; margin-bottom:8px; border:1px solid rgba(255,255,255,0.04);}
.table-wrap { overflow-x:auto; border-radius:10px; padding:6px; }
.full-width-table { width:100%; border-collapse:separate; border-spacing:0; font-size:13px; }
</style>
"""
def inject_global_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
