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

# --- 📌 ดึงข้อมูลจริงจาก Google Sheets ตามลิงก์ที่คุณส่งมา ---
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSTLK92gAXsak5e9HNDcjPngKWXNdOTFmojlq55hMKp-Ak48QNWDcHGRs4fUBWDw/pub?gid=2143365497&single=true&output=csv"

try:
    df = pd.read_csv(sheet_url)
except Exception as e:
    df = pd.DataFrame()
    st.error("ไม่สามารถเชื่อมต่อข้อมูลจาก Google Sheets ได้ กรุณาตรวจสอบการเผยแพร่เว็บอีกครั้ง")

# --- ระบบกรองข้อมูลด้วยช่องค้นหา (ไม่ให้ข้อมูลหายหรือขึ้นคำว่า empty) ---
if not df.empty and search_query:
    mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
    filtered_df = df[mask]
    # ถ้าพิมพ์ค้นหาแล้วไม่เจอข้อมูล ให้ดึงตารางทั้งหมดกลับมาแสดงเพื่อไม่ให้ตารางว่างเปล่า
    if filtered_df.empty:
        filtered_df = df
        st.warning(f"ไม่พบข้อมูลที่ตรงกับ '{search_query}' กำลังแสดงข้อมูลทั้งหมดครับ")
else:
    filtered_df = df

# แสดงผลตารางข้อมูล
st.subheader("📋 รายการข้อมูลโครงการ")
if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.info("ยังไม่มีข้อมูลใน Google Sheets ครับ")
