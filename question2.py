import requests
import time
import execjs

session = requests.session()

header = {
    "User-Agent": "yuanrenxue.project",
}


def js_from_file(file_name):
    """
    读取js文件
    :return:
    """
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()

    return result


def getM():
    res = execjs.compile(js_from_file('./question2.js')).call("getCookie")
    print(res)
    return res


cookieM = getM()


def getData(page):
    global cookieM
    cookie = {
        "m": cookieM.split(";")[0].replace("m=", "")
    }
    resp = session.get("https://match.yuanrenxue.com/api/match/2?page=" + str(page), headers=header, cookies=cookie,
                       verify=False)
    if resp.status_code != 200:
        cookieM = getM()
        getData(page)
    else:
        datas = resp.json()["data"]
        for data in datas:
            prices.append(data["value"])


prices = []
for i in range(0, 5):
    getData(i + 1)

total = 0
for price in prices:
    total += price
print(total)  # 如果小数位是0，就填整数
