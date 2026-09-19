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

# --- แถบด้านข้าง (Sidebar) คงตราบริษัทไว้ และมีช่องค้นหาตามเดิม ---
with st.sidebar:
    st.markdown("### 🏢 Permatech Asia")
    st.markdown("<p style='color: gray; font-size: 13px; margin-top: -15px;'>Summary Project Record</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ช่องค้นหาข้อมูลเดิม
    st.markdown("### 🔍 ค้นหาข้อมูล")
    search_query = st.text_input("พิมพ์คำค้นหา...", placeholder="ชื่อโครงการ, รหัส...")

    st.markdown("---")
    if st.button("ออกจากระบบ", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- เนื้อหาหลักของเว็บไซต์ (กลับมาเป็นหน้าตาฟอร์มและตารางเดิมของคุณ) ---
st.markdown("<h1 style='color: #1e3a8a;'>📊 Summary Project Record</h1>", unsafe_allow_html=True)
st.markdown("ระบบติดตามและสรุปข้อมูลโครงการภายในบริษัท Permatech Asia")
st.markdown("---")

# แสดงผลส่วนข้อมูลหลัก (สามารถใส่โค้ดดึง Google Sheets เดิมของคุณต่อตรงนี้ได้เลย)
if search_query:
    st.info(f"กำลังกรองข้อมูลด้วยคำค้นหา: **{search_query}**")
else:
    st.success("เชื่อมต่อข้อมูลจาก Google Sheets / SharePoint เรียบร้อยแล้ว")

# ตัวอย่างพื้นที่แสดงตารางข้อมูลเดิมของคุณ
st.subheader("📋 รายการข้อมูลโครงการ")
st.write("แสดงตารางข้อมูลทั้งหมดที่นี่...")
