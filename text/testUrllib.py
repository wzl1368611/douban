import urllib.request

url = "https://douban.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363 "
}
req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req)
print(response.read().decode('utf8'))
