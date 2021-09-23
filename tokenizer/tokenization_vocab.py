import MeCab
import pandas as pd
import re

def get_ksl():
    def tokenize(text):
        # vocab text 전처리
        text = re.sub("(-었)|(편지 등을)|(꽃이)|(해가)|(鬼神)", "", text)
        text = re.sub("\W", "", text)

        # 문장 토큰화
        t = MeCab.Tagger()
        result_list = []
        for line in t.parse(text).split("\n"):
            w = line.split("\t")[0]
            if w in ["", "EOS"]:
                continue
            result_list.append(w)
        return result_list

    # make csv_file
    ksl = pd.read_csv("D:\\workspace\\Git_project\\STSLC\\dataset\\ksl_data\\words.txt", sep="\t", names=["file_num", "word"])
    file_num = []
    word_origin = []
    word_encoded = []
    # put each word in list
    for i, row in ksl.iterrows():
        for word in row["word"].split(","):
            file_num.append(row["file_num"])
            word_origin.append(word)
            word_encoded.append(tokenize(word))
    # save to csv with DataFrame
    df = pd.DataFrame()
    df["file_num"] = pd.Series(file_num)
    df["word_origin"] = pd.Series(word_origin)
    df["word_encoded"] = pd.Series(word_encoded)
    df.to_csv("D:\\workspace\\Git_project\\STSLC\\dataset\\ksl_encoded_data.csv", index=False, header=False, columns=["file_num", "word_origin", "word_encoded"])


