import pandas as pd
# dataset : aihub - 수어데이터셋 (https://aihub.or.kr/keti_data_board/language_intelligence)
# 엑셀파일에서 방향이 정면이고 단어(문장도?)가 중복되지 않는 행들의 단어+파일명을 저장 > 나온 단어들과 데이터 양을 보고 S2S/레이블링, 전처리, 학습 방법 등을 생각.
# len(words+sent) : 524 | words : 419 | forward(include duplicate) : 5240

data_info = pd.read_excel("D:\\data\\SL_data\\KETI-2017-SL-Annotation-v2_1.xlsx")\
    .drop(['Unnamed: 7', 'Unnamed: 8'], axis=1)
data_info = data_info[data_info["방향"] == "정면"].drop_duplicates("한국어", ignore_index=True)

print(len(data_info))
