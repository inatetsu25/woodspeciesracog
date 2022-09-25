# 参考リンク
# メイン https://qiita.com/okateru/items/6f9daf1094ef8c2d6d68
# メイン https://streamlit.io/
# PIL→opencv変換 https://qiita.com/derodero24/items/f22c22b22451609908ee
# 仮想環境 https://qiita.com/fiftystorm36/items/b2fd47cf32c7694adc2e
# モジュールのインストール https://note.nkmk.me/python-pip-install-requirements/
# 画像の保存 https://zenn.dev/ohtaman/articles/streamlit_tips
# pythonとdropboxの接続 https://zerofromlight.com/blogs/detail/122/
# dropboxのアクセストークン取得方法 https://zerofromlight.com/blogs/detail/121/

# ライブラリのインポート
import streamlit as st
from PIL import Image
import os
import dropbox

from backend import predict, preprocess

import pandas as pd

DATA_URL = ('Book1.csv')
DATE_COLUMN = '樹種'


def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data


favicon = Image.open("名大.png")
st.set_page_config(
     page_title="日本産広葉樹判別アプリ",
     page_icon=favicon,
 )

# タイトル
st.title('木検索アプリ')
data = load_data(10000)
st.write(data)
# サイドバー
st.sidebar.title('さっそく検索する')
species_name=st.sidebar.text_input('①種名を入力', value="nodata", help="例 スギ")
st.sidebar.write('②画像をアップロード')
st.sidebar.write('③識別結果が右に表示されます。')
st.sidebar.write('--------------')
uploaded_file = st.sidebar.file_uploader("画像をアップロードしてください。", type=['jpg','jpeg', 'png'])
dbx = dropbox.Dropbox('ここにアクセストークンを入れる')
# 以下ファイルがアップロードされた時の処理
if uploaded_file is not None:
    progress_message = st.empty()
    progress_message.write('識別中です。お待ちください。')
    bar = st.progress(0)

    # 画像を保存する
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())
    dbx.files_upload(open(uploaded_file.name, 'rb').read(), '/'+species_name+uploaded_file.name)
    os.remove(uploaded_file.name)
        

    img = Image.open(uploaded_file)

    patches = preprocess.preprocess(img)
    # 各画像や、ラベル、確率を格納する空のリストを定義しておく
    results = predict.predict_name(patches)
    
    st.subheader('分析結果詳細')
    for i,result in enumerate(results):
        bar.progress(i/2)
        if result[1] > 0:
            st.write(result[0], 'の可能性:' , round(result[1],2), '%')
        else:
            pass
    st.image(img, caption='画像',use_column_width=True)
    bar.empty()

    # ここまで処理が終わったら分析が終わったことを示すメッセージを表示
    progress_message.write(f'{results[0][0]}です!')