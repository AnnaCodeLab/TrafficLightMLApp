# ファイル名：      traffic_light_detection.py
# 機能：            画像内の信号機を検出する
# 処理概要：        学習済みモデルを使用して画像から信号機の有無を判定し、結果を返す

import pickle
import cv2


# モデルの読み込み
with open('traffic_light.pkl','rb') as f:
    clf = pickle.load(f)

# 関数名  ：read_files
# 機能    ：ファイルリストから画像を読み込み、信号機の検出を行う
# 処理概要：各画像ファイルに対して信号機の検出を実行し、結果をリストで返す
def read_files(files):
    detect_list = []

    for f in files:
        detect_list.append(detect_traffic_light(f))
    return detect_list

# 関数名  ：detect_traffic_light
# 機能    ：画像内の信号機を検出する
# 処理概要：画像を読み込み、リサイズしてからモデルで予測し、結果に応じて信号機の有無を返す
def detect_traffic_light(fname):
    img = cv2.imread(fname)
    if not img is None:
        # データを整形
        img_data = cv2.resize(img,(128,128))
        img_data = img_data.reshape(-1,)

        # 予測
        pred_y = clf.predict([img_data])

        if pred_y == 1:
            # 信号機と認識された場合
            return 1
        else:
            # 信号機でない場合
            return 0
    else:
        return None # 画像が読み込めなかった場合
