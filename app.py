st.markdown("""
<style>

/* ===== พื้นหลังเจ้าหญิง ===== */
.stApp {
    background: linear-gradient(135deg, #fff0f6, #f8e8ff, #ffe3f3);
    font-family: 'Segoe UI', sans-serif;
}

/* ===== หัวข้อใหญ่ ===== */
h1 {
    text-align: center;
    font-size: 40px;
    font-weight: 900;
    background: linear-gradient(90deg,#ff4da6,#c77dff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 1px;
}

/* ===== Sidebar หรูฟุ้ง ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#fff,#ffe6f2);
    border-right: 3px solid #ffb3ec;
}

/* ===== เมนู Title ===== */
.menu-title {
    text-align: center;
    font-size: 24px;
    font-weight: 900;
    color: #ff4da6;
    margin-top: 10px;
    margin-bottom: 20px;
}

/* ===== ปุ่มเมนู ===== */
.stSidebar button {
    border-radius: 25px !important;
    border: none !important;
    background: linear-gradient(90deg,#ff66c4,#c77dff) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 10px 0px !important;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(255,105,180,0.3);
}

/* Hover วิ้งๆ */
.stSidebar button:hover {
    transform: scale(1.08);
    box-shadow: 0 6px 20px rgba(255,105,180,0.6);
    background: linear-gradient(90deg,#ff4da6,#b5179e) !important;
}

/* ===== Card Form หรู ===== */
div[data-testid="stForm"] {
    background: white;
    padding: 30px;
    border-radius: 25px;
    box-shadow: 0 10px 40px rgba(255,105,180,0.25);
}

/* ===== Input ===== */
input {
    border-radius: 15px !important;
    border: 2px solid #ffd6f6 !important;
}

/* ===== ปุ่ม Login ===== */
div[data-testid="stForm"] button {
    border-radius: 20px !important;
    background: linear-gradient(90deg,#ff4da6,#c77dff) !important;
    color: white !important;
    font-weight: bold !important;
    font-size: 16px !important;
    box-shadow: 0 4px 15px rgba(255,105,180,0.4);
}

div[data-testid="stForm"] button:hover {
    transform: scale(1.05);
}

/* ===== Warning box สวยขึ้น ===== */
.stAlert {
    border-radius: 15px !important;
}

</style>
""", unsafe_allow_html=True)
