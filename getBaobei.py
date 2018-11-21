from urllib import request
import ssl
import re
import json
import os
from bs4 import BeautifulSoup
from PIL import Image
from resizeimage import resizeimage
from http.cookiejar import CookieJar
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url = "https://detail.1688.com/offer/527531660387.html?spm=a2615.7691456.newlist.28.6a203b0a5Icc9G"
htmlfile = "/Users/luph/Documents/github/TabobaoPy/baobei.html"
outPath = "/Users/luph/Documents/sizetj/" #输出目录

# context = ssl._create_unverified_context()

# rsp = request.urlopen(url,context=context)

# req= request.Request(url, None, {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; G518Rco3Yp0uLV40Lcc9hAzC1BOROTJADjicLjOmlr4=) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'gzip, deflate, sdch','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'})
# cj = CookieJar()
# opener = request.build_opener(request.HTTPCookieProcessor(cj), request.HTTPSHandler(context=context))
# rsp = opener.open(req)

# html = rsp.read().decode('gbk',"ignore")


driver = webdriver.Chrome()
# driver.implicitly_wait(10)
driver.get(url)

#滚动底部
# js="var q=document.documentElement.scrollTop=100000" 
# driver.execute_script(js)

#滚动到某元素
target = driver.find_element_by_id('desc-lazyload-container')
driver.execute_script("arguments[0].scrollIntoView();", target)

#显式等待，直到desc-lazyload-container下加载出内容（直到offer-template-0出现）
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "offer-template-0"))
    )
except:
    driver.quit()

# time.sleep(5)  # 强制等待3秒再执行下一步

html = driver.page_source


# file = open(htmlfile, 'r') 
# html = file.read()
# file.close()

soup = BeautifulSoup(html,"lxml")


titleTag = soup.find("h1",attrs={"class":"d-title"})
print(titleTag.string)
workPath = outPath + titleTag.string



def downImg(imgurl,filename):
    coverImgDir = os.path.join(workPath,"cover")
    if not os.path.exists(coverImgDir):
        os.makedirs(coverImgDir)
    
    file_suffix = os.path.splitext(imgurl)[1]      #获得图片后缀
    filename = os.path.join(coverImgDir,"{}{}".format(filename,file_suffix))
    request.urlretrieve(imgurl,filename=filename)
    # try:
    #     image = Image.open(filename)
    #     cover = resizeimage.resize_cover(image, [460, 460])
    #     cover.save('test-image-cover.jpeg', image.format)
    # except IOError:
    #     print ("cannot create thumbnail")


def getCoverImg(soup):
    coverImgTagList = soup.findAll("li",attrs={"class":"tab-trigger"})
    i = 0
    for tag in coverImgTagList:
        attrs = tag.attrs
        if 'data-imgs' in attrs :
            imgInfo = tag['data-imgs']
            jsonImg = json.loads(imgInfo)
            imgURL = jsonImg['preview']
            imgURL = imgURL.replace("https", "http")
            print(imgURL)
            downImg(imgURL,i)
            i = i+1


        

descImgTag = soup.find("div",attrs={"id":"desc-lazyload-container"})
print(descImgTag.p)


