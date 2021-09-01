import tkinter
import pandas as pd
from hgtk.text import decompose
from cv2 import VideoCapture
from PIL.Image import fromarray
from PIL.ImageTk import PhotoImage


def vis_eng(sents: list[list[list[str]]]):
    # sent > word > char

    # tkinter
    for sent in sents:
        win = tkinter.Tk()
        # each picture's size is about (60*110)
        max_wordLen = max(len(word) for word in sent) + 1
        wid = max_wordLen*60 if (max_wordLen*60 > 800) else 800
        hei = len(sent)*110 if (len(sent)*110 > 450) else 450
        win.geometry(f"{wid}x{hei}+100+50")

        cnt = 0
        img_list = []
        lab_list = []
        sent_comp = ""
        for i, word in enumerate(sent):
            tkinter.Label(win, text=word, font="맑은고딕 13").grid(row=i, column=0, padx="5")

            for j, char in enumerate(word):
                try:
                    img_list.append(tkinter.PhotoImage(file="./dataset/asl_data/" + char + ".png", master=win))
                except tkinter.TclError:
                    img_list.append(None)
                    lab_list.append(None)
                    cnt += 1
                    continue
                lab_list.append(tkinter.Label(win, image=img_list[cnt]))
                lab_list[cnt].grid(row=i, column=j + 1)  # row, col = word order, char order
                cnt += 1

                sent_comp += char
            sent_comp += " "

        tkinter.Button(win, command=lambda: win.destroy(), text="->", font="맑은고딕 20").place(relx=0.45, rely=0.87)
        win.title(sent_comp)
        win.mainloop()


def vis_kor(sents: list[list[str]]):
    # sent > token

    # 토큰이 있는 열의 파일넘버(or 인덱스)를 가져옴(없으면 쪼개서)> 해당 파일넘버로 비디오를 가져와 비디오 출력 > 그대로 쭉 끝까지 > 끝나면 디스트로이 되게
    # 파일넘버를 가져오는 방법 | 1. data에 ,가 없게 가공 후 loc조건문(열에 파일넘버 추가)
    # 파일넘버를 가져오는 방법 | 2. 반복문 돌려서 인덱스 찾고 없으면 나눠서 > 2-1.처음부터 다시 2-2.자/모음만 모아다가
    data = pd.read_csv("./STSLC/dataset/ksl_data/words.txt", header=None,  index_col=0, names=["word"], sep="\t")
    for sent in sents:
        for token in sent:




def vis_eng_isl(sents: list[list[str]]):
    pass


