import requests
import time
import execjs
import re
import math
import base64

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


postStrs = [
    "AOyW6SvqnweCAAAAAElFTkSuQmCC",
    "7HMAAAAAElFTkSuQmCC",
    "0g3AH8BJlTqZkAngxQAAAAASUVORK5CYII=",
    "HzjKAAAAAElFTkSuQmCC",
    "AgqvQAAAABJRU5ErkJggg==",
    "3J2gmVZucHAAAAAASUVORK5CYII=",
    "80YzEyuMQpQAAAAASUVORK5CYII=",
    "sVsHrJiVs0AAAAAElFTkSuQmCC",
    "LZG6cpuRANAAAAAElFTkSuQmCC",
    "dVIiAf4ApbEnkB6qHqsAAAAASUVORK5CYII=",
]


def md5(str):
    return execjs.compile(js_from_file('./question4_md5.js')).call("hex_md5", str)


def getData(page):
    resp = session.get("https://match.yuanrenxue.com/api/match/4?page=" + str(page), headers=header,
                       verify=False)

    datas = resp.json()["info"]
    # print(datas)
    key = resp.json()["key"] + resp.json()["value"]

    base6 = base64.b64encode(key.encode('utf-8')).decode().replace("=", '')
    global filterClass
    filterClass = md5(base6)
    # print(key)

    # print(filterClass)

    res = re.split(r'<td>|</td>', datas)
    for string in res:
        number = getNumber(string)
        if number is not None:
            prices.append(number)


def getNumber(string):
    if len(string) == 0:
        return None
    pattern = re.compile(r'<img.*?>')  # 查找数字
    res = pattern.findall(string)
    length = len(res)
    numbers = []
    for i in range(0, length):
        numbers.append(0)
    curIndex = 0
    sum = 0
    for index in range(0, length):
        singleNumber = str(res[index])
        groups = re.match(r'.* src="(.*?)".*class="(.*?)".*style="left:(.*)px.*', singleNumber)
        url = groups.group(1)
        className = groups.group(2)
        if className.__contains__(filterClass):
            continue
        offset = float(groups.group(3))
        for i in range(0, len(postStrs)):
            if url.endswith(postStrs[i]):
                numbers[int(curIndex + offset / 11.5)] = i
                curIndex = curIndex + 1
                break
    for i in range(0, curIndex):
        sum = sum + numbers[i] * int(math.pow(10, curIndex - 1 - i))
    return sum


prices = []
count = []
for i in range(0, 5):
    getData(i + 1)
print(prices)
total = 0
for price in prices:
    total += price
print(total)  # 如果小数位是0，就填整数
