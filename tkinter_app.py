import tkinter as tk  # 略称の「tk」は慣例
import tkinter.ttk as ttk  # コンボボックスを利用するために必要
import tkinter.messagebox as msg  # メッセージを表示するために必要
from datetime import date   # 日付に関するモジュール

# 基本設定
root = tk.Tk()  # GUIの土台を作成（変数名の「root」は慣例）
root.title('メール本文作成アプリ')  # タイトル
root.geometry('320x410')  # 土台のサイズ
root.option_add('*font', ['Source Han Sans', 13])  # フォントの指定

# 不変のデータ
FRUITS = {'リンゴ': 100, 'バナナ': 70, 'オレンジ': 80}


# 関数の定義
def cbtn_print():  # 「入力後クリック」のボタンを押したときの処理
    txt_result.delete('1.0', 'end-1c')  # テキストボックス内の文字を消去
        #'1.0'：1行目の0文字目を指す。行は1から始まり、文字は0から始まる点に注意
        #'end-1c'：「endから1文字前」という意味だが、最後の文字を指す
    fnames = []  # 商品の名前（空のリストを作成し、後から追加）
    fnames.append(cmb_fname1.get())  # コンボボックス（商品1）の値を取得
    fnames.append(cmb_fname2.get())  # コンボボックス（商品2）の値を取得
    fnums = []   # 商品の個数（空のリストを作成し、後から追加）
    fnums.append(ent_fnum1.get())  # 入力欄（商品1の個数）の値を取得
    fnums.append(ent_fnum2.get())  # 入力欄（商品2の個数）の値を取得

    # 同じ商品が入力された場合、警告を表示
    if len(fnames) != len(set(fnames)):  # 重複した値が存在するか判定
        msg.showwarning('商品の入力について', '同じ商品が入力されています')
        return  # 警告が出た時点で関数を抜ける（これ以降の命令を実行させない）

    # 商品と個数の片方だけしか入力されなかった場合、警告を表示
    for i, j in zip(fnames, fnums):
        if (i and not j) or (j and not i):
            msg.showwarning('入力について', '商品と個数、片方だけしか入力されていません')
            return

    # 個数に「自然数（数えられる値）or 空白」が入力されなかった場合、警告を表示
    for i in fnums:
        if not ((i.isdecimal() and int(i) > 0) or i == ''):
            msg.showwarning('個数の入力について', '数えられる値を入力してください')
            return

    # 文字を数値に変換する（i.isdecimal()：2つ目の個数が空白のときのエラーを防止）
    fnums = [int(i) for i in fnums if i.isdecimal()]

    # ラッピング（オプション）の有無
    if bool_wrap.get():
        wrap_price = 100  # チェックが入っているとき
    else:
        wrap_price = 0    # チェックが入っていないとき

    # 日付とファイル名をテキストボックスに表示
    d_today = date.today()  # 今日の日付を変数に格納
    d_today_y_m_d = d_today.strftime('%Y/%m/%d')  # 「年/月/日」の形式に変換
    filename_input = ent_filename.get()  # 入力欄のファイル名を取得
    txt_result.insert('1.0', f'{d_today_y_m_d}\n\n')  # 本文の1行目に日付を表示
    if filename_input:  # ファイル名が入力されたとき、2行目にファイル名を表示
        txt_result.insert('2.0', f'{filename_input}\n')

    # 計算をして、結果をテキストボックスに表示
    total_fnum = 0    # 商品の合計個数（最初は0）
    total_fprice = 0  # 商品の合計金額（最初は0）
    for i, j in zip(fnames, fnums):
        text_main = f'{i}が{j}個で{FRUITS[i] * j}円。（1個当たり{FRUITS[i]}円）\n'
        txt_result.insert('end', text_main)  # テキストボックスに書き込む
        total_fnum += j                # 商品の合計個数が、増えていく
        total_fprice += FRUITS[i] * j  # 商品の合計金額が、増えていく
    total_price = total_fprice + wrap_price  # 全ての合計金額
    if wrap_price:  # ラッピングを利用する場合、代金を表示させる
        text_wrap = f'＊ラッピングの代金が{wrap_price}円。\n'
        txt_result.insert('end', text_wrap)  # テキストボックスに書き込む
    text_total = f'\n商品が{total_fnum}個で、合計が{total_price}円です。'
    txt_result.insert('end', text_total)  # テキストボックスに書き込む


def cbtn_file():  # 「本文をファイルに保存」のボタンを押したときの処理
    if not txt_result.get('1.0', 'end-1c'):  # テキストボックスが空の場合に警告を表示
        msg.showwarning('テキストボックスについて', 'テキストボックスが空です')
        return
    d_today = date.today()                       # 今日の日付を変数に格納
    d_today_ymd = d_today.strftime('%Y%m%d')     # 「年月日」の形式に変換
    front_name = d_today_ymd                     # ファイル名の前半は日付（年月日）
    filename_input = ent_filename.get()          # 入力欄のファイル名を取得
    back_name = filename_input + '.txt'          # 拡張子（.txt）を追加
    filename = front_name + '_' + back_name      # ファイル名の完成
    path_desktop = '/Users/user_name/Desktop/'   # デスクトップのパス
    fullpath = path_desktop + filename           # ファイルの絶対パス（フルパス）
    text_main = txt_result.get('1.0', 'end-1c')  # 本文に入力された内容を取得
    with open(fullpath, 'w', encoding='utf_8') as file:  # ファイルの作成（上書き/新規作成）
        file.write(text_main)                    # 本文に入力された内容をファイルに書き込む
    btn_file['text'] = '  ファイルに保存しました  '  # ボタンを押した後に文章を変更する


# レイアウトの設定
# コンボボックスの配色設定
cmbstyle = ttk.Style()
cmbstyle.theme_create(
    'new_style', parent='default',
    settings={'TCombobox':
              {'configure':
               {'selectbackground': '#d2ebff',  # 選択時の背景色
                'selectforeground': 'black',    # 選択時の文字色
                }}})
cmbstyle.theme_use('new_style')  # 作成した「new_style」を適用

# ファイル名の入力欄
frm_filename = tk.Frame(root)  # ファイル名のフレームを作成
frm_filename.pack(pady=10)  # フレームを配置（pady：外側の縦方向の隙間の大きさを指定）
lbl_filename = tk.Label(frm_filename, text='ファイル名：')  # ファイル名のラベル
lbl_filename.pack(side='left')  # ラベルを配置（side='left'：左詰めに配置）
ent_filename = tk.Entry(frm_filename, width=10)  # ファイル名の入力欄（width：横幅を指定）
ent_filename.pack()  # 入力欄を配置（ラベルが左詰めに配置されているので、その右横に配置される）

# 商品と個数の入力欄
frm_fruits = tk.Frame(root)  # 商品と個数のフレームを作成
frm_fruits.pack()  # フレームを配置
# 1つ目の商品
lbl_fname1 = tk.Label(frm_fruits, text='商品1')  # 商品1のラベル
lbl_fname1.grid(row=0, column=0)  # ラベルを配置
flist1 = ['リンゴ', 'バナナ', 'オレンジ']  # 商品のリスト
cmb_fname1 = ttk.Combobox(frm_fruits, width=7, state='readonly', values=flist1)
    # コンボボックスを作成（state='readonly'：入力不可で選択のみ、values：リストを指定）
cmb_fname1.set('リンゴ')  # デフォルトで表示する項目
cmb_fname1.grid(row=0, column=1)  # コンボボックスを配置
lbl_fnum1 = tk.Label(frm_fruits, text='個数')  # 商品1の個数のラベル
lbl_fnum1.grid(row=0, column=2)  # ラベルを配置
ent_fnum1 = tk.Entry(frm_fruits, width=3)  # 商品1の個数の入力欄
ent_fnum1.insert(0, '2')  # デフォルトで表示する項目（0番目に「2」を挿入、という意味）
ent_fnum1.grid(row=0, column=3)
# 2つ目の商品
lbl_fname2 = tk.Label(frm_fruits, text='商品2')
lbl_fname2.grid(row=1, column=0)
flist2 = ['', 'リンゴ', 'バナナ', 'オレンジ']
cmb_fname2 = ttk.Combobox(frm_fruits, width=7, state='readonly', values=flist2)
cmb_fname2.grid(row=1, column=1)
lbl_fnum2 = tk.Label(frm_fruits, text='個数')
lbl_fnum2.grid(row=1, column=2)
ent_fnum2 = tk.Entry(frm_fruits, width=3)
ent_fnum2.grid(row=1, column=3)

# ラッピングのチェックボックス
bool_wrap = tk.BooleanVar()  # チェックの有無を判定するために必要
bool_wrap.set(False)  # True：デフォルトでチェックが入る（何も設定しない場合はFalse）
ckb_wrap = tk.Checkbutton(root, text='ラッピング', variable=bool_wrap)
    # チェックボックスを作成（「variable=」の後に、tk.BooleanVar()を格納した変数を記載）
ckb_wrap.pack(pady=5)  # チェックボックスを配置

# 入力後にクリック（本文を表示）するボタン
btn_print = tk.Button(root, text='  入力後クリック（本文を表示）', command=cbtn_print)
btn_print.pack(pady=5)

# 本文を表示するテキストボックス
txt_result = tk.Text(root, relief='solid', bd=1, highlightthickness=0, width=35, height=9)
    # relief='solid'：枠を実線（デフォルトは'flat'で、枠がない）、bd：枠線の太さ（デフォルトは0）
    # highlightthickness=0：テキストボックスを選択しているときの枠線の太さ
    # width：横の文字数を指定, height：縦の文字数を指定
txt_result.pack(pady=5)

# 本文をファイルに保存するボタン
btn_file = tk.Button(root, text='  本文をファイルに保存  ', command=cbtn_file)
btn_file.pack(pady=5)

root.mainloop()  # メインループ：画面の表示
