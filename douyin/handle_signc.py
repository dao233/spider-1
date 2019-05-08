import json
import time

import requests
import re

from selenium import webdriver

share_id = "96956380265"
share_url = "https://www.douyin.com/share/user/"+share_id

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
}

res = requests.get(share_url, headers=headers)
# print(res.text)
dytk_search = re.compile(r"dytk: '(.*?)'")
tac_search = re.compile(r"<script>tac=(.*?)</script>")

dytk = re.search(dytk_search, res.text).group(1)
tac = "var tac="+re.search(tac_search, res.text).group(1)+";"



with open('html_header.txt', 'r') as f1:
    f1_read = f1.read()

with open('html_footer.txt', 'r') as f2:
    f2_read = f2.read().replace('&&&', share_id)

with open('test.html', 'w') as f:
    f.write(f1_read +'\n' + tac + '\n' + f2_read)


driver = webdriver.Chrome()
driver.get("file://E:\\Python\\Spider\\douyin\\test.html")
signature = driver.title
driver.close()
# signature = input(">>>")
# signature = 'RVPFOBAYGYRMH78tPmTMNUVTxS'
video_url = "https://www.iesdouyin.com/web/api/v2/aweme/post/?user_id="+share_id+"&count=21&max_cursor=0&aid=1128&_signature="+signature+"&dytk="+dytk
print(video_url)

while True:
    ress =  requests.get(video_url, headers=headers)
    # print(ress.text)
    if not json.loads(ress.text)['aweme_list']:
        # time.sleep(1)
        continue
    else:
        # print(ress.text)
        for item in json.loads(ress.text)['aweme_list']:
            video_id = item['video']['play_addr']['uri']
            video_uri = "https://aweme.snssdk.com/aweme/v1/play/?video_id=" + video_id
            print(video_uri)
            # video_res = requests.get(url=video_uri, headers=headers)
            # with open(video_id+".mp4", 'wb') as f:
            #     f.write(video_res.content)
        break

