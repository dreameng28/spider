#coding=utf-8
__author__ = 'dreameng'

import requests
import re
import urllib
import os


picUrlList = []

beginUrl = "http://www.aitaotu.com/tag/siwa.html"
baseUrl = "http://www.aitaotu.com"

# print content
content = requests.get(beginUrl).content
groupPattern = '下一页</a><a href="' + beginUrl[22: -5] + '/' + '(.*?).html">末页</a>'
groupPageNum = re.findall(groupPattern, content, re.S)
groupPageNum = int(groupPageNum[0])
print groupPageNum


# 获取全部套图首页的url
for i in range(1, groupPageNum):
    if i == 1:
        html = requests.get(beginUrl)
    else:
        otherUrl = beginUrl[: -5] + '/' + str(i) + '.html'
        print otherUrl
        html = requests.get(otherUrl)
    content = html.content
    link = re.findall('<p class="ph3"><a href="(.*?)" target="_blank" title=', content, re.S)
    for each in link:
        picUrlList.append(baseUrl + each)

print picUrlList
print(len(picUrlList))


# 遍历每个套图，并下载
for link in picUrlList:
    picHtml = requests.get(link)
    picContent = picHtml.content
    print link

    pattern = '下一页</a></li><li><a href="' + link[22: -5] + '_' + '(.*?).html">末页</a></li>'
    page = re.findall(pattern, picContent, re.S)
    page = int(page[0])

    picFileName = re.findall('<h1>(.*?)<span id="picnum"', picContent, re.S)
    picFileName = picFileName[0]

    j = 1
    for i in range(1, page + 1):
        if i == 1:
            filename = "/Users/dreameng/Desktop/pics/" + picFileName
            if not os.path.exists(filename):
                os.mkdir(filename)
            picPath = re.findall('<img src="(.*?)" alt=', picContent, re.S)
        else:
            nextUrl = link[: -5] + "_" + str(i) + ".html"
            nextContent = requests.get(nextUrl).content
            picPath = re.findall('<img src="(.*?)" alt=', nextContent, re.S)
        for eachPicPath in picPath:
            # print eachPicPath
            print "/Users/dreameng/Desktop/pics/" + picFileName + "/" + str(j) + ".jpg"
            urllib.urlretrieve(eachPicPath, "/Users/dreameng/Desktop/pics/" + picFileName + "/" + str(j) + ".jpg")
            print j
            j += 1
