__author__ = 'zlx'
import configparser
import os

class WriteConfig():
    """写入config文件"""
    def __init__(self,  filepath,filename):
        self.filename = filename
        os.chdir(filepath)
        self.cf = configparser.ConfigParser()
        self.cf.read(self.filename)    # 如果修改，则必须读原文件

    def _with_file(self):
        # write to file
        with open(self.filename, "w+") as f:
            self.cf.write(f)

    def add_section(self, section):
        # 写入section值
        self.cf.add_section(section)
        self._with_file()

    def set_options(self,section, option, value=None):
        """写入option值"""
        self.cf.set(section, option, value)
        self._with_file()

    def remove_section(self, section):
        """移除section值"""
        self.cf.remove_section(section)
        self._with_file()

    def remove_option(self, section, option):
        """移除option值"""
        self.cf.remove_option(section, option)
        self._with_file()