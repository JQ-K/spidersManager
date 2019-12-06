import requests
from bs4 import BeautifulSoup
headers = {
"user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"
}
r = requests.get('https://haokan.baidu.com/v?vid=16335743810432281251',headers = headers)

soup = BeautifulSoup(r.text,'html')

page_data = soup.find_all('script',{"id":"_page_data"})[0].text.replace("window.__PRELOADED_STATE__ = ",'')
print('page_data')
print(page_data)
