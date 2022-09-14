# 参考リンク
# メイン https://qiita.com/okateru/items/6f9daf1094ef8c2d6d68
# メイン https://streamlit.io/
# PIL→opencv変換 https://qiita.com/derodero24/items/f22c22b22451609908ee
# 仮想環境 https://qiita.com/fiftystorm36/items/b2fd47cf32c7694adc2e
# モジュールのインストール https://note.nkmk.me/python-pip-install-requirements/
# 画像の保存 https://zenn.dev/ohtaman/articles/streamlit_tips

# ライブラリのインポート
import streamlit as st
from PIL import Image
import os

from backend import predict, preprocess

favicon = Image.open("名大.png")
st.set_page_config(
     page_title="木検索アプリ",
     page_icon=favicon,
 )

# タイトル
st.title('木検索アプリ')

# サイドバー
st.sidebar.title('さっそく検索する')
species_name=st.sidebar.text_input('①種名を入力', value="nodata", help="例 スギ")
st.sidebar.write('②画像をアップロード')
st.sidebar.write('③識別結果が右に表示されます。')
st.sidebar.write('--------------')
uploaded_file = st.sidebar.file_uploader("画像をアップロードしてください。", type=['jpg','jpeg', 'png'])

# 以下ファイルがアップロードされた時の処理
if uploaded_file is not None:
    progress_message = st.empty()
    progress_message.write('識別中です。お待ちください。')
    bar = st.progress(0)

    IMG_PATH = os.path.join('imgs/', species_name)
    if not os.path.exists(IMG_PATH):
        os.mkdir(IMG_PATH)

    img_path = os.path.join(IMG_PATH, uploaded_file.name)
    # 画像を保存する
    with open(img_path, 'wb') as f:
        f.write(uploaded_file.read())
        

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