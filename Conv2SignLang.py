import pandas as pd
import matplotlib.pyplot as plt

def conv_eng(sents: list[list[list[str]]]):
    # sent > word > char
    plt.style.use('seaborn-white')
    for sent in sents:
        for i, word in enumerate(sent):
            for j, char in enumerate(word):
                # 플롯간 간격 조절
                idx = i*max(len(w) for w in sent) + (j+1)
                plt.subplot(len(sent), max(len(w) for w in sent), idx)  # (row, col) = (num of words, max length of word). make new screen for each sent.
                plt.title(char)
                plt.xticks([])
                plt.yticks([])
                plt.imshow(plt.imread("./dataset/asl_data/"+char+".png"))
        plt.show()


def conv_kor(sents: list[list[str]]):
    pass

def conv_eng_isl(sents: list[list[str]]):
    pass


conv_eng([[['h', 'i']], [['m', 'y'], ['n', 'a', 'm', 'e'], ['i', 's'], ['n', 'i', 'd']]])
