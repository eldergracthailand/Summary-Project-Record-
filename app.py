import pandas as pd
import streamlit as st

st.set_page_config(page_title="PR Catalog", page_icon="🔍", layout="wide")

# --- ส่วนของการใส่รหัสผ่าน (Password Protection) ผ่าน Secrets ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>🔒 Internal Portal Login</h2>", unsafe_allow_html=True)
    password = st.text_input("กรุณากรอกรหัสผ่านเพื่อเข้าสู่ระบบ:", type="password")
    
    if st.button("เข้าสู่ระบบ", use_container_width=True):
        # ดึงรหัสผ่านจาก st.secrets มาเทียบ (ปลอดภัย ไม่โชว์ในโค้ด)
        correct_password = st.secrets.get("APP_PASSWORD", "PMA") # ถ้าไม่ได้ตั้งใน secrets จะใช้ "PMA" เป็นค่าสำรอง
        
        if password == correct_password:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("รหัสผ่านไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง")
    st.stop()

# --- แถบด้านข้าง (Sidebar) สำหรับออกจากระบบ ---
with st.sidebar:
    st.markdown("### 🏢 เมนูจัดการ")
    if st.button("ออกจากระบบ", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- ส่วนเนื้อหาหลักและระบบค้นหาแคตตาล็อกของคุณ ---
st.title("📚 ระบบค้นหาข้อมูลแคตตาล็อกอุปกรณ์(PR)  ")
st.write("พิมพ์คำค้นหาเพื่อดูข้อมูล PR (ข้อมูลนี้สำหรับค้นหาเท่านั้น)")

# ส่วนดึงข้อมูลจาก Google Sheets ผ่าน Secrets
@st.cache_data(ttl=600)
def load_data():
  sheet_url = st.secrets["SHEET_URL"] # ดึงลิงก์ซีทจาก Secrets
  df = pd.read_csv(sheet_url)
  return df

try:
  df = load_data()

  with st.form(key='search_form'):
    search_query = st.text_input(
        "🔍 ค้นหาข้อมูล (พิมพ์คีย์เวิร์ด เช่น ชื่ออุปกรณ์ โค้ดสินค้าหรือหมวดหมู่):"
    )
    submit_button = st.form_submit_button(label="🔍 ค้นหา")

  if submit_button:
    if search_query.strip() != "":
      mask = (
          df.astype(str)
          .apply(lambda x: x.str.contains(search_query, case=False, na=False))
          .any(axis=1)
      )
      result_df = df[mask]

      st.write(
          f"ผลการค้นหา: พบ {len(result_df)} รายการสำหรับ '{search_query}'"
      )

      if not result_df.empty:
        display_df = result_df.copy()
        if "ลิงก์รูปภาพ" in display_df.columns:
          display_df = display_df.drop(columns=["ลิงก์รูปภาพ"])

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.subheader("🖼️ คลิกเพื่อดูรูปภาพของรายการที่พบ")
        for index, row in result_df.iterrows():
          if (
              "ลิงก์รูปภาพ" in row
              and pd.notna(row["ลิงก์รูปภาพ"])
              and str(row["ลิงก์รูปภาพ"]).strip() != ""
          ):
            item_name = (
                str(row["ชื่อสินค้า"])
                if "ชื่อสินค้า" in row and pd.notna(row["ชื่อสินค้า"])
                else f"รายการที่ {index+1}"
            )
            
            item_code = (
                str(row["รหัสสินค้า"])
                if "รหัสสินค้า" in row and pd.notna(row["รหัสสินค้า"]) and str(row["รหัสสินค้า"]).strip().lower() != "nan"
                else ""
            )
            
            link_url = str(row["ลิงก์รูปภาพ"]).strip()

            if item_code:
              button_label = f"🔗 ดูรูปภาพ: {item_code} - {item_name}"
            else:
              button_label = f"🔗 ดูรูปภาพ: {item_name}"

            st.link_button(button_label, link_url)
      else:
        st.warning("ไม่พบข้อมูลที่ค้นหา")
    else:
      st.warning("กรุณากรอกคำค้นหาก่อนกดปุ่มค้นหา")
  else:
    st.info("กรุณาพิมพ์คำค้นหาแล้วกดปุ่ม 'ค้นหา'")

except Exception as e:
  st.error(
      "ยังไม่ได้ตั้งค่า `SHEET_URL` หรือ `APP_PASSWORD` ใน Streamlit Secrets กรุณาตรวจสอบการตั้งค่า"
  )
