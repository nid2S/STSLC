from STSLC.Preprocessing import tokenizer
import pandas as pd

def get_ksl():
    # make csv_file
    ksl = pd.read_csv("D:\\workspace\\Git_project\\STSLC\\dataset\\ksl_data\\words.txt", sep="\t", names=["file_num", "word"])
    t = tokenizer()
    file_num = []
    word_origin = []
    word_encoded = []
    # put each word in list
    for i, row in ksl.iterrows():
        for word in row["word"].split(","):
            file_num.append(row["file_num"])
            word_origin.append(word)
            word_encoded.append(t.tokenize_kor(word))
    # save to csv with DataFrame
    df = pd.DataFrame()
    df["file_num"] = pd.Series(file_num)
    df["word_origin"] = pd.Series(word_origin)
    df["word_encoded"] = pd.Series(word_encoded)
    df.to_csv("D:\\workspace\\Git_project\\STSLC\\dataset\\ksl_encoded_data.csv", index=False, columns=["file_num", "word_origin", "word_encoded"])

def get_isl():
    isl = pd.read_csv("D:\\workspace\\Git_project\\STSLC\\dataset\\isl_data\\words.txt", sep="\t", names=["file_num", "word"])
    t = tokenizer()
    file_num = []
    word_origin = []
    word_encoded = []
    # put each word in list
    for i, row in isl.iterrows():
        for word in row["word"].split(","):
            file_num.append(row["file_num"])
            word_origin.append(word)
            word_encoded.append(t.tokenize_isl(word))
    # save to csv with DataFrame
    df = pd.DataFrame()
    df["file_num"] = pd.Series(file_num)
    df["word_origin"] = pd.Series(word_origin)
    df["word_encoded"] = pd.Series(word_encoded)
    df.to_csv("D:\\workspace\\Git_project\\STSLC\\dataset\\isl_encoded_data.csv", index=False, columns=["file_num", "word_origin", "word_encoded"])
    pass

