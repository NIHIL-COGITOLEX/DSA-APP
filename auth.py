# auth.py
import streamlit as st
import time

DEFAULT_PINS = {"11111": "viewer", "22222": "manager", "99999": "admin"}
DEFAULT_ROLES = {"viewer": "viewer", "manager": "manager", "admin": "admin"}

def get_pin_credentials():
    try:
        users = st.secrets["pins"]
        roles = st.secrets["roles"]
    except Exception:
        users = DEFAULT_PINS
        roles = DEFAULT_ROLES
    return users, roles

def require_login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.username = None

    if st.session_state.authenticated:
        return

    st.markdown(
        """
        <div style="padding:20px; max-width:420px; margin:24px auto; text-align:center;">
            <h2 style="color:#E673AC;margin:6px 0">Cogito Lex</h2>
            <p style="color:#ddd;margin:2px 0">Enter 5-digit PIN to continue</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pin = st.text_input("", type="password", max_chars=5, placeholder="•••••", label_visibility="collapsed")
    login_btn = st.button("🔓 Unlock", use_container_width=True)

    if login_btn:
        users, roles = get_pin_credentials()
        if not pin or len(pin) != 5 or not pin.isdigit():
            st.error("Please enter a valid 5-digit PIN.")
        elif pin in users:
            st.session_state.authenticated = True
            st.session_state.username = pin
            st.session_state.role = roles.get(users[pin], "viewer")
            st.success(f"Access granted ({st.session_state.role})")
            time.sleep(0.35)
            st.experimental_rerun()
        else:
            st.error("Invalid PIN.")
    st.stop()
