# coding=utf-8
# django view

import json

from django.http import HttpResponse
from django.shortcuts import render
from doRedis.connectRedis import *
from doRedis.config import redis_config


def index(request):
    return render(request, "index.html")

# 获取scan job
def getJob(request):

    # 获取redis实例
    r = getRedisInstance()
    http_data_name = redis_config["http_data_name"]
    job_num = r.llen(http_data_name)

    return HttpResponse(job_num)


# 获取scan result
def getResult(request):

    # 获取redis实例
    r = getRedisInstance()
    http_result_name = redis_config["http_result_name"]
    result_list = r.lrange(http_result_name, 0, -1)

    result_list.reverse()
    # 处理格式
    rel_list = []
    for result in result_list:
        result = json.loads(result)
        string = ""
        for r in result["payload"]:
            string += "%s=%s" % (r[1], r[2])
            result["payload"] = string
            result["position"] = r[0]
            result = json.dumps(result)
            rel_list.append(result)
    rel = ",".join(rel_list)
    rel = "[" + rel + "]"

    return HttpResponse(rel)
