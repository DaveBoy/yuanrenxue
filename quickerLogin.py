##.py

import requests
from bs4 import BeautifulSoup
import logging
import lxml

loginUrl = "https://getquicker.net/Identity/Account/Login"
logging.captureWarnings(True)  # 去掉建议使用SSL验证的显示
session = requests.session()

data = {
    "email": "email",
    "pwd": "pwd",
}


def getPara(name):
    try:
        return quicker.context.GetVarValue(name)
    except:
        return data[name]


def setPara(name, value):
    try:
        return quicker.context.SetVarValue(name, value)
    except:
        res = {name: value}
    print(res)
    return res


def requestHtml():
    response = session.get(loginUrl, verify=False)
    soup = BeautifulSoup(response.text, features="html.parser")
    requestVerificationToken = soup.find(name='input', attrs={"name": '__RequestVerificationToken'}).get("value")
    data = {"Input.Email": getPara('email'), "Input.Password": getPara('pwd'), "Input.RememberMe": "true",
            "__RequestVerificationToken": requestVerificationToken}

    response = session.post(loginUrl, data=data, verify=False, allow_redirects=False)
    set_cookie = response.headers["Set-Cookie"]
    application = set_cookie.split(";")[0].replace(".AspNetCore.Identity.Application=", "")
    setPara('text', application)


requestHtml()
