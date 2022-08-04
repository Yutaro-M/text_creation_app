import PySimpleGUI as sg  # 略語「sg」は慣例
from datetime import date   # 日付に関するモジュール

# 基本設定
sg.theme('BlueMono')  # テーマの設定
myfont = ('Source Han Sans', 13)  # フォントの設定

# 不変のデータ
FRUITS = {'リンゴ': 100, 'バナナ': 70, 'オレンジ': 80}


# 関数の定義
def cbtn_print():  # 「入力後クリック」を押したときの処理
    win['txt_result'].update('')     # テキストボックス内の文字を消去
    fnames = []  # 商品の名前（空のリストを作成し、後から追加）
    fnames.append(values['fname1'])  # コンボボックス（商品1）の値を取得
    fnames.append(values['fname2'])  # コンボボックス（商品2）の値を取得
    fnums = []   # 商品の個数（空のリストを作成し、後から追加）
    fnums.append(values['fnum1'])    # 入力欄（商品1の個数）の値を取得
    fnums.append(values['fnum2'])    # 入力欄（商品2の個数）の値を取得

    # 同じ商品が入力された場合、警告を表示
    if len(fnames) != len(set(fnames)):  # 重複した値が存在するか判定
        sg.popup('同じ商品が入力されています', title='要確認', location=(30, 450), font=myfont)
        return  # 警告が出た時点で関数を抜ける（これ以降の命令を実行させない）

    # 商品と個数の片方だけしか入力されなかった場合、警告を表示
    for i, j in zip(fnames, fnums):
        if (i and not j) or (j and not i):
            sg.popup('商品と個数、片方だけしか入力されていません', title='要確認', location=(30, 450), font=myfont)
            return

    # 個数に「自然数（数えられる値）or空白」が入力されなかった場合、警告を表示
    for i in fnums:
        if not ((i.isdecimal() and int(i) > 0) or i == ''):
            sg.popup('数えられる値を入力してください', title='要確認', location=(30, 450), font=myfont)
            return

    # 文字を数値に変換する（i.isdecimal()：2つ目の個数が空白のときのエラーを防止）
    fnums = [int(i) for i in fnums if i.isdecimal()]

    # ラッピング（オプション）の有無
    if values['use_wrap']:
        wrap_price = 100  # チェックが入っているとき
    else:
        wrap_price = 0    # チェックが入っていないとき

    # 日付とファイル名をテキストボックスに表示
    d_today = date.today()  # 今日の日付を変数に格納
    d_today_y_m_d = d_today.strftime('%Y/%m/%d')  # 「年/月/日」の形式に変換
    filename_input = values['file_input']         # 入力欄のファイル名を取得
    win['txt_result'].print(d_today_y_m_d)        # 本文の1行目に日付を表示
    if filename_input:  # ファイル名が入力されたとき、2行目にファイル名を表示
        win['txt_result'].print(filename_input)

    # 計算をして、結果をテキストボックスに表示
    win['txt_result'].print()  # 空行を入れる
    total_fnum = 0    # 商品の合計個数（最初は0）
    total_fprice = 0  # 商品の合計金額（最初は0）
    for i, j in zip(fnames, fnums):
        text_main = f'{i}が{j}個で{FRUITS[i] * j}円。（1個当たり{FRUITS[i]}円）'
        win['txt_result'].print(text_main)   # テキストボックスに書き込む
        total_fnum += j                      # 商品の合計個数が、増えていく
        total_fprice += FRUITS[i] * j        # 商品の合計金額が、増えていく
    total_price = total_fprice + wrap_price  # 全ての合計金額
    if wrap_price:  # ラッピングを利用する場合、代金を表示させる
        text_wrap = f'＊ラッピングの代金が{wrap_price}円。'
        win['txt_result'].print(text_wrap)   # テキストボックスに書き込む
    text_total = f'\n商品が{total_fnum}個で、合計が{total_price}円です。'
    win['txt_result'].print(text_total)      # テキストボックスに書き込む


def cbtn_file():  # 「本文をファイルに保存」を押したときの処理
    if values['txt_result'] == '\n':  # テキストボックスが空の場合に警告を表示（改行だけが入る）
        sg.popup('テキストボックスが空です', title='要確認', location=(30, 450), font=myfont)
        return
    d_today = date.today()                    # 今日の日付を変数に格納
    d_today_ymd = d_today.strftime('%Y%m%d')  # 「年月日」の形式に変換
    front_name = d_today_ymd                  # ファイル名の前半は日付（年月日）
    filename_input = values['file_input']     # 入力欄のファイル名を取得
    back_name = filename_input + '.txt'       # 拡張子（.txt）を追加
    filename = front_name + '_' + back_name   # ファイル名の完成
    path_desktop = '/Users/user_name/Desktop/'  # デスクトップのパス
    fullpath = path_desktop + filename        # ファイルの絶対パス（フルパス）
    text_main = values['txt_result']          # 本文に入力された内容を取得
    with open(fullpath, 'w', encoding='utf_8') as file:  # ファイルの作成（上書き/新規作成）
        file.write(text_main)                 # 本文に入力された内容をファイルに書き込む
    win['btn_file'].update('  ファイルに保存しました  ')  # ボタンを押した後に文章を変更する


# レイアウトの設定
flist1 = ['リンゴ', 'バナナ', 'オレンジ']
flist2 = ['', 'リンゴ', 'バナナ', 'オレンジ']
layout = [
    [sg.Text('ファイル名：', pad=((65, 0), (5, 0)), font=myfont),
     sg.Input(key='file_input', size=(10, 1), pad=(0, 10), font=myfont)],
    [sg.Text('商品1', pad=((55, 0), (5, 0)), font=myfont),
     sg.Combo(flist1, key='fname1', default_value='リンゴ',
              readonly=True, size=(7, 1), font=myfont),
     sg.Text('個数', pad=((0, 0), (5, 0)), font=myfont),
     sg.Input(key='fnum1', default_text='2', size=(3, 1), font=myfont)],
    [sg.Text('商品2', pad=((55, 0), (5, 0)), font=myfont),
     sg.Combo(flist2, key='fname2', readonly=True, size=(7, 1), font=myfont),
     sg.Text('個数', pad=((0, 0), (5, 0)), font=myfont),
     sg.Input(key='fnum2', size=(3, 1), font=myfont)],
    [sg.Checkbox('', key='use_wrap', default=False, pad=((110, 0), (5, 0)), font=myfont),
     sg.Text('ラッピング', pad=((0, 0), (7, 0)), font=myfont)],
    [sg.Button('  入力後クリック（本文を表示）', key='btn_print', pad=(55, 10), font=myfont)],
    [sg.Multiline(key='txt_result', size=(35, 9), font=myfont)],
    [sg.Button('  本文をファイルに保存  ', key='btn_file', pad=(75, 5), font=myfont)],
]
# ウィンドウの作成
win = sg.Window('メール本文作成アプリ', layout, location=(30, 400))

# イベントループの作成
while True:
    event, values = win.read()
    if event is None:
        break
    if event == 'btn_print':  # 「入力後クリック」を押したとき実行
        cbtn_print()
    if event == 'btn_file':  # 「本文をファイルに保存」を押したとき実行
        cbtn_file()

# ウィンドウを閉じる
win.close()
