import re
import time
import pandas as pd
import selenium.webdriver
from urllib.request import urlretrieve
from urllib.error import URLError
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException

def get_ksl_data():
    # dataset resource : https://sldict.korean.go.kr/front/sign/signList.do?top_category=CTE
    # word_len : 3847+1 (except duplicate : 3818)
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
    driver = selenium.webdriver.Chrome("D:\\python_util\\driver\\chromedriver.exe")
    driver.get("http://www.sematos.eu/isl.html")
    f = open("./dataset/isl_data/words.txt", "w+", encoding="UTF-8")
    count = 0
    page = 0
    while True:
        for i in range(22):
            for _ in range(page):  # when using back(), return to first page | Nothing changes when the page is over, so have to stop manually.
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
                time.sleep(2)
                src = driver.find_element_by_xpath('//div[@id="centre"]/div[@id="playermot"]/div/video/source[@type="video/mp4"]').get_attribute("src")

            urlretrieve(src, "./dataset/isl_data/"+str(count)+".mp4")
            f.write(str(count)+"\t"+word+"\n")
            print(str(count)+"\t"+word)
            count += 1

            driver.back()

        page += 1


def eng_preprocessing(sent: str):
    # ASL will be used char-level translate(of course word-level ASL exist, but we don't use).
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
