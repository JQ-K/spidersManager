
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
'''chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')'''
driver = webdriver.Chrome(executable_path="D://driver//chromedriver.exe", chrome_options=chrome_options)


def test():
    url = 'https://haokan.baidu.com/v?vid=16335743810432281251'
    driver.get(url)
    html = driver.page_source
    print(html)


if __name__ == '__main__':
    test()
