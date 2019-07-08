import re, os, cv2
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfd
from tkinter import messagebox as mess

# グローバル変数
acv_path = ""
f_path_list = []

### この下に関数を書く ###
# 画像追加イベント
def img_add():
	global f_cnt, f_path_list
	f_conf = [("Text Files", ("jpg", "png", "jpeg"))]
	paths = tkfd.askopenfiles(filetypes=f_conf)
	for f in paths:
		imgList.insert("", "end", values=(len(f_path_list), f.name))
		f_path_list.append(f.name)
	msgList.insert(0, "画像を{0}件追加しました".format(len(paths)))

# 画像リセットイベント
def img_reset():
	global f_cnt, f_path_list
	for i in imgList.get_children():
		imgList.delete(i)
	f_path_list = []
	msgList.insert(0 , "読み込んだ画像をリセットしました")

def rename_status():
	if renameChkVar.get():
		state = "normal"
		fg = "#000000"
	else:
		state = "disabled"
		fg = "#666666"
	
	fNameLbl["fg"] = fg
	fNumLbl["fg"] = fg
	nResLbl["fg"] = fg
	nResOut["fg"] = fg
	renameFrm["fg"] = fg
	fNameEnt["state"] = state
	fNumEnt["state"] = state
	usChk["state"] = state

# リサイズチェック
def resize_status():
	if resizeChkVar.get():
		state = "normal"
		fg = "#000000"
	else:
		state = "disabled"
		fg = "#666666"

	resizeLbl1["fg"] = fg
	resizeLbl2["fg"] = fg
	resizeEnt["state"] = state

# 保存先ディレクトリ選択
def acv_open():
	global acv_path
	acv_path = tkfd.askdirectory()
	acvEnt.configure(state="normal")
	acvEnt.delete(0, "end")
	if acv_path != "":
		acvEnt.insert(0, acv_path)
		msgList.insert(0, "保存先を{0}に設定しました".format(acv_path))
	else:
		acvEnt.insert(0, "未選択")
	acvEnt.configure(state="disabled")

# 画像処理
def img_trans():
	global f_path_list, acv_path
	f_name  = fNameEnt.get()
	f_num   = fNumEnt.get()
	img_width = resizeEnt.get()
	rename_chk = renameChkVar.get()
	resize_chk = resizeChkVar.get()
	# 簡易バリデーション
	if len(f_path_list) == 0:
		msgList.insert(0, "画像が選択されていません")
		return None
	if acv_path == "":
		msgList.insert(0, "保存先を選択してください")
		return None
	if re.match("^[a-zA-Z0-9_]+$", f_name) is None and rename_chk:
		msgList.insert(0, "「ファイル名」は英数字で入力して下さい")
		return None
	if re.match("^[0-9]+$", f_num) is None and rename_chk:
		msgList.insert(0, "「開始番号」は数字で入力して下さい")
		return None
	if re.match("^[0-9]+$", img_width) is None and resize_chk:
		msgList.insert(0, "「幅」は数字で入力して下さい")
		return None
	msg_box = mess.askquestion("Message", "変換を開始しますか？")
	if msg_box == "yes":
		try:
			for i, path in enumerate(f_path_list):
				img_data = cv2.imread(path, -1)
				if rename_chk:
					f_name_result = f_name
					if usChkVar.get():
						f_name_result += "_"
					f_name_result += str(i + int(f_num))
				else:
					f_name_result = os.path.splitext(os.path.basename(path))[0]
				if resize_chk:
					img_height = int(int(img_width) / img_data.shape[1] * img_data.shape[0])
					img_data = cv2.resize(img_data, (int(img_width), img_height))
				f_name_result += ".{0}".format(extSelect.get())
				cv2.imwrite("{0}/{1}".format(acv_path, f_name_result), img_data)
			msgList.insert(0, "変換完了")
		except:
			msgList.insert(0, "変換失敗")
		finally:
			pb["value"] = 10

# 出力結果例
def rename_disp(self):
	txt = ""
	if renameChkVar.get():
		txt = fNameEnt.get()
		if usChkVar.get():
			txt += "_"
		txt += fNumEnt.get() + "." + extSelect.get()
	nResOut["text"] = txt

if __name__ == "__main__":
	# メインウィンドウ生成
	root = tk.Tk()
	# ウィンドウタイトルを指定
	root.title("Image editing app")
	# ウィンドウサイズを指定
	root.geometry("400x550")
	# ウィンドウサイズの変更可否設定
	root.resizable(0,0)
	# ウィンドウの背景色
	root.configure(bg="white")

	# 名前例更新
	root.bind("<KeyPress>", rename_disp)
	root.bind("<Button>", rename_disp)
	root.bind("<ButtonRelease>", rename_disp)

	### この下に描画内容を書く ###
	wrpFrm = tk.Frame(root)
	wrpFrm.configure(bg="white")
	wrpFrm.pack(padx=3, pady=3, fill="both", expand=1)

	# 読み込んだ画像リスト
	imgList = ttk.Treeview(wrpFrm)
	imgList.configure(column=(1,2), show="headings", height=6)
	imgList.column(1, width=30)
	imgList.column(2, width=361)
	imgList.heading(1, text="No")
	imgList.heading(2, text="path/name")
	imgList.pack()

	# ボタン中央揃え用のフレーム
	btnFrm = tk.Frame(wrpFrm)
	btnFrm.configure(bg="white")
	btnFrm.pack(pady=5)

	# 画像追加ボタン
	addBtn = tk.Button(btnFrm)
	addBtn.configure(text="画像を追加", command=img_add)
	addBtn.pack(side="left", padx=5)

	# 画像リセットボタン
	resetBtn = tk.Button(btnFrm)
	resetBtn.configure(text="画像をリセット", command=img_reset)
	resetBtn.pack(side="left", padx=5)

	# グリッド用のFrame
	confGridFrm = tk.Frame(wrpFrm)
	confGridFrm.configure(bg="white")
	confGridFrm.pack(padx=3, pady=3, fill="x")

	# チェックボックス設置
	renameChkVar = tk.BooleanVar()
	renameChkVar.set(True)
	renameChk = tk.Checkbutton(confGridFrm)
	renameChk.configure(
		text="リネームする",
		variable=renameChkVar,
		command=rename_status,
		bg="white")
	renameChk.grid(row=0, column=0, sticky="nw")

	# ネームルールフレーム
	renameFrm = tk.LabelFrame(confGridFrm)
	renameFrm.configure(bg="white", text="リネームルール", relief="groove")
	renameFrm.grid(row=0, column=1, pady=(0,5))

	# レイアウト用のFrame
	renameFrmInn = tk.Frame(renameFrm)
	renameFrmInn.configure(bg="white")
	renameFrmInn.pack(padx=8, pady=(0,5))

	# ファイル名
	fNameLbl = tk.Label(renameFrmInn)
	fNameLbl.configure(text="ファイル名", bg="white")
	fNameLbl.grid(row=0, column=0, sticky="nw")

	# ファイル名入力欄
	fNameEnt = tk.Entry(renameFrmInn)
	fNameEnt.insert("end", "img")
	fNameEnt.grid(row=0, column=1, pady=(0,2), sticky="w")

	# 開始番号
	fNumLbl = tk.Label(renameFrmInn, text="開始番号")
	fNumLbl.configure(bg="white")
	fNumLbl.grid(row=1, column=0, sticky="w")

	# 開始番号入力欄
	fNumEnt = tk.Entry(renameFrmInn, width=10)
	fNumEnt.insert("end", "1")
	fNumEnt.grid(row=1, column=1, sticky="w")

	# アンダーバーチェック
	usChkVar = tk.BooleanVar()
	usChkVar.set(True)
	usChk = tk.Checkbutton(renameFrmInn)
	usChk.configure(
		bg="white",
		text="区切り文字にアンダースコア(_)を使用する",
		variable=usChkVar)
	usChk.grid(row=2, column=0, columnspan=2, sticky="nw")

	# 出力結果タイトル
	nResLbl = tk.Label(renameFrmInn)
	nResLbl.configure(bg="white", text="出力結果例")
	nResLbl.grid(row=3, column=0, sticky="w")

	# 出力結果
	nResOut = tk.Label(renameFrmInn)
	nResOut.configure(bg="white", text="img_1.png")
	nResOut.grid(row=3, column=1, sticky="w")

	# リサイズチェック
	resizeChkVar = tk.BooleanVar()
	resizeChkVar.set(True)
	resizeChk = tk.Checkbutton(confGridFrm)
	resizeChk.configure(
		bg="white",
		text="幅を固定値でリサイズ",
		variable=resizeChkVar,
		command=resize_status)
	resizeChk.grid(row=3, column=0, padx=(0,15), sticky="nw")

	# リサイズ幅設定フレーム
	resizeFrm = tk.Frame(confGridFrm)
	resizeFrm.configure(bg="white")
	resizeFrm.grid(row=3, column=1, sticky="nw", pady=(0,5))

	# "幅"
	resizeLbl1 = tk.Label(resizeFrm)
	resizeLbl1.configure(bg="white", text="幅")
	resizeLbl1.pack(side="left")

	# 幅指定入力欄
	resizeEnt = tk.Entry(resizeFrm)
	resizeEnt.configure(width=10, relief="groove")
	resizeEnt.insert("end", "600")
	resizeEnt.pack(side="left", padx=(15,0))

	# "px"
	resizeLbl2 = tk.Label(resizeFrm)
	resizeLbl2.configure(bg="white", text="px")
	resizeLbl2.pack(side="left")

	# 拡張子指定タイトル
	extTtlLbl = tk.Label(confGridFrm)
	extTtlLbl.configure(bg="white", text="拡張子を指定")
	extTtlLbl.grid(row=4, column=0, sticky="nw")

	# 拡張子フレーム
	extFrm = tk.Frame(confGridFrm)
	extFrm.configure(bg="white")
	extFrm.grid(row=4, column=1, sticky="nw", pady=(0,5))

	# "形式"
	extLbl = tk.Label(extFrm)
	extLbl.configure(bg="white", text="形式")
	extLbl.pack(side="left")

	# 拡張子セレクト
	extSelect = ttk.Combobox(extFrm)
	extSelect.configure(
		state="readonly",
		width=8,
		value = ("png", "jpeg"))
	extSelect.current(0)
	extSelect.pack(side="left", padx=(3,0))

	# 保存先タイトル
	acvTtlLbl = tk.Label(confGridFrm)
	acvTtlLbl.configure(bg="white", text="保存先を選択")
	acvTtlLbl.grid(row=5, column=0, sticky="nw")

	# 保存先フレーム
	acvFrm = tk.Frame(confGridFrm)
	acvFrm.configure(bg="white")
	acvFrm.grid(row=5, column=1, sticky="nw", pady=(0,5))

	# 保存先テキスト
	acvEnt = tk.Entry(acvFrm)
	acvEnt.configure(width=33)
	acvEnt.insert(0, "未選択")
	acvEnt.configure(state="disabled")
	acvEnt.pack(side="left")

	# 保存先参照ボタン
	acvBtn = tk.Button(acvFrm)
	acvBtn.configure(text="参照", command=acv_open)
	acvBtn.pack(side="left")

	# 実行ボタン
	runBtn = tk.Button(wrpFrm)
	runBtn.configure(text="実行", command=img_trans)
	runBtn.pack(
	    anchor="e",
	    pady=(0,5), padx=(0,5),
	    ipadx=15, ipady=1)

	# 通知リスト
	msgList = tk.Listbox(wrpFrm)
	msgList.configure(height=6, width=65)
	msgList.pack()

	# 進捗バー
	pb = ttk.Progressbar(wrpFrm)
	pb.configure(
	    maximum=10,
	    orient="horizontal")
	pb.pack(pady=(4,0), fill="x")

	# 描画
	root.mainloop()
