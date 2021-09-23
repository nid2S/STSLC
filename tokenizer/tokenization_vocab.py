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


ksl = pd.read_csv("D:\\workspace\\Git_project\\STSLC\\dataset\\ksl_data\\words.txt", sep="\t", names=["file_num", "word"])
file_num = []
word_origin = []
word_encoded = []
for i, row in ksl.iterrows():
    for word in row["word"].split(","):
        file_num.append(row["file_num"])
        word_origin.append(word)
        word_encoded.append(tokenize(word))
df = pd.DataFrame()
df["file_num"] = pd.Series(file_num)
df["word_origin"] = pd.Series(word_origin)
df["word_encoded"] = pd.Series(word_encoded)
df.to_csv("D:\\workspace\\Git_project\\STSLC\\dataset\\ksl_encoded_data.csv", index=False, header=False)  # header=[열이름], columns=[열이름]
