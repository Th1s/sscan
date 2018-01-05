# -*- coding: utf-8 -*-
# check_whitelist

import urlparse


def check_whitelist(url, white_list):
    if not white_list:
        return True
    host = urlparse.urlparse(url).netloc
    for wl in white_list:
        if wl.strip() in host:
            return True
    return False