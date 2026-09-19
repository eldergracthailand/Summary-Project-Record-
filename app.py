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

# --- 📌 ส่วนดึงข้อมูลและระบบกรองข้อมูล (นำตารางของคุณมาใส่ตรงนี้) ---
# ตัวอย่าง สมมติว่าคุณมี DataFrame ชื่อ df (ให้แทนที่ df ด้วยตัวแปรดึงข้อมูล Google Sheets ของคุณจริง ๆ)
# เช่น df = pd.read_csv("ลิงก์ Google Sheets ของคุณ")
# โค้ดจำลองสำหรับทดสอบ (ให้เปลี่ยนเป็นข้อมูลจริงของคุณ):
data = {
    "No.Job": ["JOB-001", "JOB-002", "JOB-003", "JOB-004"],
    "ชื่อโครงการ": ["ระบบติดตามงาน", "พัฒนาแอปภายใน", "ปรับปรุงระบบฐานข้อมูล", "ติดตั้งอุปกรณ์เน็ตเวิร์ก"],
    "สถานะ": ["กำลังดำเนินการ", "เสร็จสิ้น", "กำลังดำเนินการ", "รอดำเนินการ"]
}
df = pd.DataFrame(data)

# ⚙️ ระบบกรองข้อมูลจากช่องค้นหา
if search_query:
    # แปลงข้อความในตารางและคำค้นหาเป็นตัวพิมพ์เล็กทั้งหมด เพื่อให้ค้นหาง่าย (ไม่ 0 และไม่ต้องสนตัวพิมพ์เล็กใหญ่)
    mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
    filtered_df = df[mask]
else:
    filtered_df = df

# แสดงผลตารางข้อมูล
st.subheader("📋 รายการข้อมูลโครงการ")
st.dataframe(filtered_df, use_container_width=True)
