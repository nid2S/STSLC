from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException
from urllib.request import urlretrieve
from urllib.error import URLError
from nltk import sent_tokenize
from typing import List
import selenium.webdriver
import gensim.downloader
import pandas as pd
import numpy as np
import time
import re

class tokenizer:
    def __init__(self):
        self.kor_embedding_size = 200
        self.isl_embedding_size = 300
        f = open("D:\\workspace\\Git_project\\STSLC\\tokenizer\\ko.vec", "r+", encoding="utf-8")
        self.d_kor = dict([(vec[0], vec.split()[1:]) for vec in f.read().split("\n")[1:] if vec != ""])
        self.model = gensim.downloader.load("fasttext-wiki-news-subwords-300")
        f.close()

    def tokenize_kor(self, word: str) -> List[float]:
        # preprocessing file(SL video)'s word
        word = re.sub("(-었)|(편지 등을)|(꽃이)|(해가)|(鬼神)", "", word)
        word = re.sub("\W", "", word)
        # get token
        result_list = []
        for char in word:
            if char in ["", "는", "이", "가", "에게", "을", "를"] or char not in self.d_kor:  # passing stopword, OOV
                continue
            if char in ["은", "다"] and len(result_list) > 1:  # "은", "다" have another meaning, so removed only not first.
                continue
            try:
                result_list.append(self.d_kor[char])
            except KeyError:
                continue

        # get vectors' mean
        if len(result_list) == 0:  # case of OOV
            return [0.]*self.kor_embedding_size
        result_list = sum(np.asarray(result_list, dtype=np.float32)) / len(result_list)
        return result_list.tolist()

    def tokenize_isl(self, word: str) -> List[float]:
        word = re.sub("\W", " ", word)
        result_list = []
        for subword in word.split():
            try:  # Each word in ISL having own meaning. so don't remove stop word, get every word's meaning
                result_list.append(self.model.get_vector(subword))
            except KeyError:
                continue

        if len(result_list) == 0:
            return [0.]*self.isl_embedding_size
        result_list = sum(np.asarray(result_list, dtype=np.float32)) / len(result_list)
        return result_list.tolist()


def get_ksl_data():
    # dataset resource : https://sldict.korean.go.kr/front/sign/signList.do?top_category=CTE
    print("----------start download----------")
    driver = selenium.webdriver.Chrome("D:\\python_util\\driver\\chromedriver.exe")
    driver.get('https://sldict.korean.go.kr/front/sign/signContentsView.do?current_pos_index=0&origin_no=10127&searchWay=&top_category=CTE&category=&detailCategory=&searchKeyword=&pageIndex=1&pageJumpIndex=')
    f = open("./dataset/ksl_data/words.txt", "w+", encoding="UTF-8")
    count = 0
    while True:
        try:
            # get sighLanguage video scr
            video_element = driver.find_element_by_xpath('//div[@class="view_content clear2"]/div[@class="fl"]/div[@class="tumb_b"]/a[@*]/video[@*]/source[@type="video/mp4"]')
            video_src = video_element.get_attribute("src")
            # get korean
            korean_element = driver.find_element_by_xpath('//div[@class="main_contents"]/form[@id="signViewForm"]/dl[@class="content_view_dis"]/dd')
            word = korean_element.text
            # save video, korean
            try:
                urlretrieve(video_src, "./dataset/ksl_data/"+str(count)+".mp4")
                f.write(str(count)+"\t"+word+"\n")
                print(str(count)+"\t"+word)
            except URLError:
                driver.refresh()
                continue
            count += 1
            # if end the list, break (or direct stop)
            driver.find_element_by_xpath('//div[@class="btn_set mt_30"]/a[@path="/images/tooltip/next.gif"]').click()

        except UnexpectedAlertPresentException:  # if error, refresh
            if count > 3850:  # word number + a(for error).
                break
            driver.refresh()
            continue

    driver.close()
    f.close()

def get_isl_data():
    # dataset resource : http://www.sematos.eu/isl.html
    print("----------start download----------")
    driver = selenium.webdriver.Chrome("D:\\python_util\\driver\\chromedriver.exe")
    driver.get("http://www.sematos.eu/isl.html")
    f = open("./dataset/isl_data/words.txt", "w+", encoding="UTF-8")
    count = 0
    page = 0
    while True:
        if count > 440:  # word len(according site)
            break
        for i in range(22):
            for _ in range(page):  # when using back(), return to first page | Nothing changes when the page is over, so coundition is word len.
                time.sleep(2)
                try:
                    driver.find_element_by_xpath('//div[@id="dico_mots"]/div/img[@class="rightt"]').click()
                except NoSuchElementException:
                    time.sleep(5)
                    driver.find_element_by_xpath('//div[@id="dico_mots"]/div/img[@class="rightt"]').click()

            time.sleep(2)  # if not loaded, raised IndexError.
            try:
                li_element = driver.find_elements_by_xpath('//div[@id="dico_mots"]/div/ul/li')[i]
                word = li_element.find_element_by_xpath('./a[@class="tooltip"]').text
                li_element.find_element_by_xpath('./a[@class="tooltip"]').click()
            except IndexError:
                time.sleep(5)
                li_element = driver.find_elements_by_xpath('//div[@id="dico_mots"]/div/ul/li')[i]
                word = li_element.find_element_by_xpath('./a[@class="tooltip"]').text
                li_element.find_element_by_xpath('./a[@class="tooltip"]').click()

            time.sleep(2)  # if not loaded, raised NoSuchElementException
            try:
                src = driver.find_element_by_xpath('//div[@id="centre"]/div[@id="playermot"]/div/video/source[@type="video/mp4"]').get_attribute("src")
            except NoSuchElementException:
                time.sleep(5)
                try:
                    src = driver.find_element_by_xpath('//div[@id="centre"]/div[@id="playermot"]/div/video/source[@type="video/mp4"]').get_attribute("src")
                except NoSuchElementException:  # if raise same error, regard data to don't exist, continue.
                    print("NoVideo\t"+word)
                    driver.back()
                    continue

            urlretrieve(src, "./dataset/isl_data/"+str(count)+".mp4")
            f.write(str(count)+"\t"+word+"\n")
            print(str(count)+"\t"+word)
            count += 1

            driver.back()

        page += 1


def eng_preprocessing(text: str):
    # ASL will be used char-level translate(of course word-level ASL exist, but we don't use).
    # lowcase, remove Abbreviated & non-(english+|'|,| |)char
    result_sent = []
    for sent in sent_tokenize(text):
        sent = re.sub(r"[^a-z0-9' ]", "", sent.lower())
        sent = re.sub(r"(n't|'m|'re|in'|'s)", r" \1", sent)

        abbDict = {"n't": "not", "'m": "am", "'re": "are", "in'": "ing", "'cause": "because"}  # ('s | s') are stil shorted form.
        sent_sr = pd.Series(sent.split()).map(lambda data: abbDict[data] if data in abbDict else data)

        # split word, divide char level
        result_sent.append([[char for char in word] for word in sent_sr.values])
    return result_sent

def kor_preprocessing(text: str) -> (List[List[List[float]]], List[List[str]]):
    # sents > sent > word(token_vec)
    # lower, remove other char, tokenize/stemming/normalize
    result_sent = []
    sents = []
    t = tokenizer()
    for sent in sent_tokenize(text.lower()):
        sent = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣a-z0-1 ]", r"", sent)
        result_sent.append([t.tokenize_kor(word) for word in sent.split()])
        t_sent = [word for word in sent.split()]
        if not t_sent == []:
            sents.append(t_sent)
    return result_sent, sents

def eng_isl_preprocessing(text: str):
    result_sent = []
    sents = []
    t = tokenizer()
    for sent in sent_tokenize(text.lower()):
        # TODO 문장을 나누는 방법(to accept 등)생각.
        result_sent.append([t.tokenize_kor(word) for word in sent.split()])
        t_sent = [word for word in sent.split()]
        if not t_sent == []:
            sents.append(t_sent)
    return result_sent, sents
