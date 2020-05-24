# -*- coding:utf8 -*-
import os


# 用于搜寻文件的计数
number = 0
# 储存搜索到的匹配的歌
chooseList = []
# 用于对用户搜索进行计数
chooseNumber = 0
# 所有可引索的文件后缀
allStyle = ['.mp3', '.flac', '.dsf', '.dff', '.wav', 'ape', 'aiff', 'mqa', 'acc', 'dxd', 'dst']


# 获取目录下所有音乐文件并写到引索
def getPath(path, f):
    global number
    """
    :type path: str
    :type f: file
    """

    if ('System Volume Information' not in path) and ('$' not in path):
        file = os.listdir(path)
        for fl in file:
            if os.path.isdir(path + '\\' + fl):
                getPath(path + '\\' + fl, f)
            else:
                li = fl[fl.rfind('.'):]
                if li.lower() in allStyle:
                    f.write(fl + ':::' + path + '\\' + fl + '\n')
                    number = number + 1
                    print(str(number) + ':' + fl[:fl.rfind('.')])


def createMenu():
    global number
    with open('list', 'w+', encoding='utf-8') as f:
        getPath(os.getcwd(), f)
    print('搜索完成，共搜索到{}首歌'.format(number))
    number = 0
    startSearch()


def startMain():
    # 判断目录文件是否存在
    if os.path.exists(os.getcwd() + '\\list'):
        print('已检测到目录文件')
        startSearch()
    else:
        createMenu()


def startSearch():
    global chooseNumber
    chooseNumber = 0
    chooseList.clear()
    name = input('请输入歌名：')
    if '/ReSearch' == name:
        createMenu()
    with open('list', 'r+', encoding='utf-8') as f:
        while True:
            rawline = f.readline()
            if not rawline:
                break
            else:
                if name in rawline:
                    print(str(chooseNumber) + '.' + rawline[:rawline.rindex(':::')] + '---' + rawline[rawline.rindex(
                        ':::') + 3:-1])
                    chooseList.append((rawline[:rawline.rindex(':::')], rawline[rawline.rindex(':::') + 3:-1]))
                    chooseNumber = chooseNumber + 1
        f.close()
    if chooseNumber == 0:
        print('貌似没有找到诶......')
        startSearch()
    else:
        chooseNow()


# 在搜索指定歌后进行选择
def chooseNow():
    iChoose = input('请输入选择的序号(/Out可返回)：')
    if '/Out' == iChoose:
        startSearch()
    else:
        if iChoose.isdigit():
            choose = int(iChoose)
            if choose > chooseNumber:
                print('你输入的序号太大了......')
            elif choose < 0:
                print('貌似没有这个序号呢......')
            else:
                os.startfile(chooseList[choose][1])

        else:
            print('只叫你输入序号呢......')
        chooseNow()


if __name__ == '__main__':
    startMain()
