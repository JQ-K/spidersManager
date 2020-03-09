__author__ = 'zlx'
import configparser
import os


class ReadConifg():
    """读取配置文件"""
    def __init__(self, filename, filepath):
        os.chdir(filepath)    # 将当前工作目录切换到指定的目录
        self.cf = configparser.ConfigParser()    # 实例化configparser对象
        self.cf.read(filename)    # 读取文件

    def read_sections(self):
        """读取配置文件中sections"""
        sacs = self.cf.sections()    # 获取sections，返回list
        print("sections：", sacs, type(sacs))

    def read_options(self, sections):
        """获取配置文件中的options值"""
        opts = self.cf.options(sections)    # 获取db section下的options，返回list
        print("%s：%s" % (sections, opts), type(opts))

    def read_kv(self, sections):
        """获取配置文件中的所有键值对"""
        kvs = self.cf.items(sections)    # 获取db section下的所有键值对，返回list
        print("%s：%s" % (sections, kvs))

    def get_str(self, sections, key):
        """获取指定sectons中指定的key的value值, 返回的会是 str 类型"""
        value_str = self.cf.get(sections, key)
        return value_str

    def get_int(self, sections, key):
        """获取指定sectons中指定的key的value值, 返回的会是 int 类型"""
        value_int = self.cf.getint(sections, key)
        return value_int