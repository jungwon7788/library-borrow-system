# pages/login_page.py
import streamlit as st
import controller


def render_login():
    st.title("🔐 เข้าสู่ระบบ")
    st.write("ทดสอบ")

    # ===== ข้อมูลผู้จัดทำ =====
    st.markdown("""
    <div style="text-align:center; margin-bottom:20px;">
        <h4>ข้อมูลผู้จัดทำ</h4>
        <p style="font-size:16px; font-weight:bold; color:#6a1b9a;">
            ชลธิชา สูนย์มาตย์<br>
            6740259102<br>
            ว.6706
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ===== ฟอร์ม Login =====
    with st.form("login_form"):
        username = st.text_input(
            "ชื่อผู้ใช้",
            placeholder="เช่น admin"
        )

        password = st.text_input(
            "รหัสผ่าน",
            type="password",
            placeholder="เช่น 1234"
        )

        submitted = st.form_submit_button("Login")

    if submitted:
        ok, msgs, user_info = controller.login(username, password)

        if not ok:
            for m in msgs:
                st.error(m)
        else:
            for m in msgs:
                st.success(m)

            st.session_state["is_logged_in"] = True
            st.session_state["user"] = user_info
            st.session_state["page"] = "books"
            st.rerun()

