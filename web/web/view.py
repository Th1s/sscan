# coding=utf-8
# django view

import json

from django.http import HttpResponse
from django.shortcuts import render

from doRedis.connectRedis import *


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
        lpayload = result["payload"]
        for payload in lpayload:
            string = "%s=%s" % (payload[1], payload[2])
            result["payload"] = string
            result["position"] = payload[0]
            print result
            result['message'] = genCompleteHttpMessage(result['method'], result['url'], result['header'].copy(), result['cookie'].copy(), result['param'].copy(), result['data'].copy(), payload)
            dumps_result = json.dumps(result)
            rel_list.append(dumps_result)
    rel = ",".join(rel_list)
    rel = "[" + rel + "]"

    return HttpResponse(rel)


def genCompleteHttpMessage(method, url, header, cookie, param, data, payload):

    # 替换payload
    if payload[0] == "get":
        param[payload[1]] = payload[2]
    elif payload[0] == "post":
        data[payload[1]] = payload[2]
    elif payload[0] == "header":
        header[payload[1]] = payload[2]
    elif payload[0] == "cookie":
        cookie[payload[1]] = payload[2]

    # 构建request报文
    html = ""

    # 头部第一行
    html += method.upper() + " " + url + ("?" if param else "")
    for k, v in param.items():
        html += k + "=" + v + "&"
    # 去掉结尾的&
    if param:
        html = html[:-1]
    html += " HTTP/1.1" + "\n"

    # http header
    for k, v in header.items():
        html += k + ": " + v + "\n"
    if cookie:
        html += "cookie: "
        for k, v in cookie.items():
            html += k + "=" + v + ";"
        html += "\n"
    html += "\n"

    # http body
    for k, v in data.items():
        html += k + "=" + v + "&"
    if data:
        html = html[:-1]

    return html
