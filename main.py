import requests
import logging
from bs4 import BeautifulSoup
import execjs
import time


def js_from_file(file_name):
    """
    读取js文件
    :return:
    """
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()

    return result


session = requests.session()
logging.captureWarnings(True)  # 去掉建议使用SSL验证的显示
site_url = "https://www.52pojie.cn/"
cookie = {
    "htVC_2132_auth": "请先在网页端登录后获取cookie中的参数htVC_2132_auth",
    "htVC_2132_saltkey": "请先在网页端登录后获取cookie中的参数htVC_2132_saltkey",
}
header = {
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "sec-ch-ua": "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "Referer": "https://www.52pojie.cn/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def home(check=False):
    response = session.get(url=site_url, cookies=cookie, headers=header, verify=False)
    # print(response.text)
    soup = BeautifulSoup(response.text)
    login = soup.find('button', class_="pn vm")
    # print(soup.prettify())

    # print(login is None)
    if login is None:
        qiandao = soup.find('img', class_="qq_bind")

        if qiandao.get("src").endswith("qds.png"):
            print("未签到")
            if check is False:
                start_qiandao()
        else:
            print("已签到")
    else:
        print("登录失效，请更新cookie中的htVC_2132_auth、htVC_2132_saltkey")


# 先get https://www.52pojie.cn/home.php?mod=task&do=apply&id=2&referer=%2F 得到加密js
# 然后get https://www.52pojie.cn/CSPDREL2hvbWUucGhwP21vZD10YXNrJmRvPWFwcGx5JmlkPTImcmVmZXJlcj0lMkY=?wzwscspd=MC4wLjAuMA==  302
def start_qiandao():
    result = execjs.compile(js_from_file("52pojie.js")).call("getLocation")
    print(result)
    session.get(url="https://www.52pojie.cn" + result, headers=header, cookies=cookie, verify=False)

    time.sleep(1)
    home(True)


if __name__ == '__main__':
    home()
    # start_qiandao()
