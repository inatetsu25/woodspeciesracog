# 参考リンク
# メイン https://qiita.com/okateru/items/6f9daf1094ef8c2d6d68
# PIL→opencv変換 https://qiita.com/derodero24/items/f22c22b22451609908ee
# 仮想環境 https://qiita.com/fiftystorm36/items/b2fd47cf32c7694adc2e
# モジュールのインストール https://note.nkmk.me/python-pip-install-requirements/

# ライブラリのインポート
import streamlit as st
from PIL import Image

from backend import predict, preprocess

# タイトル
st.title('木検索アプリ')

# サイドバー
st.sidebar.title('さっそく検索する')
st.sidebar.write('①画像をアップロード')
st.sidebar.write('②識別結果が右に表示されます。')
st.sidebar.write('--------------')
uploaded_file = st.sidebar.file_uploader("画像をアップロードしてください。", type=['JPG','jpg','jpeg', 'png'])

# 以下ファイルがアップロードされた時の処理
if uploaded_file is not None:
    progress_message = st.empty()
    progress_message.write('識別中です。お待ちください。')

    img = Image.open(uploaded_file)

    patches = preprocess.preprocess(img)
    # 各画像や、ラベル、確率を格納する空のリストを定義しておく
    results = predict.predict_name(patches)
    
    st.header('分析結果詳細')

    for result in results:
        if result[1] > 0:
            st.write(result[0], 'の可能性:' , round(result[1],2), '%')
        else:
            pass
    st.image(img, caption='画像',use_column_width=True)



    # ここまで処理が終わったら分析が終わったことを示すメッセージを表示
    # progress_message.write(f'{len(face_img_list)}人の顔を検出しました!')