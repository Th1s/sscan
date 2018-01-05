# -*- coding: utf-8 -*-

from multiprocessing import Process

from proxy.proxy import *
from scan.scanWork import scanWork


if __name__ == "__main__":

    # 同时启动proxy 和 scan
    p1 = Process(target=proxyStart)
    p1.start()
    p2 = Process(target=scanWork)
    p2.start()

