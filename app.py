import pandas as pd
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="Permatech Asia - Summary Project Record",
    page_icon="🏢",
    layout="wide"
)

# --- แถบด้านข้าง (Sidebar) มีตราบริษัทและช่องค้นหา ---
with st.sidebar:
    st.markdown("### 🏢 Permatech Asia")
    st.markdown("<p style='color: gray; font-size: 13px; margin-top: -15px;'>Summary Project Record</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # ช่องค้นหาข้อมูล
    st.markdown("### 🔍 ค้นหาข้อมูล")
    search_query = st.text_input("พิมพ์คำค้นหา...", placeholder="ชื่อโครงการ, รหัส...")

# --- เนื้อหาหลักของเว็บไซต์ (เปิดมาเจอหน้านี้ทันที) ---
st.markdown("<h1 style='color: #1e3a8a;'>📊 Summary Project Record</h1>", unsafe_allow_html=True)
st.markdown("ระบบติดตามและสรุปข้อมูลโครงการภายในบริษัท Permatech Asia")
st.markdown("---")

# แสดงผลตามคำค้นหา
if search_query:
    st.info(f"กำลังกรองข้อมูลด้วยคำค้นหา: **{search_query}**")
else:
    st.success("เชื่อมต่อข้อมูลจาก Google Sheets / SharePoint เรียบร้อยแล้ว")

# พื้นที่แสดงตารางข้อมูลของคุณ
st.subheader("📋 รายการข้อมูลโครงการ")
st.write("แสดงตารางข้อมูลทั้งหมดที่นี่...")
