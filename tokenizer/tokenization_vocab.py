import MeCab
import pandas as pd
import re

def tokenize(text):
    # vocab text 전처리
    text = re.sub("(-었)|(편지 등을)|(꽃이)|(해가)|(鬼神)", "", text)
    text = re.sub("\W", "", text)

    # 문장 토큰화
    t = MeCab.Tagger()
    result_list = []
    for line in t.parse(text).split("\n"):
        result_list.append(line.split("\n")[0])
    return result_list



