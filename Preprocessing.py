import re
import time
import pandas as pd
import selenium.webdriver
from urllib.request import urlretrieve
from urllib.error import URLError

from selenium.common import exceptions
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException

def get_ksl_data():
    # dataset resource : https://sldict.korean.go.kr/front/sign/signList.do?top_category=CTE
    # word_len : 3847+1 (except duplicate : 3818)
    driver = selenium.webdriver.Chrome("D:\\python_util\\driver\\chromedriver.exe")
    driver.get('https://sldict.korean.go.kr/front/sign/signContentsView.do?current_pos_index=0&origin_no=10127&searchWay=&top_category=CTE&category=&detailCategory=&searchKeyword=&pageIndex=1&pageJumpIndex=')
    f = open("./dataset/ksl_data/words.txt", "a+", encoding="UTF-8")  # for unexpected finished, file type is a (have to change count)
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
    driver = selenium.webdriver.Chrome("D:\\python_util\\driver\\chromedriver.exe")
    driver.get("http://www.sematos.eu/isl.html")
    f = open("./dataset/isl_data/word.txt", "w+")
    count = 0
    while True:
        for i in range(22):
            time.sleep(2)  # if not loaded, raise IndexError.
            try:
                driver.find_elements_by_xpath('//div[@id="dico_mots"]/div/ul/li')[i]\
                    .find_element_by_xpath('./a[@class="tooltip"]').click()
            except IndexError:
                time.sleep(5)
                driver.find_elements_by_xpath('//div[@id="dico_mots"]/div/ul/li')[i]\
                    .find_element_by_xpath('./a[@class="tooltip"]').click()

            time.sleep(2)  # if not loaded, raise NoSuchElementException
            try:
                src = driver.find_element_by_xpath('//div[@id="centre"]/div[@id="playermot"]/div/video/source[@type="video/mp4"]').get_attribute("src")
            except NoSuchElementException:
                time.sleep(2)
                src = driver.find_element_by_xpath('//div[@id="centre"]/div[@id="playermot"]/div/video/source[@type="video/mp4"]').get_attribute("src")
            word = re.sub(r"\(\w+\)", "", driver.find_element_by_xpath('//div[@id="centre"]/h2[@id="titremot"]').text).strip()

            urlretrieve(src, "./dataset/isl_data/"+str(count)+".mp4")
            f.write(str(count)+"\t"+word+"\n")
            count += 1

            driver.back()

        try:
            driver.find_element_by_xpath('//div[@id="dico_mots"]/div/img[@class="rightt"]').click()
        except NoSuchElementException:
            pass  # have to stop manually


def eng_preprocessing(sent: str):
    # lowcase, remove Abbreviated & non-english(+|'|,| |)char
    sent = re.sub(r"[^a-z0-9' ]", "", sent.lower())
    sent = re.sub(r"s'", r"s have", sent)
    sent = re.sub(r"(n't|'m|'re|in'|'s)", r" \1", sent)

    abbDict = {"n't": "not", "'m": "am", "'re": "are", "in'": "ing", "'cause": "because"}  # 's > have? is? | wanna, gonna don't divide.
    sent_sr = pd.Series(sent.split).map(lambda row: abbDict[row] if row in abbDict else row)

    # split word, divide char level
    result_sent = [[char for char in word] for word in sent_sr.values]
    return result_sent


def kor_preprocessing(sent: str):
    pass


def eng_isl_preprocessing(sent: str):
    pass


get_isl_data()
