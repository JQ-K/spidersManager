# -*- coding: utf-8 -*-
import scrapy
import time, random, os
import subprocess
import re, json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from scrapy_splash import SplashRequest
from fontTools.ttLib import TTFont
from scrapy.utils.project import get_project_settings
from pykafka import KafkaClient
from loguru import logger

from KuaiShou.items import KuaishouUserInfoIterm


class KuaishouFontscnDecoderSpider(scrapy.Spider):
    name = 'kuaishou_fontscn_decoder'
    custom_settings = {
        'ITEM_PIPELINES': {
            'KuaiShou.pipelines.KuaishouKafkaPipeline': 700,
            'KuaiShou.pipelines.KuaishouUserSeedsMySQLPipeline': 702,
            'KuaiShou.pipelines.KuaishouScrapyLogsMySQLPipeline': 703,
        },
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': random.randint(1, 2),
        # 'CONCURRENT_REQUESTS_PER_IP' : 1,
        'DOWNLOADER_MIDDLEWARES':
            {
                # 'KuaiShou.middlewares.KuaishouDownloaderMiddleware': 727,
                'scrapy_splash.SplashCookiesMiddleware': 723,
                'scrapy_splash.SplashMiddleware': 725,
                'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
            },
        'SPIDER_MIDDLEWARES':
            {
                'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
            },
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'SPLASH_URL': 'http://localhost:8050/',
        'COOKIES_ENABLED': 'False'
    }

    def start_requests(self):
        # 设置加载完整的页面
        lua_load_base = """
            function main(splash, args)
              args = {
                url = "%s"
              }
              assert(splash:go(args.url))
              assert(splash:wait(1))
              splash:evaljs("window.onload")
              assert(splash:wait(3))
              assert(splash:go(args.url))
              assert(splash:wait(1))
              splash:evaljs("window.onload")
              assert(splash:wait(3))
              return {
                html = splash:html(),
                png = splash:png(),
                har = splash:har(),
                cookies = splash:get_cookies(),
              }
            end

        """
        settings = get_project_settings()
        # 配置kafka连接信息
        kafka_hosts = settings.get('KAFKA_HOSTS')
        kafka_topic = settings.get('KAFKA_USERINFO_SEEDS_TOPIC')
        logger.info('kafka info, hosts:{}, topic:{}'.format(kafka_hosts, kafka_topic))
        client = KafkaClient(hosts=kafka_hosts)
        topic = client.topics[kafka_topic]
        # 配置kafka消费信息
        consumer = topic.get_balanced_consumer(
            consumer_group='test',  # self.name,
            managed=True,
            auto_commit_enable=True,
            auto_commit_interval_ms=3000
        )

        # 获取被消费数据的偏移量和消费内容
        for message in consumer:
            try:
                if message is None:
                    continue
                # 信息分为message.offset, message.value
                logger.info('KAFKA offset: %s ' % message.offset)
                msg_value = message.value.decode()
                msg_value_dict = eval(msg_value)
                if 'spider_name' not in list(msg_value_dict.keys()):
                    logger.warning('Excloude key: spider_name, msg: {}'.format(msg_value))
                    continue
                if msg_value_dict['spider_name'] != 'kuaishou_user_seeds':
                    continue
                logger.info(msg_value_dict)
                principal_id = msg_value_dict['principalId']
                start_url = 'http://live.kuaishou.com/search/?keyword={pid}'.format(pid=principal_id)
                logger.info(start_url)
                # 判断SplashServer服务是否正常
                # child = subprocess.Popen(["pgrep", "-f", '/usr/bin/docker-proxy'], stdout=subprocess.PIPE, shell=False)
                # pid = child.communicate()[0].decode('utf-8')
                # if pid == '':
                #     os.system('sudo docker pull scrapinghub/splash')
                #     os.system('sudo docker run -d -p 8050:8050 scrapinghub/splash')
                lua_load_all = lua_load_base % start_url
                headers = {
                    "Host": "live.kuaishou.com",
                    "Connection": "keep-alive"
                }
                yield SplashRequest(start_url, callback=self.fontscn_decoder, endpoint='execute', headers=headers,
                                    method='GET',
                                    meta={'msg_value_dict': msg_value_dict}, args={'lua_source': lua_load_all},
                                    cache_args=['lua_source'])


            except Exception as e:
                logger.warning('Kafka message[{}] failed ！ :{}'.format(str(msg_value_dict), e))

    def fontscn_decoder(self, response):
        """
        :param response:
        :return:
        """
        n_set = [chr(i) for i in range(48, 58)]
        s_char_set = [chr(i) for i in range(97, 122)]
        total_set = n_set + s_char_set
        msg_value_dict = response.meta['msg_value_dict']
        cookie_str = ''
        for para in response.cookiejar:
            cookie_k, cookie_v = re.findall('([^\s]+)=([^\s]+)', str(para))[0]
            if cookie_k not in ['client_key', 'clientid', 'did', 'kuaishou.live.bfb1s']:
                continue
            if cookie_k == 'client_key':
                # 构造client_key值
                n_str = "".join(random.sample(n_set, 4))
                ns_str = "".join(random.sample(total_set, 4))
                cookie_v = n_str + ns_str
            cookie_str += '{}={}; '.format(cookie_k, cookie_v)
        time_float = time.time()
        hm_lvt_value = "".join(random.sample(total_set, 32))
        cookie_str = '{}didv={}; Hm_lvt_{}={}'.format(cookie_str, int(time_float * 1000), hm_lvt_value, int(time_float))
        logger.info(cookie_str)
        kuaishou_user_info_iterm = KuaishouUserInfoIterm()
        principal_id = re.findall('keyword=([^\?]+)', response.url)[0]
        r_text = response.text
        author_list = response.xpath('//*[@class="author-list"]/li')
        is_successed = -1
        kuaishou_user_info_iterm['spider_name'] = self.name
        kuaishou_user_info_iterm['principalId'] = principal_id
        if author_list == []:
            kuaishou_user_info_iterm['is_successed'] = -2
            return kuaishou_user_info_iterm
        for autor_card in author_list:
            href_list = autor_card.xpath('//div[@class="profile-card-user-info"]/a/@href').extract()
            if '/profile/{pid}'.format(pid=principal_id) not in href_list: continue
            user_info_counts_list = autor_card.xpath('//p[@class="profile-card-user-info-counts"]/text()').extract()
            if user_info_counts_list == []:
                continue
            # logger.info(user_info_counts_list)
            user_info_counts_string = user_info_counts_list[0].replace(' ', '').replace('\n', '')
            # logger.info(user_info_counts_string)
            res = re.search('([^\s]+)粉丝\s+([^\s]+)关注\s+([^\s]+)作品', user_info_counts_string)

            for i in range(3):
                try:
                    mapping = self.get_mapping(r_text)
                    break
                except:
                    pass
            is_successed = 1
            msg_value_dict['fan'] = self.decrypt_str(res.group(1), mapping)
            msg_value_dict['follow'] = self.decrypt_str(res.group(2), mapping)
            msg_value_dict['photo'] = self.decrypt_str(res.group(3), mapping)
        msg_value_dict['is_successed'] = is_successed
        user_id = msg_value_dict['userId']
        settings = get_project_settings()
        headers = {
            "accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "content-type": "application/json",
            "Origin": "https://live.kuaishou.com",
            "Referer": response.url,
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Cookie": cookie_str
        }
        search_overview_query = settings.get('SEARCH_OVERVIEW_QUERY')
        search_overview_query['variables']['keyword'] = '{}'.format(user_id)
        # logger.info(json.dumps(search_overview_query))
        yield scrapy.Request('http://live.kuaishou.com/m_graphql', headers=headers,
                             body=json.dumps(search_overview_query),
                             method='POST',
                             meta={'bodyJson': search_overview_query, 'msg_value_dict': msg_value_dict},
                             callback=self.parse_search_overview, dont_filter=True
                             )

    def parse_search_overview(self, response):
        msg_value_dict = response.meta['msg_value_dict']
        rsp_search_overview_json = json.loads(response.text)
        pc_search_overview = rsp_search_overview_json['data']['pcSearchOverview']
        search_overview_list = pc_search_overview['list']
        for search_overview in search_overview_list:
            if search_overview['type'] != 'authors': continue
            search_overview_authors = search_overview['list']
            if search_overview_authors == []: continue
            author_info = search_overview_authors[0]
            kuaishou_user_info_iterm = KuaishouUserInfoIterm()
            logger.info('Search userinfo reslut: {}'.format(str(author_info)))
            kuaishou_user_info_iterm['spider_name'] = self.name
            kuaishou_user_info_iterm['userId'] = msg_value_dict['userId']
            kuaishou_user_info_iterm['kwaiId'] = author_info['id']
            kuaishou_user_info_iterm['principalId'] = author_info['id']
            kuaishou_user_info_iterm['nickname'] = author_info['name']
            kuaishou_user_info_iterm['avatar'] = author_info['avatar']
            kuaishou_user_info_iterm['sex'] = author_info['sex']
            kuaishou_user_info_iterm['description'] = author_info['description']
            kuaishou_user_info_iterm['fan'] = msg_value_dict['fan']
            kuaishou_user_info_iterm['follow'] = msg_value_dict['follow']
            kuaishou_user_info_iterm['photo'] = msg_value_dict['photo']
            kuaishou_user_info_iterm['is_successed'] = msg_value_dict['is_successed']
            return kuaishou_user_info_iterm

    def get_mapping(self, page):
        m = re.search('(http.*?.woff)', page)
        if m:
            woff_link = m.group(1)
            headers1 = {
                'Host': "static.yximgs.com",
                'Connection': "keep-alive",
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
                'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                'Accept-Encoding': "gzip, deflate, br",
            }
            woff_res = requests.get(woff_link, headers=headers1, verify=False)
            file_name = woff_link.split('/')[-1]
            with open(file_name, 'wb') as f:
                f.write(woff_res.content)
            mapping = self.create_mapping(file_name)
            os.remove(file_name)
            return mapping

    def create_mapping(self, font_file):
        """ 打开字体文件并创建字符和数字之间的映射. """
        # 打开字体文件，加载glyf
        font = TTFont(font_file)
        glyf = font.get('glyf')
        current_map = {}
        # 创建当前字体文件的数字映射
        for i in glyf.keys():
            # 忽略不是uni开头的字符
            if not i.startswith('uni'):
                continue
            c = glyf[i]
            number = self.get_number_offset(c)
            # 发现有字符不在已有的集合中, 抛出异常.
            if number is None:
                print((c.yMax, c.xMax, c.yMin, c.xMin))
                raise Exception
            current_map[i.strip('uni')] = number
        # print(json.dumps(current_map, indent=4))
        return current_map

    def get_number_offset(self, c, max_offset=20):
        font_map = {
            (0, 0, 0, 0): ' ',
            (729, 526, -6, 32): '0',
            (726, 363, 13, 98): '1',
            (732, 527, 13, 32): '2',
            (730, 525, -6, 25): '3',
            (731, 536, 13, 26): '4',
            (717, 526, -5, 33): '5',
            (732, 530, -5, 39): '6',
            (717, 536, 13, 38): '7',
            (731, 525, -7, 33): '8',
            (730, 521, -7, 37): '9',
        }

        """ 根据偏移量计算映射出来的数字 """
        number = None
        # i, j 分别代表y和x的偏移量
        for i in range(max_offset + 1):
            for j in range(max_offset + 1):
                # 正向偏移
                number = font_map.get((c.yMax + i, c.xMax + j, c.yMin + i, c.xMin + j))
                if number:
                    # print('offset x:{} y:{}'.format(i,j))
                    return number
                # 负向偏移
                number = font_map.get((c.yMax - i, c.xMax - j, c.yMin - i, c.xMin - j))
                if number:
                    # print('offset x:{} y:{}'.format(i,j))
                    return number
        return number

    def decrypt_font(self, charater, mapping):
        """ 解密单个字符，如果可以解密就输出解密后的数字，否则原样返回"""
        s = charater.encode('unicode_escape').decode().strip('\\').upper().strip('U')
        res = mapping.get(s)
        return res if res else charater

    def decrypt_str(self, s, mapping):
        """ 解密字符串， 不需要解密的部分原样返回 """
        res = ''
        for c in s:
            res = res + self.decrypt_font(c, mapping)
        return res