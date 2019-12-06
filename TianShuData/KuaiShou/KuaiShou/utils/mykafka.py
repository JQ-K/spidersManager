from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError

class KafkaClient(object):

    def __init__(self, hbootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.producer = KafkaProducer(bootstrap_servers)

    @classmethod
    def from_settings(cls, conf_dir):
        conf_path = os.path.join(conf_dir, 'dbconf.ini')
        conf = configparser.ConfigParser()
        conf.read(conf_path)
        bootstrap_servers = conf.get('kafka', 'bootstrap_servers')

        return cls(bootstrap_servers)