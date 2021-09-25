import pandas as pd
import MeCab
import re
from gensim.models import Word2Vec

def kor_():
    talk = pd.read_csv("C:\\Users\\user\\Downloads\\talk.txt", sep="\t", names=["a1", "a2", "sent"])
    kor = pd.read_csv("C:\\Users\\user\\Downloads\\kor.txt", sep="\t", names=["eng", "kor", "info"])
    t = MeCab.Tagger()

    sents = talk["sent"].append(kor["kor"])
    result = []
    for sent in sents:
        sent = re.sub("\W", " ", sent).strip()
        encoded_sent = []
        for line in t.parse(sent).split("\n"):
            w = line.split("\t")[0]
            if w in ["", "EOS"]:
                continue
            encoded_sent.append(w)
        result.append(",".join(encoded_sent)+"\n")

    with open("D:\\workspace\\Git_project\\STSLC\\dataset\\encoded_sents_for_embedding.csv", "w+", encoding="utf-8") as f:
        f.writelines(result)

def make_model():
    vocab = open("D:\\workspace\\Git_project\\STSLC\\dataset\\encoded_sents_for_embedding.csv", "r+", encoding="utf-8").readlines()
    # train model
    model = Word2Vec(vocab, min_count=1)
    # summarize loaded_model/vocabulary
    print(model)
    print(list(model.wv.vocab))

    # access vector for one word
    print(model['sentence'])
    # save model
    model.save('model.bin')
    # load model
    new_model = Word2Vec.load('model.bin')
    print(new_model)

