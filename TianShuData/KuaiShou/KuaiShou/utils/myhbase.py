import zookeeper
from thrift.transport import TSocket  
from thrift.transport import TTransport  
from thrift.protocol import TBinaryProtocol  
from hbase.ttypes import Mutation
#from hbase.ttypes import BatchMutation
    
from hbase import Hbase  
import traceback
import time
from twisted.python import log

class HbaseClient(object):
    
    def __init__(self, retrys=3):
        self.transport = None
        self.retry_times = retrys 
        
    # @classmethod
    # def from_settings(cls, settings):
    #     znode = settings.get('thrift_znode')
    #     zkhost = settings.get('zookeeper_host')
    #     zkport = settings.get('zookeeper_port')
    #     retrys = settings.get('retrys')
    #
    #     ins = cls(retrys)
    #     ins.initWithZookeeper(znode, zkhost, zkport, retrys)
    #     return ins

    @classmethod
    def from_settings(cls, conf_dir):
        conf_path = os.path.join(conf_dir, 'dbconf.ini')
        conf = configparser.ConfigParser()
        conf.read(conf_path)
        znode = conf.get('hbase', 'thrift_znode')
        zkhost = conf.get('hbase', 'zookeeper_host')
        zkport = conf.get('hbase', 'zookeeper_port')
        retrys = conf.get('hbase', 'retrys')

        ins = cls(retrys)
        ins.initWithZookeeper(znode, zkhost, zkport, retrys)
        return ins

    def initWithZookeeper(self, hbaseThriftZnode, 
            zookeeperHost, zookeeperPort, retrys = 3):
        # get thrift from zookeeper if zookeeper configured in settings
        self.hbase_thrift_znode = hbaseThriftZnode
        self.zookeeper_host = zookeeperHost
        self.zookeeper_port = zookeeperPort
        self._getThriftServerFromZookeeper()
        self._openHbaseClient()

    def _getThriftServerFromZookeeper(self):
        self.hd = zookeeper.init("%s:%s" % (self.zookeeper_host, self.zookeeper_port))
        self.children = zookeeper.get_children(self.hd, self.hbase_thrift_znode)
        # random get a thrift server
        import random
        index = random.randint(0, len(self.children)-1)
        (self.thrift_host, self.thrift_port) = self.children[index].split(':')
        log.msg("Thrift server got from zookeeper:[%s:%s]" % \
            (self.thrift_host, self.thrift_port))
        zookeeper.close(self.hd)

    def _openHbaseClient(self):
        self.transport = TTransport.TBufferedTransport(
            TSocket.TSocket(self.thrift_host, self.thrift_port))
        self.transport.open()
        self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Hbase.Client(self.protocol)

        log.msg("HbaseHelper instance initialized! connect to %s:%s" % \
            (self.thrift_host, self.thrift_port)) 
    
    '''
    def initWithHost(self, thriftHost, thriftPort):
        self.thrift_host = thriftHost#settings.get('THRIFT_HOST')
        self.thrift_port = thriftPort#settings.getint('THRIFT_PORT')
        log.msg("Thrift server got from settings:[%s:%s]" % \
            (self.thrift_host, self.thrift_port))
        self._openHbaseClient()
    '''

    def reconnect(self):
        self.close()
        log.msg('Refetch thrift server from zookeeper:[%s:%s]' % \
            (self.zookeeper_host, self.zookeeper_port))
        self._getThriftServerFromZookeeper()
        self._openHbaseClient()
                
    def close(self):
        try:
            if self.transport:
                self.transport.close()
                self.transport = None
        except:
            pass
        
    def put(self, table_name, table_obj):
        times = 0
        start = time.time()
        while times <= self.retry_times:
            times += 1
            try:
                mutations = []
                for column, value in table_obj.column_dic.iteritems():
                    mutations.append(Mutation(column=column, value=value))
                
                self.client.mutateRowTs(table_name, table_obj.row_key, mutations, table_obj.version)
                log.msg('put record[%s] to hbase[%s] used %ss, times:%s' \
                    %(table_obj.row_key, table_name, time.time()-start, times))
                return
            except Exception as e:
                log.msg('exception raised, %s, times:%s' % (e, times))
                if times == self.retry_times:
                    raise

                log.msg(traceback.format_exc())
                time.sleep(10*times)
                self.reconnect()
            
    def get(self, tablename, row):
        start = time.time()
        result_list = []
        #result_list = self.client.get(tablename, row, column)
        result_list = self.client.getRow(tablename, row)

        log.msg('get record[%s] from hbase[%s] used %ss' \
            %(row, tablename, time.time()-start))

        if result_list:
            #print result_list[0].columns['BasicInfo:DataSource'].value
            return result_list[0]
        else:
            return None
        
    def delete(self, tablename, row, column):
        self.client.deleteAll(tablename, row, column)
