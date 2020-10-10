import requests

url = "http://baidu.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363 ",
}
response = requests.get(url, headers=headers).content.decode('utf-8')
print(response)
with open('./baidu.html', 'w+', encoding='utf-8') as f:
    f.write(response)


