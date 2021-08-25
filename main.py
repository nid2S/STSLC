from STSLC import SpeechRec, Preprocessing, Vis_SignLang
import tkinter
# 디자인
# 라이브러리 상속을 나눠 속도 증진 필요?

def switch_win(old_win: tkinter.Tk, new_win: tkinter.Tk):
    old_win.destroy()
    old_win.quit()
    new_win.mainloop()


class S2SL_Converter:
    def __init__(self):
        self.make_mainWin().mainloop()

    # private?
    def make_mainWin(self) -> tkinter.Tk:
        win = tkinter.Tk()
        win.title("S2SL")
        win.geometry("800x450+100+50")
        win.option_add("*Font", "맑은고딕 20")

        tkinter.Label(win, text="Speech to SignLanguage", pady=10).pack(side="top")
        tkinter.Button(win, text="eng", command=lambda: switch_win(win, self.eng_S2SL())).pack(side="bottom", pady="7")
        tkinter.Button(win, text="kor", command=lambda: switch_win(win, self.kor_S2SL())).pack(side="bottom", pady="7")
        tkinter.Button(win, text="isl", command=lambda: switch_win(win, self.isl_S2SL())).pack(side="bottom", pady="7")

        return win

    def STSL(self, win: tkinter.Tk, ent: tkinter.Entry, lb: tkinter.Label, lang: str):
        """lang: english(en/eng), korean(ko/kr/kor), international(int/isl/eng_isl)"""
        lang.lower()
        # get record sec
        try:
            rec_sec = int(ent.get())
        except ValueError:
            ent.delete(0, len(ent.get()))
            ent.insert(0, "wrong input. please put number.")
            return None
        # # recording
        # lb.config(text="recording... ")
        # text = SpeechRec.STT(rec_sec)
        # if text is None:  # case of recorded nothing
        #     ent.delete(0, len(ent.get()))
        #     ent.insert(0, "couldn't recognize anything.")
        #     lb.config(text="set record second(int) :")
        #     return None
        text = "hi. my name is nid. what's your name? oh, your name was nid too! nice meet you."
        # check recorded text
        tkinter.Label(win, text="check the recognized text", font="맑은고딕 20").place(x=10, rely=0.3)
        ent = tkinter.Entry(win, width=50, font="맑은고딕 15")
        ent.insert(0, text)
        ent.place(x=10, rely=0.4)
        tkinter.Button(win, text="confirm", font="맑은고딕 20", command=lambda: vis()).place(x=10, rely=0.5)

        # visualization function.
        def vis():
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
            self.make_mainWin().mainloop()

    def eng_S2SL(self) -> tkinter.Tk:
        win = tkinter.Tk()
        win.title("eng S2SL")
        win.geometry("800x450+100+50")
        win.option_add("*Font", "맑은고딕 20")

        lb = tkinter.Label(win, text="set record second(int) :")
        ent = tkinter.Entry(win, font="맑은고딕 15", width="30")
        lb.grid(row=0, column=0, padx="10", pady="12")
        ent.grid(row=0, column=1, pady="12")

        tkinter.Button(win, background="red", command=lambda: switch_win(win, self.make_mainWin()),
                       text="<-").place(relx=0.92, rely=0.02)
        tkinter.Button(win, command=lambda: self.STSL(win, ent, lb, "eng"), text="record").place(relx=0.45, rely=0.87)

        return win

    def kor_S2SL(self) -> tkinter.Tk:
        pass

    def isl_S2SL(self) -> tkinter.Tk:
        pass


if __name__ == '__main__':
    stslc = S2SL_Converter()
