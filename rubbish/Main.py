import sqlite3  # 导入数据库操作
from flask import Flask, request, render_template, send_from_directory  # 导入jinjia
app = Flask(__name__)
import os


@app.route('/', methods=['GET'])
def home():
    rubbishName = request.args.get('rubbish')
    print(rubbishName)
    if rubbishName is not None:
        if rubbishName[-4:] == '[sp]':
            return render_template('index.html', content=find(rubbishName, sp=True))
        else:
            return render_template('index.html', content=find(rubbishName))
    else:
        return render_template('index.html', content='未知')


@app.route("/favction.ico", methods=['GET'])
def download_file():
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.getcwd()  # 假设在当前目录
    return send_from_directory(directory, "favction.ico")


@app.route('/change.html', methods=['GET'])
def changeH():
    return render_template('change.html')


@app.route('/change.html', methods=['POST'])
def change():
    name = request.form.get('name')
    type = request.form.get('type')
    conn = sqlite3.connect('rubbish.sqlit3')
    c = conn.cursor()
    if c.execute('select count(*) from rubbish where name = "{:s}"'.format(name)).fetchone()[0] == 0:
        c.execute('insert into rubbish (name, type) values ("{:s}", {:d})'.format(name, int(type)))
    else:
        c.execute('update rubbish set type = {:d} where name ="{:s}"'.format(int(type), name))
    conn.commit()
    c.close()
    conn.close()
    return render_template('change.html')



def find(rubbisName, sp=True):

    """

    :param rubbisName:
    :type rubbisName: str
    :param sp:
    :return:
    """
    # 打开数据库
    conn = sqlite3.connect('rubbish.sqlit3')
    c = conn.cursor()
    a = c.execute('select type from rubbish where name = "{:s}"'.format(rubbisName)).fetchone()
    if a is not None:
        a = a[0]
    else:
        a = None
    rubbishtType = {
        None: "不知",
        1: "干垃圾",
        2: "湿垃圾",
        3: "可回收垃圾",
        4: "有害垃圾"
    }
    c.close()
    conn.close()
    if sp:
        rubbisName = rubbisName.replace('[sp]', '')
        special = {
            '#': '#',
        }
        if rubbisName in special:
            return special[rubbisName]
        else:
            return rubbishtType[a]
    else:
        return rubbishtType[a]



if __name__ == '__main__':
    # 开启服务
    app.run(host='', port=8001)

