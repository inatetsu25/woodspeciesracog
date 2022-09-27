import tensorflow as tf
import streamlit as st
from backend import member

# モデルを読み込む関数
# @st.casheで再読み込みにかかる時間を減らす。
@st.cache(allow_output_mutation=True)
def model_load():
    model = tf.keras.models.load_model('./my_model.h5')
    return model

# 顔画像が誰なのか予測値を上位3人まで返す関数
def predict_name(image):

    # モデルを読み込んで予測値を出す(予測値はラベルでなく確率で出力される）
    model = model_load()
    pred_value = model.predict(image)

    sum_pred_value = 0
    for index in range(100):
        sum_pred_value += pred_value[index][:]

    result = []
    top = 3
    max_index = sum_pred_value.argsort()[::-1][:top]
    for i in range(top):
        result.append([member.member(max_index[i],max_index[i]+1)[0],round(sum_pred_value[max_index[i]],1)])
    return result