"""
-- coding: utf-8 --
@Time : 2020/4/14 0:08
@Author : jcoool
@Site : 
@File : handle_config.py
@Software: PyCharm
"""
import os
from configparser import ConfigParser
from jiekoucs.common.handle_path import CONF_DIR

class HandleConfig(ConfigParser):
    """配置文件解析器类的封装"""

    def __init__(self, filename):
        super().__init__()
        self.read(filename, encoding="utf8")


conf = HandleConfig(os.path.join(CONF_DIR, "config.ini"))

