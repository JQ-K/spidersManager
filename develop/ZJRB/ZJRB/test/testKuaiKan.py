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


def getBookUrl(url):
    #headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}
    html = requests.get(url).text
    page_info = etree.HTML(html)
    hrefList = page_info.xpath('//a[@class="itemLink"]/@href')
    titleList = page_info.xpath('//span[@class="itemTitle"]/text()')
    #print(hrefList)
    #print(titleList)
    href_title_map = {}
    for x, y in zip(hrefList, titleList):
        href_title_map[x] = y
    #print(href_title_map)
    return href_title_map

def getHuaUrl(url):
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"}
    html = requests.get(url).text
    page_info = etree.HTML(html)
    huaHrefList = page_info.xpath('//div[@class="title fl"]/a/@href')
    return huaHrefList

def getImageUrl(huaUrl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
    #print(huaUrl)
    driver.get(huaUrl)
    html = driver.page_source
    #print(html)

    '''r = session.get(huaUrl,verify=False)
    r.html.render()  # 首次使用，自动下载chromium
    html = r.text'''

    page_info = etree.HTML(html)
    imgUrlList = page_info.xpath('//div[@class="imgList"]/img/@data-src')
    return imgUrlList

def downloadImage(url, path):
    try:
        urlretrieve(url, path)
    except OSError as err:
        print('exception..............')
        print(err)


if __name__ == '__main__':
    host = "https://www.kuaikanmanhua.com"
    url = "https://www.kuaikanmanhua.com/tag/58?state=1&page=1"
    dir = "D://download//kuaikanmanhua//58//"

    page = 1
    titlecnt = 0

    while True:
        if page > 4:
            break
        url = "https://www.kuaikanmanhua.com/tag/58?state=1&page=%d"%page
        page += 1

        href_title_map = getBookUrl(url)

        for href, title in href_title_map.items():
            titleFolderName = str(titlecnt) + "_" + title
            os.mkdir(dir + titleFolderName)
            titlecnt += 1
            bookUrl = host + href
            print(bookUrl)
            print(title)
            huaHrefList = getHuaUrl(bookUrl)
            print(huaHrefList)
            huacnt = 0
            for huaHref in huaHrefList:
                huaFolderName = str(huacnt)
                os.mkdir(dir + titleFolderName + "//" + huaFolderName)
                huacnt += 1
                huaUrl = host + huaHref
                print(huaUrl)
                imgUrlList = getImageUrl(huaUrl)
                print(imgUrlList)
                imgcnt = 0
                for imgUrl in imgUrlList:
                    imgName = str(imgcnt) + ".jpg"
                    imgcnt += 1
                    path = dir + titleFolderName + "//" + huaFolderName + "//" + imgName
                    downloadImage(imgUrl, path)
                time.sleep(1)

