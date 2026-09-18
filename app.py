import pandas as pd
import streamlit as st

st.set_page_config(page_title="Summary Project Record", page_icon="📊", layout="wide")

st.title("📊 ระบบค้นหาข้อมูล Summary Project Record")
st.write("พิมพ์คำค้นหาเพื่อดูข้อมูลโครงการ (ข้อมูลนี้สำหรับค้นหาเท่านั้น)")

# ส่วนดึงข้อมูลจาก Google Sheets (ใช้ลิงก์ CSV ของแผนกนี้)
@st.cache_data(ttl=600)
def load_data():
  sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSTLK92gAXsaK5e9HNDcjPnGkWXNdOTFmojqlq55hMKp-Ak48QNWDcHGRs4fUBWDw/pub?gid=2143365497&single=true&output=csv"
  df = pd.read_csv(sheet_url)
  return df

try:
  df = load_data()

  search_query = st.text_input(
      "🔍 ค้นหาข้อมูล (พิมพ์คีย์เวิร์ด เช่น ชื่อโครงการ, No. Job, หรือชื่อลูกค้า):"
  )

  if search_query:
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
      st.dataframe(result_df, use_container_width=True, hide_index=True)
    else:
      st.warning("ไม่พบข้อมูลที่ค้นหา")
  else:
    st.info("กรุณาพิมพ์คำค้นหาในช่องด้านบน")

except Exception as e:
  st.error("ยังไม่ได้ใส่ลิงก์ Google Sheet หรือลิงก์ยังไม่ถูกต้อง กรุณาตรวจสอบลิงก์")
