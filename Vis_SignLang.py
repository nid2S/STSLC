import tkinter
import threading
import numpy as np
import pandas as pd
from cv2 import VideoCapture, cvtColor, waitKey, COLOR_BGR2RGB
from PIL.Image import fromarray
from PIL.ImageTk import PhotoImage
from typing import List
from time import sleep


def get_most_similar(word: List[float], sl_type: str) -> str:
    data = pd.read_csv("D:\\workspace\\Git_project\\STSLC\\dataset\\"+sl_type+"_encoded_data.csv", names=["file_num", "word_origin", "word_encoded"])

    def get_cos_similar(v1: List[float], v2: List[float]) -> float:
        return np.dot(v1, v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))

    file_num = -1
    most_similarity = 0.7  # least similarity is 0.7.
    if sum(np.asarray(word) != 0) == 0:  # case of input is OOV
        return "-1"
    for idx, row in data.iterrows():
        temp_sim = get_cos_similar(word, row["word_encoded"])
        if temp_sim > most_similarity:
            most_similarity = temp_sim
            file_num = row["file_num"]

    return str(file_num)

def video_running(sl_type: str, sents: List[List[List[float]]], win: tkinter.Tk):
    """sl_type : ksl or isl"""
    # get file numbers
    file_numbers = []
    for sent in sents:
        for word in sent:
            file_numbers.append(get_most_similar(word, sl_type))
    # playing video
    lb = tkinter.Label(win)
    lb.grid()
    for file_number in file_numbers:
        if file_number == "-1":  # No more than 0.7 similarity.
            lb.configure(text="OOV", image=None)
            # TODO 숫자/영어등의 경우일때 생각
            sleep(0.5)
            continue

        video_path = "./dataset/"+sl_type+"_data/" + file_number + ".mp4"
        cap = VideoCapture(video_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # video end
            frame = cvtColor(frame, COLOR_BGR2RGB)
            image = PhotoImage(fromarray(frame))
            lb.image = image
            lb.configure(image=image)
            waitKey(1)  # 1frame == 1ms
    win.destroy()


def vis_eng(sents: List[List[List[str]]]):
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


def vis_kor(sents: List[List[List[float]]]):
    # sents > sent > word(token_vec)
    win = tkinter.Tk()
    win.title("Korean Speak to SighLanguage")
    win.geometry("800x450+100+50")  # each video's size is (700*466)

    t = threading.Thread(target=video_running, args=["ksl", sents, win])
    t.deamon = True
    t.start()

    win.mainloop()


def vis_eng_isl(sents: List[List[List[float]]]):
    # each video's size is (400*300)
    pass


