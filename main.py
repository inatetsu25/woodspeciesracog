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
import datetime
import sqlite3

from backend import predict, preprocess, member

import pandas as pd

def select_data():
    con = sqlite3.connect('./sample.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS TEST(time text,name text)")
    cur.execute("SELECT * FROM TEST")
    for row in cur:
        print(str(row[0]) + "," + str(row[1]))
    con.close()


def insert_data(time,name):
    con = sqlite3.connect('./sample.db')
    cur = con.cursor()
    sql = 'INSERT INTO TEST (time, name) values (?,?)'
    data = [str(time), name]
    cur.execute(sql, data)
    con.commit()
    con.close()

favicon = Image.open("名大.png")
st.set_page_config(
     page_title="日本産広葉樹判別アプリ",
     page_icon=favicon,
 )

# タイトル
st.title('木検索アプリ')

member10 = member.member10(0,10)
member50 = member.member(0,50)
df_member10 = pd.DataFrame(member10,columns=['樹種'])
df_member50 = pd.DataFrame(member50,columns=['樹種'])

col1, col2 = st.columns(2)

with col1:
   st.header("10種一覧")
   st.write(df_member10)

with col2:
   st.header("50種一覧")
   st.write(df_member50)

# サイドバー
st.sidebar.title('さっそく検索する')
species_name=st.sidebar.text_input('①種名を入力', value="nodata", help="例 スギ")
st.sidebar.write('②画像をアップロード')
st.sidebar.write('③識別結果が右に表示されます。')
st.sidebar.write('--------------')
uploaded_file = st.sidebar.file_uploader("画像をアップロードしてください。", type=['jpg','jpeg', 'png'])
# dbx = dropbox.Dropbox('sl.BSx6TXgsl_JhP4aMDT6BhtzcXerYwry__r2GCNqPzPB4zEpziL4TBRrXzlFS9Cf-cK1nRf7vyggHxhz0Ap05FZyeeCjWy6AxWejb2sRaoAvrsNQCgDIt6v1S_RE6BX-y7kvrkkg')
# 以下ファイルがアップロードされた時の処理
if uploaded_file is not None:
    progress_message = st.empty()
    progress_message.write('識別中です。お待ちください。')
    bar = st.progress(0)
    dt = datetime.datetime.today()
    date = dt.date()
    time = dt.time()
    format = uploaded_file.type.split('/', 1)[-1]

    # 画像を保存する
    # with open(uploaded_file.name, 'wb') as f:
    #     f.write(uploaded_file.read())
    # dbx.files_upload(open(uploaded_file.name, 'rb').read(), '/'+"img_"+str(date)+'_'+str(time)+'_'+species_name+'.'+format)
    # os.remove(uploaded_file.name)
        

    img = Image.open(uploaded_file)

    print("INSERT前")
    select_data()

    # INSERT 処理
    name='yamabousi'
    insert_data(time,name)

    print("INSERT後")
    select_data()

    # patches = preprocess.preprocess(img)
    # # 各画像や、ラベル、確率を格納する空のリストを定義しておく
    # results10,results50 = predict.predict_name(patches)
    
    st.header('分析結果詳細')
    st.subheader('50種モデルの結果')
    for i,result in enumerate(results50):
        bar.progress(i/2)
        if result[1] > 0:
            st.write(result[0], 'の可能性:' , round(result[1],2), '%')
        else:
            pass
    st.subheader('10種モデルの結果')
    for i,result in enumerate(results10):
        bar.progress(i/2)
        if result[1] > 0:
            st.write(result[0], 'の可能性:' , round(result[1],2), '%')
        else:
            pass
    st.image(img, caption='画像',use_column_width=True)
    bar.empty()

    # ここまで処理が終わったら分析が終わったことを示すメッセージを表示
    progress_message.write(f'{results50[0][0]}です!')