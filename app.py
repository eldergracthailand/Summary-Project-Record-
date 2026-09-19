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

# --- แถบด้านข้าง (Sidebar) ---
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

# --- 📌 ดึงข้อมูลจาก Google Sheets ---
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSTLK92gAXsak5e9HNDcjPngKWXNdOTFmojlq55hMKp-Ak48QNWDcHGRs4fUBWDw/pub?gid=2143365497&single=true&output=csv"

@st.cache_data(ttl=60) # ช่วยแคชข้อมูลเพื่อให้เว็บโหลดไวและเสถียรขึ้น
def load_data(url):
    return pd.read_csv(url)

try:
    df = load_data(sheet_url)
except Exception as e:
    df = pd.DataFrame()

# --- ระบบตรวจสอบและแสดงผลตาราง ---
if df.empty:
    st.error("⚠️ ไม่สามารถดึงข้อมูลจาก Google Sheets ได้ กรุณาไปที่ Google Sheets ของคุณ -> เลือก ไฟล์ (File) -> แชร์ (Share) -> เผยแพร่เว็บ (Publish to web) -> แล้วกดปุ่ม 'เผยแพร่ซ้ำ' (Republish) อีกครั้งครับ")
else:
    # ระบบกรองข้อมูลด้วยช่องค้นหา
    if search_query:
        mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
        filtered_df = df[mask]
        if filtered_df.empty:
            filtered_df = df
            st.warning(f"ไม่พบข้อมูลที่ตรงกับ '{search_query}' กำลังแสดงข้อมูลทั้งหมดครับ")
    else:
        filtered_df = df

    # แสดงผลตารางข้อมูล
    st.subheader("📋 รายการข้อมูลโครงการ")
    st.dataframe(filtered_df, use_container_width=True)
