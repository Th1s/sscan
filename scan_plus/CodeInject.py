# coding=utf-8
# code inject scanner
# by Th1s

from lib.scanner import *
from lib.config import code_inject_config


# code inject 检测模块
# 利用延时
class CodeInjectScanner(Scanner):

    def __init__(self, *args, **kwargs):

        Scanner.__init__(self, *args, **kwargs)

        # payload   dict    注入payload
        self.payload = code_inject_config['payload']

        self.p = "12345"
        self.q = "6789"
        self.pq = "83810205"

    # override
    def genPayload(self):
        payload = []
        for p in self.payload:
            p = p % (self.p, self.q)
            payload.append(p)
        return payload

    # override
    def doCheck(self, scan_param, param_position):
        flag = self.doCurl(scan_param, param_position)
        if flag:
            if self.pq in flag.content:
                logging.info('code inject in %s : %s' % (self.url, scan_param))
                self.doLogResult(scan_param)

if __name__ == "__main__":
    method = "post"
    url = "http://xxx"
    header = {}
    param = {"id": 1, "test": 3}
    data = {}
    #data = {"b": "2", "aa": 4}

    test = CodeInjectScanner(method, url, header, param, data)
    test.doWork()

    # result in scan_result
    print test.scan_result