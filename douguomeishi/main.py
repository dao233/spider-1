#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/16 上午 10:28
# @Author  : gao
# @File    : main.py
import json
from multiprocessing import Queue
from concurrent.futures import ThreadPoolExecutor
import requests

from douguomeishi.db import mongo_info

queue_list = Queue()


def handle_reques(url, data):
    header = {
        "client": "4",
        "version": "6934.2",
        "device": "OPPO R11",
        "sdk": "22,5.1.1",
        "imei": "866174010942858",
        "channel": "baidu",
        # "mac": " 6A:07:15:F0:34:85",
        "resolution": "1280*720",
        "dpi": "1.5",
        # "android-id": "6a0715f034851883",
        # "pseudo - id": "5f0348518836a071",
        "brand": "OPPO",
        "scale": "1.5",
        "timezone": "28800",
        "language": "zh",
        "cns": "3",
        "carrier": "CHINA+MOBILE",
        # "imsi": "460071060715240",
        "user-agent": "Mozilla/5.0 (Linux; Android 5.1.1; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36",
        "reach": "1",
        "newbie": "1",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "Keep-Alive",
        # "Cookie": "duid=59159842",
        "Host": "api.douguo.net",
        # "Content-Length": "74",
    }

    response = requests.post(url=url, headers=header, data=data)
    return response


def handle_index():
    url = "http://api.douguo.net/recipe/flatcatalogs"
    data = {
        "client": "4",
        # "_session": "1552715432169866174010942858",
        # "v": "1503650468",
        # "_vs": "0",   0 和 2305都可以
        "_vs": "2305",

    }

    response = handle_reques(url=url, data=data)
    # print(response.text)
    response_to_dict = json.loads(response.text)

    for item in response_to_dict['result']['cs']:
        for item_1 in item['cs']:
            for item_2 in item_1['cs']:
                data_2 = {
                    "client": "4",
                    # "_session": "1552715831226866174010942858",
                    "keyword": item_2['name'],
                    # 0:综合最佳   2: 收藏最多   3:做过最多
                    "order": "0",
                    "_vs": "400",
                }
                queue_list.put(data_2)


def handle_caipu_list(data):
    print("当前处理:", data['keyword'])
    caipu_list_url = 'http://api.douguo.net/recipe/v2/search/0/20'
    caipu_list_response = handle_reques(url=caipu_list_url, data=data)
    response_to_dict = json.loads(caipu_list_response.text)
    handle_caipu_detail(data, response_to_dict)

    count=0
    while response_to_dict['result']['end'] == 0 and len(response_to_dict['result']['list']) >= 19:
        count+=1
        print('当前页数:', data['keyword'], count)
        caipu_list_url = 'http://api.douguo.net/recipe/v2/search/{}/20'.format(count*20)
        caipu_list_response = handle_reques(url=caipu_list_url, data=data)
        response_to_dict = json.loads(caipu_list_response.text)
        handle_caipu_detail(data, response_to_dict)


def handle_caipu_detail(data, response_to_dict):

    for item in response_to_dict['result']['list']:
        caipu_info = {}
        caipu_info['shicai'] = data['keyword']

        if item['type'] == 13:
            caipu_info['author'] = item['r']['an']
            caipu_info['shicai_id'] = item['r']['id']  # 查看详细操作步骤时使用
            caipu_info['describe'] = item['r']['cookstory']
            caipu_info['caipu_name'] = item['r']['n']
            caipu_info['zuoliao_list'] = item['r']['major']

            detail_url = 'http://api.douguo.net/recipe/detail/' + str(caipu_info['shicai_id'])
            detail_data = {
                "client": "4",
                # "_session": "1552715831226866174010942858",
                "author_id": "0",
                "_vs": "2803",
                "_ext": '{"query":{"kw":' + data["keyword"] + ',"src":"2803","type":"13","id":' + str(
                    caipu_info["shicai_id"]) + '}}',
            }

            detail_response = handle_reques(url=detail_url, data=detail_data)
            # print(detail_response.text)
            detail_response_to_dict = json.loads(detail_response.text)

            caipu_info['tips'] = detail_response_to_dict['result']['recipe']['tips']
            caipu_info['cook_step'] = detail_response_to_dict['result']['recipe']['cookstep']

            print('当前入库:', caipu_info['caipu_name'])
            mongo_info.insert_item(caipu_info)

        else:
            continue






if __name__ == '__main__':
    handle_index()
    # print(queue_list.get())
    # print(queue_list.qsize())
    # while queue_list.qsize() > 0:
    # handle_caipu_list({'client': '4', 'keyword': '豆腐', 'order': '0', '_vs': '400'})
    pool = ThreadPoolExecutor()

    while queue_list.qsize() > 0:
        pool.submit(handle_caipu_list, queue_list.get())

