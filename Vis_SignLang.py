import pandas as pd
import matplotlib.pyplot as plt

def vis_eng(sents: list[list[list[str]]]):
    # sent > word > char
    plt.style.use('seaborn-white')
    for sent in sents:
        for i, word in enumerate(sent):
            for j, char in enumerate(word):
                idx = i * max(len(w) for w in sent) + (j+1)
                plt.subplot(len(sent), max(len(w) for w in sent), idx)  # (row, col) = (num of words, max length of word). make new screen for each sent.
                plt.subplots_adjust(wspace=0, hspace=0.45)  # control(adjust) gap between plots
                plt.title(char)
                plt.xticks([])
                plt.yticks([])
                plt.imshow(plt.imread("./dataset/asl_data/"+char+".png"))
        plt.show()


def vis_kor(sents: list[list[str]]):
    pass

def vis_eng_isl(sents: list[list[str]]):
    pass


vis_eng([[['h', 'i']], [['m', 'y'], ['n', 'a', 'm', 'e'], ['i', 's'], ['n', 'i', 'd']]])
