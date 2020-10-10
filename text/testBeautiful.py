from bs4 import BeautifulSoup

f = open('./baidu.html', 'rb')
html = f.read()
bs = BeautifulSoup(html, "html.parser")
print(bs.title)
print(bs.a)
