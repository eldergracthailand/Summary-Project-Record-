import streamlit as st

# ตั้งค่าหน้าเว็บให้เป็นแบบ Wide และกำหนดชื่อหัวข้อเบราว์เซอร์
st.set_page_config(
    page_title="Permatech Asia - Summary Project Record",
    page_icon="📊",
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
    # แสดงโลโก้และชื่อบริษัท (สามารถเปลี่ยน URL รูปโลโก้ของคุณได้ตรงนี้)
    st.image("https://i.imgur.com/7k12345.png", width=80) # หรือใช้ไฟล์ภาพโลโก้ของคุณ
    st.markdown("### **Permatech Asia**")
    st.markdown("<p style='color: gray; font-size: 14px;'>Summary Project Record</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 📌 เมนูการใช้งาน")
    menu = st.radio("เลือกมุมมอง:", ["📊 Dashboard ภาพรวม", "📋 ราย100% รายการโปรเจกต์"])
    
    st.markdown("---")
    if st.button("ออกจากระบบ", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- เนื้อหาหลักของเว็บไซต์ ---
st.markdown("<h1 style='color: #1e3a8a;'>📊 Summary Project Record</h1>", unsafe_allow_html=True)
st.markdown("ยินดีต้อนรับเข้าสู่ระบบติดตามและสรุปข้อมูลโครงการภายในของบริษัท Permatech Asia ครับ")

# ตัวอย่างการแบ่งสัดส่วนเนื้อหา
if menu == "📊 Dashboard ภาพรวม":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="โครงการทั้งหมด", value="12 โครงการ", delta="+2 จากเดือนก่อน")
    with col2:
        st.metric(label="กำลังดำเนินการ", value="8 โครงการ", delta="ปกติ")
    with col3:
        st.metric(label="เสร็จสิ้นแล้ว", value="4 โครงการ", delta="100%")
    
    st.markdown("---")
    st.info("💡 **คำแนะนำ:** คุณสามารถดึงข้อมูลอัปเดตล่าสุดจาก Google Sheets หรือจัดการข้อมูลผ่านแถบเมนูด้านข้างได้ทันที")

else:
    st.subheader("📋 รายการข้อมูลโครงการ")
    st.write("(แสดงตารางข้อมูลโครงการจาก Google Sheets ที่นี่...)")
