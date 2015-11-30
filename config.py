# -*-encoding:utf-8-*-
import json


def read_config(filename):
    """ 读取json文件中的配置信息
    :param filename: json配置文件名，默认为当前程序工作目录的相对路径。
    :return:一个包含配置信息的字典对象
    """
    f = open(filename, mode='r', encoding='utf-8')
    _config = json.load(f)
    f.close()
    return _config

config = read_config('setting.json')

if __name__ == "__main__":
    print(config)
