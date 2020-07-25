"""
-- coding: utf-8 --
@Time : 2020/4/14 0:04
@Author : jcoool
@Site : 
@File : handle_path.py
@Software: PyCharm
"""
import os

# 获取项目所在的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 用例模块所在的目录路径
CASE_DIR = os.path.join(BASE_DIR, "testcase")

# 用例数据所在的目录路径
DATA_DIR = os.path.join(BASE_DIR, "data")

# 配置文件所在的目录路径
CONF_DIR = os.path.join(BASE_DIR, "conf")

# 测试报告所在的目录路径
REPORT_DIR = os.path.join(BASE_DIR, "reports")

# 日志文件所在的目录路径
LOG_DIR = os.path.join(BASE_DIR, "logs")


if __name__ == '__main__':
    print(CONF_DIR)
