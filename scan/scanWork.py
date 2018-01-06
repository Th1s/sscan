# -*- coding: utf-8 -*-

import Queue
import importlib

from common.solve import solveUrlParam, solveCookie
from common.check import check_whitelist
from proxy.proxy import *

white_list = []
with open("white_list.txt", "r") as f:
    for line in f.readlines():
        white_list.append(line)


def listenRedis(r, queue, listName):
    #连接redis

    while True:
        if r.llen(listName) > 0:
            row = r.lpop(listName)
            try:
                rowJson = json.loads(row)
                if check_whitelist(rowJson['url'], white_list):
                    saveJson = solveUrlParam(rowJson)
                    queue.put(saveJson)
            except Exception as e:
                logging.exception(e)
        else:
            time.sleep(1)

def scan(r, queue, scan_modules):
    while True:
        row = queue.get()
        for module_name in scan_modules:
            # print module_name
            scan_module = importlib.import_module("scan.plus." + module_name)
            scan_module_class = getattr(scan_module,  module_name + "Scanner")
            scanner = scan_module_class(row['method'], row['url'], row['header'], row['cookie'], row['param'], row['data'])
            scanner.doWork()
            if scanner.scan_result['ret'] == 1:
                try:
                    row['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    row['type'] = module_name
                    row['payload'] = scanner.scan_result['payload']
                    resultJson = json.dumps(row)
                    r.rpush(redis_config['http_result_name'], resultJson)
                except Exception as e:
                    logging.exception(e)

def importPlus():
    plus_dir = "/scan/plus"
    now_dir = os.getcwd()
    filename = os.listdir(now_dir + plus_dir)
    scan_moudle = []
    for name in filename:
        if name.endswith(".py") and name != "__init__.py":
            name = name.split(".")[0]
            scan_moudle.append(name)
    return scan_moudle


def scanWork():
    r = redis.Redis(connection_pool=pool)
    # 定义参数
    list_name = redis_config['http_data_name']
    queue = Queue.Queue()

    scan_moudle = importPlus()

    if sys.argv[2:]:
        thread_num = int(sys.argv[2])
    else:
        thread_num = 5

    t1 = threading.Thread(target=listenRedis, args=(r, queue, list_name))
    t1.setDaemon(True)
    t1.start()

    for i in range(thread_num):
        t2 = threading.Thread(target=scan, args=(r, queue, scan_moudle))
        t2.setDaemon(True)
        t2.start()

    print "sscanHandler start..."
    # 使用while True来实现join，实现ctrl+c退出进程
    while True:
        pass