# import urllib.request
#
# response = urllib.request.urlopen("https://www.python.org")
#
# print(response.read().decode('utf-8'))
#
# import urllib.parse #请求分析模块
# import urllib.request #请求模块
#
# data = bytes(urllib.parse.urlencode({'word':'hello'}),encoding='utf-8') #定义data变量  类型bytes
#
# response = urllib.request.urlopen("https://www.python.org/post",data=data) #发送请求 参数data = data
#
# print(response.read()) #打印请求结果 read()方法

import urllib
import urllib.request
import urllib.parse
import re

D = {}


def nextInfo(html):
    '''
    :param html:下一层贴吧页面
    :return:
    '''
    nexts = re.findall(r'(/p/\w{10})', str(html))
    if nexts:
        for next in nexts:
            url = "http://tieba.baidu.com" + next
            if next not in D:
                D[next]=next
                filname = next.split('/')[-1] + '.html'
                html = loadPage(url, filname)
                writeFile(html, filname)
                nextInfo(html)
            else:
                pass
    else:
        pass


# 百度贴吧爬虫接口 组合url地址 起始页和终止页
def tiebaSpider(url, beginPage, endPage):
    """
    作用：负责处理 url 分配每一个url去发送请求
    :param url: 处理第一个url
    :param beginPage: 爬虫起始页
    :param endPage: 爬虫终止页
    :return: null
    """
    for Page in range(beginPage, endPage + 1):
        pn = (Page - 1) * 50
        filename = "第" + str(Page) + "页.html"
        # 组合url 发送请求
        fullurl = url + "&pn=" + str(pn)
        # print fullurl
        # 调用loadPage（）函数发送请求获取HTML页面
        html = loadPage(fullurl, filename)
        # 调用writePage()函数 将服务器响应文件保存到本地磁盘
        writeFile(html, filename)
        nextInfo(html)


def loadPage(url, filename):
    """
    作用：根据url发送请求 获取服务器响应数据
    :param url: 请求地址
    :param filename: 文件名
    :return:服务器响应文件
    """
    print("正在下载" + filename)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    return response.read()


def writeFile(html, filename):
    """
    作用：保存服务器文件到本地磁盘
    :param html: 服务器文件
    :param filename:本地磁盘文件名
    :return:null
    """
    print("正在存储" + filename)
    with open(filename, "wb") as f:
        f.write(html)
    print("-" * 20)


# 模拟main 函数
if __name__ == "__main__":
    # kw = input("请输入要爬取的贴吧名")
    kw = '电影'
    # 输入起始页和终止页 str转化为int类型
    # beginPage = int(input("请输入爬取的起始页"))
    beginPage = 1
    if beginPage < 1:
        beginPage = int(input('起始页面不能小于1'))
    # endPage = int(input("请输入爬取的终止页"))
    endPage = 1
    if endPage < beginPage:
        endPage = int(input('终止页面不能小于起始页面'))
    url = "http://tieba.baidu.com/f?"
    key = urllib.parse.urlencode({"kw": kw})
    # 组合后的url示例 http://tieba.baidu.com/f?kw=lol
    url = url + key
    tiebaSpider(url, beginPage, endPage)
