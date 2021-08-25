import time

import matplotlib.pyplot as plt
import tkinter


def vis_eng(sents: list[list[list[str]]]):
    # sent > word > char

    # tkinter
    for sent in sents:
        win = tkinter.Tk()

        # each picture's size is about (60*110)
        max_wordLen = max(len(word) for word in sent) + 1
        wid = max_wordLen*60 if (max_wordLen*60 > 800) else 800
        hei = len(sent)*110 if (len(sent)*110 > 150) else 450
        win.geometry(f"{wid}x{hei}+100+50")

        cnt = 0
        img_list = []
        lab_list = []
        sent_comp = ""
        for i, word in enumerate(sent):
            tkinter.Label(win, text=word).grid(row=i, column=0)

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

        tkinter.Button(win, command=lambda: win.destroy(), text="->").place(relx=0.48, rely=0.92)
        win.title(sent_comp)
        win.mainloop()


def vis_kor(sents: list[list[str]]):
    pass


def vis_eng_isl(sents: list[list[str]]):
    pass


