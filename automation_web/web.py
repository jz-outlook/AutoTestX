import time

from selenium import webdriver


def web_automation_test():
    driver = webdriver.Chrome()

    # 打开网页
    driver.get('https://baidu.com')
    time.sleep(10)
