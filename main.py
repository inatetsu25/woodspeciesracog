# 参考リンク　
# メイン　https://qiita.com/okateru/items/6f9daf1094ef8c2d6d68
# PIL→opencv変換 https://qiita.com/derodero24/items/f22c22b22451609908ee

# ライブラリのインポート
import streamlit as st
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import cv2
import io
import os
import json
import tensorflow as tf
# from azure.cognitiveservices.vision.face import FaceClient
# from msrest.authentication import CognitiveServicesCredentials

# タイトル
st.title('櫻坂46メンバー顔認識アプリ')

# サイドバー
st.sidebar.title('さっそく顔認識をする')
st.sidebar.write('①画像をアップロード')
st.sidebar.write('②識別結果が右に表示されます。')
st.sidebar.write('--------------')
uploaded_file = st.sidebar.file_uploader("画像をアップロードしてください。", type=['JPG','jpg','jpeg', 'png'])

# Face APIの各種設定
# jsonファイルを読み込む
# with open('secret.json') as f:
#   secret_json = json.load(f)

# subscription_key = secret_json['AZURE_KEY'] # AzureのAPIキー
# endpoint = secret_json['AZURE_URL'] # AzureのAPIエンドポイント

# # キーが無ければ強制終了
# assert subscription_key

# # クライアントの認証
# face_client = FaceClient(endpoint, CognitiveServicesCredentials(subscription_key))

# メンバーリスト
members = ['上村莉菜', '尾関梨香', '小池美波', '小林由依', '齋藤冬優花', '菅井友香', '土生瑞穂',
            '原田葵', '守屋茜', '渡辺梨加', '渡邉理佐', '井上梨名', '遠藤光莉', '大園玲', '大沼晶保',
            '幸阪茉里乃', '関有美子', '武元唯衣', '田村保乃', '藤吉夏鈴', '増本綺良',
            '松田里奈', '森田ひかる', '守屋麗奈', '山﨑天']


# 各関数の定義
# モデルを読み込む関数
# @st.casheで再読み込みにかかる時間を減らす。
@st.cache(allow_output_mutation=True)
def model_load():
    model = tf.keras.models.load_model('./my_model.h5')
    return model

# 顔の位置を囲む長方形の座標を取得する関数
# def get_rectangle(faceDictionary):
#     rect = faceDictionary.face_rectangle
#     left = rect.left
#     top = rect.top
#     right = left + rect.width
#     bottom = top + rect.height
#     return ((left, top), (right, bottom))

# 画像に書き込むテキスト内容を取得する関数
# def get_draw_text(faceDictionary):
#     rect = faceDictionary.face_rectangle

#     # メンバーの名前 / 89.2％のように表示する
#     text = first[0] + ' / ' + str(round(first[1]*100,1)) + '%'

#     # 枠に合わせてフォントサイズを調整
#     font_size = max(30, int(rect.width / len(text)))
#     font = ImageFont.truetype('SourceHanSans-VF.ttf', font_size)
#     return (text, font)

# # テキストを描く位置を取得する関数
# def get_text_rectangle(faceDictionary, text, font):
#     rect = faceDictionary.face_rectangle
#     text_width, text_height = font.getsize(text)

#     # ちょうど囲った長方形の上に来るように位置を取得
#     left = rect.left + rect.width / 2 - text_width / 2
#     top = rect.top - text_height - 1
#     return (left, top)

# # 画像にテキストを描画する関数
# def draw_text(faceDictionary):
#     text, font = get_draw_text(faceDictionary)
#     text_rect = get_text_rectangle(faceDictionary, text, font)
#     draw.text(text_rect, text, align='center', font=font, fill='red')

# 顔部分だけの画像を作る関数
# def make_face_image(faceDictionary):
#     rect = faceDictionary.face_rectangle
#     left = rect.left
#     top = rect.top
#     right = left + rect.width
#     bottom = top + rect.height
#     image = np.asarray(img)

#     # 取得した長方形の座標を使って画像データを切り抜き
#     face_image = image[top:bottom, left:right]

#     # np.resizeだと画像が潰れちゃうのでcv2で読み取る
#     cv2_img = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)

#     # cv2はカラー画像をBGRの順番で読み取ってしまうのでアンパックで色要素を分けて代入
#     b,g,r = cv2.split(cv2_img)

#     # RGBの順番になるようにマージ（正しいカラー画像）
#     face_image_color = cv2.merge([r,g,b])

#     # モデルの学習を(128,128,3)でやってきたので縦横のサイズを128に揃える
#     resized_image = cv2.resize(face_image_color, (64, 64))
#     return resized_image

# 顔画像が誰なのか予測値を上位3人まで返す関数
def predict_name(image):
    # resized_image = cv2.resize(image, (64, 64))
    # # 四次元配列じゃないとモデルが読み取ってくれない
    # img = resized_image.reshape(1, 64, 64, 1)

    # # テストデータも正規化を忘れない
    # img = img / 255

    # モデルを読み込んで予測値を出す(予測値はラベルでなく確率で出力される）
    model = model_load()
    pred = model.predict(image)

    top = 1

    # argsort()で確率値の小さい（可能性が低い）順に並べ、その値と対応するラベルを返す
    # その[-3:]だから終わり3つ（つまり可能性が高い上位3人のラベルを取る）
    # そのままだと[3位,2位,1位]となって扱いづらいので[::-1]にして逆向きにする
    top_indices = pred.argsort()[0][::-1][-top:]
    acc=np.max(pred)
    # top_indices = pred.argsort()[-top:][::-1]
    # メンバーの名前と確率をセットにしたリストを作って、上位3人分を返す
    result = [[members[top_indices[0]], acc]]
    return result[0]
    # return result[0], result[1], result[2]

def pil2cv(image):
#    ''' PIL型 -> OpenCV型 '''
        new_image = np.array(image, dtype=np.uint8)
        if new_image.ndim == 2:  # モノクロ
            pass
        elif new_image.shape[2] == 3:  # カラー
            new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
        elif new_image.shape[2] == 4:  # 透過
            new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
        return new_image

# 以下ファイルがアップロードされた時の処理
if uploaded_file is not None:
    progress_message = st.empty()
    progress_message.write('顔を識別中です。お待ちください。')
    # アップロードされた画像データをFaceAPIが認識できる形にする（バイナリデータ）
    # stream = io.BytesIO(uploaded_file.getvalue())
    
    # detected_faces = face_client.face.detect_with_stream(stream)
    # if not detected_faces:
    #     raise Warning('画像から顔を検出できませんでした。')

    img = Image.open(uploaded_file)
    draw = ImageDraw.Draw(img)
    img_array = np.array(img)
    # st.image(img_array,caption = 'サムネイル画像',use_column_width = True)
    im = pil2cv(img)
    # im = cv2.imread(uploaded_file)
    im=0.299*im[:,:,2]+0.587*im[:,:,1]+0.114*im[:,:,0]
    im=np.expand_dims(im,axis=2)
    im=im[:,:]
    resized_image = cv2.resize(im, (64, 64))
    resized_image = resized_image.reshape(1, 64, 64, 1)


    # 各画像や、ラベル、確率を格納する空のリストを定義しておく
    face_img_list = []

    first_name_list = []
    second_name_list = []
    third_name_list = []

    first_rate_list = []
    second_rate_list = []
    third_rate_list = []

    # 認識された顔の数だけ以下の処理を行う
    # for face in detected_faces:

    #     # モデルに読み込めるよう(128,128,3)の大きさの顔画像を作る
    #     face_img = make_face_image(face)

    #     # これも表示させたいので、一旦リストに格納
    #     face_img_list.append(face_img)

    #     # 予測したメンバーの名前上位3人をアンパックで代入
    #     first, second, third = predict_name(face_img)

    #     # 上位3人の名前とその確率をリストに格納する
    #     first_name_list.append(first[0])
    #     first_rate_list.append(first[1])

    #     second_name_list.append(second[0])
    #     second_rate_list.append(second[1])

    #     third_name_list.append(third[0])
    #     third_rate_list.append(third[1])

    #     # 元の画像の顔部分を長方形で囲んで、1番可能性が高い名前とその確率を表示
    #     draw.rectangle(get_rectangle(face), outline='red', width=5)
    #     draw_text(face)

    # face_img = make_face_image(uploaded_file)

    # これも表示させたいので、一旦リストに格納
    # face_img_list.append(face_img)

    # 予測したメンバーの名前上位3人をアンパックで代入
    # first, second, third = predict_name(face_img)
    first = predict_name(resized_image)

    # 上位3人の名前とその確率をリストに格納する
    first_name_list.append(first[0])
    first_rate_list.append(first[1])

    # second_name_list.append(second[0])
    # second_rate_list.append(second[1])

    # third_name_list.append(third[0])
    # third_rate_list.append(third[1])

    # # 元の画像の顔部分を長方形で囲んで、1番可能性が高い名前とその確率を表示
    # draw.rectangle(get_rectangle(face), outline='red', width=5)
    # raw_text(face)
    
    # 元の画像に長方形と名前が書かれているので、それを表示
    # st.image(img, use_column_width=True)

    # カラムを2列に分ける
    # ※st.beta_columns()じゃないとローカル環境では動かないです。
    # ただ本番環境にデプロイするとそれじゃ古すぎる、新しいのに変更しましょうといったアラートが 
    # 出てきたので完成版のコードはst.columns()とこの後のst.expander()にしている
    # col1, col2 = st.columns(2)
    
    # カラム1には検出した顔画像の切り抜きと名前を縦に並べて表示
    # with col1:
    #     for i in range(0, len(face_img_list)):
    #         st.header(f'{i+1}人目:{first_name_list[i]}')
    #         st.image(face_img_list[i], width = 128)

    # カラム2には、認識された顔の数だけ上位3人のラベルと確率を表示
    # st.expanderで見たい時にクリックすれば現れるエキスパンダの中に入れる
    # with col2:
    #     st.header('分析結果詳細')
    #     for i in range(0, len(face_img_list)):
    #         with st.expander(f'{i+1}人目の詳細を表示'):
    #             st.write(first_name_list[i], 'の可能性:' , round(first_rate_list[i]*100,2), '%')
    #             st.write(second_name_list[i], 'の可能性:' , round(second_rate_list[i]*100,2), '%')
    #             st.write(third_name_list[i], 'の可能性:' , round(third_rate_list[i]*100,2), '%')
    st.header('分析結果詳細')
    st.write(first_name_list[0], 'の可能性:' , round(first_rate_list[0]*100,2), '%')


    # ここまで処理が終わったら分析が終わったことを示すメッセージを表示
    # progress_message.write(f'{len(face_img_list)}人の顔を検出しました!')