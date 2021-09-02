import tkinter
import threading
import os
import pandas as pd
from hgtk.text import decompose
from cv2 import VideoCapture, cvtColor, waitKey, COLOR_BGR2RGB
from PIL.Image import fromarray
from PIL.ImageTk import PhotoImage


def video_running(sl_type: str, sents: str, data: pd.DataFrame, win: tkinter.Tk):
    """sl_type : ksl or isl"""
    file_numbers = []
    for sent in sents:
        for token in sent:
            lb = tkinter.Label(win)
            lb.grid()
            try:
                file_numbers.append(data.loc[data["word"] == token].iterrows().__next__()[1]["file_num"])
            except StopIteration:  # case of couldn't search token
                for char in decompose(token).replace('ᴥ', ' ').split():
                    file_numbers.append(data.loc[data["word"] == char].iterrows().__next__()[1]["file_num"])

    lb = tkinter.Label(win)
    lb.grid()
    for file_number in file_numbers:
        video_path = "./dataset/"+sl_type+"_data/" + str(file_number) + ".mp4"
        if not os.path.isfile(video_path):
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
            waitKey(1)

    win.destroy()


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

    data = pd.read_csv("./STSLC/dataset/ksl_data/words.txt", header=None, names=["file_num", "word"], sep="\t")
    add_words = []
    for idx, (file_num, word) in data.copy().iterrows():
        if "," in word:
            for each_word in word.split(","):
                add_words.append([file_num, each_word])
            data.drop(idx, inplace=True)
    data = data.append(pd.DataFrame(add_words, columns=["file_num", "word"]), ignore_index=True)

    win = tkinter.Tk()
    win.title("Korean Speak to SighLanguage")
    win.geometry("800x450+100+50")  # each video's size is (700*466)

    t = threading.Thread(target=video_running, args=["ksl", sents, data, win])
    t.deamon = True
    t.start()

    win.mainloop()


def vis_eng_isl(sents: list[list[str]]):
    # each video's size is (400*300)
    pass


