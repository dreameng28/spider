#coding=utf-8
__author__ = 'dreameng'

import requests
import re
import urllib
import os
from multiprocessing.managers import BaseManager

"""
研究生时的项目
"""


# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行taskmanager.py的机器:
server_addr = '10.109.33.221'
print('Connect to server %s...' % server_addr)
# 端口和验证码注意保持与taskmanager.py设置的完全一致:
m = QueueManager(address=(server_addr, 8000), authkey='abc')
# 从网络连接:
m.connect()
# 获取Queue的对象:
taskQueen = m.get_task_queue()
resultQueen = m.get_result_queue()


# picUrlSet = set()
#
# beginUrl = "http://www.aitaotu.com/tag/rentiyishu.html"
# baseUrl = "http://www.aitaotu.com"
#
# # print content
# content = requests.get(beginUrl).content
# groupPattern = '下一页</a><a href="' + beginUrl[22: -5] + '/' + '(.*?).html">末页</a>'
# groupPageNum = re.findall(groupPattern, content, re.S)
# groupPageNum = int(groupPageNum[0])
# print groupPageNum
#
#
# # 获取全部套图首页的url
# for i in range(1, groupPageNum+1):
#     if i == 1:
#         html = requests.get(beginUrl)
#     else:
#         otherUrl = beginUrl[: -5] + '/' + str(i) + '.html'
#         print otherUrl
#         html = requests.get(otherUrl)
#     content = html.content
#     link = re.findall('<p class="ph3"><a href="(.*?)" target="_blank" title=', content, re.S)
#     for each in link:
#         picUrlSet.add(baseUrl + each)
#
# print picUrlSet
# print(len(picUrlSet))


# 遍历每个套图，并下载
while True:

    try:
        link = taskQueen.get(timeout=5)
    except EOFError:
        print('task queue is empty.')
        break

    picHtml = requests.get(link)
    picContent = picHtml.content
    print link

    pattern = '下一页</a></li><li><a href="' + link[22: -5] + '_' + '(.*?).html">末页</a></li>'
    # print pattern
    page = re.findall(pattern, picContent, re.S)
    if len(page) == 0:
        pattern = '下一页</a></li><li><a href="' + link[30: -5] + '_' + '(.*?).html">末页</a></li>'
        page = re.findall(pattern, picContent, re.S)
    page = int(page[0])
    print page

    picFileName = re.findall('<h1>(.*?)<span id="picnum"', picContent, re.S)
    picFileName = picFileName[0]

    j = 1

    filename = "/Users/dreameng/Desktop/pics/" + picFileName
    if not os.path.exists(filename):
        os.mkdir(filename)
    else:
        continue

    for i in range(1, page + 1):
        if i == 1:
            picPath = re.findall('<img src="(.*?)" alt=', picContent, re.S)
        else:
            nextUrl = link[: -5] + "_" + str(i) + ".html"
            nextContent = requests.get(nextUrl).content
            picPath = re.findall('<img src="(.*?)" alt=', nextContent, re.S)
        for eachPicPath in picPath:
            # print eachPicPath
            print j
            print filename + "/" + str(j) + ".jpg"
            urllib.urlretrieve(eachPicPath, filename + "/" + str(j) + ".jpg")
            j += 1

    resultQueen.put(link)

print('worker exit.')
