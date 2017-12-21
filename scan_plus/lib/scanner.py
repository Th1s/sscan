# coding=utf-8
# sqli scanner
# by Th1s

import Queue
import logging
import threading
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [line:%(lineno)d] - %(levelname)s: %(message)s')


# 祖先类
class Scanner:

    def __init__(self, *args, **kwargs):

        # method  string  http方法
        # url     string  请求rul
        # header  dict    http头部
        # param   dict    get参数
        # data    dict    post参数
        # cookie  string  cookie

        method, url, header, cookie, param, data = args
        self.url = url
        self.method = method
        self.header = header
        self.cookie = cookie
        self.param = param
        self.data = data

        # delay     int     请求delay
        # sleep_time int    延时时长
        self.delay = 0
        self.sleep_time = 5

        # payload   dict    注入payload
        self.payload = {}

        # 扫描线程数
        self.thread_num = 5

        # 扫描结果
        self.scan_result = {}
        self.scan_result["ret"] = 0
        self.scan_result["param"] = []

        self.scan_position = ["get", "post"]

    # 生成payload
    # 默认返回self.payload
    def genPayload(self):
        return self.payload

    # 给所有的参数加上 payload
    # return type is dict
    def addPayload(self, param={}, data={}, header={}, cookie={}):
        final_params = {}
        final_data = {}
        final_cookie = {}
        final_header = {}

        payload = self.genPayload()

        if "get" in self.scan_position:
            if param:
                for k, v in param.iteritems():
                    final_params[k] = []
                    for p in payload:
                        v1 = p
                        final_params[k].append(v1)

        if "post" in self.scan_position:
            if data:
                for k, v in data.iteritems():
                    final_data[k] = []
                    for p in payload:
                        v1 = p
                        final_data[k].append(v1)

        if "header" in self.scan_position:
            if header:
                for k, v in header.iteritems():
                    final_header[k] = []
                    for p in payload:
                        v1 = p
                        final_header[k].append(v1)

        if "cookie" in self.scan_position:
            if cookie:
                for k, v in cookie.iteritems():
                    final_cookie[k] = []
                    for p in payload:
                        v1 = p
                        final_cookie[k].append(v1)
        return final_params, final_data, final_header, final_cookie

    # curl 方法
    def curl(self, param={}, data={}, header={}, cookie={}):
        if self.method.lower() == "get":
            try:
                r = requests.get(self.url, params=param, headers=header, cookies=cookie, timeout=self.sleep_time)
                return r
            except Exception as e:
                return False

        elif self.method.lower() == "post":
            try:
                r = requests.post(self.url, params=param, data=data, headers=header, cookies=cookie, timeout=self.sleep_time)
                return r
            except Exception as e:
                return False


    # 根据payload位置进行curl
    def doCurl(self, scan_param={}, param_position=""):
        if scan_param:
            if param_position == "get":
                return self.curl(scan_param, self.data, self.header, self.cookie)
            elif param_position == "post":
                return self.curl(self.param, scan_param, self.header, self.cookie)
            elif param_position == "header":
                return self.curl(self.param, self.data, scan_param, self.cookie)
            elif param_position == "cookie":
                return self.curl(self.param, self.data, self.header, scan_param)
        else:
            return self.curl(self.param, self.data, self.header, self.cookie)

    # 多线程调用doScan
    # 默认只检测 get和post参数
    # result = {"ret":1, "param":["id"]}
    def doWork(self):
        param, data, header, cookie = self.addPayload(self.param, self.data, self.header, self.cookie)

        pqueue = Queue.Queue()
        dqueue = Queue.Queue()
        hqueue = Queue.Queue()
        cqueue = Queue.Queue()

        if "get" in self.scan_position:
            if param:
                for key, values in param.iteritems():
                    for value in values:
                        scan_param = self.param.copy()
                        scan_param[key] = value
                        pqueue.put(scan_param)

        if "post" in self.scan_position:
            if data:
                for key, values in data.iteritems():
                    for value in values:
                        scan_param = self.data.copy()
                        scan_param[key] = value
                        dqueue.put(scan_param)

        if "header" in self.scan_position:
            if header:
                for key, values in header.iteritems():
                    for value in values:
                        scan_param = self.data.copy()
                        scan_param[key] = value
                        hqueue.put(scan_param)

        if "cookie" in self.scan_position:
            if cookie:
                for key, values in cookie.iteritems():
                    for value in values:
                        scan_param = self.data.copy()
                        scan_param[key] = value
                        cqueue.put(scan_param)

        for i in range(self.thread_num):
            if pqueue:
                param_position = "get"
                threading.Thread(target=self.doScan, args=(pqueue, param_position)).start()
            if dqueue:
                param_position = "post"
                threading.Thread(target=self.doScan, args=(dqueue, param_position)).start()
            if hqueue:
                param_position = "header"
                threading.Thread(target=self.doScan, args=(hqueue, param_position)).start()
            if cqueue:
                param_position = "cookie"
                threading.Thread(target=self.doScan, args=(cqueue, param_position)).start()

        pqueue.join()
        dqueue.join()
        hqueue.join()
        cqueue.join()

    def doScan(self, q, param_position):
        while not q.empty():
            scan_param = q.get()
            self.doCheck(scan_param, param_position)
            q.task_done()

    # 具体的检测逻辑
    def doCheck(self, scan_param, param_position):
        pass

    def doLogResult(self, scan_param):
        self.scan_result["param"].append(scan_param)
        self.scan_result["ret"] = 1

if __name__ == "__main__":
    print "Scanner is an ancestor class"
