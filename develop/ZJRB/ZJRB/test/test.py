import urllib.request
import urllib.parse
from lxml import etree
import json
import requests
import os
import time
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests_html import HTMLSession

session = HTMLSession()

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path="D://driver//chromedriver.exe", chrome_options=chrome_options)

def test():
    url = 'http://weibo.com/1036713140/Igj2um9gI'
    driver.get(url)
    html = driver.page_source
    print(html)

if __name__ == '__main__':
    test()
