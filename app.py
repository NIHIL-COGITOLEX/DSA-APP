# app.py
import streamlit as st
from data_loader import safe_load_companies_and_pincodes
from auth import require_login
from ui import inject_global_css
from utils import set_default, set_page
from pages import dashboard, company, pincode, formatter, about

# Page config
st.set_page_config(page_title="Cogito Lex", page_icon="🧠📜", layout="wide")
inject_global_css()

# ---- Auth ----
require_login()

# ---- App defaults ----
defaults = {
    "company_query": "",
    "company_bank": "All",
    "company_category": "All",
    "company_page": 0,
    "company_page_size": 20,
    "company_history": [],
    "company_form_q": "",
    "pincode_query": "",
    "pincode_bank": "All",
    "pincode_state": "All",
    "pincode_page": 0,
    "pincode_page_size": 20,
    "pincode_history": [],
    "pincode_form_q": "",
    "active_page": "company",
    "sidebar_collapsed_last_action": None,
    "scroll_preserve_enabled": True,
}
for k, v in defaults.items():
    set_default(k, v)

# optional: map of pages
PAGES = {
    "dashboard": dashboard,
    "company": company,
    "pincode": pincode,
    "formatter": formatter,
    "about": about,
}

# ---- Load data safely (won't throw if files absent) ----
COMPANY_DF, company_manifest, PINCODE_DF, pincode_manifest = safe_load_companies_and_pincodes()

# Provide some safe empty schemas so downstream code doesn't crash
if COMPANY_DF is None or COMPANY_DF.empty:
    COMPANY_DF = COMPANY_DF if COMPANY_DF is not None else None
    COMPANY_DF = COMPANY_DF if COMPANY_DF is not None else None  # defensive (keeps variable present)

# ---- Sidebar navigation UI (simple) ----
with st.sidebar:
    st.markdown("<div style='padding:10px 6px'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin:0;color:#E673AC;'>Cogito Lex</h3>", unsafe_allow_html=True)
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # Navigation buttons
    for key in ["dashboard", "company", "pincode", "formatter", "about"]:
        label = {
            "dashboard": "📊 Dashboard",
            "company": "🏢 Companies",
            "pincode": "📮 Pincodes",
            "formatter": "🪄 Name Formatter",
            "about": "ℹ About",
        }[key]
        is_active = st.session_state.get("active_page") == key
        btn_key = f"nav_{key}"
        if st.button(label, key=btn_key, use_container_width=True):
            set_page(key)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown(f"**Signed in as** `{st.session_state.get('username','Unknown')}`", unsafe_allow_html=True)
    if st.button("Logout"):
        for k in ["authenticated", "role", "username"]:
            st.session_state.pop(k, None)
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---- Render the active page ----
active = st.session_state.get("active_page", "company")
page_module = PAGES.get(active, company)
# Each page expects (st, dataframes, manifest)
page_module.render(
    COMPANY_DF=COMPANY_DF,
    PINCODE_DF=PINCODE_DF,
    company_manifest=company_manifest,
    pincode_manifest=pincode_manifest,
)
