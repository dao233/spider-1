import requests

url = "https://aweme.snssdk.com/aweme/v1/play/?video_id=v0300f690000bi3p9tchpahnchu8523g"

headers = {
    # "Host": 'aweme.snssdk.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    # 'Accept': '*/*',
    # 'Cache-Control': 'no-cache',
    # 'Postman-Token': '5670146f-24e5-4d17-a79e-0046157277d1,cc67e7df-d90d-411b-8770-f9b88a213bff',
    # 'accept-encoding': 'gzip, deflate',
    # 'referer': 'https://aweme.snssdk.com/aweme/v1/play/?video_id=v0300f690000bi3p9tchpahnchu8523g&logo_name=aweme',
    # 'Connection': 'keep-alive',
    # 'cache-control': 'no-cache',
}

res = requests.get(url=url, headers=headers)
with open("video.mp4", "wb") as f:
    f.write(res.content)