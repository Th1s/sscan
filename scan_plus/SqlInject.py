# coding=utf-8
# sqli scanner
# by Th1s

from lib.scanner import *
from lib.config import sqli_config


# sql 注入检测模块
# 利用延时盲注
class SqlInjectScanner(Scanner):

    def __init__(self, *args, **kwargs):

        Scanner.__init__(self, *args, **kwargs)

        # delay     int     请求delay
        # sleep_time int     延时时长
        self.sleep_time = sqli_config['sleep_time']

        # payload   dict    注入payload
        self.payload = sqli_config['payload']

    # override
    def genPayload(self):
        payload = []
        for p in self.payload:
            p = p % self.sleep_time
            payload.append(p)
        return payload

    def deepScan(self, scan_param, param_position):
        # 判断网络延迟
        check_param = eval((str(scan_param)).replace("sleep(", "aaaaa"))
        score = 0
        for i in xrange(10):
            if(self.doCurl()):
                score += 1
            if i-score > 1:
                logging.warning("network delay in %s" % self.url)
                return False
        #网络正常
        if self.doCurl(check_param, param_position):
            flag = not self.doCurl(scan_param, param_position)
            return flag
        else:
            logging.warning("network delay in %s" % self.url)
            return False

    # override
    def doCheck(self, scan_param, param_position):
        flag = not self.doCurl(scan_param, param_position)
        if flag:
            # 检测是否误报
            if self.deepScan(scan_param, param_position):
                logging.info('sqli in %s, method : "%s", payload : %s' % (self.url, self.method, scan_param))
                return True
        return False

if __name__ == "__main__":
    method = "post"
    url = "http://xxx"
    header = {}
    cookie = {}
    param = {"aaa": 1, "bbb": 3}
    data = {"id": "2", "aa": 4}

    test = SqlInjectScanner(method, url, header, cookie, param, data)
    test.doWork()

    # result in scan_result
    print test.scan_result
