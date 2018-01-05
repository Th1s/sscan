# -*- coding: utf-8 -*-
# 各类格式处理函数

import urlparse


def solveUrlParam(rowJson):
    res = {}
    res['method'] = rowJson['method']
    res['header'] = rowJson['headers']
    if res['header'].has_key('cookie'):
        res['cookie'] = solveCookie(res['header']['cookie'])
        res['header'].pop('cookie')
    else:
        res['cookie'] = {}
    #无论如何都要处理下url
    query = urlparse.urlparse(rowJson['url']).query
    res['param'] = dict([(k, v[0]) for k, v in urlparse.parse_qs(query.encode("UTF-8")).items()])
    res['data'] = {}
    res['url'] = rowJson['url'].split("?")[0]
    if res['method'].lower() == 'post':
        #目前处理a=1&b=2形式，后续添加更多形式
        if rowJson['body']:
            res['data'] = dict([(k, v[0]) for k, v in urlparse.parse_qs(rowJson['body'].encode("UTF-8")).items()])
    return res


def solveCookie(str_cookie):
    cookie = {}
    list_cookie = str_cookie.split(";")
    for l in list_cookie:
        ll = l.split("=")
        key = ll[0]
        value = ll[1] if len(ll) > 1 else ""
        cookie[key] = value
    return cookie