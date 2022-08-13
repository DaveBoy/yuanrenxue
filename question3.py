import requests
import time
import execjs

session = requests.session()

header = {
    "Host": "match.yuanrenxue.com",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "sec-ch-ua": "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "yuanrenxue.project",
    "sec-ch-ua-platform": "\"Windows\"",
    "Accept": "*/*",
    "Origin": "https://match.yuanrenxue.com",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://match.yuanrenxue.com/match/3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

cookie = {
    "qpfccr": "true",
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
    # res = execjs.compile(js_from_file('./question2.js')).call("getCookie")
    # print(res)
    return ""


cookieM = getM()


def getData(page):
    global cookieM
    session.headers.clear()
    session.headers.update(header)
    resp = session.post("https://match.yuanrenxue.com/jssm", cookies=cookie, verify=False)
    resp = session.get("https://match.yuanrenxue.com/api/match/3?page=" + str(page),
                       verify=False)
    if resp.status_code != 200:
        cookieM = getM()
        getData(page)
    else:
        datas = resp.json()["data"]
        for data in datas:
            price = data["value"]
            try:
                index = prices.index(price)
                count[index] = count[index] + 1
            except:
                prices.append(price)
                count.append(1)


prices = []
count = []
for i in range(0, 5):
    getData(i + 1)

index = 0

for c in count:
    if c > count[index]:
        index = count.index(c)
print(prices[index])  # 如果小数位是0，就填整数
# 两个请求好发现，有序不好发现
