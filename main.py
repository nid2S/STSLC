from STSLC import SpeechRec, Preprocessing, Vis_SignLang
from nltk import download, sent_tokenize
import threading
import tkinter
import os


def check_data_exist():
    if not os.path.isdir("./dataset/asl_data") and os.path.isdir("./dataset/isl_data")\
            and os.path.isdir("./dataset/ksl_data") and os.path.isfile("./dataset/asl_data/a.png"):
        raise FileExistsError("Essential file DO NOT exist")

    try:
        sent_tokenize("hello, world.")
    except LookupError:
        download('punkt')
    if not os.path.isfile("./dataset/isl_data/words.txt"):
        Preprocessing.get_isl_data()
    if not os.path.isfile("./dataset/ksl_data/words.txt"):
        Preprocessing.get_ksl_data()


def switch_win(old_win: tkinter.Tk, new_win: tkinter.Tk):
    old_win.destroy()
    old_win.quit()
    new_win.mainloop()

class S2SL_Converter:
    def __init__(self):
        self.make_mainWin().mainloop()

    def make_mainWin(self) -> tkinter.Tk:
        win = tkinter.Tk()
        win.title("S2SL")
        win.geometry("800x450+100+50")
        win.option_add("*Font", "맑은고딕 20")

        tkinter.Label(win, text="Speech to SignLanguage", pady=10).pack(side="top")
        # tkinter.Button(win, text="eng", command=lambda: switch_win(win, self.make_S2SL_win("eng"))).pack(side="bottom", pady="7")
        # tkinter.Button(win, text="kor", command=lambda: switch_win(win, self.make_S2SL_win("kor"))).pack(side="bottom", pady="7")
        # tkinter.Button(win, text="isl", command=lambda: switch_win(win, self.make_S2SL_win("isl"))).pack(side="bottom", pady="7")

        tkinter.Button(win, text="eng", command=lambda: switch_win(win, self.make_RT_S2SL_win("eng"))).pack(side="bottom", pady="7")
        tkinter.Button(win, text="kor", command=lambda: switch_win(win, self.make_RT_S2SL_win("kor"))).pack(side="bottom", pady="7")
        tkinter.Button(win, text="isl", command=lambda: switch_win(win, self.make_RT_S2SL_win("isl"))).pack(side="bottom", pady="7")

        return win

    def STSL(self, win: tkinter.Tk, ent: tkinter.Entry, lb: tkinter.Label, lang: str):
        lang.lower()
        if lang in "ko/kr/kor/korean":
            error_text = "잘못된 입력입니다. 숫자를 넣어주세요."
            recording_text = "녹음중..."
            check_text = "녹음된 문장을 확인/수정해주세요."
            confirm_text = "확인"
        else:
            error_text = "wrong input. please put number."
            recording_text = "recording..."
            check_text = "check the recognized text"
            confirm_text = "confirm"

        # get record sec
        try:
            rec_sec = int(ent.get())
        except ValueError:
            ent.delete(0, len(ent.get()))
            ent.insert(0, error_text)
            return None
        # recording
        lb.config(text=recording_text)
        if lang in "ko/kr/kor/korean":
            text = SpeechRec.STT(rec_sec, "ko-KR")
        else:
            text = SpeechRec.STT(rec_sec, "en-UR")
        if text is None:  # case of recorded nothing
            ent.delete(0, len(ent.get()))
            ent.insert(0, "couldn't recognize anything.")
            lb.config(text="set record second(int) :")
            return None

        # check recorded text
        tkinter.Label(win, text=check_text, font="맑은고딕 20").place(x=10, rely=0.3)
        ent = tkinter.Entry(win, width=50, font="맑은고딕 15")
        ent.insert(0, text)
        ent.place(x=10, rely=0.4)
        tkinter.Button(win, text=confirm_text, font="맑은고딕 20", command=lambda: vis()).place(x=10, rely=0.5)

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
            self.make_mainWin().mainloop()

    def make_S2SL_win(self, lang: str) -> tkinter.Tk:
        """lang: english(en/eng), korean(ko/kr/kor), international(int/isl/eng_isl)"""

        if lang in "en/eng/english":
            title = "eng S2SL"
            lb_text = "set record second(int) :"
            btn_text = "record"
        elif lang in "ko/kr/kor/korean":
            title = "kor S2SL"
            lb_text = "녹음할 시간을 입력해주세요(초(sec), 양수) :"
            btn_text = "녹음시작"
        elif lang in "int/isl/eng_isl/international":
            title = "isl S2SL"
            lb_text = "set record second(int) :"
            btn_text = "record"
        else:
            raise ValueError("Wrong language.")

        win = tkinter.Tk()
        win.title(title)
        win.geometry("800x450+100+50")
        win.option_add("*Font", "맑은고딕 20")

        lb = tkinter.Label(win, text=lb_text)
        ent = tkinter.Entry(win, font="맑은고딕 15", width="30")
        lb.grid(row=0, column=0, padx="10", pady="12")
        ent.grid(row=1, column=0, pady="12")

        tkinter.Button(win, background="red", command=lambda: switch_win(win, self.make_mainWin()),
                       text="<-").place(relx=0.92, rely=0.02)
        tkinter.Button(win, command=lambda: self.STSL(win, ent, lb, lang), text=btn_text).place(relx=0.45, rely=0.87)

        return win

    def RT_STSL(self, win: tkinter.Tk, lb: tkinter.Label, ent: tkinter.Entry, lang: str):
        # recording
        try:
            cycle_sec = int(ent.get())
        except ValueError:
            ent.delete(0, len(ent.get()))
            if lang == "kor":
                ent.insert(0, "정수(숫자)를 입력해 주세요 :")
            else:
                ent.insert(0, "PLZ put int(number) :")
            return None
        ent.destroy()
        lb.config(text="변환시작")
        lang = "ko-KR" if lang in "ko/kr/kor/korean" else "en-UR"

        t = threading.Thread(target=self.RT_Convert, args=[win, lang, cycle_sec])
        t.deamon = True
        t.start()

    def RT_Convert(self, win: tkinter.Tk, lang: str, cycle_sec: int):
        recorgnized_text = [""]
        announ_text = "인식된 텍스트 : " if lang == "ko-KR" else "recognized text : "

        lb = tkinter.Label(win)
        lb.grid(row=1, column=0, pady="12")

        t = threading.Thread(target=SpeechRec.RT_STT, args=[recorgnized_text, lang, cycle_sec])
        t.deamon = True
        t.start()

        while True:
            if recorgnized_text[0] is "":  # case of recorded nothing
                lb.config(text="")
                continue

            lb.config(text=announ_text + recorgnized_text[0])

            if lang in "en/eng/english":
                text_p = Preprocessing.eng_preprocessing(recorgnized_text[0])
                Vis_SignLang.vis_eng(text_p)
            elif lang in "ko/kr/kor/korean":
                text_p = Preprocessing.kor_preprocessing(recorgnized_text[0])
                Vis_SignLang.vis_kor(text_p)
            elif lang in "int/isl/eng_isl/international":
                text_p = Preprocessing.eng_isl_preprocessing(recorgnized_text[0])
                Vis_SignLang.vis_eng_isl(text_p)

            recorgnized_text[0] = ""

    def make_RT_S2SL_win(self, lang: str):
        if lang in "ko/kr/kor/korean":
            title = "kor S2SL"
            lb_text = "변환할 주기(몇 초 단위로 음성을 감지할지) 입력 :"
            btn_text = "변환시작"
        else:
            title = "eng/isl S2SL"
            lb_text = "set second of record cycle :"
            btn_text = "start convert"

        win = tkinter.Tk()
        win.title(title)
        win.geometry("800x450+100+50")
        win.option_add("*Font", "맑은고딕 20")

        lb = tkinter.Label(win, text=lb_text)
        lb.grid(row=0, column=0, padx="10", pady="12")
        ent = tkinter.Entry(win, font="맑은고딕 15", width="30")
        ent.grid(row=1, column=0, pady="12")

        win.title(title)
        win.geometry("800x450+100+50")
        win.option_add("*Font", "맑은고딕 20")

        tkinter.Button(win, background="red", command=lambda: switch_win(win, self.make_mainWin()),
                       text="<-").place(relx=0.92, rely=0.02)
        tkinter.Button(win, command=lambda: self.RT_STSL(win, lb, ent, lang), text=btn_text).place(relx=0.45, rely=0.87)

        return win


if __name__ == '__main__':
    # check_data_exist()
    stslc = S2SL_Converter()
