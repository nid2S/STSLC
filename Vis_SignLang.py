import os
import re
import tkinter
import threading
import numpy as np
import pandas as pd
from cv2 import VideoCapture, cvtColor, waitKey, COLOR_BGR2RGB
from PIL.Image import fromarray
from PIL.ImageTk import PhotoImage
from typing import List
from time import sleep

global is_converting
is_converting = False

def get_most_similar(word: List[float], word_origin: str, sl_type: str) -> str:
    # get data
    data = pd.read_csv("D:\\workspace\\Git_project\\STSLC\\dataset\\"+sl_type+"_encoded_data.csv")

    # change type of data/word
    data["word_encoded"] = data["word_encoded"].map(lambda w: np.asarray(w.strip("[]").split(","), dtype=np.float32))
    word = np.asarray(word, dtype=np.float32)

    # if word is OOV(all element is 0), return -1
    if sum(word != 0) == 0:
        # if the reason of OOV is English in KSL, return "-1"+word
        if re.sub("[a-z]+", "", word_origin) == "" and sl_type == "ksl":
            return "-1"+word_origin
        else:
            return "-1"

    # get cosine similarity
    data["similarity"] = data["word_encoded"].map(lambda word_vec: np.dot(word, word_vec)/(np.linalg.norm(word)*np.linalg.norm(word_vec)))

    # get max similarity row. if max similarity is lower than 0.7, file_num is -1
    file_num = data[data["similarity"] == max(data["similarity"])]
    if file_num["similarity"].item() < 0.7:
        return "-1"

    # get max similarity
    try:
        file_num = file_num["file_num"].item()
    except ValueError:  # case of max similarity is exist more than two.
        if file_num["word_origin"].isin([word_origin]).sum() == 1:  # this case means several chars were repeating like "내"/"내내". | isl dont be same.
            file_num = file_num[file_num["word_origin"] == word_origin]["file_num"].item()
        else:  # if same word do NOT exsit, one of most close is file_num.
            file_num["len_gap"] = file_num["word_origin"].map(lambda word_r: len(word_origin)-len(word_r))
            file_num = file_num[file_num["len_gap"] == max(file_num["len_gap"])]["file_num"].item()

    print("get one file_num : " + str(file_num))
    return str(file_num)

def video_running(sl_type: str, sents: (List[List[List[float]]], List[List[str]]), win: tkinter.Tk):
    """sl_type : ksl or isl"""
    # get file numbers
    file_numbers = []
    for sent, sent_origin in zip(sents[0], sents[1]):
        for word, word_origin in zip(sent, sent_origin):
            file_numbers.append(get_most_similar(word, word_origin, sl_type))
    # playing video
    lb = tkinter.Label(win)
    lb.grid()
    for file_number in file_numbers:
        if file_number[:2] == "-1":  # No more than 0.7 similarity / OOV / English
            lb.configure(font="맑은고딕 40")
            if file_number == "-1":  # OOV
                lb.configure(text="OOV", image=None)
            else:  # English in ksl
                lb.configure(text=file_number[2:], image=None)
            sleep(0.5)
            lb.configure(font="맑은고딕 20")
            continue

        video_path = "./dataset/"+sl_type+"_data/" + file_number + ".mp4"
        if not os.path.exists(video_path):
            win.destroy()
            raise FileNotFoundError
        cap = VideoCapture(video_path)
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # video end
            frame = cvtColor(frame, COLOR_BGR2RGB)
            image = PhotoImage(fromarray(frame))
            lb.image = image
            lb.configure(image=image)
            waitKey(2)  # Blinking can't be took action.
    win.destroy()


def vis_eng(sents: List[List[List[str]]]):
    # sent > word > char
    global is_converting
    while is_converting:
        continue
    is_converting = True

    def auto_run(win_t: tkinter.Tk):
        sleep(4)
        try:
            win_t.destroy()
        except tkinter.TclError:
            pass

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

        t = threading.Thread(target=auto_run, args=[win])
        t.daemon = True
        t.start()

        win.mainloop()

    is_converting = False


def vis_kor(sents: (List[List[List[float]]], List[List[str]])):
    # sents > sent > word(token_vec)
    global is_converting
    while is_converting:
        continue
    is_converting = True

    win = tkinter.Tk()
    win.title("Korean Speak to SighLanguage")
    win.geometry("710x480+100+50")  # each video's size is (700*466)

    t = threading.Thread(target=video_running, args=["ksl", sents, win])
    t.deamon = True
    t.start()

    win.mainloop()
    is_converting = False

def vis_eng_isl(sents: (List[List[List[float]]], List[List[str]])):
    global is_converting
    while is_converting:
        continue
    is_converting = True

    win = tkinter.Tk()
    win.title("international Speak to SighLanguage")
    win.geometry("410x310+100+50")  # each video's size is (400*300)

    t = threading.Thread(target=video_running, args=["isl", sents, win])
    t.deamon = True
    t.start()

    win.mainloop()

    is_converting = False
