# 음성 인식 후 저장 > 불러와 STT > 전처리(토큰화, 임베딩, 패딩) > 수화로 변환(레이블 정수로 부여/번역기처럼 S2S?) > 변환된 수화 출력(창에 띄움)
import speech_recognition as sr
import pyaudio

