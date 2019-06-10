#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/10 17:26
# @Author  : gao
# @File    : 01.py
import json
from collections import defaultdict

from requests_html import HTMLSession

request = HTMLSession()
cookies = {
    'PHPSESSID': 'nhs3qvsg0nq1nvnk034ebric80',
    'Hm_lvt_8bb45b8b013c8d4f9a20752d5e7465e4': '1560127792',

    "_ga": "GA1.2.387138892.1560127792",
    "_gid": "GA1.2.1175112514.1560127792",
    "Hm_lpvt_8bb45b8b013c8d4f9a20752d5e7465e4": "1560131433",
    "_gat_gtag_UA_114322073_1": "1",
    "KEEP_LOGIN": "CxngK%3A05d1a0867a8af870907e0782e548802ca5917e10f29e613518adca5cb91fc9c19b77bee6b36667c5ba71add86faf636ec57bbca67ebbadcb5a13a71d40e20aac9c69c0be68fb56d80a438a07ffbe4dd99e6b1ba7ac4ff2f5646%3A1560102641",

}


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

    for img in imgs:
        key = img.attrs.get('alt').split('.')[0]
        url = img.attrs.get('src').replace('.md', '')

        info[key].update(url=url)

    for desc_ in descs:
        key = desc_.attrs.get('href').split('/')[-1]
        desc = desc_.text if len(desc_.text.split('.')) > 1 else desc_.text + '.png'

        info[key].update(desc=desc)

    if res.html.find('.pagination-next'):
        next_url = res.html.find('.pagination-next')[0].find('a')[0].attrs.get('href')
        if next_url:
            parse_album(next_url, info=info)

    return info


info = parse_album('https://imgchr.com/album/C2pZQ')
json.dump(info, open('路过图床.json', 'w'))