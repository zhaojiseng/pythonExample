import urllib.request  # 导入urllib.request库
import urllib.parse  # 导入urllib.parse库
import json  # 导入json库
import time  # 导入time库

url = "http://fy.iciba.com/ajax.php?a=fy"
lanuage = (
    ("中日", "zh", "ja"),
    ("西中", "es", "zh"),
    ("中英", "zh", "en"),
    ("中韩", "zh", "ko"),
    ("法中", "fr", "zh"),
    ("中德", "zh", "de"),
    ("英中", "en", "zh"),
    ("日中", "ja", "zh"),
    ("中西", "zh", "es"),
    ("德中", "de", "zh"),
    ("韩中", "ko", "zh"),
    ("中法", "zh", "fr")
)
while True:
    fanyi = input("请输入翻译内容：")
    print("请选择语言")
    j = 0
    for i in lanuage:
        j = j + 1
        print("\t{:d}.{}".format(j, i[0]))
    choose = int(input("请选择翻译语言:"))
    if choose <= 12:
        data = {
            'f': lanuage[choose - 1][1],
            't': lanuage[choose - 1][2],
            'w': fanyi
        }
        data = urllib.parse.urlencode(data).encode('utf - 8')  # urlencode转换data数据并编码为utf-8码
        req = urllib.request.Request(url, data)
        req.add_header('Referer', 'http://fy.iciba.com/')
        req.add_header('User - Agent',
                       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
        response = urllib.request.urlopen(req)  # post方式打开指定网页
        html = response.read()  # 读取网页信息
        html = html.decode('utf - 8')  # 将utf-8码解码为unicode码
        target = json.loads(html)  # 把json页面转换为一个字典
        try:
            print(target['content']['out'])
        except KeyError:
            try:
                ls = target['content']['word_mean']
                for i in ls:
                    print(i)
            except KeyError:
                print("没有结果")
        time.sleep(1)  # 延迟提交数据




