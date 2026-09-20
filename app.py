หมายถึง ให้นำโค้ดชุดเชื่อมต่อข้อมูลใหม่ไปวางแทนที่ส่วนดึงข้อมูลเดิมในไฟล์ app.py ครับ เพื่อให้โค้ดวิ่งไปดึงลิงก์ความลับจาก st.secrets["SHEET_URL"] ที่เราเพิ่งบันทึกไว้ในหน้าเว็บเมื่อสักครู่นี้ครับ
เพื่อให้เห็นภาพชัดเจนและนำไปวางแทนที่ได้ทันที นี่คือ โค้ดฉบับเต็มทั้งหมดของไฟล์ app.py ที่จัดการทุกอย่างให้เรียบร้อยแล้ว (ทั้งหน้าใส่รหัสผ่าน PMA, แถบ Permatech Asia, ช่องค้นหา, และระบบดึงข้อมูลผ่าน st.secrets):
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

# --- 📌 ดึงข้อมูลจาก Google Sheets ผ่าน Secrets (ปลอดภัย ไม่โชว์ลิงก์ในโค้ด) ---
try:
    sheet_url = st.secrets["SHEET_URL"]
    
    @st.cache_data(ttl=10)
    def load_data(url):
        return pd.read_csv(url)

    df = load_data(sheet_url)
except Exception as e:
    df = pd.DataFrame()
    st.warning("⚠️ กำลังรอการตั้งค่าลิงก์ใน Secrets หรือไม่สามารถเชื่อมต่อข้อมูลได้")

# --- ระบบตรวจสอบและแสดงผลตาราง ---
if df.empty:
    st.info("💡 กรุณาตรวจสอบว่าได้บันทึก `SHEET_URL` ในเมนู Settings -> Secrets บน Streamlit เรียบร้อยแล้วหรือยัง")
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

วิธีทำ: ให้คุณ ลบโค้ดเก่าทั้งหมดในไฟล์ app.py ทิ้ง แล้วคัดลอกโค้ดชุดนี้ไปวางแทนที่ทั้งหมด กดบันทึก แล้วรีเฟรชหน้าเว็บแอปพลิเคชันดูได้เลยครับ ข้อมูลจะดึงขึ้นมาแสดงผลโดยที่ลิงก์ถูกซ่อนไว้อย่างปลอดภัยแน่นอนครับ!
