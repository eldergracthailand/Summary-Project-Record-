import pandas as pd
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Permatech Asia - Summary Project Record",
    page_icon="🏢",
    layout="wide"
)

# --- ส่วนของการใส่รหัสผ่าน (Password Protection) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>🔒 Permatech Asia Internal Portal</h2>", unsafe_allow_html=True)
    password = st.text_input("กรุณากรอกรหัสผ่านเพื่อเข้าสู่ระบบ:", type="password")
    if st.button("เข้าสู่ระบบ", use_container_width=True):
        if password == "PMA":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง")
    st.stop()

# --- แถบด้านข้าง (Sidebar) ตามแบบที่คุณต้องการ ---
with st.sidebar:
    st.markdown("### 🏢 Permatech Asia")
    st.markdown("<p style='color: gray; font-size: 13px; margin-top: -15px;'>Summary Project Record</p>", unsafe_allow_html=True)
    
    st.markdown("<br>" * 15, unsafe_allow_html=True)
    if st.button("ออกจากระบบ", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- เนื้อหาหลักของเว็บไซต์ ---
st.markdown("<h1 style='color: #1e3a8a;'>📊 Summary Project Record</h1>", unsafe_allow_html=True)
st.markdown("สรุปข้อมูลโครงการภายในบริษัท Permatech Asia")
st.markdown("---")

# 🔍 ช่องค้นหาข้อมูล
st.markdown("### 🔍 ค้นหาข้อมูล")
search_query = st.text_input("พิมพ์คำค้นหา...", placeholder="ชื่อโครงการ, No.Job")

st.markdown("---")

# ==========================================
# 📌 นำโค้ดดึงข้อมูล Google Sheets เดิมของคุณมาใส่ตรงนี้ครับ!
# ตัวอย่างเช่น: 
# df = pd.read_csv("ลิงก์ CSV ของ Google Sheets คุณ")
# หรือโค้ดเดิมที่คุณเคยใช้ดึง Google Sheets
# ==========================================
# (ตัวอย่างการดึงข้อมูล ให้เปลี่ยนบรรทัดล่างนี้เป็นโค้ดดึง Google Sheets ของคุณจริง ๆ)
try:
    # แทนที่บรรทัดด้านล่างนี้ด้วยโค้ดดึงข้อมูล Google Sheets เดิมของคุณ
    # เช่น df = pd.read_csv("YOUR_GOOGLE_SHEET_CSV_URL")
    
    # อันนี้เป็นโค้ดดึงข้อมูลตัวอย่างเดิมที่คุณเคยใช้:
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/your_sheet_id/export?format=csv") # <--- เปลี่ยนตรงนี้เป็นลิงก์ของคุณ
    
except Exception as e:
    # หากยังไม่ได้ใส่ลิงก์จริง ให้สร้างตารางเปล่าไว้ก่อนเพื่อไม่ให้เว็บพัง
    df = pd.DataFrame(columns=["No.Job", "ชื่อโครงการ", "สถานะ"])

# --- ระบบกรองข้อมูลด้วยช่องค้นหา ---
if search_query:
    mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
    filtered_df = df[mask]
else:
    filtered_df = df

# แสดงผลตารางข้อมูล
st.subheader("📋 รายการข้อมูลโครงการ")
st.dataframe(filtered_df, use_container_width=True)
