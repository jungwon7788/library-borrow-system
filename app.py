import streamlit as st

from pages import book_page
from pages import member_page
from pages import borrow_page
from pages import report_page
from pages import admin_page
from pages import login_page


# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="ระบบยืม-คืนหนังสือ",
    page_icon="📚",
    layout="wide"
)


# =========================
# 🌸 Princess Theme + Hide White Menu Only
# =========================
st.markdown("""
<style>

/* ===== ซ่อน Multi-page เมนูสีขาว ===== */
section[data-testid="stSidebarNav"] {
    display: none !important;
}

/* ===== พื้นหลังเจ้าหญิง ===== */
.stApp {
    background: linear-gradient(135deg, #fff0f6, #f8e8ff);
    font-family: 'Segoe UI', sans-serif;
}

/* ===== หัวข้อหลัก ===== */
h1 {
    text-align: center;
    font-weight: 900;
    font-size: 38px;
    background: linear-gradient(90deg,#ff4da6,#c77dff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ===== Sidebar ของเรา (ชมพูสวย ๆ) ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff, #ffe6f2);
    border-right: 2px solid #ffb3ec;
}

/* ===== ปุ่มเมนู ===== */
.stSidebar button {
    border-radius: 25px !important;
    border: none !important;
    background: linear-gradient(90deg,#ff66c4,#c77dff) !important;
    color: white !important;
    font-weight: bold !important;
    padding: 10px 0px !important;
    transition: 0.3s ease;
}

.stSidebar button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg,#ff4da6,#b5179e) !important;
}

/* ===== Form Card ===== */
div[data-testid="stForm"] {
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 10px 30px rgba(255,105,180,0.25);
}

/* ===== Input ===== */
input {
    border-radius: 12px !important;
}

/* ===== ปุ่ม Login ===== */
div[data-testid="stForm"] button {
    border-radius: 15px !important;
    background: linear-gradient(90deg,#ff4da6,#c77dff) !important;
    color: white !important;
    font-weight: bold !important;
}

</style>
""", unsafe_allow_html=True)


# =========================
# Session Init
# =========================
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None


# =========================
# Login Gate
# =========================
if not st.session_state["is_logged_in"]:
    login_page.render_login()
    st.stop()


# =========================
# Main Header
# =========================
st.title("📚 ระบบยืม-คืนหนังสือ")
st.write("ตัวอย่าง Web App เชื่อมฐานข้อมูล (MVC Concept)")


# =========================
# Sidebar User Info (อันนี้เก็บไว้)
# =========================
user = st.session_state.get("user") or {}

st.sidebar.markdown(f"👤 ผู้ใช้: **{user.get('username','-')}**")
st.sidebar.markdown(f"🔑 บทบาท: **{user.get('role','-')}**")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state["is_logged_in"] = False
    st.session_state["user"] = None
    st.session_state["page"] = "books"
    st.rerun()


# =========================
# Menu
# =========================
if "page" not in st.session_state:
    st.session_state.page = "books"

st.sidebar.markdown("""
<div style='text-align:center;
            font-size:22px;
            font-weight:800;
            color:#ff4da6;
            margin-top:10px;
            margin-bottom:20px;'>
เมนู
</div>
""", unsafe_allow_html=True)


def nav_button(label, key, icon=""):
    btn = st.sidebar.button(
        f"{icon} {label}",
        use_container_width=True,
        key=f"btn_{key}"
    )
    if btn:
        st.session_state.page = key
        st.rerun()


role = user.get("role", "admin")

nav_button("หนังสือ", "books", "📚")
nav_button("สมาชิก", "members", "👤")
nav_button("ยืม-คืน", "borrows", "🔄")

if role == "admin":
    nav_button("จัดการผู้ใช้", "admin", "🛠️")
    nav_button("รายงาน", "reports", "📊")


# =========================
# Routing
# =========================
if st.session_state.page == "books":
    book_page.render_book()

elif st.session_state.page == "members":
    member_page.render_member()

elif st.session_state.page == "borrows":
    borrow_page.render_borrow()

elif st.session_state.page == "reports":
    if role != "admin":
        st.warning("⚠ หน้านี้เฉพาะ admin")
    else:
        report_page.render_report()

elif st.session_state.page == "admin":
    if role != "admin":
        st.warning("⚠ หน้านี้เฉพาะ admin")
    else:
        admin_page.render_admin()
else:
    book_page.render_book()
