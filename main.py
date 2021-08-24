from STSLC import SpeechRec, Preprocessing, Vis_SignLang
import tkinter
# (음성 인식 후 저장 > 불러와 STT) > 전처리(토큰화, 임베딩, 패딩) > 수화로 변환(전처리 후 단어에 맞춰 변환) > 변환된 수화 출력(창에 띄움)
# 라이브러리 상속을 나눠 속도 증진 필요?

def switch_win(old_win: tkinter.Tk, new_win: tkinter.Tk):
    old_win.destory()
    new_win.mainloop()

def make_mainWin() -> tkinter.Tk:
    win = tkinter.Tk()
    win.title("S2SL")
    win.geometry("800x450+100+50")
    win.option_add("*Font", "맑은고딕 25")

    tkinter.Label(win, text="Speech to SignLanguage", pady=5).pack(side="top")
    tkinter.Button(win, text="eng", pady=5, command=lambda: switch_win(win, eng_S2SL())).pack(side="bottom")
    # add new btn

    return win


def eng_S2SL() -> tkinter.Tk:
    win = tkinter.Tk()
    win.title("eng S2SL")
    win.geometry("800x450+100+50")
    win.option_add("*Font", "맑은고딕 25")

    lb = tkinter.Label(win, text="set record second(int) :")
    ent = tkinter.Entry(win)
    lb.grid(low=0, column=0)
    ent.grid(low=0, column=1)

    def STSL():
        try:
            rec_sec = int(ent.get())
        except ValueError:
            lb.config(text="wrong input.\nplz type int.")
            return None
        text = SpeechRec.STT(rec_sec)
        if text is None:
            return None
        # text = "hi. my name is nid. what's your name? oh, your name was nid too! nice meet you."
        text_p = Preprocessing.eng_preprocessing(text)
        Vis_SignLang.vis_eng(text_p)

    tkinter.Button(win, background="black", command=lambda: STSL(), text="record").place(relx=0.48, rely=0.92)
    tkinter.Button(win, background="red", command=lambda: switch_win(win, make_mainWin()), text="<-").place(relx=0.92, rely=0.05)

    return win


if __name__ == '__main__':
    # Vis_SignLang.vis_eng(Preprocessing.eng_preprocessing("hi. my name is nid. what's your name? oh, your name was nid too! nice meet you."))
    make_mainWin().mainloop()
