# 概要
自動で計算を行い、結果が反映された文章を作成する（ファイルへの保存も可能） <br>
＊左（背景が白）がTkinter、右（背景が青色）がPySimpleGUI<br>
<img width="200" alt="アプリの画面（Tk）" src="https://user-images.githubusercontent.com/110469370/182971581-cc22248f-f4ce-440d-889b-5a08fcfa57d2.png">
<img width="225" alt="アプリの画面（sg）" src="https://user-images.githubusercontent.com/110469370/182971706-7547f879-739a-473e-9326-066642559662.png">

# 機能
- 商品の種類と数、オプションを指定できる
- 計算結果を反映させた本文を表示できる
- 必要に応じて、本文内容をファイルに保存できる

# 使用した技術
- TkinterとPySimpleGUI
- Pythonの基本的なモジュール

# デスクトップにファイルを保存するために必要な処理
- Tkinterでは88行目
- PySimpleGUIでは83行目<br>
path_desktop = '/Users/user_name/Desktop/'   # デスクトップのパス<br>
上記の「user_name」を書き換える必要あり

# 背景
これまで計算や本文の作成などは別々に行い、個別にタイピングしていた。<br>
アプリを使って、計算や本文の作成を簡単に自動化できることを体感し、<br>
プログラミングを使った業務効率化の重要性を理解した。
