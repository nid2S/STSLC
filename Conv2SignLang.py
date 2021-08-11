import pandas as pd
import matplotlib.pyplot as plt

def conv_eng(sents: list[list[list[str]]]):
    for sent in sents:
        for word in sent:
            for char in word:
                plt.imshow(plt.imread("./dataset/asl_data/"+char+".png"))
                plt.show()

def conv_kor(sents: list[list[str]]):
    pass

def conv_eng_isl(sents: list[list[str]]):
    pass


conv_eng([[['h', 'i']], [['m', 'y'], ['n', 'a', 'm', 'e'], ['i', 's'], ['n', 'i', 'd']]])
