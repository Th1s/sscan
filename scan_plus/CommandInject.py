# coding=utf-8
# command inject scanner
# by Th1s

from lib.scanner import *
from lib.config import command_inject_config
import requests
import random


# command 检测模块
# 利用ceye
class CommandInjectScanner(Scanner):

    def __init__(self, *args, **kwargs):

        Scanner.__init__(self, *args, **kwargs)

        # payload   dict    注入payload
        self.payload = command_inject_config['payload']

        # ceye
        self.ceye_host = command_inject_config["ceye_host"]
        self.ceye_api = command_inject_config["ceye_api"]

        self.scan_position = command_inject_config["scan_position"]

    # override
    def doCheck(self, scan_param, param_position):
        random_key = ''.join(str(random.random()).split('.'))
        for payload in self.payload:
            try:
                string_scan_param = str(scan_param).replace(payload, payload % (random_key, self.ceye_host))
                scan_param = eval(string_scan_param)
            except Exception as e:
                logging.exception(e)

            flag = self.doCurl(scan_param, param_position)

            try:
                r = requests.get("http://api.ceye.io/v1/records?token=%s&type=dns&filter=" % self.ceye_api)
                search_result = r.content
                if search_result.find(random_key) > 0:
                    logging.info('command inject in %s : %s' % (self.url, scan_param))
                    self.doLogResult(scan_param)
            except Exception as e:
                logging.exception(e)


if __name__ == "__main__":
    method = "get"
    url = "http://www.th1s.cn/test/sscan/command.php"
    header = {"User-Agent": "123"}
    cookie = {}
    param = {"id": 1, "test": 3}
    data = {}

    test = CommandInjectScanner(method, url, header, cookie, param, data)
    test.doWork()

    # result in scan_result
    print test.scan_result