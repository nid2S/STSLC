import matplotlib.pyplot as plt
import tkinter

def vis_eng(sents: list[list[list[str]]]):
    # sent > word > char

    # plt
    # plt.style.use('seaborn-white')
    # for sent in sents:
    #     for i, word in enumerate(sent):
    #         for j, char in enumerate(word):
    #             idx = i * max(len(w) for w in sent) + (j+1)
    #             plt.subplot(len(sent), max(len(w) for w in sent), idx)  # (row, col) = (num of words, max length of word). make new screen for each sent.
    #             plt.subplots_adjust(wspace=0, hspace=0.45)  # control(adjust) gap between plots
    #             plt.title(char)
    #             plt.xticks([])
    #             plt.yticks([])
    #             plt.imshow(plt.imread("./dataset/asl_data/"+char+".png"))
    #     plt.show()

    # tkinter
    for sent in sents:
        win = tkinter.Tk()
        win.geometry("800x450+50+50")

        cnt = 0
        img_list = []
        lab_list = []
        sent_comp = ""
        for i, word in enumerate(sent):
            for j, char in enumerate(word):
                img_list.append(tkinter.PhotoImage(file="./dataset/asl_data/"+char+".png", master=win))
                lab_list.append(tkinter.Label(win, image=img_list[cnt]))
                lab_list[cnt].grid(column=j, row=i)  # col, row = char order, word order
                cnt += 1

                sent_comp += char
            sent_comp += " "

        win.title(sent_comp)
        win.mainloop()


def vis_kor(sents: list[list[str]]):
    pass

def vis_eng_isl(sents: list[list[str]]):
    pass


vis_eng([[['h', 'i']], [['m', 'y'], ['n', 'a', 'm', 'e'], ['i', 's'], ['n', 'i', 'd']]])
