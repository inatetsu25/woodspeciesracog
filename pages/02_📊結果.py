import streamlit as st
from backend import db
from PIL import Image

favicon = Image.open("名大.png")
st.set_page_config(
     page_title="日本産広葉樹判別アプリ",
     page_icon=favicon,
 )

st.title('木検索アプリ')
st.header('結果一覧')

db_df = db.select_data()
st.write(db_df)
