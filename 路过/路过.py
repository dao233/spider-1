#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/10 9:11
# @Author  : gao
# @File    : 路过.py
import json

from requests_html import HTMLSession

header = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Accept-Language": "zh-CN,zh;q=0.9",
    # "Cache-Control": "max-age=0",
    # "Connection": "keep-alive",
    "cookie": "PHPSESSID=nhs3qvsg0nq1nvnk034ebric80;"
              " Hm_lvt_8bb45b8b013c8d4f9a20752d5e7465e4=1560127792;"
              " _ga=GA1.2.387138892.1560127792;"
              " _gid=GA1.2.1175112514.1560127792;"
              " Hm_lpvt_8bb45b8b013c8d4f9a20752d5e7465e4=1560131433;"
              " _gat_gtag_UA_114322073_1=1;"
              " KEEP_LOGIN=CxngK%3A05d1a0867a8af870907e0782e548802ca5917e10f29e613518adca5cb91fc9c19b77bee6b36667c5ba71add86faf636ec57bbca67ebbadcb5a13a71d40e20aac9c69c0be68fb56d80a438a07ffbe4dd99e6b1ba7ac4ff2f5646%3A1560102641",
    # "DNT": "1",
    # "Host": "imgchr.com",
    # "Referer": "https://imgchr.com/iceflower/albums",
    # "Upgrade-Insecure-Requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
}

cookies = {
    'PHPSESSID': 'nhs3qvsg0nq1nvnk034ebric80',
    'Hm_lvt_8bb45b8b013c8d4f9a20752d5e7465e4': '1560127792',

    "_ga": "GA1.2.387138892.1560127792",
    "_gid": "GA1.2.1175112514.1560127792",
    "Hm_lpvt_8bb45b8b013c8d4f9a20752d5e7465e4": "1560131433",
    "_gat_gtag_UA_114322073_1": "1",
    "KEEP_LOGIN": "CxngK%3A05d1a0867a8af870907e0782e548802ca5917e10f29e613518adca5cb91fc9c19b77bee6b36667c5ba71add86faf636ec57bbca67ebbadcb5a13a71d40e20aac9c69c0be68fb56d80a438a07ffbe4dd99e6b1ba7ac4ff2f5646%3A1560102641",

}

'''
示例
info_map = {
    'django': {
        'EKosNF': {
            'url': 'https://s2.ax1x.com/2019/04/27/EKosNF.png',
            'desc': 'graph_rep.png'
        }
    },
}
'''

from collections import defaultdict


def parse_album(album, info=None):
    if info is None:
        info = defaultdict(dict)
    res = request.get(url=album, cookies=cookies)
    # print(res.text)

    imgs = res.html.find('.list-item img')
    descs = res.html.find('.list-item-desc a')

    # for x in imgs:
    #     print(x.attrs.get('alt'), '  ->   ', x.attrs.get('src'))
    # for x in desc:
    #     print(x.attrs.get('href'), x.text)

    for img, desc in zip(imgs, descs):
        key = img.attrs.get('alt').split('.')[0]
        url = img.attrs.get('src').replace('.md', '')
        desc = img.attrs.get('alt')

        info[key].update(url=url, desc=desc)


    if res.html.find('.pagination-next'):
        next_url = res.html.find('.pagination-next')[0].find('a')[0].attrs.get('href')
        if next_url:
            parse_album(next_url, info=info)

    return info


def parse_index(index_url):
    info = defaultdict(dict)
    res = request.get(url=index_url, cookies=cookies)

    datas = res.html.find('.list-item-desc-title-link')

    for data in datas:
        album = data.attrs.get('href')
        direct = data.text
        info_ = parse_album(album)
        info[direct].update(info_)

    return info


if __name__ == '__main__':
    request = HTMLSession()
    index_url = 'https://imgchr.com/iceflower/albums'

    res = parse_index(index_url)
    json.dump(res, open('路过图床.json', 'w'))
    print(res)
