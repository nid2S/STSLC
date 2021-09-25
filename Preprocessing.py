import re
import time
import pandas as pd
import selenium.webdriver
from urllib.request import urlretrieve
from urllib.error import URLError
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException
from nltk import sent_tokenize
from gensim.models import Word2Vec
from typing import List
import MeCab


def tokenize(word: str) -> List[float]:
    # vocab text 전처리
    word = re.sub("(-었)|(편지 등을)|(꽃이)|(해가)|(鬼神)", "", word)
    word = re.sub("\W", "", word)
    # 문장 토큰화
    t = MeCab.Tagger()
    result_list = []
    # TODO 단어별로 임베딩 벡터화 | 거대 vocab을 가져와 mecab으로 토큰화, gensim/GloVe를 사용해 모델 생성/저장 후 사용
    for line in t.parse(word).split("\n"):
        w = line.split("\t")[0]
        if w in ["", "EOS"]:
            continue
        # w를 벡터화
        result_list.append(w)
    # result_list의 벡터들을 평균냄
    return result_list

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

def kor_preprocessing(text: str) -> List[List[List[float]]]:
    # sents > sent > word(token_vec)
    # lower, remove other char, tokenize/stemming/normalize
    result_sent = []
    for sent in sent_tokenize(text.lower()):
        sent = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ가-힣a-z0-1 ]", r"", sent)
        result_word = []
        for word in sent.split():
            res = tokenize(word)
            result_word.append(res)
        result_sent.append(result_word)
    return result_sent

def eng_isl_preprocessing(text: str):
    pass
