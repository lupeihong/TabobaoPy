from urllib import request
import ssl
import re
from bs4 import BeautifulSoup

url = "https://detail.1688.com/offer/527531660387.html?spm=a261y.7663282.0.0.7e255f73zeVxdC&sk=consign"
context = ssl._create_unverified_context()
rsp = request.urlopen(url,context=context)
html = rsp.read().decode('gbk',"ignore")

soup = BeautifulSoup(html)
tag = soup.find("h1",attrs={"class":"d-title"})
print(tag.string)