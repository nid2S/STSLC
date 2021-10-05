from typing import List
import speech_recognition as sr
import wave
import pyaudio
import os


def __record(record_sec, output_file_name, FORMAT, CHANNELS, CHUNK, RATE):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, frames_per_buffer=CHUNK, input=True)
    frames = []
    for i in range(int(RATE / CHUNK * record_sec)):
        data = stream.read(CHUNK)
        frames.append(data)
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

    return txt

def RT_STT(recorded_text: List[str], lang: str = "ko-KR", record_cycle_sec: int = 5):
    RATE = 44100
    CHUNK = 1024
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, frames_per_buffer=CHUNK, input=True)

    while True:
        frames = []
        stream.start_stream()
        for i in range(int(RATE / CHUNK * record_cycle_sec)):
            data = stream.read(CHUNK)
            frames.append(data)
        frames = b''.join(frames)
        stream.stop_stream()

        # AudioData
        recognizer = sr.Recognizer()
        audio = sr.AudioData(frame_data=frames, sample_rate=RATE, sample_width=1)

        try:
            txt = recognizer.recognize_google(audio_data=audio, language=lang)
            recorded_text[0] = txt
        except sr.UnknownValueError:
            print("언어가 인지되지 않았습니다")
            recorded_text[0] = ""



