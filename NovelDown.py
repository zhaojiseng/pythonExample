import requests
from bs4 import BeautifulSoup
import re
import threading
from os import system
from time import sleep

menuNowNumber = 0
allContent = {}
allHttp = {
    'http://www.xbiquge.la/': 'utf-8',
    'https://www.xbiquge6.com/': 'utf-8',
    'https://www.qu.la/': 'utf-8',
    'https://www.biquge8.com/': 'GB2312'
}
type = 'utf-8'

def getUrlContent(url, gzip=True):
    kv = {'user-agent': 'Mozilla/5.0',
          'verify': 'False'}
    if gzip:
        kv['Accept-Encoding'] = 'gzip, deflate'
    base = requests.get(url, headers=kv)
    base.encoding = type
    #print(base.text)
    return base.text


def getMenu(url):
    data = getUrlContent(url)
    soup = BeautifulSoup(data, 'html.parser')
    soup2 = soup.find('div', id='list')
    if soup2 == None:
        soup2 = soup.find('div', attrs={'class': 'listmain'})
    tilet = []
    urla = re.search(r'https?://.*?/', u, flags=re.S)
    for tem1 in soup2.find_all('a'):
        if re.search(r'https?://.*?/', tem1.attrs['href'], flags=re.S):
            tilet.append(tem1.attrs['href'])
        else:
            tilet.append(urla.group() + tem1.attrs['href'])

    return tilet


def getName(soup):
    bookname1 = soup.find("div", attrs={"class": "bookname"})
    return bookname1.h1.string


def getContent(soup, cleanAD=True):
    soup2 = soup.find('div', id='content')
    soup2 = re.sub(r'(<br/>)|(<p>)|(<a.*?>)|(</p>)|(</a>)|(<a>)|</div>|<div>|(<div id="content">)', '\n', str(soup2),
                   flags=re.S)
    if cleanAD:
        soup2 = re.sub('(亲,点击进去,给个好评呗,分数越高更新越快,据说给新笔趣阁打满分的最后都找到了漂亮的老婆哦!)|'
                       '(手机站全新改版升级地址：http://m.xbiquge.la，数据和书签与电脑站同步，无广告清新阅读！)', '', soup2)
    return soup2


def getAll(url):
    data = getUrlContent(url)
    soup = BeautifulSoup(data, 'html.parser')
    name = getName(soup)
    content = getContent(soup)
    return name + '\n' + content


class allContentAdd(threading.Thread):
    def __init__(self, number, url):
        threading.Thread.__init__(self)
        self.number = number
        self.url = url

    def run(self) -> None:
        global allContent, menuNowNumber
        content = getAll(self.url)
        allContent[self.number] = content
        menuNowNumber = menuNowNumber + 1
        # print('{}/{}'.format(menuNowNumber, menuNumber))


def getBookname(url):
    data = getUrlContent(url)
    soup = BeautifulSoup(data, 'html.parser')
    info = soup.find('div', id='info')
    return info.h1.string


u = input('请输入网址:')
hand = re.search(r'https?://.*?/', u, flags=re.S).group()
if hand in allHttp:
    type = allHttp[hand]
    print('支持当前网址')
else:
    print('未了解当前网址')
xc = int(input('并行下载数:'))
menu = getMenu(u)
menuNumber = len(menu)
bookname = getBookname(u)
allThread = []
out2 = True
li = 0
# 循环判断所有任务进程是否结束
while out2:
    nowAlive = 0
    system('cls')
    print(bookname)
    print(menuNumber)
    print(menuNowNumber)
    if menuNowNumber != 0:
        oa = menuNowNumber/menuNumber
        print(oa)
    for ls in allThread:
        if ls.isAlive():
            nowAlive = nowAlive + 1
    if nowAlive <= xc:
        if li < menuNumber:
            allThread.append(allContentAdd(li, menu[li]))
            allThread[-1].start()
            li = li + 1
        else:
            out2 = False

notout = True
while notout:
    k = False
    for i, tem in enumerate(allThread):
        if tem.isAlive():
            k = True
    if not k:
        dict1 = sorted(allContent)
        with open('{}.txt'.format(bookname), 'w', encoding='utf-8') as f:
            for tem in dict1:
                f.write(allContent[tem])
        notout = False
        print('ok')
