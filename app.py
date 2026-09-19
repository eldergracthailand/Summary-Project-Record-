import pandas as pd
import streamlit as st

# ตั้งค่าหน้าเว็บให้เป็นแบบ Wide และกำหนดชื่อหัวข้อเบราว์เซอร์
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

# --- ดีไซน์ Sidebar (แถบด้านข้าง) ---
with st.sidebar:
    # ใช้หัวข้อและไอคอนแทนรูปภาพ เพื่อป้องกันภาพดำเสีย
    st.markdown("### 🏢 Permatech Asia")
    st.markdown("<p style='color: gray; font-size: 13px; margin-top: -15px;'>Summary Project Record</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 📌 เมนูการใช้งาน")
    menu = st.radio("เลือกมุมมอง:", ["📊 Dashboard ภาพรวม", "📋 รายการโปรเจกต์"])
    
    st.markdown("---")
    
    # 🔍 นำช่องค้นหากลับมาไว้ที่ Sidebar ตามเดิมเพื่อให้ใช้งานง่าย
    st.markdown("### 🔍 ค้นหาข้อมูล")
    search_query = st.text_input("พิมพ์คำค้นหา...", placeholder="ชื่อโครงการ, รหัส...")

    st.markdown("---")
    if st.button("ออกจากระบบ", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- เนื้อหาหลักของเว็บไซต์ ---
st.markdown("<h1 style='color: #1e3a8a;'>📊 Summary Project Record</h1>", unsafe_allow_html=True)
st.markdown("ระบบติดตามและสรุปข้อมูลโครงการภายในบริษัท Permatech Asia")

# ตัวอย่างการแสดงผลตามเมนู
if menu == "📊 Dashboard ภาพรวม":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="โครงการทั้งหมด", value="12 โครงการ", delta="+2 จากเดือนก่อน")
    with col2:
        st.metric(label="กำลังดำเนินการ", value="8 โครงการ", delta="ปกติ")
    with col3:
        st.metric(label="เสร็จสิ้นแล้ว", value="4 โครงการ", delta="100%")
    
    st.markdown("---")
    if search_query:
        st.info(f"🔍 ผลการค้นหาสำหรับ: **'{search_query}'**")
    else:
        st.info("💡 เลือกเมนูด้านข้างหรือใช้ช่องค้นหาเพื่อดูข้อมูลรายละเอียดโครงการ")

else:
    st.subheader("📋 รายการข้อมูลโครงการทั้งหมด")
    if search_query:
        st.write(f"กำลังกรองข้อมูลด้วยคำค้นหา: **{search_query}**")
    else:
        st.write("แสดงข้อมูลจาก Google Sheets / SharePoint ที่เชื่อมต่อไว้")
