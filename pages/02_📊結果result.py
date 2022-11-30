import streamlit as st
from PIL import Image
import pandas as pd

favicon = Image.open("名大.png")
st.set_page_config(
     page_title="日本産広葉樹判別アプリ",
     page_icon=favicon,
 )

st.title('木検索アプリ')
st.header('結果一覧')

file_path = "./result.csv"
db_df = pd.read_csv(file_path)

st.write(db_df)