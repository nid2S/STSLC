import pandas as pd
import re
# dataset : aihub - 수어데이터셋 (https://aihub.or.kr/keti_data_board/language_intelligence)
# len(words+sent) : 524 | words : 419 | forward(include duplicate) : 5240

# data_info = pd.read_excel("D:\\data\\SL_data\\KETI-2017-SL-Annotation-v2_1.xlsx")\
#     .drop(['번호', '언어 제공자 ID', '취득연도', 'Unnamed: 7', 'Unnamed: 8'], axis=1)
# data_info = data_info[data_info["방향"] == "정면"].drop_duplicates("한국어", ignore_index=True)\
#     .drop(['방향', '타입(단어/문장)'], axis=1)
#
# with open("./dataset/data.txt", "a+", encoding="UTF-8") as f:
#     for row in data_info.values:
#         f.write(row[0]+"\t")
#         f.write(str(row[1])+"\n")

# data_info = pd.read_csv("D:\\workspace\\Git_project\\STSLC\\dataset\\data.txt", sep="\t", names=["파일명", "한국어"], header=None)
# data_info.sort_index(ascending=False).reset_index().drop("index", axis=1, inplace=True)
# data_info.to_csv("D:\\workspace\\Git_project\\STSLC\\dataset\\data.csv")
