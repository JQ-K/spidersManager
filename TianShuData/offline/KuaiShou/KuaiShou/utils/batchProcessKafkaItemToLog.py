from pykafka import KafkaClient
import json

# kafka 相关信息及配置
KAFKA_HOSTS = 'zb2627:9092,zb2628:9092,zb2629:9092'
ZOOKEEPER_HOSTS = 'zb2627:2181,zb2628:2181,zb2629:2181'
KAFKA_TOPIC = 'kuaishou_data'
RESET_OFFSET_ON_START = False

client = KafkaClient(hosts=KAFKA_HOSTS,
                     zookeeper_hosts=ZOOKEEPER_HOSTS,
                     broker_version='0.10.1.0')
topic = client.topics[KAFKA_TOPIC]
partitions = topic.partitions
consumer = topic.get_simple_consumer(consumer_group='testConsumer',
                                     reset_offset_on_start=RESET_OFFSET_ON_START,
                                     auto_commit_enable=True,
                                     partitions=[partitions[0]])
cnt = 0
for message in consumer:
    try:
        if message is None:
            continue
        # 信息分为message.offset, message.value
        msg_value = message.value.decode()
        msg_value_dict = json.loads(msg_value)
        print(msg_value_dict)
        cnt += 1
        print(cnt)
    except Exception as e:
        print('Kafka message structure cannot be resolved :{}'.format(str(e)))
