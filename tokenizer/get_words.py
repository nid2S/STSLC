import pandas as pd
import re
from hgtk.text import decompose


def get_KSLwords():
    ksl = pd.read_csv("D:\\workspace\\Git_project\\STSLC\\dataset\\ksl_data\\words.txt", sep="\t", names=["file_num", "word"])
    vocab = []
    for words in ksl["word"]:
        for word in words.split(","):
            # 품사(동사/관형형 전성어미/일반명사)판별 | vocab속 다로 끝나는 단어중 동사가 아닌 단어는 셋 뿐임
            if list(word)[-1] == "다" and word not in ["사이다", "다", "바다"]:
                tag = "VV"
            elif "-" in word:
                tag = "ETM"
            else:
                tag = "NNG"

            # 단어 정제
            word = re.sub("(-었)|(편지 등을)|(꽃이)|(해가)|(鬼神)", "", word)
            word = re.sub("[-¹()]", "", word)
            # 종성 여부 판별
            is_last = "T" if len(decompose("안녕", compose_code=" ").split()[-1]) == 3 else "F"
            # 형식에 맞게 합침
            line = ",".join([word, "", "", "", tag, "*", is_last, word, "*", "*", "*", "*"]) + "\n"
            if line not in vocab:  # 중복된 단어를 제거
                vocab.append(line)

    with open("D:\\workspace\\Git_project\\STSLC\\dataset\\ksl.csv", "w+", encoding="UTF-8") as f:
        f.writelines(vocab)


def get_ISLwords():
    pass


def get_output(output):
    result = []
    for line in output.split("\n"):
        result.append(line.split("\t")[0])
    return result
def check_in(output_list):
    ksl = pd.read_csv("D:\\workspace\\Git_project\\STSLC\\dataset\\ksl_data\\words.txt", sep="\t",
                      names=["file_num", "word"])["word"]
    for word in output_list:
        if word in ["", "EOS"]:
            continue
        isin = ksl.isin([word]).sum() > 0
        print(word + " | " + str(isin))



