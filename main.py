# ファイル名：      main.py
# 機能：            tkinterを用いたGUIアプリケーション。ユーザーが9つの(信号機あり・なし)画像を選択し、選択した画像をAIモデルで判定する。
# 処理概要：        1. 初期画面としてロゴ画面を表示し、その後画像選択画面に自動的に遷移。
#                  2. 画像選択画面で9つの画像を選び、選択した画像をフレーム内に表示。
#                  3. 選択した画像を確認後、AIによる判定を行う画面へ移動。
#                  4. AI判定では、指定された9枚の画像に対して、どの画像が信号機ありかを判定。
#                  5. 判定結果に基づいて画像の枠の色を変更し、再選択またはリセットが可能。

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import random
from traffic_light_detection import read_files

# クラス名：Application
# 機能    ：アプリケーションの初期設定を行う
# 処理概要：ウィンドウ設定、フレームクラスの初期化、最初の画面を表示
class Application(Tk):
    def __init__(self):
        super().__init__()
        # ウィンドウの基本設定
        self.title("ピックピクチャー")
        self.logo = PhotoImage(file='img/bot.png')
        self.iconphoto(True, self.logo)
        self.resizable(0, 0)
        self.geometry("500x720+20+20")

        # 変数の初期化
        self.frames = {}
        self.selected_img_paths = []
        self.frame_classes = {
            'LogoScreen': LogoScreen,
            'SelectImageScreen': SelectImageScreen,
            'MainScreen': MainScreen
        }

        # 行と列の重みを設定してフレームを自動調整
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 最初の画面を表示
        self.show_frame('LogoScreen')

    # 関数名  ：show_frame
    # 機能    ：指定されたフレームを表示する
    # 処理概要：指定されたフレームを表示し、フレームが存在しない場合は作成して表示する
    def show_frame(self, page_name):
        if page_name not in self.frame_classes:
            raise ValueError(f"Unknown page: {page_name}")

        self.frames.clear()  # フレームのリセット

        # フレームがまだ作成されていない場合、作成して表示
        if page_name not in self.frames:
            frame_class = self.frame_classes[page_name]
            frame = frame_class(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        frame = self.frames[page_name]
        frame.tkraise()  # フレームを前面に表示


# クラス名：LogoScreen
# 機能   ：ロゴ画面を表示する
# 処理概要：ロゴとタイトルを表示し、一定時間後に次の画面に自動遷移する
class LogoScreen(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg='#FFFFFF')
        self.logo = PhotoImage(file='img/botL.png')
        self.logo_title = PhotoImage(file='img\pickpicture.png')

        # ロゴとタイトルを表示
        Label(self, image=self.logo, bg='white').pack(pady=(200, 0))
        Label(self, image=self.logo_title, bg='white').pack()

        # 1.2秒後に次の画面へ自動的に遷移
        self.after(1200, lambda: self.controller.show_frame(
            'SelectImageScreen'))


# クラス名：SelectImageScreen
# 機能    ：ユーザーが9枚の画像を選択できる画面を表示する
# 処理概要：画像選択ボタンを提供し、選択した画像をフレーム内に3x3のグリッドで表示する
class SelectImageScreen(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg='#FFFFFF')
        self.choose_img_title = PhotoImage(file='img/choose_img_title.png')
        self.choose_img_btn = PhotoImage(file='img/choose_img_btn.png')
        self.confirm_lb_icon = PhotoImage(file='img/confirm_img_label.png')
        self.confirm_btn_icon = PhotoImage(file='img/confirm_btn.png')
        self.iie_btn_icon = PhotoImage(file='img/iie_btn.png')

        # タイトル
        Label(self, image=self.choose_img_title, bd=0, bg='white',
              activebackground='white').pack(anchor='w', pady=30, padx=20)

        # 画像表示用のフレームを作成
        self.frame = Frame(self, bg='white', width=310, height=350, relief='solid',
                           highlightthickness=3, highlightbackground='#EEEDEB', pady=20, padx=20)
        self.frame.pack(fill=X, pady=20, padx=20)

        # グリッドの設定
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)

        # 画像選択ボタン
        self.choose_img = Button(self, image=self.choose_img_btn, bd=0,
                                 bg='white', activebackground='white', command=self.get_img)
        self.choose_img.pack()

    # 関数名 ：get_img
    # 機能   ：ファイルダイアログでユーザーが画像を選択する
    # 処理概要：ファイルダイアログを開き、ユーザーが選択した画像をリストに格納し、表示する準備をする
    def get_img(self):
        # ファイルダイアログで画像を選択
        files = filedialog.askopenfilenames(title='画像選択', initialdir='sample_dir', filetypes=[
                                            ('all file', '*.*'), ('png file', '*.png'), ('jpg file', '*.jpg')])
        files = list(files)   # リストに変換
        random.shuffle(files)  # ファイルリストをランダムにシャッフル
        if files:
            self.show_img(files)

    # 関数名  ：show_img
    # 機能    ：選択された画像をフレーム内に表示する
    # 処理概要：選択された画像を3x3のグリッドに配置して表示し、確認・リセットボタンを追加する
    def show_img(self, files):
        if len(files) == 9:  # 9つの画像が選択されているか確認
            self.controller.selected_img_paths = files

            # ウイジェットを削除
            self.choose_img.destroy()

            # 選択された画像をフレーム内に表示
            for i, img_path in enumerate(files):
                img = Image.open(img_path)
                img = img.resize((100, 100), Image.LANCZOS)  # 画像をリサイズ
                photo = ImageTk.PhotoImage(img)
                lb = Label(self.frame, image=photo, bg='white')
                lb.image = photo
                # 3x3のグリッドに配置
                row = i // 3
                column = i % 3
                lb.grid(row=row, column=column, sticky='nsew')

            # 確認ボタンを作成
            self.confirm_lb = Label(
                self, image=self.confirm_lb_icon, bd=0, bg='white', activebackground='white')
            self.confirm_lb.pack(padx=(10, 0))
            self.confirm_btn = Button(self, image=self.confirm_btn_icon, bd=0, bg='white',
                                      activebackground='white', command=lambda: self.controller.show_frame('MainScreen'))
            self.confirm_btn.pack(side='left', padx=(80, 0))
            self.reset_btn = Button(self, image=self.iie_btn_icon, bd=0,
                                    bg='white', activebackground='white', command=self.reset)
            self.reset_btn.pack(side='right', padx=(0, 80))

        else:
            messagebox.askokcancel(
                title='画像選択', message='９枚の画像を選んでください。', icon='error')
            # print('choose 9 pic pls')

    # 関数名  ：reset
    # 機能    ：選択された画像をリセットし、再選択可能にする
    # 処理概要：現在のウィジェットを全て削除し、画像選択ボタンを再度表示
    def reset(self):
        self.confirm_lb.destroy()
        self.confirm_btn.destroy()
        self.reset_btn.destroy()
        widgets = self.frame.winfo_children()
        for w in widgets:
            w.destroy()
        self.choose_img = Button(self, image=self.choose_img_btn, bd=0,
                                 bg='white', activebackground='white', command=self.get_img)
        self.choose_img.pack()

# クラス名 ：MainScreen
# 機能    ：選択された画像をAIが判定する画面を表示
# 処理概要：ユーザーが選択した画像を表示し、AI判定を行うボタンを提供


class MainScreen(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(bg='#FFFFFF')

        # アイコン画像の読み込み
        self.refresh_icon = PhotoImage(file='img/refresh.png')
        self.ai_select_title = PhotoImage(file='img/ai_select_title.png')

        # タイトル
        Label(self, image=self.ai_select_title, bd=0, bg='white',
              activebackground='white').pack(anchor='w', pady=30, padx=20)

        # 上部フレーム - 画像表示用のフレーム
        self.top_frame = Frame(self, bg='white', width=350, height=320, relief='solid',
                               highlightthickness=3, highlightbackground='#EEEDEB', pady=20, padx=20)
        self.top_frame.pack(fill=X, pady=20, padx=20)

        # 3x3のグリッド配置
        self.top_frame.grid_rowconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(1, weight=1)
        self.top_frame.grid_rowconfigure(2, weight=1)
        self.top_frame.grid_rowconfigure(3, weight=1)
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(2, weight=1)

        # 下部フレーム（選択結果）の作成
        self.bottom_frame = Frame(self, bg='white', height=70)
        self.bottom_frame.pack(side=BOTTOM, fill=X)

        # AIに選んでもらうボタンを作成し、下部フレームに配置
        self.ai_button = Button(self.bottom_frame, image=self.controller.logo,
                                bg='white', bd=0, activebackground='white', command=self.ai_select)
        self.ai_button.pack(side='left', padx=(210, 0), pady=(0, 20))

        # もう一回ボタンを作成し、下部フレームに配置
        self.reset_button = Button(self.bottom_frame, image=self.refresh_icon,
                                   bg='white', bd=0, activebackground='white', command=self.reset)
        self.reset_button.pack(side='right', padx=20)

        self.load_images()  # 画像を読み込む

    # 関数名  ：load_images
    # 機能    ：選択された画像をフレームに表示する
    # 処理概要：選択された画像を3x3のグリッドに配置して表示する
    def load_images(self):
        self.image_buttons = []
        # 画像パスを取得
        self.img_paths = self.controller.selected_img_paths

        for i, img_path in enumerate(self.controller.selected_img_paths):
            img = Image.open(img_path)
            img = img.resize((100, 100), Image.LANCZOS)  # 画像をリサイズ
            photo = ImageTk.PhotoImage(img)
            img_btn = Button(self.top_frame, image=photo,
                             bg='white', relief='flat')
            img_btn.image = photo
            # 3x3のグリッドに配置
            row = i // 3
            column = i % 3
            img_btn.grid(row=row, column=column, sticky='nsew')

            self.image_buttons.append(img_btn)

    # 関数名  ：select_image
    # 機能    ：指定した画像ボタンに枠をつける
    # 処理概要：指定したインデックスの画像ボタンに枠線を追加する
    def select_image(self, idx):
        self.image_buttons[idx].config(relief='solid')

    # 関数名  ：ai_select
    # 機能    ：AIモデルで画像を判定する
    # 処理概要：選択された画像に対してAI判定を行い、結果に基づいて画像に枠をつける

    def ai_select(self):
        detect_list = read_files(self.img_paths)
        for i, result in enumerate(detect_list):
            if result == 1:
                self.select_image(i)

    # 関数名  ：reset
    # 機能    ：画像選択画面に戻る
    # 処理概要：選択された画像をクリアし、画像選択画面に戻る
    def reset(self):
        self.controller.show_frame('SelectImageScreen')


# メインの実行部分
if __name__ == "__main__":
    app = Application()
    app.mainloop()
