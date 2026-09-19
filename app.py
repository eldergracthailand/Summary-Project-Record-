import pandas as pd
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Permatech Asia - Summary Project Record",
    page_icon="🏢",
    layout="wide"
)

# --- 🔒 ระบบรหัสผ่านเดิม (Password Protection) ---
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

# --- แถบด้านข้าง (Sidebar) คงตราบริษัทและปุ่มออกจากระบบไว้ ---
with st.sidebar:
    st.markdown("### 🏢 Permatech Asia")
    st.markdown("<p style='color: gray; font-size: 13px; margin-top: -15px;'>Summary Project Record</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ช่องค้นหาข้อมูลที่ Sidebar
    st.markdown("### 🔍 ค้นหาข้อมูล")
    search_query = st.text_input("พิมพ์คำค้นหา...", placeholder="ชื่อโครงการ, รหัส...")

    st.markdown("---")
    if st.button("ออกจากระบบ", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- เนื้อหาหลักของเว็บไซต์ (เอาแถบแจ้งเตือนสีเขียวออกเรียบร้อย) ---
st.markdown("<h1 style='color: #1e3a8a;'>📊 Summary Project Record</h1>", unsafe_allow_html=True)
st.markdown("ระบบติดตามและสรุปข้อมูลโครงการภายในบริษัท Permatech Asia")
st.markdown("---")

# พื้นที่แสดงตารางข้อมูล (ไม่มีข้อความแจ้งเตือนกวนใจ)
st.subheader("📋 รายการข้อมูลโครงการ")
if search_query:
    st.write(f"กำลังกรองข้อมูลด้วยคำค้นหา: **{search_query}**")
else:
    st.write("แสดงตารางข้อมูลทั้งหมดที่นี่...")
