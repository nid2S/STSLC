from STSLC import SpeechRec, Preprocessing, Vis_SignLang
import tkinter
# (음성 인식 후 저장 > 불러와 STT) > 전처리(토큰화, 임베딩, 패딩) > 수화로 변환(전처리 후 단어에 맞춰 변환) > 변환된 수화 출력(창에 띄움)
# 전부 클래스화 요망
# 라이브러리 상속을 나눠 속도 증진 필요?

def switch_win(old_win: tkinter.Tk, new_win: tkinter.Tk):
    old_win.destroy()
    old_win.quit()
    new_win.mainloop()

def make_mainWin() -> tkinter.Tk:
    win = tkinter.Tk()
    win.title("S2SL")
    win.geometry("800x450+100+50")
    win.option_add("*Font", "맑은고딕 20")

    tkinter.Label(win, text="Speech to SignLanguage", pady=5).pack(side="top")
    tkinter.Button(win, text="eng", pady=5, command=lambda: switch_win(win, eng_S2SL())).pack(side="bottom")
    # add new btn

    return win

def STSL(win: tkinter.Tk, ent: tkinter.Entry, lb: tkinter.Label, lang: str):
    """lang: english(en/eng), korean(ko/kr/kor), international(int/isl/eng_isl)"""
    lang.lower()
    try:
        rec_sec = int(ent.get())
    except ValueError:
        lb.config(text="wrong input.\nplz type int.")
        return None
    # text = SpeechRec.STT(rec_sec)
    # if text is None:
    #     return None
    text = "hi. my name is nid. what's your name? oh, your name was nid too! nice meet you."
    win.destroy()
    win.quit()
    if lang in "en/eng/english":
        text_p = Preprocessing.eng_preprocessing(text)
        Vis_SignLang.vis_eng(text_p)
    elif lang in "ko/kr/kor/korean":
        text_p = Preprocessing.kor_preprocessing(text)
        Vis_SignLang.vis_kor(text_p)
    elif lang in "int/isl/eng_isl/international":
        text_p = Preprocessing.eng_isl_preprocessing(text)
        Vis_SignLang.vis_eng_isl(text_p)
    else:
        raise ValueError("Wrong language.")

    make_mainWin().mainloop()

def eng_S2SL() -> tkinter.Tk:
    win = tkinter.Tk()
    win.title("eng S2SL")
    win.geometry("800x450+100+50")
    win.option_add("*Font", "맑은고딕 20")

    lb = tkinter.Label(win, text="set record second(int) :")
    ent = tkinter.Entry(win)
    lb.grid(row=0, column=0)
    ent.grid(row=0, column=1)

    tkinter.Button(win,  command=lambda: STSL(win, ent, lb, "eng"), text="record").place(relx=0.48, rely=0.92)
    tkinter.Button(win, background="red", command=lambda: switch_win(win, make_mainWin()), text="<-").place(relx=0.92, rely=0.05)

    return win

def kor_S2SL() -> tkinter.Tk:
    pass

def isl_S2SL() -> tkinter.Tk:
    pass


if __name__ == '__main__':
    make_mainWin().mainloop()
