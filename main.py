from STSLC import SpeechRec, Preprocessing, Vis_SignLang
# (음성 인식 후 저장 > 불러와 STT) > 전처리(토큰화, 임베딩, 패딩) > 수화로 변환(전처리 후 단어에 맞춰 변환) > 변환된 수화 출력(창에 띄움)
# 라이브러리 상속을 나눠 속도 증진 필요?
Vis_SignLang.vis_eng(Preprocessing.eng_preprocessing("hi. my name is none. but, you have name right? so plz give me your name."))

