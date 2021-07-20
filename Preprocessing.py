import time
import selenium.webdriver
from selenium.common.exceptions import ElementNotInteractableException
from urllib.request import urlretrieve

driver = selenium.webdriver.Chrome("D:\\python_util\\driver\\chromedriver.exe")
driver.get('https://sldict.korean.go.kr/front/sign/signList.do?top_category=CTE')  # dataset resource

f = open("./dataset/ksl_data/_words.txt", "w+")

count = 0
driver.find_element_by_class_name("hand_thumb").click()
while True:
    video_element = driver.find_element_by_xpath('//div[@class="view_content clear2"]/div[@class="fl"]/div[@class="tumb_b"]/a[@*]/video[@*]/source[@type="video/mp4"]')
    video_src = video_element.get_attribute("src")

    korean_element = driver.find_element_by_xpath('//div[@class="main_contents"]/form[@id="signViewForm"]/dl[@class="content_view_dis"]/dd')
    word = korean_element.text

    f.write(str(count)+"\t"+word+"\n")
    urlretrieve(video_src, "./dataset/ksl_data/"+str(count)+".mp4")
    count += 1

    try:
        driver.find_element_by_xpath('//div[@class="btn_set mt_30"]/a[@path="/images/tooltip/next.gif"]').click()
    except ElementNotInteractableException:
        break

driver.close()
f.close()
