from pykafka import KafkaClient
import json
import time

from mysql import MySQLClient


KAFKA_HOSTS = 'zb2627:9092,zb2628:9092,zb2629:9092'
ZOOKEEPER_HOSTS = 'zb2627:2181,zb2628:2181,zb2629:2181'
KAFKA_TOPIC = 'kuaishou_data'
RESET_OFFSET_ON_START = True

MYSQL_HOST = '10.8.26.106'
MYSQL_USER = 'scrapy'
MYSQL_PASSWORD = 'Scrapy_123'
MYSQL_DATABASE = 'tianshuData'
MYSQL_KUAISHOU_SCRAPY_LOGS_TABLENAME = 'kuaishou_scrapy_logs'


def processDict(item, mysql_client):
    # print(item)
    msg = {}
    msg['item_type'] = item['spider_name']
    msg['is_successed'] = 1
    msg['scrapy_time'] = item['spider_datetime']

    if item['spider_name'] == 'kuaishou_shop_score':
        msg['item_id'] = item['userId']
    if item['spider_name'] == 'kuaishou_shop_product_list':
        msg['item_id'] = item['productId']
    if item['spider_name'] == 'kuaishou_shop_product_detail':
        msg['item_id'] = item['productId']
    if item['spider_name'] == 'kuaishou_shop_product_comment':
        msg['item_id'] = item['commentId']

    # mysql_client.insert(MYSQL_KUAISHOU_SCRAPY_LOGS_TABLENAME, msg)
    # mysql_client.commit()


def runBatch():
    mysql_client = MySQLClient(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, dbname=MYSQL_DATABASE)

    client = KafkaClient(hosts=KAFKA_HOSTS,
                         zookeeper_hosts=ZOOKEEPER_HOSTS,
                         broker_version='0.10.1.0')
    topic = client.topics[KAFKA_TOPIC]
    consumer = topic.get_simple_consumer(consumer_group='batchProcessKafkaItemToLog_data',
                                         reset_offset_on_start=RESET_OFFSET_ON_START,
                                         auto_commit_enable=True,
                                         )

    cnt = 0
    for message in consumer:
        try:
            if message is None:
                continue
            # 信息分为message.offset, message.value
            msg_value = message.value.decode()
            msg_value_dict = json.loads(msg_value)
            #msg_value_dict = eval(msg_value)
            processDict(msg_value_dict, mysql_client)
            cnt += 1
            if cnt % 10000 == 0:
                print(cnt)
            #print(cnt)
        except Exception as e:
            print('except :{}'.format(str(e)))
            print(cnt)
            print(message)

    mysql_client.close()

runBatch()
