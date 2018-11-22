from urllib import request
import ssl
import re
import json
import os
from bs4 import BeautifulSoup
from PIL import Image
from resizeimage import resizeimage
# from http.cookiejar import CookieJar
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import time

url = "https://detail.1688.com/offer/556263839475.html?spm=a2615.7691456.newlist.11.4f7225f5cD6kRB"
outPath = "/Users/luph/Documents/baobei" #输出目录

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
workPath = os.path.join(outPath,titleTag.string)

#清洗url
def clearUrl(imgurl):
    imghttp = imgurl.replace("https","http")
    if not imgurl.startswith("http") :
        imghttp = "http:" + imgurl
    return imghttp

def downImg(imgurl,filename,dir):
    coverImgDir = os.path.join(workPath,dir)
    if not os.path.exists(coverImgDir):
        os.makedirs(coverImgDir)
    
    file_suffix = os.path.splitext(imgurl)[1]      #获得图片后缀
    filename = os.path.join(coverImgDir,"{}{}".format(filename,file_suffix))
    imghttp = clearUrl(imgurl)
    try:
        request.urlretrieve(imghttp,filename=filename)
    except:
        print("下载失败:{}",imgurl)
    # try:
    #     image = Image.open(filename)
    #     cover = resizeimage.resize_cover(image, [460, 460])
    #     cover.save('test-image-cover.jpeg', image.format)
    # except IOError:
    #     print ("cannot create thumbnail")


#返回原图列表，用于过滤封面里的宝贝图
def getBaobeiImg(soup):
    baobeiImgTagList = soup.findAll("div",attrs={"class":"unit-detail-spec-operator active","class":"unit-detail-spec-operator"})
    imgOriImgList = []
    for tag in baobeiImgTagList:
        if "data-unit-config" in tag.attrs and "data-imgs" in tag.attrs:
            baobeiNameInfo = tag['data-unit-config']
            imgInfo = tag['data-imgs']
            jsonName = json.loads(baobeiNameInfo)
            jsonImg = json.loads(imgInfo)
            name = jsonName['name'] #宝贝名
            imgURL = jsonImg['preview'] #大图
            imgOriUrl = jsonImg['original'] #原图
            imgOriImgList.append(imgOriUrl)
            print("{}：{}".format(name,imgURL))
            downImg(imgURL,name,"baobei")
    return imgOriImgList


def getCoverImg(soup,outList):
    coverImgTagList = soup.findAll("li",attrs={"class":"tab-trigger"})
    i = 0
    for tag in coverImgTagList:
        attrs = tag.attrs
        if 'data-imgs' in attrs :
            imgInfo = tag['data-imgs']
            jsonImg = json.loads(imgInfo)
            imgURL = jsonImg['preview']
            imgOriUrl = jsonImg['original'] #原图
            if imgOriUrl in outList:
                continue
            print("封面{}：{}".format(i,imgURL))
            downImg(imgURL,i,"cover")
            i = i+1


def getDescImg(soup):
    descImgTag = soup.find("div",attrs={"id":"desc-lazyload-container"})
    descImgSoup = BeautifulSoup(str(descImgTag.getText),"lxml")
    descImgList = descImgSoup.find_all("img")
    i = 0
    for tag in descImgList:
        imgUrl = tag["src"]
        print("详情图{}：{}".format(i,imgUrl))
        downImg(imgUrl,i,"desc")
        i = i+1
        



def main():
    imgOriImgList = getBaobeiImg(soup)
    getCoverImg(soup,imgOriImgList)
    getDescImg(soup)

if __name__ == "__main__":
    main()
    print("爬取完毕")




