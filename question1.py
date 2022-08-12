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


prices = []


def requestData(number):
    now = int(time.time()) * 1000 + 100000000
    m = execjs.compile(js_from_file('./question1.js')).call("hex_md5", str(now)) + "丨" + str(int(now / 1000))
    resp = session.get("https://match.yuanrenxue.com/api/match/1?page=" + str(number) + "&m=" + m, verify=False,
                       headers=header)
    datas = resp.json()["data"]
    for data in datas:
        prices.append(data["value"])


for i in range(0, 5):
    requestData(i + 1)

total = 0
for price in prices:
    total += price
print(total / len(prices))  # 如果小数位是0，就填整数
