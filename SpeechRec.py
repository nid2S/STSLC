import speech_recognition as sr
import wave
import pyaudio
import os


def __record(record_sec, output_file_name, FORMAT, CHANNELS, CHUNK, RATE):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, frames_per_buffer=CHUNK)
    frames = []
    # print("녹음시작")
    for i in range(int(RATE / CHUNK * record_sec)):
        data = stream.read(CHUNK)
        frames.append(data)
    # print("녹음종료")
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(output_file_name, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


def STT(record_sec: int,
        record_lang: str,
        output_file_name="./audio/output.wav",
        FORMAT=pyaudio.paInt16,
        CHANNELS=1,
        CHUNK=1024,
        RATE=44100):
    """lang - ko-KR or en-UR"""

    output_file_name = os.path.abspath(output_file_name)
    if not os.path.exists(output_file_name):
        os.mkdir(output_file_name)

    __record(record_sec, output_file_name, FORMAT, CHANNELS, CHUNK, RATE)
    recognizer = sr.Recognizer()
    with sr.AudioFile(output_file_name) as source:
        audio = recognizer.record(source)

    try:
        txt = recognizer.recognize_google(audio_data=audio, language=record_lang)
    except sr.UnknownValueError:
        print("언어가 인지되지 않았습니다")
        return None

    # print("인지된 문자 : " + txt)

    return txt
