# ファイル名：      train_model.py
# 機能：            信号機検出の学習用データを作成し、モデルを学習する
# 処理概要： 
import cv2
import pickle
import glob
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 初期設定
img_size = (128,128)
y = [] # ラベルのリスト（信号機の有無）
x = [] # 特徴量のリスト（画像データ）


# データラベルの作成
# dir: ディレクトリパス、label: ラベル（1 = 信号機あり、0 = 信号機なし）
def make_data(dir, label):
    # 指定されたディレクトリ内のすべてのファイルを読み込む
    files = glob.glob(dir + '/*')
    for f in files:
        # データ整形
        img = cv2.imread(f)
        img = cv2.resize(img, img_size)
        img_data = img.reshape(-1,)
        # ラベルと特徴量をリストに追加
        y.append(label)
        x.append(img_data)

# 信号機ありの画像と信号機なしの画像のデータを作成
make_data('traffic_light',1)
make_data('no_traffic_light',0)

# トレーニング・テストデータに分割
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2)

# ランダムフォレストモデルの学習
clf = RandomForestClassifier()
clf.fit(train_x, train_y)

# 予測
pred_y = clf.predict(test_x)
# 予測精度の評価
print(accuracy_score(test_y, pred_y))


# 学習したモデルを保存
with open('traffic_light.pkl', 'wb')as f:
    pickle.dump(clf,f)