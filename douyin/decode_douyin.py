#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 10:50
# @Author  : gao
# @File    : decode_douyin.py

import json

from douyin.handle_mongo import save_task


def response(flow):
    if 'aweme/v1/user/follower/list/' in flow.request.url:
        for user in json.loads(flow.response.text)['followers']:
            douyin_info = {}
            douyin_info['share_id'] = user['uid']
            douyin_info['douyin_id'] = user['short_id']
            save_task(douyin_info)
